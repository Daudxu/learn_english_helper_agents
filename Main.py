from fastapi import FastAPI,BackgroundTasks,WebSocket,WebSocketDisconnect

app = FastAPI()
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，您可以根据需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}

    

@app.post("/chat")
def SyncChat(query: str,background_tasks: BackgroundTasks):
    agent = AgentClass()
    msg = agent.run_agent(query)
    unique_id = str(uuid.uuid4()) 
    #voice
    voice = Voice(uid=unique_id)
    background_tasks.add_task(voice.get_voice,msg["output"])
    return {"msg": msg, "id": unique_id}

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
async def add_urls(urls: str):
    add_doc = AddDocClass()
    await add_doc.add_urls(urls)

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
    # uvicorn app:app --reload --host 0.0.0.0 --port 8000