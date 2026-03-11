# LangChain RAG 实战

## 项目表述

RAG-Sys 是一个基于 **检索增强生成（Retrieval-Augmented Generation, RAG）** 技术的智能文档检索问答系统。该系统能够上传多种格式的文档（PDF、Word、TXT），通过父子文档块分割策略和向量检索技术，结合大语言模型提供精准的文档问答服务。

### 核心特性

- 📚 **多文档格式支持**：支持 PDF、DOCX、TXT 等多种文档格式上传。

- 🔍 **智能检索**：基于 Chroma 向量数据库的高效语义检索。

- 🧠 **父子文档块策略**：采用 Parent-Child Chunking 技术，提升检索精度和上下文完整性。

- 💬 **流式对话**：支持流式输出的自然语言对话体验。

- 🗄️ **持久化存储**：使用 MySQL 存储文档元数据和对话历史。

- 🎨 **友好界面**：基于 Streamlit 的现代化 Web 界面。

  

## 技术架构

### 系统架构

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  客户端应用   │ ──→  │  Streamlit  │ ──→  │ RAG Service │
└─────────────┘      └─────────────┘      └─────┬───────┘
                                               │
                       ┌───────────────────────┼───────────────────────┐
                       ▼                       ▼                       ▼
           ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
           │  Vector         │     │  Document       │     │  LLM            │
           │  Store          │     │  Processor      │     │  Model          │
           │                 │     │                 │     │                 │
           └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
                    │                       │                       │
                    ▼                       ▼                       ▼
           ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
           │  Chroma         │     │  MySQL          │     │  DashScope      │
           │  (向量存储)      │     │  (文档存储)       │     │  (文生模型)      │
           └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 技术栈

- **前端界面**: Streamlit
- **大语言模型**: 通义千问 (qwen3.5-plus) 
- **向量模型**: BGE-Large-ZH-v1.5 (本地部署)
- **向量数据库**: ChromaDB (持久化存储)
- **关系数据库**: MySQL + SQLAlchemy ORM
- **文档处理**: LangChain Document Loaders
- **文本分割**: LangChain Text Splitters
- **检索压缩**: Contextual Compression Retriever



## 项目结构

```
rag-sys/ 
├── src/ # 源代码目录 
│ ├── main.py # 主程序入口 (Streamlit 应用) 
│ └── app/ # 应用核心模块 
│ | ├── config.py # 配置文件 
│ | ├── chat_system.py # 聊天系统逻辑 
│ | ├── document_processor.py # 文档处理器 
│ | ├── vector_store.py # 向量存储管理 
│ | ├── ui/ # 用户界面模块 
│ | │ ├── ui_components.py # UI 组件定义 
│ | │ └── ui_logic.py # UI 交互逻辑 
│ | └── db/ # 数据库模块 
│ | | ├── db_manager.py # 数据库管理器 
│ | | └── db_models.py # 数据库模型定义 
└── .env # 项目配置文件
└── README.md # 项目文档
└── requirements.txt # 项目依赖
```



## 核心模块

1. **文档处理模块** (`DocumentProcessor`)
   - 文档加载：支持 PDF、DOCX、TXT 格式
   - 文本分割：三层分割策略（通用、父文档、子文档）
   - 父子文档块关联：Parent-Child Chunking

2. **向量存储模块** (`VectorStore`)
   - 双集合设计：父文档集合 + 子文档集合
   - 向量检索：基于子文档检索，父文档返回
   - 上下文压缩：LLMChainExtractor 优化检索结果

3. **聊天系统模块** (`ChatSystem`)
   - 普通对话模式：直接调用 LLM
   - RAG 对话模式：基于文档检索的智能问答
   - 对话历史管理：支持最近 N 轮对话上下文

4. **数据库模块** (`DatabaseManager`)
   - 文档元数据管理
   - 对话历史存储
   - 父子文档块关系维护



## 安装与部署

### 环境准备

- Python 3.10+
- MySql 5.7+
- BGE-Large-ZH-v1.5(ModeScope 下载嵌入模型)

### 安装步骤

1. 克隆项目

2. 安装依赖

   ```
   pip install -r requirements.txt
   ```

3. 配置环境（在.env文件中）

   ```
   # 阿里千问模型
   DASHSCOPE_API_KEY=your api-key
   DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   # MySql 
   MYSQL_PASSWORD=your password
   ```

4. 启动应用

```
streamlit run main.py
```



























