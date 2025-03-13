import os, requests
from dotenv import load_dotenv
# llm
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
# 工具
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.vectorstores import Qdrant
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from qdrant_client import QdrantClient
from pydantic import SecretStr
from langchain_qdrant import QdrantVectorStore
from langchain_core.output_parsers import JsonOutputParser


# 加载.env 文件中的环境变量
load_dotenv()

# 从环境变量中获取值
openai_api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("BASE_URL")
serp_api_key = os.getenv("SERP_API_KEY")  
yfj_api_key = os.getenv("YFJ_API_KEY")  

@tool
def test():
    """"test tool"""
    return "test"  

@tool
def search(query: str):
    """"需要搜索的时候搜索"""
    try:
        print("query==================: ", query)
        serpapi = SerpAPIWrapper(serpapi_api_key=serp_api_key)
        return serpapi.run(query)
    except Exception as e:
        print(f"搜索出错: {str(e)}")
        return "搜索过程中发生错误，请稍后重试"