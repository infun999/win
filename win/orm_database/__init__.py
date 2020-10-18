#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 19:09
# ===========================

# 加载代码后新创建的对象保存在ORM_MAPPINGS中
import re
from .base_orm import ORMModel, IntegerField, PrimaryField
from .database import UserDB
from win import config

# 保存（表名---对象）映射关系
ORM_MAPPINGS = dict()

# 连接数据库，并创建数据库对象
DB = UserDB(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            db=config.DB_BASENAME,
            )