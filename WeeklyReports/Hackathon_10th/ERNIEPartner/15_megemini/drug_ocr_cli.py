#!/usr/bin/env python3
"""Drug instruction leaflet intelligent recognition and voice broadcast pipeline - CLI.

Usage:
    python drug_ocr_cli.py --image resource/1.jpg
    python drug_ocr_cli.py --image resource/1.jpg --no-split --ocr-tokens 5120 --llm-tokens 1024
    python drug_ocr_cli.py --image resource/1.jpg --num-splits 9 --overlap 0.15
"""

import argparse
import base64
import gc
import io
import logging
import math
import os
import sys
import tempfile
import time
from multiprocessing import Process, Queue
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.io.wavfile import read as wav_read
from scipy.io.wavfile import write as wav_write

logger = logging.getLogger("drug_ocr")


# ============================================================================
# Image splitting
# ============================================================================

def split_image(image, num_splits=4, overlap_ratio=0.1):
    """Split an image into num_splits parts (NxN grid) with overlap."""
    grid_size = int(math.sqrt(num_splits))
    if grid_size * grid_size != num_splits:
        raise ValueError(f"num_splits must be a perfect square (e.g. 4, 9, 16), got: {num_splits}")

    w, h = image.size
    cell_w = w / grid_size
    cell_h = h / grid_size
    overlap_w = cell_w * overlap_ratio
    overlap_h = cell_h * overlap_ratio

    sub_images = []
    for row in range(grid_size):
        for col in range(grid_size):
            left = max(0, col * cell_w - overlap_w)
            upper = max(0, row * cell_h - overlap_h)
            right = min(w, (col + 1) * cell_w + overlap_w)
            lower = min(h, (row + 1) * cell_h + overlap_h)
            sub_img = image.crop((int(left), int(upper), int(right), int(lower)))
            sub_images.append(sub_img)

    return sub_images


# ============================================================================
# OCR module (subprocess)
# ============================================================================

def ocr_worker_process(ocr_model_dir, image_data_list, max_new_tokens, result_queue):
    """Worker function for OCR subprocess - loads model, performs OCR, returns result."""
    try:
        import time
        import base64
        import io
        from PIL import Image
        from fastdeploy import LLM, SamplingParams

        # Load OCR model
        print("[OCR Worker] Loading OCR model (PaddleOCR-VL)...")
        start = time.perf_counter()
        ocr_model = LLM(
            model=ocr_model_dir,
            tensor_parallel_size=1,
            max_model_len=8192,
            block_size=16,
            quantization="wint8",
            graph_optimization_config={"use_cudagraph": False},
        )
        elapsed = time.perf_counter() - start
        print(f"[OCR Worker] OCR model loaded, elapsed: {elapsed:.2f}s")

        # Process each image
        all_ocr_texts = []
        for i, img_bytes in enumerate(image_data_list):
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            print(f"[OCR Worker] Recognizing image {i+1}/{len(image_data_list)}, size: {image.size}")

            # Prepare image for OCR
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
            image_url = f"data:image/png;base64,{base64_image}"

            prompts = [{
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": "OCR:"},
                    ],
                }]
            }]
            sampling_params = SamplingParams(
                temperature=0.8, top_p=0.95, max_tokens=max_new_tokens,
            )
            outputs = ocr_model.generate(prompts, sampling_params)
            response = outputs[0].outputs.text
            all_ocr_texts.append(response)
            print(f"[OCR Worker] Image {i+1} done, text length: {len(response)}")

        # Combine results
        combined_text = "\n\n".join(all_ocr_texts)
        print(f"[OCR Worker] All images done, total text length: {len(combined_text)}")

        # Put result in queue
        result_queue.put(("success", combined_text))

        # Clean up
        del ocr_model
        import gc
        gc.collect()
        print("[OCR Worker] OCR model released")

    except Exception as e:
        import traceback
        result_queue.put(("error", str(e) + "\n" + traceback.format_exc()))


