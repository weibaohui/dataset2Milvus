from flask import Flask, request, jsonify

import Transformer
import main

app = Flask(__name__)

transformer = Transformer.Transformer()


@app.route("/hello", methods=["POST"])
def hello():
    if request.is_json:
        data = request.get_json()
        return data["key"]
    else:
        # 如果请求体不是JSON格式，返回错误信息
        return jsonify({"error": "Request body is not in JSON format"})


@app.route("/search", methods=["POST"])
def search():
    if request.is_json:
        data = request.get_json()
        key = data["q"]
        commands = search_with_transformer(key)
        result = f"""
        我想要:\t{key} 。\n
        参考命令:\t{commands} 。\n
        请给我一个完整的具体的可执行的命令，只要命令本身，其他啥都不要返回，用纯文本格式返回，也不要用引号反引号`包裹命令
        """
        return {
            "result": result
        }
    else:
        # 如果请求体不是JSON格式，返回错误信息
        return jsonify({"error": "Request body is not in JSON format"})


def search_with_transformer(search_text: str):
    search_vector = transformer.get_embedding(search_text)
    res = main.MILVUS_HELPER.client.search(
        collection_name=main.COLLECTION_NAME,  # Replace with the actual name of your collection
        data=[search_vector],
        limit=3,
        search_params={"metric_type": "IP", "params": {}}  # Search parameters
    )
    ids_list = [item['id'] for item in res[0]]
    res = main.MILVUS_HELPER.client.get(
        collection_name=main.COLLECTION_NAME,
        ids=ids_list
    )
    return [item['command'] for item in res]


if __name__ == '__main__':
    app.run(debug=True, port=3388)
