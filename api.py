import os
import requests
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

app = FastAPI()

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration & Provisioning ---
# Update these with your actual GitHub details
GITHUB_USER = "dmg-xx"
REPO_NAME = "contrarian-lora-lab"
RELEASE_TAG = "v4.1.0-stable"

MODEL_PATH = "mlx-community/Llama-3.2-3B-Instruct-4bit"
ADAPTER_PATH = Path("adapters/skeptic_lora")

def ensure_assets_provisioned():
    """
    Architectural Decision: Automated Asset Provisioning
    Ensures LoRA weights are pulled from GitHub Releases if not present locally.
    """
    if not ADAPTER_PATH.exists():
        ADAPTER_PATH.mkdir(parents=True, exist_ok=True)
    
    files = ["adapters.safetensors", "adapter_config.json"]
    base_url = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/releases/download/{RELEASE_TAG}"
    
    for file in files:
        target_file = ADAPTER_PATH / file
        if not target_file.exists():
            print(f"📡 Artifact missing: {file}. Provisioning from GitHub Release {RELEASE_TAG}...")
            try:
                response = requests.get(f"{base_url}/{file}", stream=True)
                response.raise_for_status()
                with open(target_file, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Successfully provisioned {file}")
            except Exception as e:
                print(f"❌ Critical Error: Could not download {file}. Error: {e}")
                print("Please ensure your GITHUB_USER and REPO_NAME are correct in api.py.")

# Ensure weights exist before model loading
ensure_assets_provisioned()

# --- Model Initialization ---
print("🧠 Loading Contrarian Persona Engine (MLX-LM)...")
model, tokenizer = load(MODEL_PATH, adapter_path=str(ADAPTER_PATH))

# Global state management
chat_history = []

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: ChatInput):
    global chat_history
    
    # 1. Update State
    chat_history.append({"role": "user", "content": data.message})
    
    # 2. Build Multi-Turn Contextual Prompt
    # System prompt reflects the 'Contrarian' archetype without ageist language
    system_nudge = (
        "You are Barnaby, a whimsical and deeply skeptical contrarian. "
        "You answer questions with absurdist logic, internal monologues, "
        "and a general suspicion of modern consensus."
        "Do not use technical, programming, or computer science terminology in your analogies."
    )
    
    full_prompt = f"<|system|>\n{system_nudge}\n"
    for turn in chat_history:
        full_prompt += f"<|{turn['role']}|>\n{turn['content']}\n"
    full_prompt += "<|assistant|>\n"

    # 3. Inference with High Entropy (Temperature 1.1)
    # Balanced for whimsical/surrealist outputs
    sampler = make_sampler(temp=1.1)
    response = generate(
        model, 
        tokenizer, 
        prompt=full_prompt, 
        sampler=sampler, 
        max_tokens=200, # Increased slightly for anecdotal rambling
        verbose=False
    )
    
    clean_response = response.strip()
    
    # 4. Finalize State
    chat_history.append({"role": "assistant", "content": clean_response})
    
    # Sliding window to prevent context overflow (Last 10 turns)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return {"reply": clean_response}

@app.post("/reset")
async def reset():
    global chat_history
    chat_history = []
    print("🧹 Context buffer cleared.")
    return {"status": "success", "message": "Barnaby's memory has been reset."}

if __name__ == "__main__":
    import uvicorn
    # Log the successful deployment
    print("\n🚀 Contrarian Lab API is active at http://localhost:8000")
    print("✨ Ready for eccentric interactions.\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)