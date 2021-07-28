#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021-‎7‎-‎25‎ 17:49:48
# @Author  : NagisaCo
import os
import sys
import pickle
import Tools.CourseId as CourseId
import Tools.GradeInfo as GradeInfo
from Tools.API.bkxk import RSAError
from Tools.API.mxj import TokenError
import Tools.CourseInfo as CourseInfo
import Tools.ConfigLoader as ConfigLoader

def __LoadConfig() -> ConfigLoader.Config:
    """
    加载配置文件
    
    Parameters:
    
    Returns:
        ConfigLoader.Config - 配置文件内容
    """
    try:
        return ConfigLoader.load()
    except ConfigLoader.LoadConfigError as err:
        print("【%s】%s" % (err.name,err.reason))
        sys.exit(1)

def __storeResult(course :list):
    """
    保存已获取列表至本地
    
    Parameters:
        course - 已获取详情

    Returns:
        
    """
    with open("result.txt", "wb") as f:
        pickle.dump(course, f)

def __loadResult() -> list:
    """
    加载本地数据
    
    Parameters:
    
    Returns:
        list - 加载的列表
    """
    with open("result.txt", "rb") as f:
        result = pickle.load(f)
    return result

def __getInfo(config :ConfigLoader.Config) -> list:
    """
    获取课程数据
    
    Parameters:
        config - 配置文件内容
    Returns:
        list - 获取的课程详情
    """
    try:
        idList = CourseId.getCourseId(config.htmlSource)
        session = CourseInfo.init(config)
        course = CourseInfo.getCourseInfo(idList, config.gnmkdm, session)
        course_grade = GradeInfo.getGradeInfo(course, config.token)
    except (CourseId.LoadError, RSAError, TokenError) as err:
        print("【%s】%s" % (err.name,err.reason))
        sys.exit(1)

    return course_grade

if __name__ == "__main__":
    
    config = __LoadConfig()
    info = __getInfo(config)

    __storeResult(info)
    