def ocr_step(
    ocr_model_dir,
    image_path,
    enable_split=True,
    num_splits=4,
    overlap_ratio=0.1,
    max_new_tokens=5120,
):
    """Execute the OCR step in a subprocess: load image, optionally split, and run OCR."""
    step_start = time.perf_counter()
    logger.info("[OCR Step] Loading image...")
    image = Image.open(image_path).convert("RGB")
    logger.info("[OCR Step] Image loaded, size: %s", image.size)

    if enable_split:
        logger.info("[OCR Step] Splitting image (num_splits=%d, overlap=%.2f)...", num_splits, overlap_ratio)
        sub_images = split_image(image, num_splits=num_splits, overlap_ratio=overlap_ratio)
        ocr_images = [image] + sub_images
        logger.info("[OCR Step] Split done, 1 original + %d split = %d total", len(sub_images), len(ocr_images))
    else:
        logger.info("[OCR Step] Skipping image split")
        ocr_images = [image]

    # Serialize images to bytes for subprocess
    image_data_list = []
    for img in ocr_images:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        image_data_list.append(buf.getvalue())

    # Create subprocess for OCR
    logger.info("[OCR Step] Starting OCR subprocess...")
    result_queue = Queue()
    ocr_process = Process(
        target=ocr_worker_process,
        args=(str(ocr_model_dir), image_data_list, max_new_tokens, result_queue)
    )
    ocr_process.start()

    # Wait for result
    status, result = result_queue.get()
    ocr_process.join()
    ocr_process.close()

    if status == "error":
        logger.error("[OCR Step] OCR subprocess failed: %s", result)
        raise RuntimeError(f"OCR subprocess failed: {result}")

    combined_ocr_text = result
    logger.info("[OCR Step] OCR complete, total text length: %d, elapsed: %.2fs", len(combined_ocr_text), time.perf_counter() - step_start)

    return {"ocr_text": combined_ocr_text, "ocr_images": ocr_images}


# ============================================================================
# LLM module (subprocess)
# ============================================================================

def clean_for_tts(text):
    """Clean text for TTS synthesis by removing emojis and markdown formatting."""
    import re
    # Remove emojis (Unicode ranges for common emojis)
    # NOTE: Must avoid ranges that overlap with CJK characters (U+4E00-U+9FFF)
    text = re.sub(
        r"[\U0001F600-\U0001F64F"  # emoticons
        r"\U0001F300-\U0001F5FF"   # symbols & pictographs
        r"\U0001F680-\U0001F6FF"   # transport & map
        r"\U0001F1E0-\U0001F1FF"   # flags
        r"\U00002702-\U000027B0"   # dingbats
        r"\U000024C2-\U0000324F"   # enclosed alphanumerics (stop before CJK)
        r"\U0001F200-\U0001F251"   # enclosed CJK supplement (above CJK range)
        r"\U0001F900-\U0001F9FF"   # supplemental symbols
        r"\U0001FA00-\U0001FA6F"   # chess symbols
        r"\U0001FA70-\U0001FAFF"   # symbols extended-A
        r"\U00002600-\U000026FF"   # misc symbols
        r"\U0000FE00-\U0000FE0F"   # variation selectors
        r"\U0000200D"              # zero-width joiner
        r"]+",
        "",
        text,
    )
    # Remove markdown code blocks (```...```)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove inline code (`...`) -> content
    text = re.sub(r"`([^`\n]+)`", r"\1", text)
    # Remove markdown headers (# ## ### etc.) at line start
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove markdown bold (**text**) -> text
    text = re.sub(r"\*\*([^*\n]+?)\*\*", r"\1", text)
    # Remove markdown bold (__text__) -> text
    text = re.sub(r"__([^_\n]+?)__", r"\1", text)
    # Remove markdown italic (*text*) -> text
    text = re.sub(r"\*([^*\n]+?)\*", r"\1", text)
    # Remove markdown italic (_text_) -> text (only when _ is at word boundary)
    text = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"\1", text)
    # Remove markdown links [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove markdown images ![alt](url)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    # Remove markdown horizontal rules (---, ***, ___)
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Remove markdown bullet list markers (- , * , + ) at line start, keep content
    text = re.sub(r"^(\s*)[-*+]\s+", r"\1", text, flags=re.MULTILINE)
    # Remove markdown numbered list markers (1. 2. etc.) at line start, keep content
    text = re.sub(r"^(\s*)\d+\.\s+", r"\1", text, flags=re.MULTILINE)
    # Remove markdown table pipes
    text = re.sub(r"\|", " ", text)
    # Remove markdown table separator lines (---:---:---)
    text = re.sub(r"^[-: ]+$", "", text, flags=re.MULTILINE)
    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    # Remove leading/trailing whitespace overall
    text = text.strip()
    return text


