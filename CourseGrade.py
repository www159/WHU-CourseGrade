#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021-‎7‎-‎25‎ 17:49:48
# @Author  : NagisaCo
import os
import sys
import pickle
import Tools.DB as DB
import Tools.CourseId as CourseId
import Tools.GradeInfo as GradeInfo
import Tools.CourseInfo as CourseInfo
import Tools.ConfigLoader as ConfigLoader
from Tools.API.bkxk import RSAException
from Tools.API.mxj import TokenException

def __LoadConfig() -> dict:
    """
    加载配置文件
    
    Parameters:
    
    Returns:
        dict - 配置文件内容
    """
    try:
        return ConfigLoader.load()
    except ConfigLoader.LoadConfigException as err:
        print(f"【{err.name}】{err.reason}")
        sys.exit(1)

def __storeFile(course :list):
    """
    保存已获取列表至本地
    
    Parameters:
        course - 已获取详情

    Returns:
        
    """
    with open("result", "wb") as f:
        pickle.dump(course, f)

def __loadFile() -> list:
    """
    加载本地数据
    
    Parameters:
    
    Returns:
        list - 加载的列表
    """
    with open("result", "rb") as f:
        result = pickle.load(f)
    return result

def __getCourse(config :dict) -> list:
    """
    获取课程数据
    
    Parameters:
        config - 配置文件内容
    Returns:
        list - 获取的课程详情
    """
    try:
        idList = CourseId.getCourseId(config['base']['htmlsource'])
        session = CourseInfo.init(config)
        course = CourseInfo.getCourseInfo(idList, config['bkxk']['gnmkdm'], session)
        course_grade = GradeInfo.getGradeInfo(course, config['mxj']['token'])
    except (CourseId.LoadException, RSAException, TokenException) as err:
        print(f"【{err.name}】{err.reason}")
        sys.exit(1)

    return course_grade

def __storeDatabase(course :list):
    """
    保存已获取列表至数据库
    
    Parameters:
        course - 已获取详情

    Returns:
        
    """
    DB.init(config['db']['server'], config['db']['username'], config['db']['encryptedpassword'], config['db']['database'])
    try:
        for item in course:
            DB.update(item)
    
        DB.close()
    except Exception:
        print("【数据库操作失败】请检查数据库结构或重新导入course_grade.sql后重试...")
        sys.exit(1)

if __name__ == "__main__":
    
    config = __LoadConfig()
    info = __getCourse(config)
    __storeFile(info)
    #info = __loadFile() 
    
    if (config['db']['server'] != "" and config['db']['username'] != "" and config['db']['encryptedpassword'] != "" and config['db']['database'] != ""):
        __storeDatabase(info)
    
