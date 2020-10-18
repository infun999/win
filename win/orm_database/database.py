#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 4:28
# ===========================


import re
from collections import Iterable
from pymysql import connect
from pymysql.cursors import DictCursor


# 装饰器
def item_filter(drop_item: dict, in_arg: str):
    """
    过滤装饰器（删除指定位置参数（字典参数） 中的特定值 所对应的键值对）
    :param drop_item: 元组形式保存的，要删除的值
    :param position: 要执行过滤的参数所在位置
    :return:
    """
    def set_func(func):
        def call_func(*args, **kwargs):
            # 如果没有显式的指定table_field 字典,则装饰器不做处理
            try:
                table_field = kwargs[in_arg]
            except KeyError:
                return func(*args, **kwargs)

            # 存在字段字典
            else:
                # 新字典保存不删除的键值对
                new_item = dict()
                # 删除指定中的键值对
                for k, v in table_field.items():
                    if v not in drop_item:
                        new_item[k] = v
                # 原kwargs参数的指定位置（数据表字段---插入值的字典），用新字典替换回来
                kwargs[in_arg] = new_item
            return func(*args, **kwargs)
        return call_func
    return set_func


# 装饰器
# def check_primary_key(in_arg):
#     """
#     验证是否指定primary key参数，
#     若已经指定primary key，且在定义表字段的字典的 key值中，则不处理
#     若未指定primary key, 提示可选的 表字段 key值，接收用户输入，传递参数。 无输入使用默认pk
#     :param position: 定义表字段的字典参数，在字典型参数中的index
#     :return:
#     """
#     def set_func(func):
#         def call_func(*args, **kwargs):
#             # 提取数据表全部字段定义的字典
#             try:
#                 field_define_dict = kwargs[in_arg]
#             except KeyError:
#                 raise
#             else:
#                 field_names = [field for field in field_define_dict.keys()]
#
#             pk_in_field_names = False
#             try:
#                 primary_keys = kwargs['primary_key']
#             except KeyError:
#                 pass
#             else:
#                 # 分割多主键情况,查询pk是否全部在表字段中
#                 primary_keys = primary_keys.split(',')
#                 primary_keys = [pk.strip() for pk in primary_keys]
#                 for pk in primary_keys:
#                     pk_in_field_names = True if pk in field_names else False
#                     # 存在主键不在表字段中情况
#                     if not pk_in_field_names:
#                         break
#
#             if not pk_in_field_names:
#                 print(field_names)
#                 while True:
#                     pk = input("""
#                                     从以上列表中选择字段作为primary key
#                                     或按 “回车键”，使用系统默认自增“auto_id”字段作为primary key
#                                 """)
#                     # 以关键字参数方式追加 primary_key【需和创建表方法中形参名一致2020/10/07】
#                     if pk in field_names:
#                         kwargs.update({'primary_key': pk})
#                         break
#                     # 未输入任何值情况， 选择使用默认值作为参数
#                     if pk == '':
#                         double_check = input('输入Y/y，确认使用默认值。 其他任意键返回选择')
#                         if double_check.lower() == 'y':
#                             break
#                         else:
#                             continue
#                     # 输入错误值
#                     else:
#                         print('Unknown input: {}'.format(pk))
#                         continue
#             return func(*args, **kwargs)
#         return call_func
#     return set_func


