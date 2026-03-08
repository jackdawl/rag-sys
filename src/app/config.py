import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    OPENAI_BASE_URL = os.getenv("DASHSCOPE_BASE_URL")
    OPENAI_MODEL_NAME = "qwen3.5-plus"
    # OPENAI_API_KEY = "ollama"
    # OPENAI_BASE_URL = "http://localhost:11434/v1"
    # OPENAI_MODEL_NAME = "deepseek-r1:7b"

    # MySQL配置
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = "rag_sys"

    # Chroma配置
    CHROMA_PERSIST_DIR = "./chroma_db"

    # 其他配置
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP =  200
    TOP_K = 5