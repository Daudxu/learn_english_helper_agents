# fastapi
from fastapi import FastAPI,BackgroundTasks,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
# llm
from src.Agents import AgentClass
from openai import RateLimitError, models
# other
import os, uvicorn, asyncio, uuid
from dotenv import load_dotenv
from pydantic import SecretStr


app = FastAPI()
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，您可以根据需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从 .env 文件中加载环境变量
load_dotenv()

# 从环境变量中获取值
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
serp_api_key = os.getenv("SERP_API_KEY")
model_name = os.getenv("MODEL_NAME")

chatmodel = ChatOpenAI(
    base_url=base_url,
    api_key=SecretStr(openai_api_key) if openai_api_key else None,
    model=model_name if model_name else "doubao-1-5-pro-32k-250115",
    model_kwargs={
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    streaming=True
)

@app.get("/")
async def root(): 
    return {"message": "Hello World!"}


@app.post("/chat")
def SyncChat(query: str,background_tasks: BackgroundTasks):
    agent = AgentClass(chatmodel=chatmodel, modelname="doubao-1-5-lite-32k-250115" )
    msg = agent.run_agent(query)
    return {"msg": msg}

# 心跳检测
async def send_heartbeat(websocket: WebSocket):
    while True: 
        try:
            await websocket.send_text("Ping")
            await asyncio.sleep(2)  # 心跳间隔
        except Exception as e:
            print("心跳发送失败", e)
            break  # 连接断开

@app.post("/add_urls") 
# async def add_urls(urls: str):
    # add_doc = AddDocClass()
    # await add_doc.add_urls(urls)

@app.post("/add_pdfs")
  
# def add_pdfs(files: str):
    # pass
@app.post("/add_txts")
# def add_txts(files: str):
    # pass
@app.post("/add_youtubes")
# def add_youtubes(files: str):
    # pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 接受客户端的 WebSocket 连接
    await websocket.accept()
    try:
        while True:
            # 接收客户端发送的消息
            data = await websocket.receive_text()
            # 向客户端发送响应消息
            # await websocket.send_text(f"你发送的消息是: {data}")
            await websocket.send_json({"response": data})
    except Exception as e:
        print(f"发生错误: {e}")
    finally: 
        # 关闭 WebSocket 连接
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="localhost", port=8000)
    # uvicorn Main:app --reload --host 0.0.0.0 --port 8000