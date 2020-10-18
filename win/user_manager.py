#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 6:43
# ===========================
"""
用户决策和账户
"""
# from win.common import IntegerField, PrimaryField, ORMModel
# from win import common

# frame 2020/10/10
class AccountModel(ORMModel):
    """
    账户表模板, 实际账户继承模板，type动态创建
    """
    # code = IntegerField(code='int unsigned')  # 代码
    # name = IntegerField(name='varchar(10)')  # 名称
    # # market = IntegerField(market='varchar(5)')       # 所属市场
    # price = IntegerField(price='int unsigned')  # 单位用:分
    # cost = IntegerField(cost='int unsigned')  # 成本
    # amount = IntegerField(amount='int unsigned')  # 持仓数量
    #
    # state = IntegerField(state='enumerate(0,1)')  # 是否持仓(清仓后标记历史记录)
    # event = IntegerField(event='enumerate(0,1)')  # 交易方向
    # e_time = IntegerField(e_time='varchar(30)')  # 交易时间 (用python获取时间，sql有
    #
    # float_wl = IntegerField(float_wl='int unsigned')  # 复动盈亏
    # pct = IntegerField(pct='smallint')  # 盈亏百分比
    # e_time = IntegerField(e_time='varchar(30)')      # 交易时间 (用python获取时间，sql有
    code = IntegerField('code','int unsigned')         # 代码
    name = IntegerField('name', 'varchar(10)')          # 名称
    # market = IntegerField('market', 'varchar(5)')       # 所属市场
    price = IntegerField('price', 'int unsigned')       # 单位用:分
    cost = IntegerField('cost', 'int unsigned')         # 成本
    amount = IntegerField('amount', 'int unsigned')     # 持仓数量

    state = IntegerField('state', 'enumerate(0,1)')     # 是否持仓(清仓后标记历史记录)
    event = IntegerField('event', 'enumerate(0,1)')     # 交易方向
    e_time = IntegerField('e_time', 'varchar(30)')      # 交易时间 (用python获取时间，sql有

    float_wl = IntegerField('float_wl', 'int unsigned') # 复动盈亏
    pct = IntegerField('pct', 'smallint')               # 盈亏百分比
    # e_time = IntegerField('e_time', 'varchar(30)')      # 交易时间 (用python获取时间，sql有
    # AND SO ON
    # AND SO ON

    """以下定义账户常用统计功能"""
    # 仓位
    @property
    def position(self):
        return

    # 持股
    @property
    def on_hold(self):
        return

    # 策略执行池
    def pool(self):
        return

    # 盈亏
    @property
    def win_pct(self):
        return ()

    # 交易频率
    @property
    def bs_frequence(self):
        return

    """以下定义账户常用操作"""
    # 人工执行买卖
    def buy(self):
        pass

    def sell(self):
        pass

    # 策略执行池添加个股
    def pool_add(self):
        pass

    def pool_del(self):
        pass

    def show(self):
        pass

    # 自动对持股和策略池执行策略
    def auto_execute_strategy(self):
        """
        API ???
        遍历pool,买入或加仓，遍历on_hold,清仓或减仓
        :return: API，决策结果（代码和金额）
        """
        pass

# 初定数据表field  2020/10/10
class User(AccountModel):
    account_id = IntegerField('code', 'int unsigned')         # 代码
    # account_id
    # acc_desc
    #
    # win
    # win_pct
    #
    # found
    # position
    #
    # stock_amount
    # stock_n_c
    #
    # bs_frequece





    """
    用户管理，实际对应数据库的表管理
    """
    @staticmethod
    def show_general():
        """
        展示各账户概要:账户id， 策略说明/市值/资金/盈亏比
        :return:
        """
        return 1

    @staticmethod
    def create_account(id=0, money=200000, strategy='strategy'):
        """
        增加一个账户,数据库中增加一个对象(user+行，创建account表)
        :param id:
        :param money:
        :param strategy:
        :return:
        """
        pass

    def edit_account(self):
        """编辑账户，策略，持股，"""

    def clone_account(self):
        pass

    def del_account(self):
        """
        同时删除表
        :return:
        """
        pass

    @staticmethod
    def refresh_account(order):
        """刷新数据库"""
        pass

    @staticmethod
    def select_account():
        """
        选择操作账户
        :return:账户实例
        """
        general = User.show_general()
        print(general)
        s = input('输入账户编号')
        # if True:
            # if s in general.key():
            # return Account()


if __name__ == "__main__":
    # 定义表
    class Test1245(ORMModel):
        uid = IntegerField('uid', 'int unsigned')
        name = IntegerField('username', 'varchar(30)')
        pk = PrimaryField('uid')
        # print(pk,type(pk))

    # Test1245(uid=7, name='inf').save()
    # ret = Test1245(7).get_uid()
    # print(ret,type(ret))
    # ks = ('name', 'uid')
    # vs=[['inf',88],['mov','777']]
    # Test1245(ks,vs).save_all()
    ret = Test1245(name='inf', uid='===7').get_by_kvs()
    print(ret)

    #     @staticmethod
    #     def foo():
    #         print('in foo')
    #
    #     def bar(self):
    #         print(self)
    #         print('bar')
    #
    #
    # class TESTPKCHECK(ORMModel):
    #     uid = IntegerField('uid', 'int unsigned')
    #     name = IntegerField('username', 'varchar(30)')


    # u = Test(uid=789, name='inf')
    # t = Test()
    # t.create_table()

    # Test(uid=456, name='inf').save()
    # t.save()
    # t.bar()
    # t.foo()
    # t = TESTPKCHECK(uid=789, name='inf')
    # t.save()

    # help(t)
    # pass
    # t.save()
    # TESTPKCHECK().create()