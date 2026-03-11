import sqlite3
import sqlite_vec
import struct
from typing import List

# 1. 连接数据库（这里使用内存数据库作为示例）
db = sqlite3.connect(":memory:")

# 2. 加载 sqlite-vec 扩展
db.enable_load_extension(True)
sqlite_vec.load(db)  # 这会自动找到并加载编译好的扩展库
db.enable_load_extension(False)

# 3. 验证扩展是否加载成功
sqlite_version, vec_version = db.execute("select sqlite_version(), vec_version()").fetchone()
print(f"SQLite Version: {sqlite_version}, Sqlite-Vec Version: {vec_version}")

# 4. 创建向量虚拟表
# 定义一个表来存储 4 维的浮点数向量
db.execute("""
    CREATE VIRTUAL TABLE vec_items USING vec0(
        embedding FLOAT[4]  -- 指定向量维度为 4
    )
""")

# 5. 准备数据和辅助函数
def serialize_f32(vector: List[float]) -> bytes:
    """将浮点数列表序列化为紧凑的字节格式"""
    return struct.pack(f'{len(vector)}f', *vector)

# 插入一些示例向量
items = [
    (1, [0.1, 0.1, 0.1, 0.1]),
    (2, [0.2, 0.2, 0.2, 0.2]),
    (3, [0.3, 0.3, 0.3, 0.3]),
    (4, [0.4, 0.4, 0.4, 0.4]),
]

# 执行批量插入
with db:
    for id, vector in items:
        db.execute(
            "INSERT INTO vec_items(rowid, embedding) VALUES (?, ?)",
            [id, serialize_f32(vector)]
        )

# 6. 执行向量相似度搜索 (KNN)
query_vector = [0.3, 0.3, 0.3, 0.3]

rows = db.execute("""
    SELECT rowid, distance 
    FROM vec_items 
    WHERE embedding MATCH ? 
    ORDER BY distance 
    LIMIT 3
""", [serialize_f32(query_vector)]).fetchall()

print("最相似的向量:", rows)
# 输出示例: [(3, 0.0), (4, 0.20000001788139343), (2, 0.20000001788139343)]