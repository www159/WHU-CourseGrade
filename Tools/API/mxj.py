#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021‎-‎7-‎28‎ ‏‎9:20:30
# @Author  : NagisaCo
import json
import time
import requests
from Tools.API.bkxk import CourseInfo
from Tools.Exception import TokenException

_path = "https://www.campuses.cn"

class GradeInfo:
    """
    成绩详情
    """
    def __init__(self):
        name = "" #课程名称
        teacher = "" #任课教师
        number = 0 #分数统计人数
        score = 0.0 #平均分数
        scoreSection=[] #分数区间人数百分比

def __getTime() -> str:
    """
    获取当前13位时间戳
    
    Parameters:
        
    Returns:
        str - 当前时间戳
    """
    return str(round(time.time() * 1000))

def __getGrade(courseName :str, token :str) -> GradeInfo:
    """
    获取相应课程成绩信息
    
    Parameters:
        courseName - 课程名称
        token - mxj登录token

    Returns:
        GradeInfo/False - 返回查询成绩详情/False(未成功)

    Exceptions:
        TokenError - Token异常
    """

    url = _path + f"/api/v2/grader?name={courseName}&pageNumber=0&pageSize=100"
    payload={}
    headers = {
      'Host': 'www.campuses.cn',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MMWEBID/3258 MicroMessenger/8.0.7.1920(0x28000736) Process/appbrand0 WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm32 MiniProgramEnv/android',
      'charset': 'utf-8',
      'token': token,
      'content-type': 'application/json',
      'Referer': 'https://servicewechat.com/wxd67391d40f50f14b/181/page-frame.html',
    }
    s = requests.session()
    s.keep_alive = False
    requests.adapters.DEFAULT_RETRIES = 10
    response = s.request("GET", url, headers=headers, data=payload, timeout=20).json()
    s.close()
    time.sleep(0.5)
    if (response['code'] == 0):
        result = []
        for i in response['data']:
            grade = GradeInfo()
            grade.__dict__ = i #dict转为object
            grade.time = __getTime()
            result.append(grade)
        if (result == []): #无相关课程
            return False
        return result
    elif(response['code'] == 401 and response["message"] == "auth error: token is invalid"): #token无效
        raise TokenException("campuses登录失败","token无效或已过期，请重新抓包后重试...")
    else: #其他错误
        return False
    
def getInfo(_x :tuple) -> CourseInfo:
    """
    获取相应课程详情信息 整合信息
    
    Parameters:
        _in - 打包传入的参数(待查询Course对象, 登录token)

    Returns:
        CourseInfo - 返回已添加成绩的Course对象

    Exceptions:
        TokenError - Token异常
    """
    course, token= _x
    grade = __getGrade(course.name, token)

    course.grade = grade #course中添加grade成员
    return course
