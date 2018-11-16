#!/usr/bin/env python
# coding:utf-8
# Author:Yang

import socketserver
import json
import os
import hashlib
from conf import setting

class MyTCPHandler(socketserver.BaseRequestHandler):

    def authenticat(self,*args):
        '''服务端登录验证'''
        user_dic =args[0]
        username =user_dic['username']
        password =user_dic['password']
        try:
            with open(setting.BASE_DIR+"/data/%s.txt"%username,"r") as f:
              data=json.loads(f.read())

            f.close()
            user_dir=data['user_dir']
            if data['username'] == username:
                if data['password'] == password:                                  
                    self.request.send(b"login success")
                    return True,user_dir
                else:
                    self.request.send(b"error password")
                    print("username:%s login failed:error password"%username)
                    return False,None
        except FileNotFoundError as e:
            print("error username:",username)
            self.request.send(b"error username")
            return False,None


    def ls(self,*args):
        ''' 查看当前目录下文件'''
        cmd_dic=args[0]
        user_dir=cmd_dic["user_dir"]
        print(user_dir)
        msg = os.popen("ls "+user_dir).read()
        self.request.send(msg.encode())
        return user_dir

    def pwd(self,*args):
        '''查看当前位置'''
        cmd_dic=args[0]
        user_dir=cmd_dic["user_dir"]
        msg = os.popen("cd "+user_dir+";pwd").read()
        self.request.send(msg.encode())
        print(user_dir)
        return user_dir

    def cd(self,*args):
        '''cd'''
        cmd_dic=args[0]
        user_dir=cmd_dic["user_dir"]
        cd_dir=cmd_dic["cd_dir"]
        user_dir=user_dir+"/"+cd_dir
        msg="the current dir is %s"%user_dir
        print(user_dir)
        self.request.send(msg.encode())
        return user_dir

    def cd_back(self,*args):
        '''cd ..'''
        cmd_dic=args[0]
        username=args[1]
        user_dir=cmd_dic["user_dir"]
        if user_dir == "/root/ftpserver/ftp_server/%s"%username:
            msg="this is already in home"
            print(msg)
            self.request.send(msg.encode())
        else:
            list=user_dir.split("/")
            list.remove(list[len(list)-1])
            user_dir="/".join(list)
            msg="the current dir is %s"%user_dir
            print(user_dir)
            self.request.send(msg.encode())
        return user_dir




    def get(self,*args):
        '''发送文件到客户端'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        user_dir = cmd_dic["user_dir"]
        if os.path.isfile(user_dir+"/"+filename):
            filesize=os.stat(user_dir+"/"+filename).st_size
            self.request.send(str(filesize).encode())
            client_response=self.request.recv(1024) # 服务端收到客户端准备传输的信号
            f=open(user_dir+"/"+filename,"rb")
            m=hashlib.md5()
            for line in f:
                self.request.send(line)
                m.update(line)
            else:
                print("file put success...")
            f.close()
            file_md5=m.hexdigest()
            self.request.send(file_md5.encode())


        else:
            message="filename:[%s] is not exist.."%filename
            print(message)
            self.request.send(b"FileNotFound")

        return user_dir


    def put(self,*args):
        ''' 接受客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["size"]
        user_dir = cmd_dic["user_dir"]
        print(user_dir+"/"+filename)
        if os.path.isfile(user_dir+"/"+filename):# 文件存在时
            f = open(user_dir+"/"+filename+".new","wb")
        else: # 文件不存在时
            f = open(user_dir+"/"+filename,"wb")
        self.request.send(b"200 ok")
        received_size=0
        m=hashlib.md5()
        while received_size < filesize:
            if filesize-received_size >1024: # 解决黏包
                size=1024
            else:
                size=filesize-received_size
            data = self.request.recv(size)
            m.update(data)
            f.write(data)
            received_size+=len(data) # 因为data本来就是byte len（data）就可以直接获取data大小（字节数）
        else:
            print("filename: [%s] has uploaded..."%filename)
        f.close()
        file_md5 = m.hexdigest()
        file_client_md5 = self.request.recv(1024).decode()

        if file_md5 == file_client_md5:
            print("server file's md5 is the same as client file's md5:uploading success!!")
        else:
            print("md5 is different with client file's md5:uploading failed...")
        return user_dir




    def handle(self):
        '''handler处理类'''


        self.user_dic=self.request.recv(1024).strip().decode()
        try:
            user_data=json.loads(self.user_dic)
        except Exception as e:
            pass
        login_signal,user_dir=self.authenticat(user_data)
        if login_signal:
            while True:
                self.data=self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
                cmd_dic = json.loads(self.data.decode())
                cmd_dic['user_dir']=user_dir
                action = cmd_dic["action"]
                if hasattr(self,action):
                     if action !="cd_back":
                         func = getattr(self,action)
                         user_dir=func(cmd_dic)
                     else:
                         func =getattr(self,action)
                         user_dir=func(cmd_dic,user_data['username'])


def run():
    HOST,PORT="172.16.95.131",9999
    server = socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()