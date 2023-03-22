import json
import pickle
import re  # 读取数据库 用于判断 表格是否存在 是否需要创建
import pandas as pd  # 读取文件
import pymysql  # 数据库连接
import os  # 操作文件 读取内存大小

# 读取Excel文件
excel_file = "students_scores.xlsx"  # 读取文件
df = pd.read_excel(excel_file, sheet_name=None)  # 遍历sheet  None可以指明哪张表名

# 输出所有内容
print(df)


def table_exists(con, table_name):  # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0  # 不存在返回0


conn = pymysql.connect(
    host='localhost',  # MySQL服务器地址
    port=3306,  # MySQL服务器端口号
    user='root',  # 用户名
    password='111111',  # 密码
    database='pythonprogramming',  # 数据库名称
    charset='utf8mb4'  # 字符集
)
cursor = conn.cursor()

# 判断数据库是否存在表格 不存在 则创建
if table_exists(cursor, 'students') != 1:
    # 创建表
    create_table_query = """
    CREATE TABLE students(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT,
        gender VARCHAR(10)
        # TODO: 添加更多字段
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_table_query)

# 将数据插入表中
for sheet_name in df.keys():
    sheet = df[sheet_name]
    for row in sheet.iterrows():  # 逐行遍历
        #    for row in df.iterrows():
        insert_query = """
        INSERT IGNORE INTO students(name, age, gender) VALUES (%s, %s, %s) 
        """

        values = tuple(row[1])  # 注意：这里需要转换为元组
        cursor.execute(insert_query, values)
    conn.commit()

# 保存为二进制格式文件
# binary_file = "students_scores.pkl"
# df.to_pickle(binary_file)

binary_file = "students_scores.pkl"
with open(binary_file, "wb") as f:
    pickle.dump(df, f)

# 保存为JSON文本格式文件
# json_file = "students_scores.json"
# df.to_json(json_file)

# 使用了一个字典推导式来遍历所有的表单，并将每个表单转换为字典，
# 最终将所有表单的字典组成一个新的字典作为json.dump函数的第一个参数。
# 这样可以避免直接将DataFrame对象序列化为JSON字符串而产生的错误。
json_file = "students_scores.json"
with open(json_file, "w") as f:
    json.dump({sheet_name: sheet.to_dict() for sheet_name, sheet in df.items()}, f)

# 比较文件大小
print("Excel文件大小：", os.path.getsize(excel_file))
print("二进制文件大小：", os.path.getsize(binary_file))
print("JSON文件大小：", os.path.getsize(json_file))

# 关闭连接
cursor.close()
conn.close()
