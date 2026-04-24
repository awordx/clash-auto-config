# 使用最轻量级的 Python 镜像
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /workspace

# 安装必要的 Python 库
RUN pip install --no-cache-dir requests ruamel.yaml

# 将脚本复制进镜像
COPY get_config.py /workspace

# 设置环境变量：默认每 24 小时更新一次 (86400秒)
ENV UPDATE_INTERVAL=86400

# 运行一个简单的循环脚本：执行 Python -> 等待 -> 循环
CMD ["sh", "-c", "while true; do python get_config.py; echo \"Next update in $UPDATE_INTERVAL seconds...\"; sleep $UPDATE_INTERVAL; done"]