from langchain.agents import AgentExecutor,create_tool_calling_agent,tool
from langchain_openai import ChatOpenAI
from .Prompt import PromptClass
# from .Memory import MemoryClass
from .Emotion import EmotionClass
from .Tools import *
from dotenv import load_dotenv

import os

# 从 .env 文件中加载环境变量
load_dotenv()

# 从环境变量中获取值
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
serp_api_key = os.getenv("SERP_API_KEY")
# model_name = os.getenv("MODEL_NAME") if os.getenv("MODEL_NAME") else "doubao-1-5-lite-32k-250115"

# chatmodel = ChatOpenAI(
#     base_url=base_url,
#     api_key=SecretStr(openai_api_key) if openai_api_key else None,
#     model=model_name if model_name else "gpt-3.5-turbo",
#     model_kwargs={
#         "temperature": 0.7,
#         "max_tokens": 1000,
#     },
#     streaming=True
# )

class AgentClass:
    def __init__(self, chatmodel=ChatOpenAI(
        model_kwargs={
            "temperature": 0.7,
            "max_tokens": 1000,
        }
    ), modelname=None):
        self.modelname = modelname
        self.chatmodel = chatmodel
        self.tools = [search]
        self.memorykey = "chat_history"
        self.feeling = "default"
        self.prompt = PromptClass(memorykey=self.memorykey,feeling=self.feeling).Prompt_Structure()
        self.memory = ""
        # 直接使用传入的 chatmodel 实例
        self.emotion = EmotionClass(model=self.chatmodel)
        self.agent = create_tool_calling_agent(
            llm=self.chatmodel,
            tools=self.tools,
            prompt=self.prompt,
        )
        self.agent_chain = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=None,
            verbose=True
        )
    

    def run_agent(self,input):
        # run emotion sensing
        self.feeling = self.emotion.Emotion_Sensing(input)
        # 确保feeling不为None，如果为None则使用默认值
        self.prompt = PromptClass(memorykey=self.memorykey, feeling=self.feeling if self.feeling else "default").Prompt_Structure()
        # print(self.feeling)
        # print(self.prompt)
        res = self.agent_chain.invoke({ 
            "input": input,
            "chat_history": "chat_history",  # 添加 chat_history 变量
            "agent_scratchpad": []  # 根据需要初始化 agent_scratchpad
        })
        return res
    
    # async def run_agent_ws(self,input):
    #     # run emotion sensing
    #     self.feeling = self.emotion.Emotion_Sensing(input)
    #     self.prompt = PromptClass(memorykey=self.memorykey,feeling=self.feeling).Prompt_Structure()
    #     async for event in self.agent_chain.astream_events({"input": input,"chat_history":self.memory},version="v2"):
    #         kind = event["event"]
    #         if kind == "on_chat_model_stream":
    #             content = event["data"]["chunk"].content
    #             if content:
    #                 print(content, end="|")
    #                 yield content
        
