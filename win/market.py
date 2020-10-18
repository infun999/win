#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 2:30
# ===========================

import requests
import re
import time
import baostock as bs
from collections import Iterable
from win.common import IntegerField, PrimaryField, ORMModel, ORM_MAPPINGS

# 登录baostock
lg = bs.login(user_id="anonymous", password="123456")

# def history(code: str):
#     """和讯网,历史查询"""
#     if re.match(r'(600|601|602|603|688|51\w1)\w3', code):
#         # 上证
#         url = 'http://webstock.quote.hermes.hexun.com/a/kline?code=sse513100&start=20200909150000&number=-10&type=5&callback=callback'
#
#     elif re.match(r'(000|001|002|300|159)\w3', code):
#         # 深圳
#         url = 'http://webstock.quote.hermes.hexun.com/a/kline?code=szse002007&start=20200909150000&number=-10&type=5&callback=callback'
#     else:
#         return None
#     ret = requests.get(url)
#     return ret

# def history(url):
#     ret = requests.get(url)
#     pass
#     return ret


# def real_time(code: str):
#     """新浪网,实时数据"""
#     url = 'http://hq.sinajs.cn/list=sh600999'
#     url = 'http://hq.sinajs.cn/list=sz002007'
#     ret = requests.get(url)
#     return ret


# def real_time(url):
#     ret = requests.get(url)
#     pass
#     return ret

# pass test
def judge_market(code: str) -> str:
    """判断所属市场"""
    market = ''
    if re.match(r'^(600|601|603|605|688|51\d)\d{3}', code):
        market = 'sh'
    elif re.match(r'^(000|001|002|300|159)\d{3}', code):
        market = 'sz'
    return market



# field确定,
# 待>>>写方法(核心是查询方法;重写覆盖父类保存数据条[插入多列表]方法,其他创建表继承父类)
# >>>type继承本class,创建各子市场表
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


# 基本方法完成, 待和讯api\新浪返回数据格式处理 /模块测试 2020/10/10
class BaoStock(StockModel):
    """baostock查询股票信息, 改单例模式"""
    # 查询当前数据库表
    # tables = orm_database.DB.show_table()

    # def __init__(self, stock_model, db):
    #     pass

    @staticmethod
    def _get(code: str, date_start: str, date_end: str, period='d'):
        """
        baostock模块查询历史
        :param code: 'sz.002007'
        :param date_start: '2020-04-24'
        :param date_end: '2020-04-28'
        :param period: "d"
        :return:
        """
        rs = bs.query_history_k_data(code,
                             "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                             start_date=date_start, end_date=date_end,
                             frequency=period, adjustflag="2")  # frequency="d"取日k线，adjustflag="3"默认不复权
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        return data_list

    @staticmethod
    def _save(code, datas):
        tb_name = 's_' + re.findall(r'(\d{3})', code)[0]

    # StockModel.

    # @classmethod
    # def update_history(cls, code: str, date_start: str, date_end: str):
    #     new_c = judge_market(code) + '.' + code
    #     ret = BaoStock.get_history(new_c, date_start, date_end)
    #     # 如果不存在code对应的市场表,则先创建表
    #     if ret and "m" + re.findall(r'(\d{3})\d{3}', code)[0] not in cls.tables:
    #         super().dynamic_create_table()

class Foo:
    __instance = None
    __init_flag = False
    def __new__(cls, *args, **kwargs):

        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def get_now(code):
        """新浪网,实时数据"""
        code = judge_market(code)+code
        url = 'http://hq.sinajs.cn/list={}'.format(code)
        ret = requests.get(url)
        return ret  # 格式待处理

    @staticmethod
    def day_history(start, forward=1000):
        """
        和讯网, 如513100的数据
         获取日交易历史数据,用于分析候选买点
        http://webstock.quote.hermes.hexun.com/a/kline?code=sse601398&start=20200909150000&number=-10&type=5&callback=callback
        http://webstock.quote.hermes.hexun.com/a/kline?code=sse513100&start=20200909150000&number=-10&type=5&callback=callback
        http://webstock.quote.hermes.hexun.com/a/kline?code=szse002007&start=20200909150000&number=-10&type=5&callback=callback
        :param code:
        :param start:
        :param forward:
        :return:
        """
        return

class Foo1(StockModel):
    date = IntegerField('date', 'char(10)')
    code = IntegerField('code', 'char(10)')  # 代码
    o = IntegerField('open', 'int unsigned')  # 单位用:分
    c = IntegerField('close', 'int unsigned')

if __name__ == "__main__":
    a = '600166'
    # StockModel().dynamic_create_table('bz0',StockModel)
    Foo1().create_table()
    print(ORM_MAPPINGS)
    print('aaa')
    pass
    # ret = BaoStock.get_history('688001', '2013-04-24','2013-04-28')
    # print(ret)
    # b=judge_market(a)
    # print(b,type(b))
    # class Foo:
    #     @staticmethod
    #     def bar():
    #         print('in foo')
    #
    #
    # def cc():
    #     return type('Abc', (Foo,), dict())
    #
    #
    # a = cc()().bar()
    # MarketModel().dynamic_create_table('Bao10', MarketModel)