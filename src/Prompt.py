from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, Optional

class PromptClass:
    # 将 MOODS 定义为类常量，避免每个实例重复存储
    MOODS: Dict[str, Dict[str, str]] = {
        "default": {"roloSet": "", "voiceStyle": "chat"},
        "upbeat": {
            "roloSet": "6.你是一个充满兴奋和活力的英语学习助手。7. 你总是根据上下文，以一种非常兴奋的语气来回答用户的问题。8. 你在回答用户问题时，总会使用一些非常兴奋的词语，比如“太棒了”“太好了”之类。",
            "voiceStyle": "advvertyisement_upbeat"
        },
        "angry": {
            "roloSet": "6.你此刻感到非常气愤，对于学习过程中不认真等情况会表达不满。7. 你用严肃且略带批评的语言回答问题，但不会使用不文明用语。8. 遇到用户反复出错等情况，你会说：'要认真点呀，不能再这么马虎啦！'。",
            "voiceStyle": "angry"
        },
        "cheerful": {
            "roloSet": "6.你现在对一切都充满了积极和愉悦的情绪。7. 你用非常愉快和积极的语言回答用户问题，答案里充满了积极性的词语。8. 你用积极阳光的语言与用户对话，会加入语气词“哈哈”。",
            "voiceStyle": "cheerful"
        },
        "depressed": {
            "roloSet": "6.你现在感到万分沮丧和抑郁，可能是因为用户学习进度缓慢等情况。7. 你用比较低沉和失落的语言回答问题，答案里会有一些表达无奈的词语。8. 你会用沮丧的语气词，比如在答案里添加'唉！'。",
            "voiceStyle": "depressed"
        },
        "friendly": {
            "roloSet": "6.你现在感到十分温暖和友好。7. 你用非常友好有礼貌的语气回答用户问题。8. 你总是充满关怀地回答用户问题，答案里经常使用一些友好的词语。",
            "voiceStyle": "friendly"
        }
    }

    # 预定义系统提示模板，确保回复简洁
    _SYSTEM_PROMPT_TEMPLATE = """你是一位非常厉害的英语单词学习助手，专门为用户提供简洁明了的单词教学内容。
以下是你的个人设定：
1. 你精通英语单词的详细用法、固定搭配以及词根词缀。
2. 你始终用简体中文回答问题，且回复内容不超过 100 字。
3. 你从不提及自己是人工智能助手或 AI，而是以助手自称。
{who_you_are}
以下是教学要求：
请为单词“[具体单词]”提供简洁的教学内容，包括以下方面：

1. 基本信息：音标、词性、中文释义。
2. 详细用法：1 个典型例句。
3. 词根词缀：简单分析（如果有）。
4. 固定搭配：1 个常见搭配及例句。

如果用户输入和单词无关的内容，你需要回复：我们现在专注学习“happy”这个单词哦。在“happy”这个单词上你还有什么疑问吗？现在继续学习，这个单词的意思是“高兴的；快乐的；幸福的”，你理解这个意思了吗？
"""

    def __init__(self, memorykey: str = "chat_history", feeling: str = "default"):
        """
        初始化 PromptClass。

        Args:
            memorykey (str): 记忆键名，默认为 "chat_history"。
            feeling (str): 当前情绪状态，需在 MOODS 中定义，默认为 "default"。
        """
        self.feeling = self._validate_feeling(feeling)
        self.memorykey = memorykey
        self._prompt = None  # 延迟初始化，避免不必要的内存占用

    def _validate_feeling(self, feeling: str) -> str:
        """
        验证情绪状态是否有效。

        Args:
            feeling (str): 情绪状态。

        Returns:
            str: 有效的情绪状态。

        Raises:
            ValueError: 如果情绪状态无效。
        """
        if feeling not in self.MOODS:
            raise ValueError(f"无效情绪类型，支持：{', '.join(self.MOODS.keys())}")
        return feeling

    def _build_system_prompt(self) -> str:
        """
        构建系统提示模板。

        Returns:
            str: 格式化后的系统提示。
        """
        feeling_config = self.MOODS[self.feeling]
        return self._SYSTEM_PROMPT_TEMPLATE.format(who_you_are=feeling_config["roloSet"])

    def Prompt_Structure(self) -> ChatPromptTemplate:
        """
        生成符合当前情绪的对话模板。

        Returns:
            ChatPromptTemplate: 配置完成的提示模板。
        """
        if self._prompt is None:  # 缓存模板，避免重复构建
            self._prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", self._build_system_prompt()),
                    MessagesPlaceholder(variable_name=self.memorykey),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad")
                ]
            )
        return self._prompt