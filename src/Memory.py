# from typing import Optional, List
# from langchain.memory import ConversationTokenBufferMemory
# from langchain_community.chat_message_histories import RedisChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from src.Prompt import PromptClass
# from dotenv import load_dotenv

# load_dotenv()

# class MemoryClass:
#     def __init__(self, memory_key: str = "chat_history", model: str = "gpt-4o-mini") -> None:
#         """初始化记忆管理类

#         Args:
#             memory_key: 记忆键名
#             model: 使用的模型名称
#         """
#         self.memory_key = memory_key
#         self.memory: List = []
#         self.chat_model = ChatOpenAI(model=model)
#         self.prompt_manager = PromptClass()

#     def summary_chain(self, store_message: str) -> str:
#         """对对话历史进行总结

#         Args:
#             store_message: 需要总结的对话历史

#         Returns:
#             总结后的内容
#         """
#         system_prompt = self.prompt_manager.SystemPrompt
#         moods = self.prompt_manager.MOODS
        
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", f"{system_prompt}\n这是一段你和用户的对话记忆，对其进行总结摘要，摘要使用第一人称'我'，"
#                       "并且提取其中的用户关键信息，如用户姓名、生日、爱好等，以如下格式返回：\n"
#                       "总结摘要|用户关键信息\n"
#                       "例如 用户张三问候我好，我礼貌回复，然后他问我今年运势如何，我回答了他今年的运势，"
#                       "然后他告辞离开。|张三,生日1990年1月1日"),
#             ("user", "{input}")
#         ])
#         chain = prompt | self.chat_model
#         return chain.invoke({
#             "input": store_message,
#             "who_you_are": moods["default"]["roloSet"]
#         })

#     def get_memory(self) -> Optional[RedisChatMessageHistory]:
#         """获取Redis中存储的对话历史

#         Returns:
#             RedisChatMessageHistory对象或None（如果发生错误）
#         """
#         try:
#             chat_history = RedisChatMessageHistory(
#                 url="redis://localhost:6379/0",
#                 session_id="session1"
#             )
            
#             store_message = chat_history.messages
#             if len(store_message) > 10:
#                 message_text = "\n".join(
#                     f"{type(message).__name__}: {message.content}"
#                     for message in store_message
#                 )
                
#                 summary = self.summary_chain(message_text)
#                 chat_history.clear()
#                 chat_history.add_message(summary)
#                 print("添加总结后:", chat_history.messages)
#             else:
#                 print("go to next step")
                
#             return chat_history
            
#         except Exception as e:
#             print(f"获取记忆时发生错误: {e}")
#             return None

#     def set_memory(self) -> ConversationTokenBufferMemory:
#         """设置对话记忆

#         Returns:
#             配置好的ConversationTokenBufferMemory对象
#         """
#         self.memory = ConversationTokenBufferMemory(
#             llm=self.chat_model,
#             human_prefix="user",
#             ai_prefix="陈大师",
#             memory_key=self.memory_key,
#             output_key="output",
#             return_messages=True,
#             max_token_limit=1000,
#             chat_memory=self.get_memory(),
#         )
#         return self.memory

    