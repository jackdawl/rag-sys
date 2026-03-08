import streamlit as st
from app.ui.ui_components import configure_page, render_chat_header, render_status_indicator, display_message, \
    display_welcome_message, render_sidebar
from app.ui.ui_logic import init_system, handle_user_input


def main():
    """页面加载主函数"""
    # 配置页面
    configure_page()

    # 初始化系统
    config, db_manager, doc_processor, vector_store, chat_system = init_system()

    # 渲染侧边栏并获取选中的文档
    selected_doc_ids = render_sidebar(db_manager, doc_processor, vector_store)

    # 渲染主聊天界面
    render_chat_header()
    render_status_indicator(selected_doc_ids)

    # 初始化会话状态
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 聊天消息显示区域
    chat_container = st.container()

    with chat_container:
        if not st.session_state.messages:
            display_welcome_message()
        else:
            for message in st.session_state.messages:
                display_message(
                    message["role"],
                    message["content"],
                    message.get("docs")
                )

    # 用户输入处理
    if prompt := st.chat_input("💬 输入你的问题..."):
        handle_user_input(chat_system, prompt, selected_doc_ids)


if __name__ == '__main__':
    main()

