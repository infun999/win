#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/8 7:08
# ===========================

import re
from collections import Iterable
from win.orm_database import DB, ORM_MAPPINGS


class IntegerField(dict):
    """定义对应数据表的字段"""
    def __init__(self, field_name, field_define):
        dict.__init__(self, {field_name: field_define})


class PrimaryField(list):
    """定义对应数据表的primary key"""
    def __init__(self, *args):
        ret = [arg for arg in args]
        list.__init__(self, ret)

# done
class MetaMapping(type):
    """
        1. 分配内存空间
        2. 将类名保存为__table__类属性； 将IntegerField类型的类属性,构造映射字典保存为__mappings__类属性
        3. type.__new__() 返回修改后的类
        类名 + 类属性 则映射了 一张数据表
        即： 类对象 映射 数据表
    """
    def __new__(mcs, name, bases, attrs):
        mappings = dict()
        primary_key = list()
        # 指定类型的对象，用来生成数据表的字段，并转换为私有属性形式
        # 其余类型保持不变
        for k, v in attrs.items():
            # 类属性中 IntegerField 类型 为定义表结构
            if isinstance(v, IntegerField):
                mappings[k] = v
            # 类属性中 PrimaryField 类型 为定义表主键
            if isinstance(v, PrimaryField):
                primary_key = v

        # 删除已经保存在mappings中的"类属性"
        for k in mappings.keys():
            attrs.pop(k)

        attrs["__mappings__"] = mappings
        attrs["__table__"] = name
        attrs["__primary_key__"] = primary_key
        obj = type.__new__(mcs, name, bases, attrs)

        # 保存对象名 和 指针 的映射
        ORM_MAPPINGS[name.lower()] = obj
        return obj

# done
class InstanceMapping(object, metaclass=MetaMapping):
    """
        1. 用 __init__(self, **kwargs) 接收 键值对参数（每一对，都是对应数据表的：字段--值）
        2. 将所有的键值对参数 保存为 实例属性
        全部实例属性 则映射了 表中一条数据
        即：实例对象 映射 一条数据
    """
    def __init__(self, *args, **kwargs):
        """
        :param kwargs:
        """
        for name, value in kwargs.items():
            setattr(self, name, value)
        if args:
            setattr(self, '_args', args)

    def _class_property_name_mapping_db_table_field_name(self):
        """
        如果定义
        class Test(metaclass=***):
            uid = IntegerField('unit_id', 'int unsigned')
            name = IntegerField('username', 'varchar(30)')
            pk = PrimaryField('uid','names')

        则
        Test()._class_property_name_mapping_db_table_field_name()
        其返回值为:
        {
            "uid": 'unit_id',
            "name": 'username',
            "age": 'age',
        }
        """
        ret = dict()
        for usr_view, database_view in self.__mappings__.items():
            k = usr_view
            v = list(database_view.keys())[0]
            ret[k] = v
        return ret


