from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


def _load_text(text: Optional[str], text_file: Optional[str]) -> str:
    if text and text_file:
        raise click.UsageError("Use only one of --text or --text-file.")
    if text:
        return text
    if text_file:
        return Path(text_file).read_text(encoding="utf-8")
    raise click.UsageError("Provide --text or --text-file.")


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--model",
    default="Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    show_default=True,
    help="Hugging Face model id. Use a CustomVoice or VoiceDesign checkpoint.",
)
@click.option("--language", default="Italian", show_default=True)
@click.option(
    "--speaker",
    default=None,
    help="CustomVoice speaker name. If omitted, uses the first supported speaker.",
)
@click.option(
    "--instruct",
    default="Voce di insegnante, ritmo lento, pronuncia chiara.",
    show_default=True,
    help="Style instruction for the voice.",
)
@click.option("--text", default=None, help="Text to speak.")
@click.option("--text-file", default=None, type=click.Path(exists=True), help="UTF-8 text file.")
@click.option(
    "--out",
    default="audio/out.wav",
    show_default=True,
)
@click.option(
    "--device",
    type=click.Choice(["auto", "cpu", "cuda"], case_sensitive=False),
    default="auto",
    show_default=True,
    help="Force device selection.",
)
def main(
    model: str,
    language: str,
    speaker: Optional[str],
    instruct: str,
    text: Optional[str],
    text_file: Optional[str],
    out: str,
    device: str,
) -> None:
    """Generate speech audio with Qwen3-TTS and write a WAV file."""
    content = _load_text(text, text_file)

    if device.lower() == "cpu":
        dev = "cpu"
    elif device.lower() == "cuda":
        dev = "cuda:0"
    else:
        dev = "cuda:0" if torch.cuda.is_available() else "cpu"

    dtype = torch.bfloat16 if dev.startswith("cuda") else torch.float32

    click.echo(f"Loading model: {model}")
    click.echo(f"Device: {dev} | dtype: {dtype}")
    tts = Qwen3TTSModel.from_pretrained(model, device_map=dev, dtype=dtype)

    # Choose generation path based on checkpoint type.
    if "CustomVoice" in model:
        chosen_speaker = speaker or tts.get_supported_speakers()[0]
        click.echo(f"Speaker: {chosen_speaker}")
        wavs, sr = tts.generate_custom_voice(
            text=content,
            language=language,
            speaker=chosen_speaker,
            instruct=instruct,
        )
    elif "VoiceDesign" in model:
        wavs, sr = tts.generate_voice_design(
            text=content,
            language=language,
            instruct=instruct,
        )
    else:
        raise click.ClickException(
            "Unsupported model type. Use a model id containing 'CustomVoice' or 'VoiceDesign'."
        )

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out_path.as_posix(), wavs[0], sr)
    click.echo(f"Wrote {out_path} @ {sr} Hz")


if __name__ == "__main__":
    main()