def llm_worker_process(llm_model_dir, ocr_text, max_new_tokens, result_queue):
    """Worker function for LLM subprocess - loads model, extracts info, returns result."""
    try:
        import time
        from fastdeploy import LLM, SamplingParams

        # Load LLM model
        print("[LLM Worker] Loading LLM model (ERNIE)...")
        start = time.perf_counter()
        llm_model = LLM(
            model=llm_model_dir,
            tensor_parallel_size=1,
            max_model_len=8192,
            block_size=16,
            quantization="wint8",
            graph_optimization_config={"use_cudagraph": False},
        )
        elapsed = time.perf_counter() - start
        print(f"[LLM Worker] LLM model loaded, elapsed: {elapsed:.2f}s")

        # Prepare prompt
        prompt_text = f"""以下是药品说明书的 OCR 识别结果，供参考：

{ocr_text}

请根据以上 OCR 识别结果，提取并整理以下关键信息，用清晰易懂的语言重新表述，方便老年人阅读理解：

1. 药品名称
2. 药品适应症（这个药治什么病）
3. 药品的用法与用量（怎么吃、吃多少）
4. 药品的禁忌（什么人不能吃、什么情况不能吃）
5. 药品的不良反应（吃药后可能出现的不舒服）

要求：
- 只输出整理后的关键信息，不要重复或复述 OCR 原文
- 用简洁、通俗的语言回答，避免使用专业术语
- 不要使用表情符号、emoji
- 不要使用markdown格式符号（如#、**、-等），直接用纯文本输出
- 用自然流畅的口语化表达，方便语音播报
- 总字数控制在 {max_new_tokens} 字以内"""

        prompts = [prompt_text]
        sampling_params = SamplingParams(
            temperature=0.8, top_p=0.95, max_tokens=max_new_tokens,
        )

        print(f"[LLM Worker] Generating response (max_new_tokens={max_new_tokens})...")
        gen_start = time.perf_counter()
        outputs = llm_model.generate(prompts, sampling_params)
        result = outputs[0].outputs.text
        gen_elapsed = time.perf_counter() - gen_start

        # Clean result
        result = clean_for_tts(result)
        print(f"[LLM Worker] Extraction done, gen elapsed: {gen_elapsed:.2f}s, result length: {len(result)}")

        # Put result in queue
        result_queue.put(("success", result))

        # Clean up
        del llm_model
        import gc
        gc.collect()
        print("[LLM Worker] LLM model released")

    except Exception as e:
        import traceback
        result_queue.put(("error", str(e) + "\n" + traceback.format_exc()))


def llm_step(
    llm_model_dir,
    ocr_text,
    max_new_tokens=1024,
):
    """Execute the LLM extraction step in a subprocess."""
    step_start = time.perf_counter()
    logger.info("[LLM Step] LLM extraction...")

    # Create subprocess for LLM
    logger.info("[LLM Step] Starting LLM subprocess...")
    result_queue = Queue()
    llm_process = Process(
        target=llm_worker_process,
        args=(str(llm_model_dir), ocr_text, max_new_tokens, result_queue)
    )
    llm_process.start()

    # Wait for result
    status, result = result_queue.get()
    llm_process.join()
    llm_process.close()

    if status == "error":
        logger.error("[LLM Step] LLM subprocess failed: %s", result)
        raise RuntimeError(f"LLM subprocess failed: {result}")

    extracted_info = result
    logger.info("[LLM Step] LLM extraction done, result length: %d, elapsed: %.2fs", len(extracted_info), time.perf_counter() - step_start)

    return {"extracted_info": extracted_info}


