# test_retrieval.py
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.config import Config
from app.vector_store import VectorStore

print("=" * 50)
print("测试向量检索")
print("=" * 50)

config = Config()
print("✓ 配置加载完成")

try:
    vector_store = VectorStore(config)
    print("✓ 向量存储初始化完成")
except Exception as e:
    print(f"✗ 向量存储初始化失败：{e}")
    sys.exit(1)

# 检查文档数量
try:
    child_count = vector_store.child_vector_store._collection.count()
    parent_count = vector_store.parent_vector_store._collection.count()
    print(f"✓ 父文档数：{parent_count}, 子文档数：{child_count}")

    if child_count == 0:
        print("⚠️ 警告：子文档库为空！请先上传文档")
        sys.exit(1)
except Exception as e:
    print(f"✗ 检查文档数量失败：{e}")
    sys.exit(1)

# 测试检索
print("\n开始测试检索...")
retriever = vector_store.create_retriever(use_compression=False)
print("✓ 检索器创建完成")

test_question = "deepseek的主要影响"
print(f"检索问题：{test_question}")

try:
    results = retriever.invoke(test_question)
    print(f"✓ 检索成功，找到 {len(results)} 个文档")
    for i, doc in enumerate(results[:3], 1):
        print(f"\n文档 {i}:")
        print(f"内容：{doc.page_content[:100]}...")
except Exception as e:
    print(f"✗ 检索失败：{e}")
    import traceback

    traceback.print_exc()

print("\n测试完成")
