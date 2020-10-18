#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 18:46
# ===========================

import re
from win.orm_database.base_orm import IntegerField, PrimaryField, ORMModel, database
from win.orm_database import ORM_MAPPINGS
from win import config


"""
修改项目结构：
1、一个py文件专门配置ORM 对象
2、配置文件中写，哪些表用1中的对象动态或静态生成
3、项目初始化文件__init__，读取config.py中配置，读取数据库表名
    如配置新表，则创建新表（自动会在win.orm_database.base_orm.ORM_MAPPINGS中保存name和对象的映射）
    其他存在的表，根据配置中name和动态生成对象，并在上述ORM_MAPPINGS中保存映射关系
    接口在common中的ORM_MAPPINGS
4、 market.py和usermanager.py 直接从common中获取对象进行操作

5、其他：新表需求时，修改配置，
"""