# ============================================================================
# TTS module (subprocess)
# ============================================================================

def tts_worker_process(text, output_path, result_queue):
    """Worker function for TTS subprocess - loads model, synthesizes speech, returns result."""
    try:
        import time
        from paddlespeech.cli.tts.infer import TTSExecutor
        from scipy.io.wavfile import read as wav_read

        # Load TTS model
        print("[TTS Worker] Loading TTS model (PaddleSpeech)...")
        start = time.perf_counter()
        tts_model = TTSExecutor()
        elapsed = time.perf_counter() - start
        print(f"[TTS Worker] TTS model loaded, elapsed: {elapsed:.2f}s")

        # Synthesize speech
        print(f"[TTS Worker] Synthesis start, input text length: {len(text)}")
        tts_model(text=text, output=output_path)

        # Read audio data
        sr, wav_data = wav_read(output_path)

        if wav_data is not None:
            audio_duration = len(wav_data) / sr
            print(f"[TTS Worker] Synthesis done, audio duration: {audio_duration:.2f}s, sample rate: {sr} Hz")
            result_queue.put(("success", (sr, wav_data.tolist())))  # Convert to list for serialization
        else:
            print("[TTS Worker] Synthesis failed")
            result_queue.put(("error", "TTS synthesis failed"))

        # Clean up
        del tts_model
        import gc
        gc.collect()
        print("[TTS Worker] TTS model released")

    except Exception as e:
        import traceback
        result_queue.put(("error", str(e) + "\n" + traceback.format_exc()))


def tts_step(
    text,
    output_path="output.wav",
):
    """Execute the TTS synthesis step in a subprocess."""
    step_start = time.perf_counter()
    logger.info("[TTS Step] TTS synthesis...")

    # Create subprocess for TTS
    logger.info("[TTS Step] Starting TTS subprocess...")
    result_queue = Queue()
    tts_process = Process(
        target=tts_worker_process,
        args=(text, output_path, result_queue)
    )
    tts_process.start()

    # Wait for result
    status, result = result_queue.get()
    tts_process.join()
    tts_process.close()

    if status == "error":
        logger.error("[TTS Step] TTS subprocess failed: %s", result)
        logger.warning("[TTS Step] TTS synthesis failed")
        return {"audio": None}

    sr, wav_data_list = result
    wav_data = np.array(wav_data_list, dtype=np.int16)  # Convert back from list

    audio_duration = len(wav_data) / sr
    logger.info("[TTS Step] TTS synthesis done, audio duration: %.2fs, elapsed: %.2fs", audio_duration, time.perf_counter() - step_start)

    return {"audio": (sr, wav_data)}


# ============================================================================
# Pipeline
# ============================================================================

def drug_ocr_pipeline(
    ocr_model_dir,
    llm_model_dir,
    image_path,
    enable_split=True,
    num_splits=4,
    overlap_ratio=0.1,
    ocr_max_new_tokens=5120,
    llm_max_new_tokens=1024,
):
    """Drug instruction leaflet intelligent recognition and voice broadcast pipeline.

    Uses subprocess for each model to ensure proper memory cleanup.
    """
    pipeline_start = time.perf_counter()
    logger.info("=" * 60)
    logger.info("Drug OCR pipeline started (subprocess mode)")
    logger.info("  Image path: %s", image_path)
    logger.info("  Image split: %s (num_splits=%d, overlap=%.2f)", enable_split, num_splits, overlap_ratio)
    logger.info("=" * 60)

    result = {}

    # Step 1: OCR (runs in subprocess, automatically cleaned up)
    ocr_result = ocr_step(
        ocr_model_dir=ocr_model_dir,
        image_path=image_path,
        enable_split=enable_split,
        num_splits=num_splits,
        overlap_ratio=overlap_ratio,
        max_new_tokens=ocr_max_new_tokens,
    )
    result["ocr_text"] = ocr_result["ocr_text"]

    # Step 2: LLM extraction (runs in subprocess, automatically cleaned up)
    llm_result = llm_step(
        llm_model_dir=llm_model_dir,
        ocr_text=ocr_result["ocr_text"],
        max_new_tokens=llm_max_new_tokens,
    )
    result["extracted_info"] = llm_result["extracted_info"]

    # Step 3: TTS synthesis (runs in subprocess, automatically cleaned up)
    tts_result = tts_step(
        text=llm_result["extracted_info"],
    )
    result["audio"] = tts_result["audio"]

    pipeline_elapsed = time.perf_counter() - pipeline_start
    logger.info("=" * 60)
    logger.info("Pipeline complete, total elapsed: %.2fs", pipeline_elapsed)
    logger.info("=" * 60)

    return result


