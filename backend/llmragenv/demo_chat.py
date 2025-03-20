'''
Author: lpz 1565561624@qq.com
Date: 2025-03-19 20:28:13
LastEditors: lpz 1565561624@qq.com
LastEditTime: 2025-03-20 10:01:51
FilePath: /lipz/NeutronRAG/NeutronRAG/backend/llmragenv/demo_chat.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from typing import List, Optional

from chat.chat_base import ChatBase
from chat.chat_withoutrag import ChatWithoutRAG
from chat.chat_vectorrag import ChatVectorRAG
from chat.chat_graphrag import ChatGraphRAG
from chat.chat_unionrag import ChatUnionRAG
from database.vector.Milvus.milvus import MilvusDB
from llmragenv.LLM.llm_factory import ClientFactory
from database.graph.graph_dbfactory import GraphDBFactory
from llmragenv.Cons_Retri.KG_Construction import KGConstruction

from dataset.dataset import Dataset
from logger import Logger
import subprocess

class Demo_chat:
    def __init__(self,
                 model_name,
                 dataset,
                 top_k=5,
                 threshold=0.5,
                 chunksize=100,
                 k_hop=2,
                 keywords=None,
                 pruning=False,
                 strategy="default",
                 api_key="ollama",
                 url="http://localhost:11434/v1"):
        """
        初始化 Demo_chat 类。

        :param model_name: 使用的模型名称
        :param dataset: 语料库或数据集
        :param top_k: 选择前 k 个最佳答案
        :param threshold: 置信度阈值
        :param chunksize: 处理数据时的分块大小
        :param k_hop: k-hop 查询的步长（用于知识图谱）
        :param keywords: 关键词列表
        :param pruning: 是否进行剪枝优化
        :param strategy: 检索或生成的策略
        """
        self.model_name = model_name
        self.dataset = dataset
        self.top_k = top_k
        self.threshold = threshold
        self.chunksize = chunksize
        self.k_hop = k_hop
        self.keywords = keywords if keywords else []
        self.pruning = pruning
        self.strategy = strategy
        self.api_key = api_key
        self.url = url
        self.llm = self.load_llm(self.model_name,self.url,self.api_key)
        

    def load_llm(self, model_name, url, api_key):
        try:
            llm = ClientFactory(model_name, url, api_key).get_client()
            return llm
        except Exception as e:
            print(f"Failed to load LLM: {e}")
            return None
        

    def chat_test(self):
        response = self.llm.chat_with_ai(prompt = "How are you today",history = None)
        return response


        
#为了实现切换模型和停止生成时资源的立即释放
    def close(self):
        if self.api_key == "ollama" and self.llm is not None:
            subprocess.run(["ollama", "stop", self.model_name])
            print(f"Stopped model: {self.model_name}")
            self.llm = None
            self.model_name = None
        else:
            self.llm = None
            self.model_name = None



if __name__ == "__main__":
    chat = Demo_chat(model_name="llama3:8b",dataset="rgb")
    print(chat.chat_test())
    chat.close()





