#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/18 11:47
# ===========================

import re
from ..orm_database import ORMModel, IntegerField, PrimaryField


class Market(ORMModel):
    """市场股票代码汇总表"""
    code = IntegerField('code', 'char(10)')
    name = IntegerField('name', 'char(10)')
    state = IntegerField('state', 'tinyint unsigned')
    pk = PrimaryField('code')


class StockModel(ORMModel):
    """定义股市通用数据表,父类"""
    date = IntegerField('date', 'char(10)')
    code = IntegerField('code', 'char(10)')  # 代码
    o = IntegerField('open', 'int unsigned')  # 单位用:分
    c = IntegerField('close', 'int unsigned')  # 单位用:分
    h = IntegerField('high', 'int unsigned')  # 单位用:分
    l = IntegerField('low', 'int unsigned')  # 单位用:分
    pre_close = IntegerField('pre_close', 'int unsigned')  # 单位用:分
    vol = IntegerField('vol', 'int unsigned')
    amount = IntegerField('amount', 'int unsigned')  # 成交量
    turn = IntegerField('turn', 'tinyint unsigned')  # *100
    state = IntegerField('state', 'tinyint unsigned')  # 是否停牌
    pct_chg = IntegerField('pct_chg', 'tinyint unsigned')  # 涨跌幅
    pe_ttm = IntegerField('pe_ttm', 'int')  # 单位用:分
    pb_ttm = IntegerField('pb_ttm', 'int')

    pk = PrimaryField(' date,  code ')

    def create_stock_table(self, code):
        tb_name = 's_' + re.findall(r'(\d{3})', code)[0]
        super().dynamic_create_table(tb_name, StockModel)


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