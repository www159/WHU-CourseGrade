#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎2021-‎7‎-‎27‎ ‏‎10:14:52
# @Author  : NagisaCo
import os
import requests
from bs4 import BeautifulSoup
from Tools.Exception import LoadException


def __getCourseIdFile(path:str) -> list:
    """
    由本地文件获取course id列表信息
    
    Parameters:
        path - 本地文件路径
    
    Returns:
        list - course id列表
    """
    htmlfile = open(path, 'r', encoding='utf-8')
    return __getIdList(htmlfile.read())
    
def __getCourseIdUrl(url :str) -> list:
    """
    由url获取course id列表信息
    
    Parameters:
        url - url 地址
    
    Returns:
        list - course id 列表
    """
    result = requests.get(url)
    return __getIdList(result.content)

def __getIdList(content :bytes) -> list:
    """
    通过beautifulsoup处理后的内容获取course id
    
    Parameters:
        content - beautifulsoup处理后的内容
    
    Returns:
        list - course id列表
    """
    soup = BeautifulSoup(content, 'html.parser')

    result=[]

    for item in soup.find_all("span","kcmc"):
        result.append(item['id'][5:])

    return result

def getCourseId(htmlSource :str) -> list:
    """
    获取course id列表信息
    
    Parameters:
        path - 本地文件路径
    
    Returns:
        list - course id列表

    Exceptions:
        LoadError - 读取异常
    """
    try:
        print("========================================")
        print("Start fetching id list")
        print("========================================")
        if (os.path.isfile(htmlSource)): #判断为文件还是url
            idList=__getCourseIdFile(htmlSource)
        else:
            idList=__getCourseIdUrl(htmlSource)
        print("========================================")
        print("Complete fetching id list")
        print(f"Totol: {len(idList)}")
        print("========================================")
        return idList
    except Exception as err:
        raise LoadException('读取失败',f'当前路径为{htmlSource}，请检查后重试...')