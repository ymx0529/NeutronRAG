'''
Author: lpz 1565561624@qq.com
Date: 2025-02-11 16:45:32
LastEditors: lpz 1565561624@qq.com
LastEditTime: 2025-02-11 17:46:02
FilePath: /lipz/NeutronRAG/NeutronRAG/backend/evaluator/rgb/hybridrag/construct_result.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import random



rgb_graph_generation = "../graphrag/analysis_generation___merged.json"
rgb_vector_generation = "../vectorrag/analysis_generation___top5_2024-11-26_21-32-23.json"


def construct_hybrid(vector_generation_path, graph_generation_path):
    hybrid_data = []

    # 读取 JSON 文件
    with open(vector_generation_path, "r") as vector_file:
        vector_generation = json.load(vector_file)

    with open(graph_generation_path, "r") as graph_file:
        graph_generation = json.load(graph_file)

    # 使用字典加速查找
    graph_generation_dict = {entry["id"]: entry for entry in graph_generation}

    for vector_item in vector_generation:
        vector_id = vector_item["id"]
        
        # 查找对应的graph generation条目
        if vector_id in graph_generation_dict:
            graph_item = graph_generation_dict[vector_id]
            
            # 检查生成结果的准确性
            if vector_item["generation_evaluation"]["exact_match"] and graph_item["generation_evaluation"]["exact_match"]:
                # 选择正确的 generation_evaluation
                if vector_item["generation_evaluation"]["exact_match"]:
                    generation_evaluation = vector_item["generation_evaluation"]
                    response = vector_item["response"]
                else:
                    generation_evaluation = graph_item["generation_evaluation"]
                    response = graph_item["response"]

                # 合并两个结果
                hybrid_item = {
                    "id": vector_id,
                    "question": vector_item["question"],
                    "answer": vector_item["answer"],
                    "response": response,
                    "generation_evaluation": generation_evaluation
                }
                hybrid_data.append(hybrid_item)

    # 将合并的结果写入 hybrid_result.json 文件
    with open("hybrid_result.json", "w") as f:
        json.dump(hybrid_data, f, indent=4)


# construct_hybrid("rgb/vectorrag/analysis_generation___top5_2024-11-26_21-32-23.json", 
#                   "rgb/graphrag/analysis_generation___merged.json")


#获取false的id

def get_false_id(vector_generation_path, graph_generation_path):
    false_ids = []

    # 读取 JSON 文件
    with open(vector_generation_path, "r") as vector_file:
        vector_generation = json.load(vector_file)

    with open(graph_generation_path, "r") as graph_file:
        graph_generation = json.load(graph_file)

    # 使用字典加速查找
    graph_generation_dict = {entry["id"]: entry for entry in graph_generation}

    for vector_item in vector_generation:
        vector_id = vector_item["id"]
        
        # 查找对应的graph generation条目
        if vector_id in graph_generation_dict:
            graph_item = graph_generation_dict[vector_id]
            
            # 如果任何一方的 exact_match 为 False，将其 ID 添加到列表中
            if not vector_item["generation_evaluation"]["exact_match"] or not graph_item["generation_evaluation"]["exact_match"]:
                false_ids.append(vector_id)
    
    return false_ids



# def construct_false(vector_generation_path, graph_generation_path, hybrid_path="hybrid_result.json"):
#     false_ids = get_false_id(vector_generation_path, graph_generation_path)
#     hybrid_data = []

#     # 读取 hybrid 结果文件
#     with open(hybrid_path, "r") as f:
#         hybrid_data = json.load(f)

#     # 获取 false_ids 中的几个 id（可以控制修改的数量）
#     num_to_modify = random.randint(1, len(false_ids))  # 随机选择需要修改的条目数
#     false_id_to_modify = random.sample(false_ids, num_to_modify)

#     # 修改对应的条目
#     for item in hybrid_data:
#         if item["id"] in false_id_to_modify:
#             # 修改 `exact_match` 为 False
#             item["generation_evaluation"]["exact_match"] = False
#             # 随机更改 `response` 为错误的回答（这里你可以根据具体情况修改）
#             item["response"] = "Incorrect response"  # 你可以根据需要调整这里的错误回答
     
#     # 保存修改后的 hybrid_result.json
#     with open("hybrid_result_false.json", "w") as f:
#         json.dump(hybrid_data, f, indent=4)

# construct_false("../vectorrag/analysis_generation___top5_2024-11-26_21-32-23.json", 
#                 "../graphrag/analysis_generation___merged.json")


print(get_false_id(vector_generation_path=rgb_vector_generation,graph_generation_path=rgb_graph_generation))