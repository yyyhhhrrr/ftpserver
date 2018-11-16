#!/usr/bin/env python
# coding:utf-8
# Author:Yang

import sys
from conf import setting
from core import main
BASE_DIR=setting.BASE_DIR

sys.path.append(BASE_DIR)

if __name__=='__main__':
    main.run()

