import math
from functools import wraps

from flask import session, request, redirect, url_for


def is_login(func):
    @wraps(func)
    def wraper(*args,**kwargs):
        if 'user_id' in session or 'token' in request.cookies:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('back.login'))
    return wraper

class PageBean():
    # 每页显示的数据
    # goodlist = []
    # 总页数
    #totalPage
    # 当前页
    #currentPage = 1
    # 总条数
    #totalCount
    # 当前显示条数
    #currentCount = 10

    def __init__(self,alllist,currentPage,currentCount=10):
        self.goodlist = alllist[currentCount*(currentPage-1):currentCount*currentPage]
        self.totalCount = len(alllist)
        self.totalPage = math.ceil(self.totalCount/currentCount)
        self.currentPage = currentPage
        self.currentPage = currentCount




