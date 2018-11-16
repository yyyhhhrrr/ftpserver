#!/usr/bin/env python
# coding:utf-8
# Author:Yang

import json
from conf import setting

user_data={
    "username":"yhr123",
    "password":"960314",
    "user_dir":setting.BASE_DIR+"/yhr123"
}

with open("yhr123.txt","w+") as f:
    f.write(json.dumps(user_data))

