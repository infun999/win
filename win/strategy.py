#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 6:23
# ===========================


import re


class Strategies:
    def refresh_market_data(market, code):
        """
        更新历史数据（默认执行此功能？）
        :param market:
        :param code:
        :return:
        """
        return



    # decorator is better 自动添加functions到列表
    # def choose_func():
    #     """
    #     选择执行的功能
    #     :return:
    #     """
    #     func_list = []
        # c = input("选择功能")
        # choice = int(c) if re.match(r'\d+', c) else choose_func()
        # return func_list[choice]