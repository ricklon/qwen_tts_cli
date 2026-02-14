"""Smolagents tool wrapper for Qwen-TTS CLI.

This module provides a tool that can be used with smolagents to generate
text-to-speech audio using Qwen3-TTS models.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from smolagents import Tool


class QwenTTSTool(Tool):
    """Generate speech audio from text using Qwen3-TTS.

    This tool wraps the qwen-tts-cli command to provide text-to-speech
    capabilities for smolagents. It's particularly useful for:
    - Language learning applications
    - Creating audio narration for assignments
    - Accessibility features
    - Generating spoken content from text
    """

    name = "qwen_tts_generator"
    description = """
    Generates speech audio from text using Qwen3-TTS models.
    Can handle inline text or text from files, supports multiple languages,
    and allows voice style customization through instruction prompts.
    Returns the path to the generated WAV audio file.
    """

    inputs = {
        "text": {
            "type": "string",
            "description": "The text to convert to speech.",
            "nullable": False,
        },
        "language": {
            "type": "string",
            "description": "The target language for speech synthesis (e.g., 'Italian', 'English', 'Spanish'). Default: 'English'",
            "nullable": True,
        },
        "instruct": {
            "type": "string",
            "description": "Voice style instruction (e.g., 'Teacher voice, slow pace, clear pronunciation'). Default: 'Clear and natural voice'",
            "nullable": True,
        },
        "output_filename": {
            "type": "string",
            "description": "Name for the output WAV file (saved in audio/ directory). Default: 'agent_output.wav'",
            "nullable": True,
        },
        "device": {
            "type": "string",
            "description": "Device to use: 'auto', 'cpu', or 'cuda'. Default: 'auto'",
            "nullable": True,
        },
    }

    output_type = "string"

    def forward(
        self,
        text: str,
        language: str = "English",
        instruct: str = "Clear and natural voice",
        output_filename: str = "agent_output.wav",
        device: str = "auto",
    ) -> str:
        """Generate speech audio from text.

        Args:
            text: The text to convert to speech
            language: Target language for speech synthesis
            instruct: Voice style instruction prompt
            output_filename: Name for the output file (in audio/ directory)
            device: Device to use ('auto', 'cpu', or 'cuda')

        Returns:
            Path to the generated WAV audio file
        """
        import os

        # Ensure output filename has .wav extension
        if not output_filename.endswith(".wav"):
            output_filename = f"{output_filename}.wav"

        # Construct output path (audio/ directory)
        output_path = f"audio/{output_filename}"

        # Build the CLI command
        cmd = [
            "uv", "run", "--",
            "qwen-tts-cli",
            "--text", text,
            "--language", language,
            "--instruct", instruct,
            "--out", output_path,
            "--device", device,
        ]

        # Execute the command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            )

            # Return the absolute path to the generated file
            abs_path = str(Path(output_path).absolute())
            return f"Audio generated successfully: {abs_path}"

        except subprocess.CalledProcessError as e:
            return f"Error generating audio: {e.stderr}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# Alternative: Simple decorator-based tool (recommended for basic usage)
def create_qwen_tts_tool():
    """Create a simple Qwen-TTS tool using the @tool decorator.

    This is a simpler alternative to the full Tool class above.
    Use this if you don't need the full class structure.
    """
    from smolagents import tool

    @tool
    def qwen_tts_generator(
        text: str,
        language: str = "English",
        instruct: str = "Clear and natural voice",
        output_filename: str = "agent_output.wav",
        device: str = "auto",
    ) -> str:
        """Generate speech audio from text using Qwen3-TTS.

        Converts text to speech using Qwen3-TTS models. Supports multiple languages
        and voice style customization through instruction prompts.

        Args:
            text: The text to convert to speech
            language: Target language for speech synthesis (e.g., 'Italian', 'English')
            instruct: Voice style instruction (e.g., 'Teacher voice, slow pace')
            output_filename: Name for the output file (saved in audio/ directory)
            device: Device to use ('auto', 'cpu', or 'cuda')

        Returns:
            Path to the generated WAV audio file
        """
        import subprocess
        from pathlib import Path
        import os

        # Ensure output filename has .wav extension
        if not output_filename.endswith(".wav"):
            output_filename = f"{output_filename}.wav"

        # Construct output path
        output_path = f"audio/{output_filename}"

        # Build the CLI command
        cmd = [
            "uv", "run", "--",
            "qwen-tts-cli",
            "--text", text,
            "--language", language,
            "--instruct", instruct,
            "--out", output_path,
            "--device", device,
        ]

        # Execute the command
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            abs_path = str(Path(output_path).absolute())
            return f"Audio generated successfully: {abs_path}"
        except subprocess.CalledProcessError as e:
            return f"Error generating audio: {e.stderr}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return qwen_tts_generator


# Example usage
if __name__ == "__main__":
    print("Testing Qwen-TTS smolagent tool...\n")

    # Using the decorator version (recommended and tested)
    simple_tool = create_qwen_tts_tool()
    print(f"Tool name: {simple_tool.name}")
    print(f"Tool description: {simple_tool.description[:100]}...\n")

    result = simple_tool(
        text="Ciao! Come stai?",
        language="Italian",
        instruct="Teacher voice, slow and clear",
        output_filename="test_smolagent.wav",
        device="cpu"
    )
    print(f"Result: {result}")

    # Note: The Tool class version (QwenTTSTool) may have compatibility issues
    # with some versions of smolagents. Use create_qwen_tts_tool() instead.
