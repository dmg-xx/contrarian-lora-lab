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

# --- Startup: Load Barnaby ---
MODEL_PATH = "mlx-community/Llama-3.2-3B-Instruct-4bit"
ADAPTER_PATH = "./adapters/skeptic_lora"

print("👴 Barnaby is putting on his glasses (loading model)...")
model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)

# Global memory (Shared for your local session)
chat_history = []

class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(data: ChatInput):
    global chat_history
    
    # 1. Add User message to memory
    chat_history.append({"role": "user", "content": data.message})
    
    # 2. Build the full ChatML prompt with context
    full_prompt = "<|system|>\nYou are Barnaby, a grumpy and rambling old man who answers questions with suspicious questions and anecdotes.\n"
    for turn in chat_history:
        full_prompt += f"<|{turn['role']}|>\n{turn['content']}\n"
    full_prompt += "<|assistant|>\n"

    # 3. Generate response with Sampler (Creativity control)
    sampler = make_sampler(temp=1.1)
    response = generate(
        model, 
        tokenizer, 
        prompt=full_prompt, 
        sampler=sampler, 
        max_tokens=150,
        verbose=False
    )
    
    clean_response = response.strip()
    
    # 4. Add Barnaby's response to memory
    chat_history.append({"role": "assistant", "content": clean_response})
    
    # Keep memory from getting too heavy (sliding window of 10 turns)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return {"reply": clean_response}

@app.post("/reset")
async def reset():
    global chat_history
    chat_history = []
    return {"status": "success", "message": "Barnaby forgot everything."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)