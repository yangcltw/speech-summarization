import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或指定 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/process/")
async def process_audio(file: UploadFile = File(...)):
    print("api-gateway process_audio")
    # 轉發請求到 STT Service
    files = {"file": (file.filename, file.file, file.content_type)}
    stt_response = requests.post("http://stt-service:8000/transcribe/", files=files)

    # 檢查回應是否成功
    if stt_response.status_code != 200:
        return {"error": "STT service error", "details": stt_response.text}
    
    transcription = stt_response.json()["transcription"]
    print(f"api-gateway transcription json",transcription)
    summarize_response = requests.post("http://summarization-service:8001/summarize/", json={"text": transcription})
    
    if summarize_response.status_code != 200:
        return {"error": "Summarize service error", "details": summarize_response.text}
    summary = summarize_response.json()["summary"]
    
    return {"transcription": transcription, "summary": summary}
