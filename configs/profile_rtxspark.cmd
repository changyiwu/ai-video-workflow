@echo off
rem RTX Spark laptop (Windows on Arm, 64GB unified memory shared by CPU and GPU). NOT TESTED YET - see docs\hardware_rtxspark.md
rem Same models as the 16GB VRAM versions. Unified memory: pinned host memory and async offload only duplicate data in the same pool, so turn them off.
rem --reserve-vram 6 leaves room for Windows and the desktop in the shared pool. If H3 runs out of memory, raise it or add --lowvram.
set COMFY_HOST=http://127.0.0.1:8188
set COMFY_DIR=C:\AI\H3\ComfyUI-0.36.0
set H3_UNET=minimax_h3_ref2va_pruned_int8_convrot.safetensors
set H3_CLIP=qwen3vl_32b_h3_ultra_uncensored_heretic_int8_convrot.safetensors
set H3_VIDEO_VAE=minimax_h3_video_vae_fp16.safetensors
set COMFY_EXTRA_ARGS=--reserve-vram 6 --disable-pinned-memory --disable-async-offload
rem RTX VSR (nvidia-vfx) has no Windows ARM64 build: upscale with ffmpeg lanczos (or set UPSCALE=flashvsr)
set UPSCALE=lanczos
echo [profile] RTX Spark (Windows on Arm, unified memory, UNTESTED): ComfyUI %COMFY_EXTRA_ARGS%, UPSCALE=%UPSCALE%. Close other big apps.