class DataBase:
    __instance = None
    __init_flag = False

    def __new__(cls, *args, **kwargs):

        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, host: str, port: int, user: str, password: str, database_name: str, charset: str = 'utf8', **kwargs):
        # 初始化服务端
        if not DataBase.__init_flag:
            self.client = connect(host=host, port=port, user=user, password=password, db=database_name, charset=charset, **kwargs)
            self.cursor = self.client.cursor()
            self.dict_cursor = self.client.cursor(cursor=DictCursor)
            DataBase.__init_flag = True

    def close(self):
        self.cursor.close()
        self.client.close()

    def create_table(self, table_name: str, table_field: dict, *args, user_sql: str = '',
                     primary_key: str = '', **kwargs):
        """
        子类调用时，关键字参数需显式的使用关键字传递参数方式
        :param table_name: 表的基本属性:表名
        :param table_field: 表的基本属性: 字段定义
        :param args: 预留位置参数
        :param user_sql: 关键字参数: 调用自定义限制条件,如创建时间,更新时间等参数,
        :param primary_key: 关键字参数: 主键; 如为空,则默认弹出选择项, 是否使用自增id列
        :param auto_pk_name: 关键字参数: 是否自动主键; 如不为空,则默认用此字段名作为自动主键,如为空,则使用("表名"+"_id")作为自动主键
        :param kwargs: 预留关键字参数
        :return:
        """
        field_define = []
        # 用实参字典table_field,构造mysql表的基本字段定义
        for k, v in table_field.items():
            _ = k + ' ' + v
            field_define.append(_)
        sql = [','.join(field_define), ]

        # 判断是否正确设置主键,否则设置默认自增字段作为Primary key
        # 查询主键设置数量  逐个判断是否全部在 表的field name中
        pk_list = primary_key.split(',')
        pk_list = [i.strip() for i in pk_list]
        pk_num = len(pk_list)

        # 设置主键,并且全部在 表字段中
        pk_in_field = False
        for pk in pk_list:
            if pk not in table_field.keys():
                pk_in_field = False
                break
            pk_in_field = True

            # 设置唯一主键,但不在field name中 , 则使用此主键作为 自增列的 field name
        if not pk_in_field and pk_num == 1 and pk_list[0]:
            sql.append('{} int not null auto_increment, primary key({})'.format(primary_key, primary_key))
        else:
            # 设置主键,且全部在 field name 中
            if pk_in_field:
                sql.append('primary key({})'.format(primary_key))
            # 未设置主键\设置错误多主键
            else:
                auto_pk_name = table_name.lower() + '_id'
                sql.append('{} int not null auto_increment, primary key({})'.format(auto_pk_name, auto_pk_name))
                print("""No effective user define primary-key !\n"{}" set automatic as primary key""".format(
                    auto_pk_name))

        # 添加其他用户自定义语句
        if user_sql:
            sql.append(user_sql)

        # 构造sql语句
        sql = ','.join(sql)
        sql = 'create table {}({})'.format(table_name, sql)
        print(sql)
        self.cursor.execute(sql)


    def show_table(self):
        """
        2020/10/07
        :return: 表名 列表
        """
        sql = "show tables"
        self.cursor.execute(sql)
        return [i[0] for i in self.cursor.fetchall()]

    def show_create_table(self, table: str):
        """查询表的创建的结构"""
        sql = "show create table {}".format(table)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        pass

    # def show_field(self, table: str):
    #     """
    #     返回指定表中的字段
    #     :param table:
    #     :return:
    #     """
    #     sql = "select * from {}".format(table) # sql语句问题
    #     self.cursor.execute(sql)
    #     return [i[0] for i in self.cursor.description]

    def insert_item(self, table: str, item: dict):
        # """insert, if 'duplicate-key-error' ignore insert action"""
        if not item:
            return
        keys, values = list(item.keys()), list(item.values())
        sql = "insert ignore into {} ({}) values({})".format(table, ','.join(keys), ','.join(['%s'] * len(keys)))
        self.cursor.execute(sql, values)
        self.client.commit()

    def insert_update(self, table: str, item: dict):
        # """insert, if duplicate-key-error then update  """
        if not item:
            return

        keys, values = list(item.keys()), list(item.values())
        upd_str = ','.join(['{}=values({}) '.format(k, k) for k in keys])
        sql = "insert into {} ({}) values({}) on duplicate key update {}".format(
            table, ','.join(keys), ','.join(['%s'] * len(keys)), upd_str)
        self.cursor.execute(sql, values)
        self.client.commit()

    # 此方法用时较少，本次未重构 2020/10/06
    # def update_item(self, table: str, loc_dict: dict, update_item: dict):
    #     # """update 'update_item'(dict) where located by 'loc_dict'"""
    #     if not update_item:
    #         return
    #     _ = [str(k)+"='"+str(v)+"'" for k, v in loc_dict.items()]
    #     loc_ = ' and '.join(_)
    #     _ = [str(k)+"='"+str(v)+"'" for k, v in update_item.items()]
    #     upd = ' , '.join(_)
    #     sql = "update {} set {} where {}".format(table, upd, loc_)
    #     self.cursor.execute(sql)
    #     self.client.commit()

    # 此方法本项目用时较少，本次未重构 2020/10/06
    # def fetch_range(self, table: str, key: str = None, low=None, high=None):
    #     # """
    #     # 默认获取全range
    #     # :param table: 数据表
    #     # :param key: 定位column
    #     # :param low: column取值下限
    #     # :param high: column取值上限
    #     # :return:
    #     # """
    #     if key and low and high:
    #         sql = 'select * from {} where {}>={} and {}<{}'.format(table, key, low, key, high)
    #     elif key and low:
    #         sql = 'select * from {} where {}>={}'.format(table, key, low,)
    #     elif key and high:
    #         sql = 'select * from {} where {}<{}'.format(table, key, high)
    #     else:
    #         sql = 'select * from {}'.format(table)
    #     self.cursor.execute(sql)
    #     return self.cursor.fetchall()

    def fetch_all(self, table: str, mode='tuple', user_restrict: str = ''):
        """

        :param table:
        :param user_restrict: sql查询限制语句（注入风险2020/10/07）
        :param mode: 选择游标返回类型 tuple/dict
        :return: like((1, 'inf', 18, 'female'), (2, 'molve', 19, 'male'), )
        """
        sql = 'select * from {}'.format(table)
        if user_restrict:
            sql = sql + ' {}'.format(user_restrict)
        if mode == 'dict':
            self.dict_cursor.execute(sql)
            return self.dict_cursor.fetchall()
        elif mode == 'tuple':
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    # 此方法用时较少，本次未重构 2020/10/06
    # def change_table_name(self, name_dict: dict):
    #     # """name_dict: key=old name      value=new name"""
    #     for k, v in name_dict.items():
    #         sql = 'ALTER TABLE {} RENAME TO {}'.format(k, v)
    #         self.cursor.execute(sql)

    def drop_table(self, tables):
        # """传入删除数据表的列表"""
        if isinstance(tables, Iterable):
            for table in tables:
                sql = "drop table {} ".format(table)
                self.cursor.execute(sql)
        else:
            raise Exception('not iterable')

    # 此方法用时较少，本次未重构 2020/10/06
    # def add_column(self, table: str, define_dict: dict):
    #     new_column = []
    #     for k, v in define_dict.items():
    #         if isinstance(v, str) and isinstance(k, str):
    #             k, v = str(k).lower(), str(v).lower()
    #             if 'char' in v or 'text' in v:
    #                 _ = k + ' ' + v + ' ' + 'default ""'
    #             elif 'int' in v or 'float' in v or 'double' in v:
    #                 _ = k + ' ' + v + ' ' + 'default 0'
    #             else:
    #                 _ = k + ' ' + v
    #             new_column.append(_)
    #     sql = "alter table {} add ({})".format(table, ','.join(new_column))
    #     self.cursor.execute(sql)


