import openpyxl  # 打开Excel文件并读取数据
import json
import pickle
import os
# 链接数据库
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 打开Excel文件并读取数据
wb = openpyxl.load_workbook('学生成绩.xlsx')
ws1 = wb['Sheet1']
ws2 = wb['Sheet2']
# 读取更多的Sheet...

# 连接到数据库并将数据写入表格
engine = create_engine('sqlite:///学生成绩.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Score(Base):
    _tablename_ = 'scores'

    id = Column(Integer, primary_key=True)
    # 定义更多的字段...


for row in ws1.iter_rows(min_row=2):
    s = Score()
    s.field1 = row[0].value
    s.field2 = row[1].value
    # 读取更多的字段...
    session.add(s)

session.commit()

# 将数据保存为二进制文件
with open('学生成绩.bin', 'wb') as f:
    pickle.dump([ws1.values, ws2.values], f)

# 将数据保存为JSON文件
with open('学生成绩.json', 'w') as f:
    json.dump([ws1.values, ws2.values], f)

# 比较文件大小
excel_size = os.path.getsize('学生成绩.xlsx')
bin_size = os.path.getsize('学生成绩.bin')
json_size = os.path.getsize('学生成绩.json')

print('Excel文件大小:', excel_size)
print('二进制文件大小:', bin_size)
print('JSON文件大小:', json_size)
