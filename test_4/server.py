import socket
import threading
import mysql.connector
from mysql.connector import Error
import pandas as pd


class Server:
    def __init__(self, host, port, backlog):
        self.host = host
        self.port = port
        self.backlog = backlog

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.backlog)

        self.database_connection = mysql.connector.connect(
            host='localhost',
            database='pythonprogramming',
            user='root',
            password='111111'
        )

        self.start()

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def handle_client(self, client_socket, address):
        print(f"Connected by {address}")

        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break

            if data.endswith('.xlsx') or data.endswith('.xls'):
                count = self.process_file(client_socket, data)
                client_socket.send(str(count).encode('utf-8'))
            else:
                response = data.upper()
                client_socket.send(response.encode('utf-8'))

        client_socket.close()

    import pandas as pd

    def process_file(self, client_socket, file_path):
        cursor = self.database_connection.cursor()

        try:
            # 读取 Excel 文件并将数据存储到数据库中
            # 这里是示例代码，请根据你的实际情况进行修改
            data = pd.read_excel(file_path)
            for row in data.itertuples(index=False):
                try:
                    cursor.execute("INSERT IGNORE INTO records (name, age, gender, scores) VALUES (%s, %s, %s, %s)",
                                   (row[0], int(row[1]), row[2], int(row[3])))
                except IndexError:
                    print("Invalid row:", row)
                    continue

            self.database_connection.commit()

            # 统计记录数并返回
            cursor.execute("SELECT COUNT(*) FROM records")
            count = cursor.fetchone()[0]

            return count

        except Error as e:
            print(f"Error: {e}")

        finally:
            cursor.close()


if __name__ == '__main__':
    server = Server('127.0.0.1', 8000, 5)
