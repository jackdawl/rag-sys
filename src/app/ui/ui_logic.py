import time
import streamlit as st

from app.config import Config
from app.db.db_manager import DatabaseManager
from app.document_processor import DocumentProcessor
from app.vector_store import VectorStore
from app.chat_system import ChatSystem
from app.ui.ui_components import display_message

def init_system():
    """初始化系统组件"""

    config = Config()
    db_manager = DatabaseManager(config)
    doc_processor = DocumentProcessor(config)
    vector_store = VectorStore(config)
    chat_system = ChatSystem(config, db_manager, vector_store)
    return config, db_manager, doc_processor, vector_store, chat_system


def stream_response_generator(chat_system, message, selected_doc_ids, session_id, is_rag_mode=True):
    """生成流式响应的生成器函数"""
    if is_rag_mode:

        print("============>chat_with_documents")
        response, retrieved_docs = chat_system.chat_with_documents(
            message, selected_doc_ids, session_id
        )

        print("============>response")
        words = response.split()
        current_response = ""

        for i, word in enumerate(words):
            current_response += word + " "
            yield current_response.strip(), retrieved_docs if i == len(words) - 1 else None
            time.sleep(0.05)
    else:
        response = chat_system.normal_chat(message, session_id)

        words = response.split()
        current_response = ""

        for word in words:
            current_response += word + " "
            yield current_response.strip(), None
            time.sleep(0.05)


def display_streaming_message(role, generator, docs_placeholder=None):
    """显示流式消息"""

    message_class = "message user" if role == "user" else "message"
    avatar_class = "user-avatar" if role == "user" else "assistant-avatar"
    content_class = "user-message" if role == "user" else "assistant-message"
    avatar_icon = "👤" if role == "user" else "🤖"

    message_placeholder = st.empty()
    final_content = ""
    retrieved_docs = None

    for content, docs in generator:
        final_content = content
        if docs is not None:
            retrieved_docs = docs

        display_content = content + " <span class='streaming-cursor'></span>"

        message_placeholder.markdown(f"""
        <div class="{message_class}">
            <div class="message-avatar {avatar_class}">
                {avatar_icon}
            </div>
            <div class="message-content {content_class}">
                {display_content}
            </div>
        </div>
        """, unsafe_allow_html=True)

    message_placeholder.markdown(f"""
    <div class="{message_class}">
        <div class="message-avatar {avatar_class}">
            {avatar_icon}
        </div>
        <div class="message-content {content_class}">
            {final_content}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if retrieved_docs and role == "assistant" and docs_placeholder:
        with docs_placeholder:
            with st.expander("📚 参考来源", expanded=False):
                for i, doc in enumerate(retrieved_docs, 1):
                    st.markdown(f"""
                    <div class="doc-card">
                        <strong>📄 片段 {i}</strong><br>
                        {doc.page_content[:200]}{'...' if len(doc.page_content) > 200 else ''}
                    </div>
                    """, unsafe_allow_html=True)

    return final_content, retrieved_docs



def handle_user_input(chat_system, prompt, selected_doc_ids):
    """处理用户输入"""
    if 'session_id' not in st.session_state or st.session_state.session_id is None:
        st.session_state.session_id = chat_system.generate_session_id()

    st.session_state.messages.append({"role": "user", "content": prompt})
    display_message("user", prompt)

    docs_placeholder = st.empty()

    with st.spinner("🤔 思考中..."):
        if selected_doc_ids:
            print("============>使用RAG模式")
            generator = stream_response_generator(
                chat_system, prompt, selected_doc_ids,
                st.session_state.session_id, is_rag_mode=True
            )
            final_content, retrieved_docs = display_streaming_message(
                "assistant", generator, docs_placeholder
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_content,
                "docs": retrieved_docs
            })
        else:
            generator = stream_response_generator(
                chat_system, prompt, [],
                st.session_state.session_id, is_rag_mode=False
            )
            final_content, _ = display_streaming_message("assistant", generator)
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_content
            })
