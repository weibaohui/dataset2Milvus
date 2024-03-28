FROM python:latest
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /app
COPY . .

# install python dep
RUN pip install uv \
    && uv venv \
    && source .venv/bin/activate \
    && uv pip install -r requirements.txt

# install sentence transformer off line
RUN mkdir -p /data/model/gte-large-zh
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/config.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/model.safetensors
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/modules.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/pytorch_model.bin
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/sentence_bert_config.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/special_tokens_map.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/tokenizer.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/tokenizer_config.json
RUN wget -P /data/model/gte-large-zh https://huggingface.co/thenlper/gte-large-zh/resolve/main/vocab.txt
RUN mkdir -p /data/model/gte-large-zh/1_Pooling
RUN wget -P /data/model/gte-large-zh/1_Pooling https://huggingface.co/thenlper/gte-large-zh/resolve/main/1_Pooling/config.json
# set transformer model
ENV TRANSFORMERS_OFFLINE=1
ENV TRANSFORMERS_OFFLINE_NAME=thenlper/gte-large-zh
ENV TRANSFORMERS_OFFLINE_PATH=/data/model/gte-large-zh

EXPOSE 80
CMD ["bash", "-c","start-web.sh"]