class UserDB(DataBase):
    """"""
    def __init__(self, host, port, user, password, db, charset='utf8'):
        super().__init__(host, port, user, password, db, charset)

    # @check_primary_key(in_arg='table_field')  # 2020/10/12 create_table全部采用关键字参数时,直接用key去查找,不用再指定field定义的参数位置
    def create_table(self, table_name: str, table_field: dict, primary_key: str = '',
                     create_ts=False, update_ts=False, num_default=None, str_default=None):
        """
        创建数据表,比父类基本方法,增加创建\修改\默认数值\默认字符串的功能
        :param table_name:
        :param table_field: 字段
        :param primary_key: 主键
        :param create_ts: 创建数据时间,项目默认不设置
        :param update_ts: 修改数据时间,项目默认不设置
        :param num_default: 设置数字类型字段默认值
        :param str_default: 设置字符类型字段默认值
        :return:
        """
        # 检查是否存在同名表
        exist_table = super().show_table()
        if table_name in exist_table:
            print('Table "{}" exist. Fail to create table.'.format(table_name))
            return

        # 统一设置字符串和数字类型字段的默认0p.值，默认不设置
        for k, v in table_field.items():
            if str_default and re.match(r'(\w*char|text|binary|blob|enum|set)', v, re.I):
                table_field[k] = v + ' ' + 'default {}'.format(str_default)
            if num_default and re.match(r'(\w*int|float|double|decimal)', v, re.I):
                table_field[k] = v + ' ' + 'default {}'.format(num_default)

        user_sql = list()
        # 设置创建时间字段
        if create_ts:
            user_sql.append('crt_ts datetime DEFAULT CURRENT_TIMESTAMP')
        # 设置修改时间字段
        if update_ts:
            # usersql.append('upd_ts datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
            user_sql.append('upd_ts datetime')  # mysql 5.7以下版本
        user_sql = ','.join(user_sql)

        # 创建数据表
        super().create_table(table_name, table_field, user_sql=user_sql, primary_key=primary_key,)
        return

    def insert_item(self, table: str, item: dict):
        super().insert_item(table, item)

    @item_filter(drop_item=(0, ''), in_arg='item')    # 删除第3个位置参数（字典）中的值在(0, '')中的 键值对
    def insert_update(self, table: str, item: dict):
        # 过滤特定值的字段
        super().insert_update(table, item)

    # 以下定义常用查询方法

    # 多限制条件查询
    def fetch_by_kvs(self, table: str, mode='dict', kvs=None):
        """
        kvs写法eg: {"objname":'inf', "objage": '=18', "objscore": '>=60'}  在value中不写运算符默认为'='
        :param table:
        :param mode:
        :param kvs: 用户定义的字典格式的 键值对 限制查询条件
        :return:
        """
        # 用kvs字典键值对构造查询条件
        if isinstance(kvs, dict):
            user_restrict_str = list()
            for k, v in kvs.items():

                try:
                    iegal_value = re.findall(r'^(=|>|<|!=|>=|<=|)(\w+)', str(v))[0]
                except IndexError:
                    # 输入不是 (值) 或 (判断逻辑符号 值)的形式
                    print(""" "{}" is NOT a iegal restrict, ignored! """.format(v))
                    continue
                else:
                    # 用户在字典的v中指定限制方式:=|>|<|!=|>=|<=|
                    if iegal_value[0]:
                        user_restrict_str.append('''{}{}"{}"'''.format(k, iegal_value[0], iegal_value[1]))
                    # 如果查询条件中不以(=|>|<|!=|>=|<=|)开头,或限制符其后无 值,则默认采取"="方式
                    else:
                        user_restrict_str.append('''{}="{}"'''.format(k, v))

            user_restrict_str = 'where ' + ' and '.join(user_restrict_str)
            fetch_ret = super().fetch_all(table, mode, user_restrict_str)
        else:
            fetch_ret = super().fetch_all(table, mode)

        # dict_cursor获取的转json格式，默认cursor返回元组格式
        if mode == 'dict':
            fetch_ret = dict(enumerate(fetch_ret, start=0))
        elif mode == 'tuple':
            pass

        return fetch_ret

    # 单主键查询
    def fetch_by_uid(self, table: str, mode='dict', kv=None):
        """
        单主键查询方法
        :param table:
        :param mode:
        :param kv:
        :return: 只返回一条结果的单主键查询
        """
        if isinstance(kv, dict) and len(kv) == 1:
            user_restrict_str = ''
            for k, v in kv.items():
                user_restrict_str = 'where {}={}'.format(k, v)
            ret = super().fetch_all(table, mode=mode, user_restrict=user_restrict_str)
            ret = ret if len(ret) == 1 else None    # 限制单主键查询出来的单条结果
            return ret
        else:
            return None


# 接口


if __name__ == "__main__":
    pass
    # table_c = {
    #     'id': 'int',
    #     'name': 'varchar(30)',
    #     'age': 'tinyint',
    # }
    # table_i1 = {
    #     'name': 'inf',
    #     'age': 18,
    # }
    # table_i2 = {
    #     'name': 'inf',
    #     'age': '0',
    # }
    # table_i3 = {
    #     'name': 'inf',
    #     'age': 0,
    # }
    # u = UserDB(config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PASSWORD, config.DB_BASENAME,)
    #
    # # u.create_table('user', table_c, 'id')
    # # u.create_table('user1', table_c, 'id')
    # # tb_name = 'user4'
    # # if tb_name not in u.show_table():
    # #     u.create_table(tb_name, table_c, )
    # # ret = u.show_item('user6')
    # # print(ret, type(ret))
    # ret = u.show_create_table('test')
    # print(ret)