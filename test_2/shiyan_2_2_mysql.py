import os
import pandas as pd
import pymysql

# 读取Excel文件
excel_file = "students_scores.xlsx"  # 读取文件
df = pd.read_excel(excel_file, sheet_name=None)  # None未指明哪张表名

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
        # 查询数据
        while 1:
            name = input("请输入你要查询人的姓名(输入0结束)：")
            if name == "0":
                break
            query_sql = "SELECT * FROM students WHERE name = %s"
            cursor.execute(query_sql, name)
            result = cursor.fetchall()

            for data in result:
                print(data)

            # 将需要比较的数据存储在一个列表中
            data_to_compare = {data[1], data[2], data[3], data[4]}

            # 遍历每个sheet表
            for sheet_name, xls in df.items():
                # 遍历需要比较的数据
                if data[1] in xls.values and data[2] in xls.values \
                        and data[3] in xls.values and data[4] in xls.values:
                    print(f"{name} 存在这张表： {sheet_name}")
                    print(data)
                    break

        selectAll_sql = "SELECT * FROM students"
        cursor.execute(selectAll_sql)
        result = cursor.fetchall()
        df_list = []
        for data in result:
            print(data)
            # 将所有数据存储在一个DataFrame列表中
            df_temp = pd.DataFrame(data).transpose()
            df_list.append(df_temp)
            # 将数据转换成 DataFrame 格式
        df_to_write = pd.DataFrame(result, columns=['id', 'name', 'gender', 'age', 'score'])

        # 将数据追加到现有的Excel文件中
        # Excel文件路径
        filename = 'new_student_scores.xlsx'
        if os.path.exists(filename):
            with pd.ExcelWriter(filename, mode='a', if_sheet_exists='new', engine='openpyxl') as writer:
                sheet_name = 'Sheet' + str(len(writer.book.sheetnames) + 1)
                pd.concat(df_list).to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        else:
            # 如果文件不存在，则创建新文件并写入数据
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                pd.concat(df_list).to_excel(writer, sheet_name='Sheet1', index=False, header=False)
    # conn.commit()

except Exception as e:
    print(f"发生错误：{e}")
    conn.rollback()

finally:
    # 关闭连接
    cursor.close()
    conn.close()
