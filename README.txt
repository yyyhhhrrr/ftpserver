基于socket的多用户在线的轻量级ftp server:
功能：1.用户加密认证
      2.允许多用户同时登陆
      3.每个用户都有自己的家目录，且只能访问家目录（权限控制）
      4.允许用户在ftp server 上切换目录
      6.允许用户查看当前下目录的文件
      7.支持上传、下载，保证文件一致性
      8.文件传输过程显示进度条

|-- ftpserver 轻量级ftp server
    |-- ftp_client  ftp客户端（windows 或linux）
        |-- a.txt
        |-- b.txt
        |-- ftp_client.py ftp 主程序
        |-- show_process.py 显示进度条的功能类
        |-- test.py
        |-- __init__.py
    |-- ftp_server ftp 服务端（linux）
        |-- __init__.py
        |-- bin
        |   |-- ftp_server.py  启动程序
        |   |-- __init__.py
        |-- conf
        |   |-- setting.py  配置文件
        |   |-- __init__.py
        |   |-- __pycache__
        |   |   |-- setting.cpython-37.pyc
        |   |   |-- __init__.cpython-37.pyc
        |-- core  核心功能
        |   |-- b.txt
        |   |-- main.py  程序主入口
        |   |-- __init__.py
        |   |-- __pycache__
        |   |   |-- main.cpython-37.pyc
        |   |   |-- __init__.cpython-37.pyc
        |-- data
        |   |-- create_data.py  生成用户json数据
        |   |-- yang.txt  用户json数据
        |   |-- yhr123.txt
        |-- log
        |   |-- __init__.py
        |-- yang  用户家目录
        |   |-- a.txt.new
        |   |-- b.txt
        |   |-- b.txt.new
        |   |-- a
        |   |   |-- 1.txt
        |   |-- b
        |   |   |-- 2.txt
        |-- yhr123 用户家目录
        |   |-- 3.txt
        |   |-- __init__.py
        |   |-- a
        |   |   |-- 1.txt
        |   |-- b
        |   |   |-- 2.txt
