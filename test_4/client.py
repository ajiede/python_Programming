import os
import tkinter as tk
from tkinter import filedialog, messagebox
import socket


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x300")
        self.root.title("Client")

        self.input_label = tk.Label(self.root, text="输入内容:")
        self.input_label.pack()

        self.input_text = tk.Entry(self.root)
        self.input_text.pack()

        self.send_button = tk.Button(self.root, text="发送", command=self.send_message)
        self.send_button.pack()

        self.result_label = tk.Label(self.root, text="服务器响应:")
        self.result_label.pack()

        self.result_text = tk.Text(self.root, height=5)
        self.result_text.pack()

        self.upload_button = tk.Button(self.root, text="上传文件", command=self.upload_file)
        self.upload_button.pack()

        self.file_label = tk.Label(self.root, text="数据条数:")
        self.file_label.pack()

        self.file_text = tk.Text(self.root, height=5)
        self.file_text.pack()

        self.server_host = '127.0.0.1'
        self.server_port = 8000

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        self.root.mainloop()

    def send_message(self):
        message = self.input_text.get()
        self.client_socket.send(message.encode('utf-8'))
        self.input_text.delete(0, 'end')  # 清除输入框内容

        response = self.client_socket.recv(1024).decode('utf-8')
        self.result_text.insert(tk.END, response + '\n')

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if os.path.splitext(file_path)[1] not in ['.xlsx', '.xlsm', '.xls']:
            # 如果选择的不是Excel文件，弹出提示框并退出函数
            messagebox.showwarning('Warning', '请选择Excel文件')
            return

        self.client_socket.send(file_path.encode('utf-8'))

        count = self.client_socket.recv(1024).decode('utf-8')
        self.file_text.insert(tk.END, '数据条数: ' + count + '\n')


if __name__ == '__main__':
    client_gui = ClientGUI()
