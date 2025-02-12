import json
import time
from flask import Flask, Response, request, jsonify, render_template, session
from zhipuai import ZhipuAI
from user import User  # 假设你的 User 类定义在 user.py 中
from llmragenv.llmrag_env import LLMRAGEnv

app = Flask(__name__)
app.secret_key = 'ac1e22dfb44b87ef38f5bf2cd1cb0c6f93bb0a67f1b2d8f7'  # 用于 flash 消息


@app.route('/')
def index():
    return render_template('demo.html')  # 大模型页面
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')  # 注册页面
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


# [
    # {
    #     "id": 83,
    #     "question": "Who won the 2022 Tour de France?",
    #     "answer": [
    #         "Jonas Vingegaard"
    #     ],
    #     "vector_response": "Denmark's Jonas Vingegaard (Jumbo-Visma) won the yellow jersey as the overall winner of the 2022 Tour de France.",
    #     "graph_response": "Jonas Vingegaard",
    #     "hybrid_response": "Jonas Vingegaard",
    #     "type": "GREEN"
    # },

@app.route('/read-file', methods=['GET'])
def read_file():
    try:
        # 设定文件路径
        file_path = '/home/lipz/NeutronRAG/NeutronRAG/backend/evaluator/rgb/type_result.json'
        
        # 读取文件并解析 JSON 内容
        with open(file_path, 'r') as file:
            data = json.load(file)

        # 这里可以根据需要处理数据
        # 例如，如果你只想返回某些字段，可以在这里做处理
        result = []
        for item in data:
            # 假设你想返回 id, question, answer 和 response 字段
            result.append({
                'id': item.get('id'),
                'question': item.get('question'),
                'answer': item.get('answer'),
                'hybrid_response': item.get('hybrid_response'),
                'type' : item.get('type')
            })

        # 返回经过处理的数据
        return jsonify({'content': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()  # 获取前端传来的 JSON 数据
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not all([username, email, phone, password, confirm_password]):
        return jsonify({"error": "所有字段都是必需的！"}), 400

    try:
        user = User(username=username, email=email, phone=phone, password=password)
        if user.register(confirm_password):
            return jsonify({"message": "注册成功！"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()  # 获取前端传来的 JSON 数据
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "用户名和密码是必需的！"}), 400

    try:
        user = User(username=username, email=None, phone=None, password=password)
        if user.login(password):
            session['username'] = username  # 将用户名存储到 session
            session['user_id'] = user.get_user_id()  # 存储用户 ID
            return jsonify({"message": "登录成功！"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400



# def web_chat(self, message : str, history: List[Optional[List]] | None, op0 : str,op1 : str, op2 : str, op3 : str):
        
#         """Used to chat with LLM from ./webchat.py

#         Args:
#             message (list[str]): The query list
#             op0 (str): The llm name ("qwen:0.5b", "llama2:7b", "llama2:13b", "llama2:70b","qwen:7b","qwen:14b","qwen:72b", etc)
#             op1 (str): The RAG way ("graph rag", "vector rag", "without rag", "union rag")
#             op2 (str): The name of graph database ("nebulagraph", "neo4j", ect)
#             op3 (str): The name of vector database ("MilvusDB")
#         """
# <div class="chat-type-selector">
#     <select id="chatType">
            # <option value="general">VectorRAG</option>
            # <option value="technical">GraphRAG</option>
            # <option value="union">Hybrid RAG</option>
            # <option value="fun">Without RAG</option>
#     </select>
#这个函数改成前端post的数据要加上 mode [Without_RAG,GraphRAG,VectorRAG]  model：str 

@app.route('/api/chat', methods=['POST'])
def web_chat():
    chat_env = LLMRAGEnv()
    data = request.get_json()
    user_input = data.get('user_input')
    model = "qwen:0.5b" #这里写死了，你们改一下
    rag_mode = data.get('mode')
    graph_db = "nebulagraph"
    vector_db = "milvus"
    history = [] 

    # 使用生成器进行流式响应
    def generate_chat():
        try:
            # 调用生成器方法，模拟生成流式数据
            answer = chat_env.web_chat(
                message=user_input,
                history=history,
                op0=model,
                op1=rag_mode,
                op2=graph_db,
                op3=vector_db
            )
            for msg in answer:
                # 按 SSE 格式发送 JSON 消息
                print(f"data: {json.dumps({'message': msg})}")
                yield f"data: {json.dumps({'message': msg})}\n\n"
                time.sleep(0.1)  # 模拟延时

            # 流结束时，发送特殊的结束标志
            yield "data: {\"message\": \"[END]\"}\n\n"

        except Exception as e:
            # 如果发生异常，返回错误消息
            print(f"Error occurred: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


    def test_chat():
        answer = ["hello", "welcome", "to", "china"]
        for msg in answer:
            # 返回有效的 JSON 格式的消息
            print(f"data: {json.dumps({'message': msg})}")
            yield f"data: {json.dumps({'message': msg})}\n\n".encode('utf-8')
            time.sleep(1)  # 延时模拟流式输出

        # 添加结束标志
        yield "data: {\"message\": \"[END]\"}\n\n".encode('utf-8')
    

    # 返回流式数据
    return Response(generate_chat(), content_type='text/event-stream'),200

    



# @app.route('/api/chat', methods=['POST'])
# def memory_chat():

#     data = request.get_json()  # 获取前端传来的 JSON 数据
#     user_input = data.get('user_input')
#     model = data.get('model')
    
#     client = ZhipuAI(api_key="de2e91484b4b40ebad17347e4ab33f23.L1zrAybIgusCtTKL")
#     if model == "模型1":
#         client = ZhipuAI(api_key="de2e91484b4b40ebad17347e4ab33f23.L1zrAybIgusCtTKL")
#     # elif model == "模型2":
#     #     client = ZhipuAI(api_key="your_api_key")
#     # elif model == "模型3":
#     #     client = OpenAI(api_key="your_api_key")
#     # elif model == "模型4":
#     #     client = OpenAI(api_key="your_api_key")

#     response = client.chat.completions.create(
#             model="glm-4-plus",  # 选择合适的模型
#             messages=[
#                 {"role": "user", "content": user_input}
#             ],
#         )
#     # 获取回答内容

#     answer = response.choices[0].message.content

#     user_id = session.get('user_id')  # 从 session 中获取用户 ID
#     session_id = 1      # 假设用户在进行第1个对话

#     return jsonify({"message": answer}), 200
#     '''  
#   try:
#         user = User(username=None, email=None, phone=None, password=None)
#         if not user_id:
#             return jsonify({"error": "用户未登录！"}), 401
#         if user.message_memory(session_id, user_input):
#             return jsonify({"message": "消息已保存！"}), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 400
#     '''
    
@app.route('/api/get-username', methods=['GET'])
def get_username():
    username = session.get('username')  # 从 session 获取用户名
    if username:
        return jsonify({"username": username}), 200
    else:
        return jsonify({"error": "用户未登录"}), 401
    
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()  # 清除所有 session 数据
    return jsonify({"message": "注销成功"}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
