import json

def adviser(type_result_path="/home/lipz/NeutronRAG/NeutronRAG/backend/evaluator/rgb/type_result.json"):
    try:
        # 打开并加载JSON文件
        with open(type_result_path, 'r') as file:
            data = json.load(file)
        
        # 初始化计数器
        count_green = 0
        count_red = 0
        count_yellow = 0
        
        # 遍历数据并统计每种类型的数量
        for item in data:
            if item.get('type') == 'GREEN':
                count_green += 1
            elif item.get('type') == 'RED':
                count_red += 1
            elif item.get('type') == 'YELLOW':
                count_yellow += 1
        
        # 输出统计结果
        #
        print(f"GREEN: {count_green}")
        print(f"RED: {count_red}")
        print(f"YELLOW: {count_yellow}")
    
    except FileNotFoundError:
        print(f"文件 {type_result_path} 未找到，请检查路径是否正确。")
    except json.JSONDecodeError:
        print("文件内容无效，无法解析为JSON格式。")
    except Exception as e:
        print(f"发生错误: {e}")



