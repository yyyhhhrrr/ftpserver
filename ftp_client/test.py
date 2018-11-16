#!/usr/bin/env python
# coding:utf-8
# Author:Yang

# path="/root/ftpserver/venv/bin/python"
# list=path.split("/")
# list.remove(list[len(list)-1])
# print("/".join(list))
import sys
def show_progress(total, finished, percent):
    progress_mark = "=" * int(percent / 2)
    print("[%s/%s]%s>%s%s\r" % (total, finished, progress_mark, percent,"%"))
    sys.stdout.flush()
    if percent == 100:
        print ('\n')


tatal=10000000
finished=0
percent=0
while not finished == tatal:
    finished +=1
    cur_percent=int(float(finished)/tatal *100)
    if cur_percent > percent:
        percent = cur_percent
        show_progress(tatal,finished,percent)
else:
    print("done")

