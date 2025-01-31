import json


# rgb_result_path = "/home/lipz/NeutronRAG/neutronrag/results/analysis/rgb"
# rgb_graph_generation = "/home/lipz/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/analysis_generation___merged.json"
# rgb_graph_retrieval = "/home/lipz/NeutronRAG/neutronrag/results/analysis/rgb/graphrag/analysis_retrieval___merged.json"
# rgb_vector_generation = "/home/lipz/NeutronRAG/neutronrag/results/analysis/rgb/vectorrag/analysis_generation___top5_2024-11-26_21-32-23.json"
# rgb_vector_retrieval = "/home/lipz/NeutronRAG/neutronrag/results/analysis/rgb/vectorrag/analysis_retrieval___top5_2024-11-26_21-32-23.json"
# rgb_hybrid_generation = ""


# todo完成对graph_generation的统计 两个指标 #             "exact_match": false, "hallucinations": 0.0 返回数据集中两个的平均值 exact_match定义为 hallucinations平均值定义为faithfulness exact_match定义为accuracy
#  {
#         "id": 6,
#         "question": "Where is the Super Bowl held in 2022?",
#         "answer": [
#             "SoFi Stadium"
#         ],
#         "response": "State farm stadium",
#         "generation_evaluation": {
#             "exact_match": false,
#             "hallucinations": 0.0
#         }
#     },
def statistic_graph_generation(dataset):
    faithfulness = 0.0
    accuracy = 0.0
    exact_match_sum = 0.0
    hallucinations_sum = 0.0

    try:
        with open(dataset, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")

    total_count = len(dataset)
    assert total_count > 0, "The dataset is empty"

    for data in dataset:
        exact_match_sum += data['generation_evaluation']['exact_match']
        hallucinations_sum += data['generation_evaluation']['hallucinations']

    faithfulness = hallucinations_sum / total_count 
    accuracy = exact_match_sum / total_count
    print("faithfulness:",faithfulness)
    print("accuracy:",accuracy)
    return faithfulness, accuracy



    # {
    #     "id": 90,
    #     "question": "Who is the lead actor in the film Carter?",
    #     "answer": [
    #         "Joo Won"
    #     ],
    #     "response": "",
    #     "retrieve_results": {},
    #     "retrieval_evaluation": {
    #         "relevance": 0,
    #         "recall": 0.0
    #     }
    # }

    
# todo完成对graph_retrieval的统计 两个指标  recall和relevance

def statistic_graph_retrieval(dataset):
    recall = 0.0
    relevance = 0.0
    recall_sum = 0.0
    relevance_sum = 0.0
    try:
        with open(dataset, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")

    total_count = len(dataset)
    assert total_count > 0, "The dataset is empty"

    for data in dataset:
        recall_sum += data['retrieval_evaluation']['recall']
        relevance_sum += data['retrieval_evaluation']['relevance']
        
    recall = recall_sum / total_count 
    relevance = relevance_sum / total_count
    print("recall:",recall)
    print("relevance:",relevance)
    return recall,relevance


    # {
    #     "id": 139,
    #     "question": "When does the iPhone 14 Plus release?",
    #     "answer": [
    #         [
    #             "October 7",
    #             "Oct 7",
    #             "Oct. 7",
    #             "October 7",
    #             "7 October",
    #             "7 Oct",
    #             "7 Oct.",
    #             "7 October"
    #         ]
    #     ],
    #     "response": "October 7, 2022",
    #     "generation_evaluation": {
    #         "exact_match": true,
    #         "hallucinations": 1.0
    #     }
    # },
#todo 同理

def statistic_vector_generation(dataset):
    faithfulness = 0.0
    accuracy = 0.0
    exact_match_sum = 0.0
    hallucinations_sum = 0.0

    try:
        with open(dataset, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")

    total_count = len(dataset)
    assert total_count > 0, "The dataset is empty"

    for data in dataset:
        exact_match_sum += data['generation_evaluation']['exact_match']
        hallucinations_sum += data['generation_evaluation']['hallucinations']

    faithfulness = hallucinations_sum / total_count 
    accuracy = exact_match_sum / total_count
    print("faithfulness:",faithfulness)
    print("accuracy:",accuracy)
    return faithfulness, accuracy



    # {
    #     "id": 142,
    #     "question": "Which team will Kyle Busch join in 2023?",
    #     "answer": [
    #         "Richard Childress Racing"
    #     ],
    #     "response": "Richard Childress Racing.",
    #     "evidences": "Sep 14, 2022 ... Richard Childress Racing announced Tuesday that Kyle Busch will drive for the organization in the 2023 NASCAR Cup Series.",
    #     "retrieve_results": [
    #         {
    #             "node_score": 0.8298640251159668,
    #             "node_text": "Sep 14, 2022 ... Richard Childress Racing announced Tuesday that Kyle Busch will drive for the organization in the 2023 NASCAR Cup Series."
    #         },
    #         {
    #             "node_score": 0.7981891632080078,
    #             "node_text": "Sep 10, 2022 ... Kyle Busch will not return to Joe Gibbs Racing for the 2023 NASCAR season, ending a highly successful driver‐team pairing that won 56 races."
    #         },
    #         {
    #             "node_score": 0.7743661403656006,
    #             "node_text": "Dec 30, 2022 ... 8 Chevrolet in 2023. The move is a serious blow to Toyota, which invested in Busch when he joined the OEM in 2008 as a hot-headed young gun ..."
    #         },
    #         {
    #             "node_score": 0.7641044855117798,
    #             "node_text": "Busch joins a two-car RCR team that has Austin Dillon and Tyler Reddick under contract for next season. RCR will presumably expand to three cars to accommodate Busch’s arrival, though the team could negotiate a buyout of Reddick’s contract that has one year remaining after Reddick announced earlier this year that he’s leaving to join 23XI Racing in 2024. Jordan Bianchi: How Kyle Busch’s 15-year, two-title run with Joe Gibbs Racing came to an end (Photo: Mike Dinovo / USA Today) Get all-access to exclusive stories. Subscribe to The Athletic for in-depth coverage of your favorite players, teams, leagues and clubs. Try a week on us. Jordan Bianchi  is a motorsports reporter for The Athletic. He is a veteran sports reporter, having covered the NBA, NFL, Major League Baseball, college basketball, college football, NASCAR, IndyCar and sports business for several outlets."
    #         },
    #         {
    #             "node_score": 0.7375945448875427,
    #             "node_text": "Sep 14, 2022 ... The manufacturer switch will also apply to Busch's Truck Series team Kyle Busch Motorsports, which had exclusively fielded Toyotas since their ..."
    #         }
    #     ],
    #     "retrieval_evaluation": {
    #         "precision": 1.0,
    #         "relevance": 0.2,
    #         "recall": 1.0
    #     }
    # },
    # todo统计vector的retrieval的三个指标 同理
    
def statistic_vector_retrieval(dataset):
    precision = 0.0
    relevance = 0.0
    recall = 0.0
    precision_sum = 0.0
    relevance_sum = 0.0
    recall_sum = 0.0

    try:
        with open(dataset, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")

    total_count = len(dataset)
    assert total_count > 0, "The dataset is empty"

    for data in dataset:
        precision_sum += data['retrieval_evaluation']['precision']
        relevance_sum += data['retrieval_evaluation']['relevance']
        recall_sum += data['retrieval_evaluation']['recall']

    precision = precision_sum / total_count 
    relevance = relevance_sum / total_count
    recall = recall_sum / total_count
    print("precision:",precision)
    print("relevance:",relevance)
    print("recall:",recall)
    return precision,relevance,recall


def statistic_hybrid_generation():

    return



def statistic_hybrid_retrieval():

    return


def flatten_answers(answers):
    """
    有的答案是嵌套的列表，需要展开。
    """
    flattened = []
    for answer in answers:
        if isinstance(answer, list):
            flattened.extend(flatten_answers(answer))
        else:
            flattened.append(answer)
    return flattened

# 分析一下错因 检索结果与正确答案answer进行字符匹配 1.检索到了但是回答错误 2.没检索到但是回答错误 3.没检索到但是回答正确。 返回这三种错因的id_list
def statistic_error_cause(generation_dataset, retrieval_dataset, mode):
    retrieve_error = []  # 检索到了但回答错误
    lose_error = []  # 没检索到但回答错误
    lose_correct = []  # 没检索到但回答正确

    try:
        # 打开并加载数据集
        with open(generation_dataset, 'r', encoding='utf-8') as f:
            generation_dataset = json.load(f)
        with open(retrieval_dataset, 'r', encoding='utf-8') as f:
            retrieval_dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")
    
    result_data = []
    # 遍历数据集进行统计
    for retrieval_data in retrieval_dataset:
        answers = flatten_answers(retrieval_data['answer'])
        retrieve_results = retrieval_data['retrieve_results']

        # 根据不同数据集检查是否检索到答案（不区分大小写）
        if mode == "graph":
            retrieved = any(
                any(
                    any(answer.lower() in value.lower() for value in values)
                    for key, values in retrieve_results.items()
                )
                for answer in answers
            )
        elif mode == "vector":
            retrieved = any(
                any(answer.lower() in result['node_text'].lower() for result in retrieve_results)
                for answer in answers
            )
        elif mode == "hybrid":
            print("Not implemented yet")

        generation_data = next((item for item in generation_dataset if item['id'] == retrieval_data['id']), None)
        assert generation_data is not None, f"Cannot find the generation data for id {retrieval_data['id']}"

        correct_answer = generation_data['generation_evaluation']['exact_match']
        
        # 保存每个id的详细信息到result_data
        result_data.append({
            'id': retrieval_data['id'],
            'answers': answers,
            'retrieved': retrieved,
            'correct_answer': correct_answer
        })
        # 保存到文件方便查看（可删除）
        with open("/home/yangxb/RAGWebUi_demo/rgb/result.json", 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)

        if retrieved:
            if not correct_answer:
                retrieve_error.append(retrieval_data['id'])  
        else:
            if correct_answer:
                lose_correct.append(retrieval_data['id'])  
            else:
                lose_error.append(retrieval_data['id'])   
    print("retrieve_error",retrieve_error)
    print("lose_error",lose_error)
    print("lose_correct",lose_correct)
    return retrieve_error, lose_error, lose_correct


#todo这个函数我想统计一下每种RAG回答的情况 比如Hybrid回答正确，但vector graph回答错误，都回答错误，Hybrid错误但graph，vector其中一个回答正确
# 可以用key value来统计 比如都对 value为""GREEN" ,只有hybrid一个对""YELLOW"，Hybrid错误但graph，vector其中一个回答正确为""BlUE"  都错为""RED" 这样返回前端应该好整一点

# 或是你可以定义一个question_eval类 去储存每个question的id,query_str,answer,response,type(错误)

# 返回的是一个List[question_eval] 

def statistic_question(vector_dataset, graph_dataset, hybrid_dataset):
    question_eval = []
    
    try:
        # 打开并加载数据集
        with open(vector_dataset, 'r', encoding='utf-8') as f:
            vector_dataset = json.load(f)
        with open(graph_dataset, 'r', encoding='utf-8') as f:
            graph_dataset = json.load(f)
        with open(hybrid_dataset, 'r', encoding='utf-8') as f:
            hybrid_dataset = json.load(f)
    except Exception as e:
        print(f"Error reading the dataset: {e}")
    
    for vector_data in vector_dataset:
        vector = vector_data['generation_evaluation']['exact_match']

        graph_data = next((item for item in graph_dataset if item['id'] == vector_data['id']), None)
        assert graph_data is not None, f"Cannot find the graph data for id {vector_data['id']}"
        graph = graph_data['generation_evaluation']['exact_match']

        hybrid_data = next((item for item in hybrid_dataset if item['id'] == vector_data['id']), None)
        assert hybrid_data is not None, f"Cannot find the hybrid data for id {vector_data['id']}"
        hybrid = hybrid_data['generation_evaluation']['exact_match']

        if vector and graph and hybrid:
                response_situation = "GREEN"
        elif not vector and not graph and hybrid:
                response_situation = "YELLOW"
        elif (vector or graph) and not hybrid:
                response_situation = "BLUE"
        else:
                response_situation = "RED"
        question_eval.append({
            'id': vector_data['id'],
            'question': vector_data['question'],
            'answer': vector_data['answer'],
            'vector_response': vector_data['response'],
            'graph_response': graph_data['response'],
            'hybrid_response': hybrid_data['response'],
            'type': response_situation
        })
        with open("/home/yangxb/RAGWebUi_demo/rgb/result.json", 'w', encoding='utf-8') as f:
            json.dump(question_eval, f, ensure_ascii=False, indent=4)

    return question_eval

if __name__ == '__main__':
    
    # 数据集路径，需要替换一下
    rgb_result_path = "/home/yangxb/RAGWebUi_demo/rgb"
    rgb_graph_generation = "/home/yangxb/RAGWebUi_demo/rgb/graphrag/analysis_generation___merged.json"
    rgb_graph_retrieval = "/home/yangxb/RAGWebUi_demo/rgb/graphrag/analysis_retrieval_merged.json"
    rgb_vector_generation = "/home/yangxb/RAGWebUi_demo/rgb/vectorrag/analysis_generation___top5_2024-11-26_21-32-23.json"
    rgb_vector_retrieval = "/home/yangxb/RAGWebUi_demo/rgb/vectorrag/analysis_retrieval___top5_2024-11-26_21-32-23.json"
    # statistic_graph_generation(rgb_graph_generation)
    # statistic_graph_retrieval(rgb_graph_retrieval)
    # statistic_vector_generation(rgb_vector_generation)
    # statistic_vector_retrieval(rgb_vector_retrieval)
    # statistic_error_cause(rgb_vector_generation, rgb_vector_retrieval, "vector")
    # statistic_error_cause(rgb_graph_generation, rgb_graph_retrieval, "graph")