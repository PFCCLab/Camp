### 姓名
侯悦欣

### 实习项目
Nougat复现及优化

### 本周工作

1. **源码转换为Paddle API**

	* 使用PaConvert自动转换
	* 转换失败部分手动处理
 * PaConvert 结果:

```yaml
===========================================
Convert Summary:
===========================================
There are 204 Pytorch APIs in this Project:
 144  Pytorch APIs have been converted to Paddle successfully!
 60  Pytorch APIs are not supported to convert to Paddle currently!
 Convert Rate is: 70.588%

For these 60 Pytorch APIs that do not support to Convert now, which have been marked by >>> before the line, 
please refer to https://www.paddlepaddle.org.cn/documentation/docs/zh/develop/guides/model_convert/convert_from_pytorch/pytorch_api_mapping_cn.html 
and convert it by yourself manually. In addition, these APIs will be supported in future.
```

在没有自动转换成功的api中，完成手动转换的API:

Lightning module.py

```yaml
def train_dataloader(self):
>>>>>>        loaders = [torch.utils.data.DataLoader(torch.utils.data.
            ConcatDataset(self.train_datasets), batch_size=self.
            train_batch_sizes[0], num_workers=self.config.num_workers,
            pin_memory=True, worker_init_fn=self.seed_worker, generator=
            self.g, shuffle=True, collate_fn=self.ignore_none_collate)]
        return loaders

    def val_dataloader(self):
>>>>>>        loaders = [torch.utils.data.DataLoader(torch.utils.data.
            ConcatDataset(self.val_datasets), batch_size=self.
            val_batch_sizes[0], pin_memory=True, shuffle=True, collate_fn=
            self.ignore_none_collate)]
        return loaders
```

```yaml
def train_dataloader(self):
        loaders = [paddle.io.DataLoader(paddle.io.
            ComposeDataset(self.train_datasets), batch_size=self.
            train_batch_sizes[0], num_workers=self.config.num_workers,
            use_shared_memory=True, worker_init_fn=self.seed_worker, shuffle=True, collate_fn=self.ignore_none_collate)]
        return loaders

def val_dataloader(self):
        loaders = [paddle.io.DataLoader(paddle.io.
            ComposeDataset(self.val_datasets), batch_size=self.
            val_batch_sizes[0], use_shared_memory=True, shuffle=True, collate_fn=
            self.ignore_none_collate)]
        return loaders
```

in model.py：

```jsx
if self.align_long_axis and (
            (self.input_size[0] > self.input_size[1] and img.width > img.height)
            or (self.input_size[0] < self.input_size[1] and img.width < img.height)
        ):
            img = rotate(img, angle=-90, expand=True)
        img = resize(img, min(self.input_size))
```

```jsx
if self.align_long_axis and (self.input_size[0] > self.input_size[1
            ] and img.width > img.height or self.input_size[0] < self.
            input_size[1] and img.width < img.height):
            img = paddle.vision.transforms.functional.rotate(img, angle=90,expand=True)
        img = paddle.vision.transforms.functional.resize(img, min(self.input_size))
```

暂未转换的API:

in model.py:

```python
self.model = timm.models.swin_transformer.SwinTransformer(img_size=
            self.input_size, depths=self.encoder_layer, window_size=self.
            window_size, patch_size=self.patch_size, embed_dim=self.
            embed_dim, num_heads=self.num_heads, num_classes=0)
swin_state_dict = timm.create_model('swin_base_patch4_window12_384'
                , pretrained=True).state_dict()

self.tokenizer = transformers.PreTrainedTokenizerFast(tokenizer_file
            =str(tokenizer_file))
self.model = transformers.MBartForCausalLM(config=transformers.
            MBartConfig(is_decoder=True, is_encoder_decoder=False,
            add_cross_attention=True, decoder_layers=self.decoder_layer,
            max_position_embeddings=self.max_position_embeddings,
            vocab_size=len(self.tokenizer), scale_embedding=True,
            add_final_layer_norm=True, d_model=hidden_dimension))
bart_state_dict = transformers.MBartForCausalLM.from_pretrained(
                'facebook/mbart-large-50').state_dict()

class NougatConfig(transformers.modeling_utils.PretrainedConfig):

class StoppingCriteriaScores(transformers.StoppingCriteria):

class NougatModel(transformers.modeling_utils.PreTrainedModel):

encoder_outputs = transformers.file_utils.ModelOutput(last_hidden_state
            =last_hidden_state, attentions=None)
stopping_criteria=transformers.StoppingCriteriaList([
            StoppingCriteriaScores()] if early_stopping else [])
```

 in lightning_module.py:
```python
torch.nn.utils.rnn.pad_sequence()
torch.backends.mps.is_available():
```

2. **模型移植的环境和数据准备工作**


3.. **问题疑惑与解答**


	* 问题a 在未完成迁移的api中，torch.backends.mps.is_available()没有搜索到足够资料进行复现，请问paddle有对应的实现或替代示例吗？

        答：这个api paddle中暂时没有，但是我理解不影响对齐，不使用mps即可

	* 问题b 通过transformer模块和timm模块导入的api，是否有转换案例可以参考？我在下面设想了一种思路，请问有什么建议吗？

        答：基于numpy的部分可以直接直接复用，模型迁移就是常规操作。

### 下一步工作计划

	* 目前尚未完成的API转换主要为huggingface的transformer模块和timm模块，计划移植相关代码到本地，重新执行nougat源码。跑通后再使用PaConvert转换新植入的模块
 	* 使用PaDiff排除差异快速对齐

### 导师点评

可以加速完成前向对齐～
