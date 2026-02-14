# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A command-line text-to-speech tool using Qwen3-TTS for educational applications (language learning, assignment narration, accessibility). Built with Click CLI and managed with uv.

## Development Environment

### Package Management
This project uses **uv** for dependency management and task execution.

**Install dependencies:**
```bash
uv sync
```

**Run the CLI:**
```bash
uv run -- qwen-tts-cli --text "Your text here" --out audio/output.wav
```

**Run directly via Python:**
```bash
uv run -- python src/qwen_tts_cli/cli.py --text "Test" --out audio/test.wav
```

**Note:** Output directory (`audio/` by default) is created automatically if it doesn't exist.

### Critical Dependencies
The following dependencies are **pinned** for stability:
- `numpy==2.1.3` - Import errors occur with other versions
- `transformers==4.57.3` - Required for Qwen3-TTS compatibility

Do not change these versions without testing thoroughly.

### GPU Support (Optional)
For CUDA support on WSL + NVIDIA:
```bash
uv pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio
```

Verify GPU availability:
```bash
uv run -- python -c "import torch; print(torch.cuda.is_available())"
```

### Performance Optimization (Optional)
Installing `flash-attn` improves inference speed but is not required:
```bash
uv pip install flash-attn
```
The CLI will show a warning if flash-attn is not installed, but will work correctly using the manual PyTorch version.

## Architecture

### Entry Point
The CLI entry point is defined in [pyproject.toml:15](pyproject.toml#L15):
```toml
[project.scripts]
qwen-tts-cli = "qwen_tts_cli.cli:main"
```

### Code Structure
- **[src/qwen_tts_cli/cli.py](src/qwen_tts_cli/cli.py)** - Single module containing entire CLI logic
- All functionality is in one file by design for simplicity

### Generation Paths
The CLI supports two model types with distinct generation methods:

1. **CustomVoice models** ([cli.py:82-90](src/qwen_tts_cli/cli.py#L82-L90))
   - Model ID contains "CustomVoice"
   - Requires speaker selection
   - Uses `tts.generate_custom_voice()`
   - Example: `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`

2. **VoiceDesign models** ([cli.py:91-96](src/qwen_tts_cli/cli.py#L91-L96))
   - Model ID contains "VoiceDesign"
   - No speaker parameter
   - Uses `tts.generate_voice_design()`
   - Example: `Qwen3-TTS-1.7B-VoiceDesign`

When adding features, respect this dual-path architecture.

### Device Selection Logic
The CLI auto-detects CUDA availability ([cli.py:68-75](src/qwen_tts_cli/cli.py#L68-L75)):
- `--device auto` - Uses CUDA if available, falls back to CPU
- `--device cuda` - Forces CUDA (fails if unavailable)
- `--device cpu` - Forces CPU
- Uses `torch.bfloat16` for CUDA, `torch.float32` for CPU

### Text Input
Text can be provided via ([cli.py:12-19](src/qwen_tts_cli/cli.py#L12-L19)):
- `--text` - Inline text string
- `--text-file` - Path to UTF-8 text file
- Mutually exclusive (enforced by `_load_text()`)

## Example Usage

**Basic usage:**
```bash
uv run -- qwen-tts-cli --text "Ciao! Benvenuto." --out audio/lesson.wav
```

**From file with custom style:**
```bash
uv run -- qwen-tts-cli \
  --text-file text/airport_lesson.txt \
  --language Italian \
  --instruct "Voce di insegnante, ritmo lento, pronuncia chiara." \
  --out audio/airport.wav
```

**Force CPU execution:**
```bash
uv run -- qwen-tts-cli --text "Test" --out audio/test.wav --device cpu
```

## Smolagents Integration

The project includes a smolagents tool wrapper at [src/qwen_tts_cli/smolagent_tool.py](src/qwen_tts_cli/smolagent_tool.py).

**Install smolagents:**
```bash
uv sync --extra smolagents
```

**Two implementation approaches:**
1. **`QwenTTSTool` class** - Full `Tool` subclass with all metadata
2. **`create_qwen_tts_tool()` function** - Returns a `@tool` decorated function (simpler)

**Examples:** See [examples/smolagent_example.py](examples/smolagent_example.py) and [examples/README.md](examples/README.md)

**Key points:**
- Tool calls `uv run -- qwen-tts-cli` via subprocess
- All imports must be inside methods (required for Hub sharing)
- Returns path to generated audio file as string
- Can be shared to Hugging Face Hub with `tool.push_to_hub()`

## Git Workflow

**Default branch:** `main` (not `master`)

When creating commits or pull requests, target the `main` branch.
