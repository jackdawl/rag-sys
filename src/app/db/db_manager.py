
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db_models import  ChatHistory, Document, ParentChunk, ChildChunk

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseManager:
    """数据库管理器"""
    def __init__(self, config):
        self.config = config
        self.engine = None
        self.SessionLocal = None
        self.init_database()

    def init_database(self):
        """创建数据库连接"""

        connection_string = f"mysql+pymysql://{self.config.MYSQL_USER}:{self.config.MYSQL_PASSWORD}@{self.config.MYSQL_HOST}:{self.config.MYSQL_PORT}/{self.config.MYSQL_DATABASE}?charset=utf8mb4"
        try:
            self.engine = create_engine(connection_string, echo=False)
            # 创建所有的表
            Base.metadata.create_all(self.engine)
            self.SessionLocal = sessionmaker(bind=self.engine)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise

    def get_session(self):
        """获取数据库连接session"""
        return self.SessionLocal()

    def get_chat_history(self, session_id, limit=10):
        """获取聊天记录"""
        session = self.get_session()
        try:
            chats = session.query(ChatHistory).filter(
                ChatHistory.session_id == session_id
            ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
            return list(reversed(chats))
        finally:
            session.close()


    def save_chat_history(self, session_id, user_message, assistant_message, document_ids=None, used_chunks=None):
        """保存聊天记录"""
        session = self.get_session()
        try:
            chat = ChatHistory(
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_message,
                document_ids=document_ids,
                used_chunks=used_chunks
            )
            session.add(chat)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def save_document_with_chunks(self, filename, file_path, content, parent_docs, child_docs, parent_vector_ids,
                                  child_vector_ids):
        """保存文档及其父子文档块"""
        session = self.get_session()
        try:
            # 保存主文档
            doc = Document(
                filename=filename,
                file_path=file_path,
                content=content,
                chunk_count=len(child_docs)
            )
            session.add(doc)
            session.flush()  # 获取文档ID
            doc_id = doc.id

            # 保存父文档块
            parent_chunk_map = {}  # parent_id -> parent_chunk_id 映射
            for i, (parent_doc, vector_id) in enumerate(zip(parent_docs, parent_vector_ids)):
                parent_chunk = ParentChunk(
                    document_id=doc_id,
                    parent_id=parent_doc.metadata.get('parent_id', f'parent_{i+1}'),
                    content=parent_doc.page_content,
                    json_metadata=str(parent_doc.metadata),
                    vector_id=vector_id
                )
                session.add(parent_chunk)
                session.flush()
                parent_chunk_map[parent_chunk.parent_id] = parent_chunk.id

            # 保存子文档块
            for child_doc, vector_id in zip(child_docs, child_vector_ids):
                parent_id = child_doc.metadata.get('parent_id', 'unknown')
                parent_chunk_id = parent_chunk_map.get(parent_id)

                child_chunk = ChildChunk(
                    document_id=doc_id,
                    parent_chunk_id=parent_chunk_id,
                    child_id=child_doc.metadata.get('child_id', f'child_{len(child_docs)}'),
                    content=child_doc.page_content,
                    json_metadata=str(child_doc.metadata),
                    vector_id=vector_id
                )
                session.add(child_chunk)

            session.commit()
            return doc_id

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def get_all_documents(self):
        """获取所有文档"""
        session = self.get_session()
        try:
            docs = session.query(Document).filter(Document.is_active == True).all()
            return docs
        finally:
            session.close()