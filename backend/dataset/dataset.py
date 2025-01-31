'''
Author: fzb0316 fzb0316@163.com
Date: 2024-10-18 14:57:50
LastEditors: fzb0316 fzb0316@163.com
LastEditTime: 2024-11-04 16:04:32
FilePath: /BigModel/RAGWebUi_demo/dataset/dataset.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
from pathlib import Path
import json
from utils.file_util import file_exist


RGB_PATH = os.path.join(Path(__file__).parent, "rgb", "en.json")
# RGB_PATH = os.path.join(Path(__file__).parent, "rgb", "en_refine.json")
MULTIHOP_PATH = os.path.join(Path(__file__).parent, "multihop", "dataset", "MultiHopRAG.json")



class Dataset:
    def __init__(self, name : str):
        self.dataset_name = name
        self.query = []
        self.answer = []
        self.corpus = []
        self.get_data()


    def get_data(self):
        if self.dataset_name == 'rgb':
            rgb_data_path = RGB_PATH
            assert file_exist(rgb_data_path), f"File {rgb_data_path} does not exist"
            with open(rgb_data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # print(json.loads(line).keys())
                    self.query.append(json.loads(line)['query'])
                    answer = json.loads(line)['answer']
                    if len(answer) == 1 and isinstance(answer[0], list):
                        self.answer.append(answer[0])
                    else:
                        self.answer.append(answer)
                    # self.answer.append(json.loads(line)['answer'])
        
        elif self.dataset_name == 'multihop':
            multihop_data_path = MULTIHOP_PATH
            # multihop_data_path = os.path.join(Path(__file__).parent, "multihop", "dataset", "process.json")
            assert file_exist(multihop_data_path), f"File {multihop_data_path} does not exist"
            with open(multihop_data_path, 'r', encoding='utf-8') as f:
                # for line in f:
                #     self.query.append(json.loads(line)['query'])
                #     self.answer.append(json.loads(line)['answer'])
                data = json.load(f)
            for item in data:
                self.query.append(item['query'])
                self.answer.append(item['answer'])
        
        else:
            raise ValueError("Invalid dataset name")

    def get_corpus(self, option : str = "positive"):
        if self.dataset_name == 'rgb':
            rgb_data_path = RGB_PATH
            assert file_exist(rgb_data_path), f"File {rgb_data_path} does not exist"
            with open(rgb_data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # print(json.loads(line).keys())
                    if option == "positive":
                        self.corpus.append(json.loads(line)['positive'])
                    elif option == "negative":
                        self.corpus.append(json.loads(line)['negative'])
                    elif option == "full":
                        self.corpus.append(json.loads(line)['positive'])
                        self.corpus.append(json.loads(line)['negative'])
                    else:
                        raise ValueError("Invalid option")