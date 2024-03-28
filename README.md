# 思路说明
本项目示例如何将k8s命令集导入到milvus中。
Datasets：https://huggingface.co/datasets/ComponentSoft/k8s-kubectl
1. 将datasets进行简单处理，增加了一个strs字段，存放需要计算向量的内容 。并删除不必要字段
2. 将datasets 存入 sqlite 临时数据库。vector字段为空。
3. 从sqlite中读取vector为空的数据，逐行进行向量计算，将向量结果更新回数据库
4. 将sqlite中的数据，导入到milvus中
5. 提供了一个使用向量进行查询的示例

# 环境准备
## 安装依赖
1. Install uv - Python Package manager (https://github.com/astral-sh/uv)
2. uv venv
3. source .venv/bin/activate
4. uv pip install -r requirements.txt  

# 配置
1. 参考main.py 中的变量设置，设置milvus db、collection名称
2. 参考data.py 调整datasets中的字段
3. 参考SqliteDataBase.py 设置对应dataset的数据库字段、sqlite数据库名称等
4. 参考Transformer.py 设置对应的计算向量用的文本transformer
5. 使用Gemini大模型，需要配置API_KEY
```bash
export GOOGLE_API_KEY='xxxxxxxxxxx'
```


# Docker 运行环境配置
1. 镜像内置 thenlper/gte-large-zh sentence transformer,如需更改，请更新Dockerfile文件
2. 镜像默认启动flask，连接Milvus进行查询
3. Milvus连接配置需要通过env进行指定
4. Docker run
```docker
docker run   -e MILVUS_HOST=host.docker.internal \
             -e MILVUS_HOST_PORT=19530 \
             -e MILVUS_DB_NAME=book \
             -e MILVUS_COLLECTION_NAME=book \
             -it --rm \
             -p 3388:80 \
             ghcr.io/weibaohui/vector-helper:latest
             
```

# enjoy
