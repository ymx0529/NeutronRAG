# 🔨Setup

```bash


# 创建conda环境：python >= 3.10
conda create --name llmrag python=3.10.14 -y

conda activate llmrag

# 安装相关的python包：
pip install -r requirements.txt

```

# 测试OLlama是否可用：
```bash
ollama run llama2:7b
```


📦 部署图数据库
1. NebulaGraph Installation Guide
Step 1: Install docker-compose
Ensure that you have docker-compose installed. If not, you can install it with the following command:

```bash
sudo apt install docker-compose
```
Step 2: Clone NebulaGraph Docker Compose Repository
In a directory of your choice, clone the NebulaGraph Docker Compose files:

```bash
git clone https://github.com/vesoft-inc/nebula-docker-compose.git
cd nebula-docker-compose
```
Step 3: Start NebulaGraph
In the nebula-docker-compose directory, run the following command to start NebulaGraph:

```bash
docker-compose up -d
```
Step 4: Check NebulaGraph Container Status
After starting, you can verify that the NebulaGraph container is running by using:

```bash
docker ps
```
Step 5: Connect to NebulaGraph
To connect to NebulaGraph inside the container, use the following command:

```bash
nebula-console -u <user> -p <password> --address=graphd --port=9669
#Replace <user> and <password> with the actual username and password. Ensure that port 9669 is used for the default configuration.
```
Step 6: Enable Data Persistence
To ensure that data persists even after the container is restarted, you can mount persistent volumes. Either modify the volumes section in the docker-compose.yaml file, or manually run the following command with specified persistence paths:

```bash
docker run -d --name nebula-graph \
    -v /yourpath/nebula/data:/data \
    -v /yourpath/nebula/logs:/logs \
    -p 9669:9669 \
    vesoft/nebula-graphd:v2.5.0
#Replace /yourpath/nebula with your actual data persistence path.
```




2. Neo4j(暂时可以不安装)






# 💄Run 
```
#配置临时环境变量环境
例子 export PYTHONPATH=$PYTHONPATH:/home/lipz/RAGWebUi/RAGWebUi_demo/backend
export PYTHONPATH=$PYTHONPATH:/your/path/backend

```

```
# 执行一个weiui，以显示前端网页： 
python webui_chat.py

# 使用另一个终端执行一个图的网页，用来在前端网页中显示图拓扑：
python graph.py
```

```
# 使用后端执行主要为了做一些研究工作：
python backend_chat.py --dataset_name "rgb" --llm "llama2:7b" --func "Graph RAG" --graphdb "nebulagraph" --vectordb "MilvusDB"
```

# Notion

1. 现在弃用了.env文件的读取方式，改为客户端输入。包括大模型的名字
2. ./llmragenv/llmrag_env.py 中，有一个low_chat的方法，这个是一个阉割的输入，大模型的名字、数据库的使用等参数直接在这里指定了；而web_chat是一个全的版本
3. 关于大模型的支持：在llm_factory中由llm_provider字典，包含了现在支持的运行在本地的大模型。（因为使用商用大模型的api_key付费，这里暂时不开放，但可以自己去买，相关配置在./config/config-local.ymal）
4. 网页端口与数据库相关配置在./config/config-local.ymal进行更改（向量数据库与nebulagraph在代码里指定，这里需要重构）
5. 代码架构：
![avatar](./resource/codestruc/codestruc.bmp)


# 问题：
web_chat()中虽然可以指定每次聊天的大模型，但是问题是启动网页之后只有第一次的输入是有用的，后续大模型都只用最开始选的那个。
# 代码结构：

Chat:
/<yourpath>/RAGWebUi_demo/chat
graphrag和vectorrag




# Reference
[Meet-libai from BinNong](https://github.com/BinNong/meet-libai)