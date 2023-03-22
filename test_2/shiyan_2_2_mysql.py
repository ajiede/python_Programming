import pymysql

# 连接MySQL
conn = pymysql.connect(
    host='localhost',  # MySQL服务器地址
    port=3306,  # MySQL服务器端口号
    user='root',  # 用户名
    password='111111',  # 密码
    database='pythonprogramming',  # 数据库名称
    charset='utf8mb4'  # 字符集
)

# 执行SQL语句
try:
    with conn.cursor() as cursor:
        # 创建表格
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS scores (
                id INT(11) NOT NULL AUTO_INCREMENT,
                name VARCHAR(20) NOT NULL,
                subject VARCHAR(20) NOT NULL,
                score INT(11) NOT NULL,
                PRIMARY KEY (name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        cursor.execute(create_table_sql)

        # 插入数据
        insert_sql = '''
            INSERT IGNORE INTO scores (name, subject, score) VALUES
                ('张三', '语文', 90),
                ('李四', '数学', 85),
                ('王五', '英语', 95)
        '''
        cursor.execute(insert_sql)

        # 查询数据
        query_sql = "SELECT * FROM scores"
        cursor.execute(query_sql)
        result = cursor.fetchall()

        for row in result:
            print(row)

    conn.commit()

except Exception as e:
    print(f"发生错误：{e}")
    conn.rollback()

finally:
    # 关闭连接
    conn.close()
