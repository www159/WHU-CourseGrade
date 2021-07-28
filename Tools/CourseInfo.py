#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021‎-‎7‎-‎25 ‏‎17:50:55
# @Author  : NagisaCo
import os
import Tools.API.bkxk as bkxk
from Tools.ConfigLoader import Config
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor, as_completed

def __divList(ls :list,num :int) ->list:
    """
    等分列表
    
    Parameters:
        ls - 待切分列表
        num - 切分份数
    
    Returns:
        list - 已切分列表
    """
    each = ls.__len__() // num #平均每份个数
    re = ls.__len__() % num #余下未分配个数

    l = 0
    ans = []
    for i in range(0,num):
        if (i < re):#前re份多分配1个
            ans.append(ls[l: l + each + 1])
            l = l + each + 1
        else:
            ans.append(ls[l: l + each + 0])
            l =l + each + 0
    
    return ans

def init(configSetting :Config):
    """
    初始化
    
    Parameters:
        configSetting - 配置文件
    
    Returns:
        requests.session - 已登录的session
    """
    config = configSetting
    return bkxk.init(config.studentNum,config.encryptedPassword,config.gnmkdm)

def func_threadpool(idList :list) -> list:
    """
    线程池，用于单进程中多线程爬虫
    
    Parameters:
        idList - 待获取course id列表    

    Returns:
        list - 已获取course信息列表
    """
    executor = ThreadPoolExecutor(max_workers=10)
    all_tasks = [executor.submit(bkxk.getInfo, (item)) for item in idList]

    result= []
    for future in as_completed(all_tasks):
        data = future.result()
        if (data == False):
            print(f'failed {data.id}')
        else:
            print(f'success {data.id}')
            result.append(data)
    return result

def getCourseInfo(idList :list, gnmkdm :str, session :Session) -> list:
    """
    使用多进程获取course详细信息
    
    Parameters:
        idList - 待获取couse id列表
        gnmkdm - 配置文件中的项目，用于查询
        session - 已登录的session
    
    Returns:
        list - 已获取course信息列表
    """
    processNum = os.cpu_count()
    pre =[]
    for i in idList:#参数打包
        pre.append((idList.index(i),i,gnmkdm,session))

    workList = __divList(pre,processNum)

    executor = ProcessPoolExecutor(max_workers=processNum)
    print("========================================")
    print("Start fetching course info")
    print("========================================")
    all_tasks = [executor.submit(func_threadpool, (item)) for item in workList]#每个进程多线程查询
    
    result =[]
    
    for future in as_completed(all_tasks):
        data = future.result()
        for i in data:#将每个进程的结果拆分重组
            result.append(i)

    print("========================================")
    print("Complete fetching course info")
    print(f"Totol: {len(result)}")
    print("========================================")

    return result