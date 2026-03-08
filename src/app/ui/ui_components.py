import streamlit as st


def get_custom_css():
    """自定义CSS样式"""
    return """
<style>
    /* 聊天容器 */
    .chat-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 20px auto;
        max-width: 800px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    /* 头部样式 */
    .chat-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 12px 12px 0 0;
    }

    .chat-title {
        font-size: 24px;
        font-weight: 600;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .chat-subtitle {
        font-size: 14px;
        opacity: 0.9;
        margin-top: 5px;
    }

    /* 聊天消息区域 */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #f8f9fa;
    }

    /* 消息样式 */
    .message {
        margin-bottom: 16px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }

    .message.user {
        flex-direction: row-reverse;
    }

    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }

    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .assistant-avatar {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
    }

    .message-content {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 18px;
        font-size: 14px;
        line-height: 1.4;
    }

    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }

    .assistant-message {
        background: white;
        color: #333;
        border: 1px solid #e1e5e9;
        border-bottom-left-radius: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* 流式输出动画 */
    .streaming-cursor::after {
        content: '▊';
        animation: blink 1s infinite;
        color: #667eea;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    /* 文档卡片样式 */
    .doc-card {
        background: 000000;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }

    .doc-card:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
    }

    /* 状态指示器 */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }

    .status-rag {
        background: #e3f2fd;
        color: #1976d2;
    }

    .status-normal {
        background: #f3e5f5;
        color: #7b1fa2;
    }

    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    #header {visibility: hidden;}

    /* 自定义按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .chat-container {
            margin: 10px;
            height: 85vh;
        }

        .message-content {
            max-width: 85%;
        }
    }
</style>
"""


# ==============================================
# 页面配置
# ==============================================
def configure_page():
    """配置主界面"""
    st.set_page_config(
        page_title="智能文档检索助手",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # 应用 CSS 样式
    st.markdown(get_custom_css(), unsafe_allow_html=True)


# ==============================================
# UI 组件
# ==============================================
def render_chat_header():
    """渲染聊天头部"""
    st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-title">
                    🤖 智能文档检索助手
                </div>
                <div class="chat-subtitle">
                    基于知识库的智能问答系统
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_status_indicator(selected_doc_ids):
    """渲染状态指示器"""
    col1, col2 = st.columns([2, 1])
    with col1:
        if selected_doc_ids:
            st.markdown(f"""
            <div class="status-indicator status-rag">
                🔍 知识库模式 ({len(selected_doc_ids)} 个文档)
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-indicator status-normal">
                💭 普通对话模式
            </div>
            """, unsafe_allow_html=True)


def display_message(role, content, docs=None):
    """显示静态消息"""
    message_class = "message user" if role == "user" else "message"
    avatar_class = "user-avatar" if role == "user" else "assistant-avatar"
    content_class = "user-message" if role == "user" else "assistant-message"
    avatar_icon = "👤" if role == "user" else "🤖"

    st.markdown(f"""
    <div class="{message_class}">
        <div class="message-avatar {avatar_class}">
            {avatar_icon}
        </div>
        <div class="message-content {content_class}">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 如果有参考文档，显示在消息下方
    if docs and role == "assistant":
        with st.expander("📚 参考来源", expanded=False):
            for i, doc in enumerate(docs, 1):
                st.markdown(f"""
                <div class="doc-card">
                    <strong>📄 片段 {i}</strong><br>
                    {doc.page_content[:200]}{'...' if len(doc.page_content) > 200 else ''}
                </div>
                """, unsafe_allow_html=True)


def display_welcome_message():
    """显示欢迎消息"""
    st.markdown("""
    <div class="message">
        <div class="message-avatar assistant-avatar">🤖</div>
        <div class="message-content assistant-message">
            👋 你好！我是你的 AI 智能助手。<br><br>
            💡 <strong>我能做什么：</strong><br>
            • 📚 基于你上传的文档回答问题<br>
            • 💬 进行日常对话交流<br>
            • 🔍 提供准确的信息检索<br><br>
            请上传文档或直接开始对话吧！
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_document_card(doc):
    """渲染文档卡片"""
    st.markdown(f"""
    <div class="doc-card">
        <strong>📄 {doc.filename}</strong><br>
        <small>📅 {doc.created_at.strftime('%Y-%m-%d %H:%M')}</small><br>
        <small>📊 {doc.chunk_count} 个文档块</small>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar(db_manager, doc_processor, vector_store):
    """渲染侧边栏"""

    with st.sidebar:
        st.markdown("### 📁 文档管理")

        # 文档上传
        uploaded_files = st.file_uploader(
            "上传知识库文档",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="支持 PDF、Word 和 txt 文件"
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                if st.button(f"📤 处理 {uploaded_file.name}", key=f"process_{uploaded_file.name}"):
                    if upload_and_process_document(uploaded_file, doc_processor, vector_store, db_manager):
                        st.rerun()

        # 水平线分隔符
        st.markdown("---")

        # 已有文档
        st.markdown("### 📚 知识库")
        documents = db_manager.get_all_documents()

        if documents:
            doc_options = {f"{doc.filename}": doc.id for doc in documents}
            selected_docs = st.multiselect(
                "选择知识源",
                options=list(doc_options.keys()),
                help="选择后将基于文档内容回答问题"
            )
            selected_doc_ids = [doc_options[doc] for doc in selected_docs]

            # 显示文档列表
            for doc in documents:
                render_document_card(doc)
        else:
            st.info("暂无文档，请先上传")
            selected_doc_ids = []

        total_docs = len(documents) if documents else 0
        st.metric("📊 文档数", total_docs)

        if st.button("🗑️ 清空对话"):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.rerun()

    return selected_doc_ids if documents else []


def upload_and_process_document(uploaded_file, doc_processor, vector_store, db_manager):
    """处理上传的文档"""
    with st.spinner(f"正在处理文档 {uploaded_file.name}..."):
        try:
            documents = doc_processor.load_document(uploaded_file)
            parent_docs, child_docs = doc_processor.create_parent_child_chunks(documents, uploaded_file.name)
            parent_vector_ids, child_vector_ids = vector_store.add_documents(parent_docs, child_docs, 0)

            content = "\n".join([doc.page_content for doc in documents])
            print(parent_vector_ids)
            doc_id = db_manager.save_document_with_chunks(
                filename=uploaded_file.name,
                file_path="",
                content=content,
                parent_docs=parent_docs,
                child_docs=child_docs,
                parent_vector_ids=parent_vector_ids,
                child_vector_ids=child_vector_ids
            )

            for doc in parent_docs + child_docs:
                doc.metadata['document_id'] = str(doc_id)

            st.success(f"✅ 文档 '{uploaded_file.name}' 上传成功！")
            return True
        except Exception as e:
            st.error(f"❌ 文档处理失败：{str(e)}")
            return False