# save/create_table [done];
# get()方法通用性,是否必要?是否增加del table方法? 2020/10/10
class ORMModel(InstanceMapping):
    """
    利用ORM和sql语句，实现对'对象'操作映射为 对'表/数据'的操作
    定义所有表的通用方法
    其他:本项目默认全部使用dict cursor
    """
    db = DB

    @staticmethod
    def dynamic_create_subclass(name, superclass):
        """
        动态创建对象
        :param name: Iterable
        :param superclass:
        :return:
        """
        # type对象 创建类
        subclass = type(name, (superclass,), dict())
        return subclass

    @staticmethod
    def exist_table(expect_name):
        """如果表不存在则创建表，如果存在则"""
        exist_table = ORMModel.db.show_table()
        if expect_name in exist_table:
            print('Table "{}" already exist in:\n'.format(expect_name),exist_table)
            return True
        else:
            return False

    def create_table_with_orm(self, name):
        """
        基本ORM对象创建表方法
        :param name:
        :return:
        """

        table_field = dict()
        # 遍历映射关系表
        for kwarg_k, column_define in self.__mappings__.items():
            # 提取表的 字段名 和 字段定义,用于创建表
            table_field.update(column_define)

        # self.__user_args(对象属性) 映射 表的关键字设置
        pk = ','.join([arg for arg in self.__primary_key__])
        # 调用数据库基本创建表方法
        ORMModel.db.create_table(table_name=name, table_field=table_field, primary_key=pk)
        return True

    def dynamic_create_table(self, name, model_table):
        """
        动态创建表
        :param name:
        :param model_table: 用于创建动态表的基本模板(即动态表仅名称不一样)
        :return:
        """
        # 如果存在表则跳过创建
        if self.exist_table(name):
            return
        # 动态创建子类 ORM 对象
        subclass = self.dynamic_create_subclass(name=name, superclass=model_table)
        # 调用子类对象中方法,创建映射的表
        subclass.create_table_with_orm(self, name)

    def create_table(self):
        """
        默认创建self对象映射的表
        :return:
        """
        if not self.exist_table(self.__table__.lower()):
            return self.create_table_with_orm(self.__table__)

    def _replace_key_of_instance_init_kwargs_with_mapping_db_filed_name(self):
        """
        __init__实例化对象时,其键值对方式传入的参数,会保存在实例属性中,对照__mappings__属性(即实例映射的数据表字段)
        将实例键值对参数,映射为表字段和字段值关系,用字典保存并返回
        如果定义
        class Test(metaclass=***):
            uid = IntegerField('unit_id', 'int unsigned')
            name = IntegerField('username', 'varchar(30)')
            pk = PrimaryField('uid','names')

        则
        Test(uid=1, name='inf', age=18)._replace_key_of_instance_init_kwargs_with_mapping_db_filed_name()
        其返回值为:
        {
            "unit_id": 1,
            "username": 'inf',
            "age": 18,
        }
        :return:
        """
        ret = dict()
        for usr_view, database_view in self.__mappings__.items():
            try:
                v = self.__getattribute__(usr_view)
                k = list(database_view.keys())[0]
                ret[k] = v
            except Exception:
                continue
        return ret

    def save(self):
        """
        保存单条数据
        :return:
        """
        # 将实例关键字参数,构造为 映射表(filed和value的对)的字典
        insert_kv = self._replace_key_of_instance_init_kwargs_with_mapping_db_filed_name()
        # 调用数据库插入数据方法保存
        ORMModel.db.insert_update(table=self.__table__, item=insert_kv,)

    def save_all(self,):
        """一次保存多条数据
            类对象传入固定位置参数2个列表,
            第1个: obj 中参数名
            第2个: 可迭代2维列表或2维元组
            eg:  Test(['name','age','gender'],[['inf',18,'f'],['mol','19','m'],['el','1','f']]).save_all()
        """
        # 查询对象obj name和表filed name对应关系
        obj_2_field = self. _class_property_name_mapping_db_table_field_name()

        # 获取init 中元组参数*args,有且仅有2个,且都可迭代
        if len(self._args) == 2 and isinstance((self._args[0], self._args[1]), Iterable):

            # 由映射关系, 将用户传入参数列表 转换为数据表字段名列表
            field_name = list()
            for usr_name in self._args[0]:
                field_name.append(obj_2_field[usr_name])

            # 逐条获取并保存插入值
            field_num = len(self._args[0])
            for data_row in self._args[1]:
                if len(data_row) == field_num:
                    # 构造一行数据的字典,并保存
                    _ = dict()
                    # 按顺序从两个列表(列表1: field_name; 列表2: 一条数据)取值构建字典
                    for i in range(field_num):
                        _[field_name[i]] = data_row[i]

                    ORMModel.db.insert_update(table=self.__table__, item=_, )

    def get_uid(self, *args, **kwargs):
        """用于单主键表的,又用主键查询出唯一结果的
            前提条件:
            1\ 多字段主键的不能用此方法
            2\ 用类对象定义的时候,应定义PrimaryField

            写了3种调用方法,1\在实例方法中位置参数;  2\ 实例方法中关键字参数   3\ 实例初始化时传参,实例方法不带参数
        """
        primary_key = ','.join([i for i in self.__primary_key__])      # 元类中设置的 类属性
        try:
            # 如果在实例方法中传入唯一关键字参数,且是k是数据表的primary key
            if len(kwargs) == 1:
                if primary_key == list(kwargs.keys())[0]:
                    data = ORMModel.db.fetch_by_uid(table=self.__table__, kv={primary_key: list(kwargs.values())[0]})
                    return data[0]

            # 如果在实例方法中传入唯一参数
            elif len(args) == 1:
                data = ORMModel.db.fetch_by_uid(table=self.__table__, kv={primary_key: args[0]})
                return data[0]

            # 实例初始化时,有且仅有一个  init的位置参数
            elif len(self._args) == 1:
                search_value = self._args[0]               # 实例化时设置的 实例属性
                data = ORMModel.db.fetch_by_uid(table=self.__table__, kv={primary_key: search_value})
                return data[0]
        except Exception:
            raise Exception('输入或调用不合法.  方法仅可用于单主键表的,且用主键查询出唯一结果的情况.')

    # ? 可用,但是风格不统一,不使用实例方法而改写成实例init参数调用?
    def get_by_kvs(self):
        """
        用于多限制条件查询
        like *orm_instance.get_by_kvs(class='2', age='>=18', score='<60')
        查询class=2,age>=18,score<60,
        此处的class,age,score都是对象中的属性,并非数据表的field字段名
        """
        search_kvs = self._replace_key_of_instance_init_kwargs_with_mapping_db_filed_name()
        return ORMModel.db.fetch_by_kvs(table=self.__table__, kvs=search_kvs)

