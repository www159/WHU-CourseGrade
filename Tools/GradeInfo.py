#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021‎-‎7‎-‎28‎ 10:03:44
# @Author  : NagisaCo
import os
import Tools.API.mxj as mxj
from Tools.Tool import __divList
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor, as_completed

def func_threadpool(courseList :list) -> list:
    """
    线程池，用于单进程中多线程爬虫
    
    Parameters:
        idList - 待获取course列表    

    Returns:
        list - 已获取course_grade列表
    """
    executor = ThreadPoolExecutor(max_workers=10)
    all_tasks = [executor.submit(mxj.getInfo, (item)) for item in courseList]

    result= []
    for future in as_completed(all_tasks):
        data = future.result()
        if (data == False):
            print(f'failed {data.name}')
        else:
            print(f'success {data.name}')
            result.append(data)
    return result

def getGradeInfo(courseList :list, token :str) -> list:
    """
    使用多进程获取course详细信息
    
    Parameters:
        courseList - 待获取couse列表
        token - 配置文件中token项，用于验证登录
    
    Returns:
        list - 已获取course_grade列表
    """
    processNum = os.cpu_count()
    pre =[]
    for i in courseList:
        pre.append((i,token))

    workList = __divList(pre,processNum)
    
    executor = ProcessPoolExecutor(max_workers=processNum)
    print("========================================")
    print("Start fetching grade info")
    print("========================================")
    all_tasks = [executor.submit(func_threadpool, (item)) for item in workList]
    
    result =[]
    
    for future in as_completed(all_tasks):
        data = future.result()
        for i in data:
            result.append(i)
    
    print("========================================")
    print("Complete fetching grade info")
    print(f"Totol: {len(result)}")
    print("========================================")

    return result
