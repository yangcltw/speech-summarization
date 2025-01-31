from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# 初始化 FastAPI
app = FastAPI()
# 載入 summarization pipeline（使用小型語言模型）
summarizer = pipeline("summarization", model="google/pegasus-xsum")

# 定義 API 請求格式
class SummarizationRequest(BaseModel):
    text: str

# 定義 API 端點
@app.post("/summarize/")
async def summarize(request: SummarizationRequest):
    text = request.text.strip()
    # 確保輸入不為空
    print(f"/summarize/",text)
     # 輸入驗證
    
    if not text:
        raise HTTPException(status_code=400, detail="❌ 輸入文本不能為空！")
    if len(text.split()) < 10:  # 如果字數太少，直接返回原文
        return {"summary": text}

    try:
        summary = summarizer(text, max_length=50, min_length=10, do_sample=False)
        return {"summary": summary[0]["summary_text"]}
    except PipelineException as e:
        raise HTTPException(status_code=500, detail=f"❌ Summarization 失敗: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 未知錯誤: {str(e)}")

# from fastapi import FastAPI
# from transformers import pipeline

# from fastapi.middleware.cors import CORSMiddleware


# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 或指定 ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# summarizer = pipeline("summarization")

# @app.post("/summarize/")
# async def summarize_text(text: str):
#     print(f"/summarize/",str)
#     summary = summarizer(text, max_length=150, min_length=5, do_sample=False)
#     return {"summary": summary[0]['summary_text']}
