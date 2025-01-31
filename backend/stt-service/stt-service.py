from fastapi import FastAPI, UploadFile, File
import whisper
import os
import torchaudio
import numpy as np
import torch
import io
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the model type from the environment variable
model_type = os.getenv("MODEL_TYPE", "base")
model = whisper.load_model(model_type)

@app.post("/upload/")
async def transcribe_audio(file: UploadFile = File(...)):
    audio = await file.read()
    result = model.transcribe(audio)
    return {"transcription": result["text"]}

@app.post("/transcribe/")
async def upload_audio(file: UploadFile = File(...)):
    # 讀取音訊檔案內容
    audio_bytes = await file.read()

    # 轉成 Tensor 格式
    audio_tensor, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
    
    # 確保音訊是 numpy 格式
    audio_numpy = audio_tensor.numpy().flatten()
    result = model.transcribe(audio_numpy)
    print(f"stt-service transcription", result)
    return {"transcription": result["text"]}