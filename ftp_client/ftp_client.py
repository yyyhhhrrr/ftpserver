#!/usr/bin/env python
# coding:utf-8
# Author:Yang

import socket
import os
import json
import hashlib
import sys

class FtpClient(object):
    def __init__(self):
        '''客户端实例'''

        self.client = socket.socket()
    def help(self):
        ''' 查看帮助'''

        msg = '''
        ls
        pwd
        cd ../..
        get filename
        put filename
        '''
    def connect(self,ip,port):
        '''建立socket连接'''

        self.client.connect((ip,port))

    def authenticat(self):
        '''登录功能'''
        username=input("please input your username:")
        password=input("please input your password:")
        msg_dic={
            "username":username,
            "password":password
        }
        self.client.send(json.dumps(msg_dic).encode())
    def interactive(self):
        '''交互功能'''

        self.authenticat() # 登录
        server_response=self.client.recv(1024).decode()
        if server_response == "login success":
            while True:
                cmd = input(">>:")
                if len(cmd) == 0:continue
                cmd_str = cmd.split()[0] # split 后是一个列表形式
                if cmd=="cd ..":
                    func = getattr(self, "cmd_cd_back")
                    func(cmd)
                else:

                    if hasattr(self,"cmd_%s"%cmd_str): # 反射

                            func =getattr(self,"cmd_%s"%cmd_str)
                            func(cmd)
                    else:
                        self.help()


        else:
            print(server_response)
    def cmd_put(self,*args):
        '''上传文件到服务端功能'''


        cmd_split = args[0].split() # 获取输入的命令转换为列表形式
        if len(cmd_split) >1:
            filename = cmd_split[1]
            if os.path.isfile(filename): # 判断文件是否存在
                filesize = os.stat(filename).st_size # 文件大小
                msg_dic ={
                    "action":"put",
                    "filename":filename,
                    "size":filesize,
                    "overridden":True
                }
                self.client.send(json.dumps(msg_dic).encode()) # 字典转json 再转byte
                # 防止黏包，等服务器确认
                server_response = self.client.recv(1024)
                # 可以写标准请求码
                # .....
                f = open(filename,"rb")
                m = hashlib.md5()
                persent=0
                for line in f:
                    m.update(line)
                    self.client.send(line)
                    send_size=len(line)
                    cur_percent = int(float(send_size) / filesize * 100)
                    if cur_percent > persent:
                        persent = cur_percent
                        self.show_progress(filesize, send_size, persent)

                else:    # for/else 当for执行完毕走else,如果for break了就不走else
                    print("file put success...")
                    file_md5=m.hexdigest()
                    # print(file_md5)
                    self.client.send(file_md5.encode())
                    f.close()
            else:
                print(filename,"is not exist")
        else:
            print("put need 1 argument at least such as filename")
    def cmd_get(self,*args):
        '''下载服务端文件功能'''


        cmd_split = args[0].split()
        if len(cmd_split)>1:
            filename = cmd_split[1]
            msg_dic={
                "action":"get",
                "filename":filename,
                "overridden":True
            }
            self.client.send(json.dumps(msg_dic).encode())
            server_response=self.client.recv(1024)
            if server_response != b"FileNotFound":
                if os.path.isfile(filename):
                    f = open(filename + ".new", "wb")
                else:
                    f = open(filename, "wb")
                m=hashlib.md5()
                self.client.send(b"200 OK") # 客户端发送可以传输信号给服务端
                filesize=int(server_response.decode())
                reseived_size=0
                persent=0
                while reseived_size<filesize:
                    if filesize-reseived_size>1024:
                        size=1024
                    else:
                        size=filesize-reseived_size
                    data=self.client.recv(size)
                    f.write(data)
                    m.update(data)
                    reseived_size+=len(data)
                    cur_percent = int(float(reseived_size)/filesize *100)
                    if cur_percent > persent:
                        persent=cur_percent
                        self.show_progress(filesize,reseived_size,persent)

                else:
                    print("file [%s] has uloaded..."%filename)
                f.close()
                file_md5=m.hexdigest()
                server_file_md5=self.client.recv(1024).decode()
                if file_md5 == server_file_md5:
                    print("server file's md5 is the same as server file's md5:uploading success!!")
                else:
                    print("md5 is different with client file's md5:uploading failed..")
            else:
                print("file [%s] is not exist in server"%filename)
        else:
            print("get need 1 argument at least such as filename")

    def cmd_ls(self,*args):
        msg_dic={
            "action":"ls"

        }
        self.client.send(json.dumps(msg_dic).encode())
        server_response=self.client.recv(1024).decode()
        print(server_response)
    def cmd_pwd(self,*args):
        msg_dic={
            "action":"pwd"
        }
        self.client.send(json.dumps(msg_dic).encode())
        server_response=self.client.recv(1024).decode()
        print(server_response)

    def cmd_cd(self,*args):
        cmd_split=args[0].split()
        cd_dir=cmd_split[1]
        msg_dic={
            "action":"cd",
            "cd_dir":cd_dir
        }
        self.client.send(json.dumps(msg_dic).encode())
        server_response = self.client.recv(1024).decode()
        print(server_response)
    def cmd_cd_back(self,*args):
        msg_dic={
            "action":"cd_back"
        }
        self.client.send(json.dumps(msg_dic).encode())
        server_response = self.client.recv(1024).decode()
        print(server_response)

    def show_progress(self,total, finished, percent):
        '''进度条'''
        progress_mark = "=" * int(percent / 2)
        print("[%s/%s]%s>%s%s\r" % (total, finished, progress_mark, percent, "%"))
        sys.stdout.flush()
        if percent == 100:
            print('\n')

ftp =FtpClient()
ftp.connect("172.16.95.131",9999)
ftp.interactive()


