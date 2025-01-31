'''
Author: fzb fzb0316@163.com
Date: 2024-09-15 21:12:31
LastEditors: fzb0316 fzb0316@163.com
LastEditTime: 2024-11-20 20:04:44
FilePath: /RAGWebUi_demo/chat/chat_unionrag.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''



# from icecream import ic
from typing import List, Optional
from overrides import override
from database.vector.vector_database import VectorDatabase
from llmragenv.Cons_Retri.Vector_Retriever import RetrieverVector
from database.graph.graph_database import GraphDatabase
from llmragenv.Cons_Retri.KG_Retriever import RetrieverGraph


from chat.chat_base import ChatBase
from llmragenv.LLM.llm_base import LLMBase




Hybrid_prompt = (

    "You are an expert Q&A system that is trusted around the world. "
    "Always answer the query using the provided context information, and not prior knowledge. "
    "Some rules to follow:\n"
    "1. Never directly reference the given context in your answer.\n"
    "2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.\n"
    "Context information is below.\n"
    "---------------------\n"
    "{nodes_text}"

    "{context}"
    "---------------------\n"
    "Given the context information and not prior knowledge, answer the query. Note that only answer questions without explanation.\n"
    "Query: {message}\n"
    "Answer:"
)

class ChatUnionRAG(ChatBase):

    def __init__(self, llm: LLMBase, vector_db: VectorDatabase, graph_db: GraphDatabase):
        super().__init__(llm)
        self.vector_db = vector_db
        self.retriver_vector = RetrieverVector(llm,vector_db)
        self.graph_database = graph_db
        self.retriver_graph = RetrieverGraph(llm,graph_db)

    def retrieve_triplets(self, message, space_name):
        """
        Args:
            message (str): the query from users
            space_name (str): the graph name of graph database

        Returns:
            list[dict["source", "relationship", "destination"]]: retrieve triplets
        """
        self.triplets = self.retriver_graph.retrieve_2hop(question=message)
        return self.triplets
    
    def get_triplets(self):
        if self.triplets:
            return self.triplets
        else:
            return ["还未检索!"]
    

    def Vector_retrieval_result(self):
        return self.retrieve_result

    def Graph_retrieval_result(self):
        return self.triplets
    @override
    def web_chat(self, message: str, history: List[Optional[List]] | None):

        self.retrieve_result = self.retriver_vector.retrieve(question=message)
        node_result = self.retriver_vector.format_chunks(self.retrieve_result)
        print("retrieve result:",node_result)

        self.triplets = self.retriver_graph.retrieve_2hop(question=message, pruning = 30)

        prompt = Hybrid_prompt(message = message, nodes_text = node_result, context = self.triplets)
        
        # ic(message)
        # ic(history)

        # answers = self._llm.chat_with_ai_stream(message, history)
        # result = ""
        # for chunk in answers:
        #     result =  result + chunk.choices[0].delta.content or ""
        #     yield result
        answers = self._llm.chat_with_ai(prompt, history)
        return answers
        
        # ic(result)
