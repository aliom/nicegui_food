FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制主程序
COPY main.py .

# 暴露端口 (NiceGUI 默认 8080)
EXPOSE 8080

# 启动命令
CMD ["python", "main.py"]