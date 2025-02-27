'''
Author: lpz 1565561624@qq.com
Date: 2025-02-18 15:29:13
LastEditors: lpz 1565561624@qq.com
LastEditTime: 2025-02-21 15:02:02
FilePath: /lipz/NeutronRAG/NeutronRAG/backend/evaluator/test_para.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
from llmragenv.LLM.ollama.client import OllamaClient
from tqdm import tqdm



###目前的两个方案 1.修改提示词  2.重新生成response


SUMMARIZE_PROMPT = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Below I will give you an entity and a series of triples about this entity. Please form a summary description of this entity based on the information of these triples.
Please only output the summary, do not output anything irrelevant to the summary
###Example
Entity:The overall winner of the 2022 tour de france
Triples:[('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Is the second rider from', 'Denmark to win the tour de france'), (' Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france '), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Won the tour by', '3:34 over tadej pogačar'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Won', 'Stage 11'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Outlasted', 'Tadej pogačar'), 
('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Finished safely behind', 'The peloton at the end of stage 21'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Lost time to', 'Tadej pogačar'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Won', 'The yellow jersey'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Took', 'The yellow jersey'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Attacked', 'On the steep slopes of the col du granon'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Rode', 'An almost perfect race'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Was biding his time for', 'The alps'), ('Jonas vingegaard', 'Is', 'The overall winner of the 2022 tour de france'), ('Jonas vingegaard', 'Is', '25 year old from a fishing town in northern denmark')]

Response: Jonas Vingegaard was the overall winner of the 2022 Tour de France. He became the second rider from Denmark to win the prestigious race, securing victory with a 3-minute and 34-second lead over Tadej Pogačar. 
Vingegaard delivered a dominant performance, notably winning Stage 11 and taking the yellow jersey after a decisive attack on the steep slopes of Col du Granon. He strategically bided his time for the Alps, outlasting his main rival, Pogačar, and maintaining his lead through the final stages. Vingegaard ultimately finished safely behind the peloton at the end of Stage 21, sealing his victory. At just 25 years old, he rode an almost perfect race and cemented his place in cycling history as Denmark's latest Tour de France champion.

###Real Data
Entity: {entity}
Triples: {triples}
Response:
"""


def find_right_arrow(s):
    """
    查找字符串中所有 "->" 的起始位置
    """
    right_arrow_positions = []
    i = 0
    while i < len(s) - 1:  # 确保不会越界
        if s[i:i+2] == "->":
            right_arrow_positions.append(i)
            i += 2  # 跳过这两个字符，避免重复查找
        else:
            i += 1
    return right_arrow_positions


def find_left_arrow(s):
    """
    查找字符串中所有 "<-" 的起始位置
    """
    left_arrow_positions = []
    i = 0
    while i < len(s) - 1:  # 确保不会越界
        if s[i:i+2] == "<-":
            left_arrow_positions.append(i)
            i += 2  # 跳过这两个字符，避免重复查找
        else:
            i += 1

    return left_arrow_positions



# arrows_index : 所有箭头的索引从小到大排序

#获取所有的-的位置，但它不一定是关系的分隔符
def get_all_dash(s):
    dash_positions = []
    i = 0
    while i < len(s):
        if s[i] == "-":
            # 检查当前位置是否属于箭头的一部分
            if i > 0 and ((s[i:i+2] == "->") or (s[i-1:i+1] == "<-")):
                i += 1  # 跳过整个箭头（两个字符），避免误判 "-" 为单独的 "-"
                continue
            dash_positions.append(i)
        i += 1
    return dash_positions



def find_dash_positions(s,all_dash):
    dash_positions = []
    

    for i in all_dash:
        if s[i-1] == " "  or s[i+1] == " ":
            dash_positions.append(i)
        

    return dash_positions




# 示例使用
# sample_string = "The overall winner of the 2022 tour de france <-Is- Jonas vingegaard -Is-> 25-year-old from a fishing town in northern denmark"

# right_arrows = find_right_arrow(sample_string)
# left_arrows = find_left_arrow(sample_string)
# all_dash = get_all_dash(sample_string)
# dash_positions = find_dash_positions(sample_string,all_dash)

# print("Right arrow positions:", right_arrows)
# print("Left arrow positions:", left_arrows)
# print("Dash positions:", dash_positions)

def split_relation(rel_seq):
    parts = []
    all_dash = get_all_dash(rel_seq)
    right_arrows = find_right_arrow(rel_seq)
    left_arrows = find_left_arrow(rel_seq)
    dash_positions = find_dash_positions(rel_seq,all_dash)

    arrows_index = sorted(right_arrows+left_arrows)

    if len(arrows_index) == 1:
        if arrows_index[0] in right_arrows:
            source = rel_seq[:dash_positions[0]]
            rel = rel_seq[dash_positions[0]+1:arrows_index[0]]
            dst = rel_seq[arrows_index[0]+2:]
            parts.append((source,rel,dst))
        else:
            dst = rel_seq[:arrows_index[0]]
            rel = rel_seq[arrows_index[0]+2:dash_positions[0]]
            source = rel_seq[dash_positions[0]+1:]
            parts.append((source,rel,dst))

        return parts

    ###多跳的分解###
    i = 0
    for arrows in arrows_index:
        if  arrows in right_arrows:
            if i == 0:
                source = rel_seq[:dash_positions[0]].strip()
                rel = rel_seq[dash_positions[0]+1:arrows_index[0]].strip()
                dst = rel_seq[arrows_index[0]+2:min(dash_positions[1],arrows_index[1])].strip()
                parts.append((source,rel,dst))
                i+=1
            elif i == len(arrows_index)-1:
                dst = rel_seq[arrows_index[-1]+2:].strip()
                rel = rel_seq[dash_positions[-1]+1:arrows_index[-1]].strip()
                source = rel_seq[max(dash_positions[i-1]+1,arrows_index[i-1]+2):dash_positions[-1]].strip()
                parts.append((source,rel,dst))
                i+=1

            else:#既不是第一个也不是最后一个
                source = rel_seq[max(dash_positions[i-1]+1,arrows_index[i-1]+2):dash_positions[i]].strip()
                rel = rel_seq[dash_positions[i]+1:arrows_index[i]].strip()
                dst = rel_seq[arrows_index[i]+2:min(dash_positions[i+1],arrows_index[i+1])].strip()
                parts.append((source,rel,dst))
                i+=1


        if arrows in left_arrows:
            if i == 0:
                dst = rel_seq[:arrows_index[i]].strip()
                rel = rel_seq[arrows_index[i]+2:dash_positions[i]].strip()
                source = rel_seq[dash_positions[i]+1:min(dash_positions[i+1],arrows_index[i+1])].strip()
                parts.append((source,rel,dst))
                i+=1
            elif i == len(arrows_index)-1:
                source = rel_seq[dash_positions[i]+1:].strip()
                rel = rel_seq[arrows_index[i]+2:dash_positions[i]].strip()
                dst = rel_seq[max(arrows_index[i-1]+2,dash_positions[i-1]+1):arrows_index[i]].strip()
                parts.append((source,rel,dst))
                i+=1
                
            else:
                source = rel_seq[dash_positions[i]:min(dash_positions[i+1],arrows_index[i+1])].strip()
                rel = rel_seq[arrows_index[i]+2:dash_positions[i]].strip()
                dst = rel_seq[max(dash_positions[i-1]+1,arrows_index[i-1]+2):arrows_index[i]].strip()
                parts.append((source,rel,dst))
                i+=1


    return parts




def convert_to_triples(result_path):
    """
    将 result_path 指定的文件中的 JSON 数据转换为三元组形式，支持多种边的关系。
    返回的结构是 {key: [(subject, relationship, object), ...]}。
    """
    with open(result_path, 'r') as file:
        data = json.load(file)  # 加载 JSON 数据
    
    # 用字典来存储每个 key 对应的三元组列表
    triples_dict = {}

    for item in data:
        retrieve_results = item['retrieve_results']
        
        for key, value_list in retrieve_results.items():
            # 初始化 key 的三元组列表（如果不存在）
            if key not in triples_dict:
                triples_dict[key] = []

            for value in value_list:
                # 使用 split_relation 解析关系
                parsed_triples = split_relation(value)
                
                # 将解析出的三元组添加到相应的 key 对应的列表中
                for t in parsed_triples:
                    triples_dict[key].append(t)

    return triples_dict




def replace_result(model, input_path="merged.json", output_path="replace.json"):
    with open(input_path, 'r') as file:
        input_data = json.load(file)

    # 使用 tqdm 显示处理进度，遍历 input_data 中的每个 item
    for item in tqdm(input_data, desc="Processing items", unit="item"):
        retrieve_results = item['retrieve_results']

        # 对每个 retrieve_results 中的 key 和 value_list 进行处理
        for key, value_list in retrieve_results.items():
            triples = []
            for value in value_list:
                parsed_triples = split_relation(value)
                for t in parsed_triples:
                    triples.append(t)
            
            prompt = SUMMARIZE_PROMPT.format(entity=key, triples=triples)
            response = model.chat_with_ai(prompt=prompt, history=None)

            # 用 response 替换原始的检索结果
            retrieve_results[key] = response

    # 将修改后的数据写回到 output_path 文件
    with open(output_path, 'w') as outfile:
        json.dump(input_data, outfile, indent=4)

    print(f"Data has been updated and saved to {output_path}")


    

 
def replace_list(replace_path = "replace.json"):
    with open(replace_path, 'r') as file:
        data = json.load(file)
    for item in data:
        retrieve_results = item['retrieve_results']

        for key,value in retrieve_results.items():
            retrieve_results[key] = [value]

    with open(replace_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)



def remove_evidences_triplets(replace_path="replace.json"):
    # 打开并读取 JSON 文件
    with open(replace_path, "r") as file:
        data = json.load(file)
    
    # 遍历每个元素，并删除 evidences_triplets 属性
    for item in data:
        if 'evidences_triplets' in item:
            del item['evidences_triplets']
    
    # 将修改后的数据保存回 JSON 文件
    with open(replace_path, "w") as file:
        json.dump(data, file, indent=4)


DEFAULT_TEXT_QA_PROMPT_TMPL = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)

def replace_response(model: OllamaClient, file_path="/home/lipz/NeutronRAG/NeutronRAG/backend/evaluator/replace_response.json"):
    # 打开并读取文件
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 使用 tqdm 进度条包装 data 以显示处理进度
    for item in tqdm(data, desc="Processing Responses", unit="item"):
        text_chunks = []
        retrieve_results = item.get('retrieve_results', [])
        
        # 收集文本片段
        for value in retrieve_results:
            text_chunks.append(value)
        
        # 格式化 Prompt
        prompt = DEFAULT_TEXT_QA_PROMPT_TMPL.format(context_str="\n".join(text_chunks), query_str=item["query"])
        
        # 调用模型生成 response
        response = model.chat_with_ai(prompt=prompt, history=None)
        
        # 更新 item 中的 response 字段
        item["response"] = response

    # 将更新后的数据写回文件
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Responses have been updated and written back to {file_path}")






def convert_to_triples(retrieve_results):
    """
    将 retrieve_results 中的字符串转换为三元组形式，支持多种边的关系。
    """
    triples = set()
    
    for key, value_list in retrieve_results.items():
        
        for value in value_list:
            # 使用 parse_relationship 解析关系
            parsed_triples = split_relation(value)
            
            # 将解析出的三元组加入到结果中
            for t in parsed_triples:
                triples.add(t)
                
    return list(triples)




def calculate_redundancy_triplet(file_path = "merged.json"):
    triples = set()
    re_triples = []
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        retrieve_results = item.get('retrieve_results', [])

        for key, value_list in retrieve_results.items():

            for value in value_list:
                parsed_triples = split_relation(value)

                for t in parsed_triples:
                    triples.add(t)
                    re_triples.append(t)

    triples = list(triples)
    
    re = (len(re_triples) - len(triples))/len(re_triples)

    return re
    

                

        
    


            





if __name__ == '__main__':

    # rgb_retrieval_path = "/home/lipz/NeutronRAG/NeutronRAG/backend/evaluator/rgb/graphrag/analysis_retrieval_merged.json"
    # # url: http://localhost:11434/v1
    # # key: ollama
    # model_name = "llama3.1:70b"
    # url = "http://localhost:11434/v1"
    # key = "ollama"

    # # triplets = convert_to_triples(result_path = rgb_retrieval_path)
    # # entity = "Kyle busch"
    # # triples = triplets[entity]

    # # prompt = SUMMARIZE_PROMPT.format(entity = entity,triples = triples)
    # # # print(prompt)
    # model = OllamaClient(model_name, url, key)

    # respone = model.chat_with_ai(prompt=prompt,history=None)
    # # print(respone)
    # replace_result(model=model)
    # replace_list()
    # remove_evidences_triplets()
    # replace_response(model=model)

    # replace_list(replace_path="replace_response.json")

    print("rgb：",calculate_redundancy_triplet())