# ============================================================================
# CLI entry point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Drug instruction leaflet intelligent recognition and voice broadcast pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python drug_ocr_cli.py --image resource/1.jpg
  python drug_ocr_cli.py --image resource/1.jpg --no-split
  python drug_ocr_cli.py --image resource/1.jpg --num-splits 9 --overlap 0.15
  python drug_ocr_cli.py --image resource/1.jpg --ocr-tokens 5120 --llm-tokens 1024
""",
    )
    parser.add_argument("--image", required=True, help="Path to the drug instruction leaflet image")
    parser.add_argument("--ocr-model", default="baidu/PaddleOCR-VL-1.5", help="OCR model directory (default: baidu/PaddleOCR-VL-1.5)")
    parser.add_argument("--llm-model", default="baidu/ERNIE-4.5-0.3B-Paddle", help="LLM model directory (default: baidu/ERNIE-4.5-0.3B-Paddle)")
    parser.add_argument("--no-split", dest="enable_split", action="store_false", help="Disable image splitting")
    parser.add_argument("--num-splits", type=int, default=4, choices=[4, 9, 16], help="Number of image splits (must be perfect square, default: 4)")
    parser.add_argument("--overlap", type=float, default=0.1, help="Overlap ratio for image splits (default: 0.1)")
    parser.add_argument("--ocr-tokens", type=int, default=5120, help="OCR max new tokens (default: 5120)")
    parser.add_argument("--llm-tokens", type=int, default=1024, help="LLM max new tokens (default: 1024)")
    parser.add_argument("--output-audio", default=None, help="Output audio file path (default: output.wav in current directory)")
    parser.add_argument("--output-text", default=None, help="Output extracted text file path (default: print to stdout only)")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Validate image path
    if not os.path.isfile(args.image):
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    # Validate model directories
    if not Path(args.ocr_model).exists():
        print(f"Error: OCR model directory not found: {args.ocr_model}", file=sys.stderr)
        sys.exit(1)
    if not Path(args.llm_model).exists():
        print(f"Error: LLM model directory not found: {args.llm_model}", file=sys.stderr)
        sys.exit(1)

    # Run pipeline
    result = drug_ocr_pipeline(
        ocr_model_dir=args.ocr_model,
        llm_model_dir=args.llm_model,
        image_path=args.image,
        enable_split=args.enable_split,
        num_splits=args.num_splits,
        overlap_ratio=args.overlap,
        ocr_max_new_tokens=args.ocr_tokens,
        llm_max_new_tokens=args.llm_tokens,
    )

    # Print results
    print("\n" + "=" * 60)
    print("OCR Result:")
    print("=" * 60)
    print(result["ocr_text"])

    print("\n" + "=" * 60)
    print("Extracted Info:")
    print("=" * 60)
    print(result["extracted_info"])

    # Save extracted text if requested
    if args.output_text:
        with open(args.output_text, "w", encoding="utf-8") as f:
            f.write(result["extracted_info"])
        print(f"\nExtracted text saved to: {args.output_text}")

    # Save audio
    if result["audio"] is not None:
        sr, wav_data = result["audio"]
        audio_path = args.output_audio or "output.wav"
        wav_write(audio_path, sr, wav_data.astype(np.float32))
        audio_duration = len(wav_data) / sr
        print(f"\nAudio saved to: {audio_path} (duration: {audio_duration:.2f}s)")
    else:
        print("\nTTS synthesis failed, no audio output.")


if __name__ == "__main__":
    main()
