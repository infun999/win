#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ===========================
# @Author   :   inf
# @Time     :   2020/10/4 4:56
# ===========================
import re
import logging
from win import user_manager

# 保存定义功能的装饰器
FUNC = dict()


def set_func_id(func_id):
    """
    保存被装饰对象的 变量名映射引用 的关系到FUNC字典
    :param func_id:
    :return:
    """
    def set_func(func):
        FUNC["{}: ".format(func_id) + func.__name__] = func

        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func


@set_func_id(1)
def manual_run():
    """手工执行策略"""
    while True:
        account = user_manager.User.select_account()

        # 选择执行账户obj
        account.show_account()
        # 执行策略，生成订单
        order = account()
        # 确认订单，则刷新账户数据
        if 'confirm':
            user_manager.User.refresh_account(order)
        # 其他人工调整order情况？
        else:
            pass
        return manual_run()


@set_func_id(2)
def auto_run():
    """自动执行刷新全部账户"""
    pass


@set_func_id(3)
def show_user():
    """全部账户概要"""
    pass


@set_func_id(4)
def show_account():
    """单个账户总览"""
    pass


def main():
    while True:
        for i in FUNC.keys():
            print(i)
        print('press "q/Q" for quit')
        f = input('选择功能编号: ')
        for k, v in FUNC.items():
            try:
                if f == re.findall(r'(\d+): ', k)[0]:
                    v()
                elif f.lower() == 'q':
                    exit()
            except Exception:
                print('Not a correct choice.')
                pass



if __name__ == "__main__":
    main()