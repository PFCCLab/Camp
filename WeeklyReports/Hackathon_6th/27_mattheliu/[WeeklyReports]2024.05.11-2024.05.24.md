### 姓名
刘卓鑫

### 实习项目
#### PaddleSpeech 套件能力建设

### 本周工作

1. **跑PaddleSpeech/Demos**
   **已跑完25/25**   **验证完成进度13/25**

 | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|
|PaddleSpeech=develop，PaddlePaddle-gpu=develop，验证完成进度（13/25）| | | | | | | | |
|方向|命令|目录|进度（验证中/未验证/验证完成）|能否直接跑通|报错|备注|二次验证|截图|
|ASR|paddlespeech_client acs --server_ip 127.0.0.1 --port 8090 --input ./zh.wav|[audio_content_search](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/audio_content_search) |验证中|否|报错[2024-05-06 22:41:47,376] [ INFO] - acs http client start<br/>[2024-05-06 22:41:47,377] [ INFO] - endpoint: http://127.0.0.1:8090/paddlespeech/asr/search<br/>[2024-05-06 22:41:47,382] [ ERROR] - Failed to speech recognition.<br/>[2024-05-06 22:41:47,383] [ ERROR] - HTTPConnectionPool(host='127.0.0.1', port=8090): Max retries exceeded with url: /paddlespeech/asr/search (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fbaf10e6830>: Failed to establish a new connection: [Errno 111] Connection refused')) $ python test.py <br/>[2024-05-06 22:48:23,017] [ INFO] - acs http client start<br/>[2024-05-06 22:48:23,017] [ INFO] - endpoint: http://127.0.0.1:8490/paddlespeech/asr/search<br/>Traceback (most recent call last):<br/> File "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/urllib3/connection.py", line 200, in _new_conn<br/> sock = connection.create_connection(<br/> File "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/urllib3/util/connection.py", line 85, in create_connection<br/> raise err<br/> File "/opt/conda/envs/python35-paddle120-env/lib/python3.10/site-packages/urllib3/util/connection.py", line 73, in create_connection<br/> sock.connect(sa)<br/>ConnectionRefusedError: [Errno 111] Connection refused<br/><br/>The above exception was the direct cause of the following exception:|![image](https://github.com/mattheliu/Camp/assets/102272920/6921da56-e4cd-42fc-a476-d9767ef3cab8)  |from paddle.nn.layer.layers import in_declarative_mode ModuleNotFoundError: No module named 'paddle.nn.layer.layers'| ![image](https://github.com/mattheliu/Camp/assets/102272920/5636462f-9c3e-4972-9342-c90c10cacead)|
| | | [audio_searching](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/audio_searching)|验证中| |需要docker| ![image](https://github.com/mattheliu/Camp/assets/102272920/16b359b4-5e46-4ab2-afff-26d6eb932393)| |  ![image](https://github.com/mattheliu/Camp/assets/102272920/54b75685-5343-4a6d-a23b-e53dba9409f1)|
| |paddlespeech cls --input ./cat.wav --topk 10|[audio_tagging](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/audio_tagging) |验证完成|是| [image](https://github.com/mattheliu/Camp/assets/102272920/235d748d-3dfe-4a3d-816b-130d041f7c62)| | | |
| | |[automatic_video_subtitiles](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/automatic_video_subtitiles) |验证完成|是| ![image](https://github.com/mattheliu/Camp/assets/102272920/b7e57a60-301e-495c-81af-2774df0a8916)| | | |
| | |[custom_streaming_asr](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/custom_streaming_asr) |验证完成|是|需要docker|  ![image](https://github.com/mattheliu/Camp/assets/102272920/37c47a16-cd62-4a07-b3b5-6153acba875e)| | |
| |paddlespeech kws --input ./hey_snips.wav paddlespeech kws --input ./non-keyword.wav|[keyword_spotting](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/keyword_spotting) |验证完成|是| ![image](https://github.com/mattheliu/Camp/assets/102272920/25bafa81-3d30-4e8f-8a48-3f7b356b5af4)| | | |
| | |[metaverse](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/metaverse) |验证中|否|报错| ![image](https://github.com/mattheliu/Camp/assets/102272920/2a037ed4-5b4a-4234-8596-673923bb3e93)| | |
| |paddlespeech text --input 今天的天气真不错啊你下午有空吗我想约你一起去吃饭| [punctuation_restoration](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/punctuation_restoration)|验证完成|是| | | | |
| |paddlespeech vector --task spk --input 85236145389.wav|[speaker_verification](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speaker_verification) |验证完成|是| ![image](https://github.com/mattheliu/Camp/assets/102272920/fb9602ef-4055-460c-b8ba-4a2ba231bded) | | | |
| |paddlespeech asr --input ./zh.wav -v| [speech_recognition](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_recognition)|验证完成|是|  ![image](https://github.com/mattheliu/Camp/assets/102272920/abb6e456-05e2-4dda-99f3-6221dd99b332)| | | |
| |paddlespeech asr --model transformer_librispeech --lang en --input ./en.wav -v|  [speech_recognition](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_recognition)|验证完成|是| | | | |
| |paddlespeech asr --model conformer_talcs --lang zh_en --codeswitch True --input ./ch_zh_mix.wav -v|  [speech_recognition](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_recognition)|验证完成|是| | | | |
| |paddlespeech asr --input ./zh.wav -v "。 paddlespeech text --task punc -v|[speech_recognition](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_recognition)|验证完成|是| | | | |
| |paddlespeech_server start --config_file ./conf/application.yaml| [speech_server](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_server)|验证中|否| ![image](https://github.com/mattheliu/Camp/assets/102272920/5eb18ed0-9cc2-405b-8128-9f11b62a51c0)| | |  ![image](https://github.com/mattheliu/Camp/assets/102272920/0c57f4c9-5988-48ce-9cd2-705b003b1eb0)|
| |paddlespeech ssl --task asr --lang en --input ./en.wav|[speech_ssl](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_ssl)|验证中|否| ![image](https://github.com/mattheliu/Camp/assets/102272920/69df4d6f-4918-4c18-91b9-4eb75e503050)| | | |
| |paddlespeech ssl --task vector --lang en --input ./en.wav|demos/speech_ssl|验证中|否| | | | |
| |paddlespeech st --input ./en.wav|[speech_translation](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_translation) |验证完成|是| ![image](https://github.com/mattheliu/Camp/assets/102272920/2831f0dc-3476-47b7-ab93-b7ffe33c52e9)| | | |
| | | [speech_web](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/speech_web) |验证完成|是|  ![image](https://github.com/mattheliu/Camp/assets/102272920/6585d22d-3adf-4367-96fb-4eb9f131bfd3)| | | |
| |paddlespeech_server start --config_file ./conf/ws_conformer_wenetspeech_application.yaml|[streaming_asr_server](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/streaming_asr_server)|验证完成|是| ![image](https://github.com/mattheliu/Camp/assets/102272920/b397ab55-293b-4885-9cf5-2e0e5f674e89)| | | |
| |paddlespeech_server start --config_file ./conf/ws_conformer_wenetspeech_application_faster.yaml| | | | | | | |
| |paddlespeech_client asr_online --server_ip 127.0.0.1 --port 8090 --input ./zh.wav| | | | | | | |
| |paddlespeech_server start --config_file conf/punc_application.yaml| | | | | | | |
| |paddlespeech whisper --task transcribe --input ./zh.wav|demos/whisper|验证中| | | | | |
| |paddlespeech whisper --lang en --size base --task transcribe --input ./en.wav| |验证中| | | | | |
| |paddlespeech whisper --task translate --input ./zh.wav|  [whisper](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/whisper)|验证中|否|报错PaddlePaddle version 2.3.0 or higher is required, but 0.0.0 installed, Maybe you are using a develop version, please make sure the version is good with your code.| | | |
|TTS|paddlespeech tts --input "你好，欢迎使用百度飞桨深度学习框架！"|[text_to_speech](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/text_to_speech) |验证中|否| ![image](https://github.com/mattheliu/Camp/assets/102272920/45eadf64-59c2-4536-b4ba-e400a4be9d9e)| | | |
| | | |验证中| | | | | |
| | | |验证中| | | | | |
| | | |验证中| | | | | |
| | | |验证中| | | | | |
| | | [streaming_tts_server](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/streaming_tts_server)|验证中|否| | | | |
| | |[streaming_tts_serving_fastdeploy](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/streaming_tts_serving_fastdeploy) |验证中|否|需要docker|  ![image](https://github.com/mattheliu/Camp/assets/102272920/7bcb6c2c-cabc-4dd2-80f2-2e58d8750dfb)| | |
| | |[style_fs2](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/style_fs2)|验证中|否| ![image](https://github.com/mattheliu/Camp/assets/102272920/17c938ed-1f4e-4c52-9e90-da31b88c05a7) | | | |
| | |[story_talker](https://github.com/PaddlePaddle/PaddleSpeech/tree/develop/demos/story_talker)|验证中|否| [image](https://github.com/mattheliu/Camp/assets/102272920/3ca1ed1e-9473-4bb5-8def-d4126a5ffa6b) | | | |

### 下周工作

1. 修复Issue #3652 #3544 #3530
2. 修复demos/speech_server和demos/audio_content_search中存在的bug

### 导师点评
