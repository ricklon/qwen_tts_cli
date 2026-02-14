# Smolagents Integration Examples

This directory contains examples of using Qwen-TTS CLI as a tool with [smolagents](https://github.com/huggingface/smolagents).

## What is Smolagents?

Smolagents is a lightweight library from Hugging Face for building AI agents that can use tools. It allows you to create agents that can plan, reason, and execute tasks using LLMs.

## Installation

Install the smolagents optional dependencies:

```bash
uv sync --extra smolagents
```

Or with pip:

```bash
uv pip install "qwen-tts-cli[smolagents]"
```

## Quick Start

### Option 1: Using the Tool Class

```python
from smolagents import CodeAgent, HfApiModel
from qwen_tts_cli.smolagent_tool import QwenTTSTool

# Initialize the tool
tts_tool = QwenTTSTool()

# Create an agent
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(tools=[tts_tool], model=model, add_base_tools=True)

# Use the agent
agent.run("Generate Italian audio saying 'Ciao!' in a friendly voice")
```

### Option 2: Using the Decorator (Simpler)

```python
from smolagents import CodeAgent, HfApiModel
from qwen_tts_cli.smolagent_tool import create_qwen_tts_tool

# Create the tool
tts_tool = create_qwen_tts_tool()

# Use with agent (same as above)
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(tools=[tts_tool], model=model, add_base_tools=True)
```

### Option 3: Direct Tool Usage (No Agent)

```python
from qwen_tts_cli.smolagent_tool import QwenTTSTool

# Use the tool directly
tts_tool = QwenTTSTool()
result = tts_tool(
    text="Hello world!",
    language="English",
    instruct="Clear and friendly voice",
    output_filename="hello.wav"
)
print(result)  # Audio generated successfully: /path/to/audio/hello.wav
```

## Running Examples

```bash
# Run the interactive example chooser
uv run -- python examples/smolagent_example.py

# Or run directly
uv run -- python examples/smolagent_example.py
```

## Tool Parameters

The Qwen-TTS tool accepts the following parameters:

- **text** (string, required): The text to convert to speech
- **language** (string, default: "English"): Target language (e.g., "Italian", "Spanish", "French")
- **instruct** (string, default: "Clear and natural voice"): Voice style instruction
  - Examples: "Teacher voice, slow pace", "News anchor", "Friendly conversational"
- **output_filename** (string, default: "agent_output.wav"): Output filename (saved in `audio/` directory)
- **device** (string, default: "auto"): Device to use ("auto", "cpu", or "cuda")

## Use Cases

### Language Learning Assistant

```python
agent.run(
    "Create pronunciation exercises for Italian airport vocabulary, "
    "using a slow, clear teacher voice"
)
```

### Content Narration

```python
agent.run(
    "Read this assignment text in a professional narrator voice and save it as assignment_audio.wav"
)
```

### Multilingual Content Creation

```python
agent.run(
    "Generate greetings in 3 languages: English, Spanish, and Italian, "
    "each with an appropriate voice style"
)
```

## Sharing Your Tool to Hugging Face Hub

You can share your Qwen-TTS tool to the Hub:

```python
from qwen_tts_cli.smolagent_tool import QwenTTSTool

tool = QwenTTSTool()
tool.push_to_hub("your-username/qwen-tts-tool", token="your_hf_token")
```

Then others can load it:

```python
from smolagents import load_tool

tool = load_tool("your-username/qwen-tts-tool", trust_remote_code=True)
```

## Requirements

- Hugging Face account and API token for using agents with HF models
- Set your token: `export HF_TOKEN=your_token_here`
- Or use local models with smolagents

## Learn More

- [Smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Smolagents GitHub](https://github.com/huggingface/smolagents)
- [Tool Tutorial](https://huggingface.co/docs/smolagents/tutorials/tools)
