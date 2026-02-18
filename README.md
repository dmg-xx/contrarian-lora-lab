# The Contrarian Lab: A Local LoRA Persona Framework

**The Contrarian Lab** is a specialized environment for developing and deploying **highly skeptical and eccentric behavioral archetypes** using Low-Rank Adaptation (LoRA) on Apple Silicon. 

The primary persona, **Barnaby**, is an intentionally curmudgeonly and whimsical contrarian. He is designed to stress-test an LLM's ability to maintain a difficult, non-compliant "Skeptic" persona while remaining conversationally coherent across multi-turn interactions.

---

## 🏗️ Architectural Overview

This framework is optimized for high-performance local inference on Apple Silicon:

* **Inference Engine:** [MLX-LM](https://github.com/ml-explore/mlx-examples) utilizing Apple Silicon Unified Memory.
* **Base Model:** Llama-3.2-3B-Instruct (4-bit quantization).
* **Persona Layer:** A Rank 32 LoRA adapter fine-tuned for a specific "Absurdist Contrarian" voice.
* **Service Layer:** Asynchronous **FastAPI** wrapper with a sliding-window conversation buffer.
* **Deployment Path:** Zero-config asset provisioning via **GitHub Releases**.


---

## 🚀 Quick Start

The system is architected to be "clonable and runnable." It automatically handles model weight provisioning on the first launch.

### 1. Prerequisites
* A Mac with Apple Silicon (M1/M2/M3/M4).
* Python 3.10+ and a virtual environment (`.venv`).

### 2. Setup & Execution
```bash
# Clone the repository
git clone [https://github.com/dmg-xx/contrarian-lora-lab.git](https://github.com/dmg-xx/contrarian-lora-lab.git)
cd contrarian-lora-lab

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API
python api.py