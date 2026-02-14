# 🎙️ Qwen-TTS CLI

A command-line text-to-speech tool built with **Qwen3-TTS**, managed with **uv**, and exposed via a **Click CLI**.

This project is designed for:

* Language learning audio generation
* Assignment narration
* Accessibility overlays
* Classroom TTS labs
* Rapid speech prototyping from text files

---

## ✨ Features

* 🧠 Qwen3-TTS speech synthesis
* 🗣️ CustomVoice + VoiceDesign models
* 🎛️ Style prompting (`--instruct`)
* 📄 Text or file input
* 💻 CPU or GPU support
* ⚡ uv-managed reproducible environment
* 🧩 Click-based CLI
* 🤖 Smolagents integration for AI agent workflows

---

## 📦 Project Structure

```
qwen_tts_cli/
├── main.py
├── pyproject.toml
├── README.md
└── .venv/
```

---

## 🚀 Quick Start

### 1️⃣ Clone / create project

```bash
git clone <repo-url>
cd qwen_tts_cli
```

Or initialize locally:

```bash
uv init
```

---

### 2️⃣ Install dependencies

```bash
uv sync
```

Dependencies include:

* qwen-tts
* transformers (pinned)
* numpy (pinned)
* soundfile
* click

---

### 3️⃣ Run the CLI

```bash
uv run -- qwen-tts-cli \
  --text "Ciao! Benvenuto all'esercizio." \
  --out lesson.wav
```

---

## 🗣️ Example: Language Assignment Audio

```bash
uv run -- qwen-tts-cli \
  --text-file lesson1.txt \
  --language Italian \
  --instruct "Voce di insegnante, ritmo lento, pronuncia chiara." \
  --out airport.wav
```

---

## 📄 Example Input File

**lesson1.txt**

```
All’aeroporto:

Dov’è il ritiro bagagli?
Dove posso prendere un taxi?
Dove si prende lo shuttle per andare alla Stazione Termini?
```

---

## 🎛️ CLI Options

| Option        | Description         |
| ------------- | ------------------- |
| `--model`     | HF model id         |
| `--language`  | Spoken language     |
| `--speaker`   | CustomVoice speaker |
| `--instruct`  | Voice style prompt  |
| `--text`      | Inline text         |
| `--text-file` | Path to text file   |
| `--out`       | Output WAV file     |
| `--device`    | auto / cpu / cuda   |

---

## 🧠 Model Examples

| Model                        | Use Case              |
| ---------------------------- | --------------------- |
| `Qwen3-TTS-0.6B-CustomVoice` | Fast classroom demos  |
| `Qwen3-TTS-0.6B-Base`        | Voice cloning         |
| `Qwen3-TTS-1.7B-VoiceDesign` | Style-designed voices |

---

## 🎨 Voice Style Prompting

Example:

```bash
--instruct "Voce di insegnante, lenta, incoraggiante."
```

Other ideas:

* News anchor
* Tourist guide
* Sci-fi narrator
* ASMR whisper
* Language lab instructor

---

## 🖥️ GPU Support (Optional)

If running on CUDA (WSL + NVIDIA):

```bash
uv pip install \
  --index-url https://download.pytorch.org/whl/cu121 \
  torch torchvision torchaudio
```

Verify:

```bash
uv run -- python -c "import torch; print(torch.cuda.is_available())"
```

---

## 🧪 Development

Run script directly:

```bash
uv run -- python src/qwen_tts_cli/cli.py --text "Test" --out audio/test.wav
```

---

## 🤖 AI Agent Integration (Smolagents)

Use Qwen-TTS as a tool in AI agent workflows with [smolagents](https://github.com/huggingface/smolagents):

**Install smolagents support:**

```bash
uv sync --extra smolagents
```

**Use as a tool:**

```python
from smolagents import CodeAgent, HfApiModel
from qwen_tts_cli.smolagent_tool import QwenTTSTool

tts_tool = QwenTTSTool()
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(tools=[tts_tool], model=model, add_base_tools=True)

agent.run("Generate Italian audio saying 'Benvenuto!' in a teacher's voice")
```

See [examples/README.md](examples/README.md) for more details.

---

## 📚 Educational Use Cases

* Language listening exercises
* Pronunciation drills
* Assignment narration
* Accessibility audio overlays
* LMS content generation

---

## 🛠️ Troubleshooting

### NumPy import errors

Ensure pinned version:

```bash
uv add "numpy==2.1.3"
uv sync
```

### Transformers import issues

Pin version:

```bash
uv add "transformers==4.57.3"
```

### Model download slow

Use smaller checkpoint:

```
Qwen3-TTS-0.6B-CustomVoice
```

---

## 📜 License

See upstream model + repo licenses:

* Qwen3-TTS
* Hugging Face Transformers

---

## 🙌 Credits

* QwenLM
* Hugging Face
* Astral uv
* Click CLI

---

## 📣 Future Enhancements

* Preset voice styles
* Batch folder processing
* Subtitle (.srt) export
* Gradio web UI
* LMS integration tooling

---

Happy synthesizing 🎙️
