#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021‎-‎7‎-‎29‎ 9:24:52
# @Author  : NagisaCo
import rsa
import time
import base64
import pymysql
from Tools.API.mxj import GradeInfo
from Tools.Tool import __decryptRSA
from Tools.Tool import __getDatetime
from Tools.API.bkxk import CourseInfo
from Tools.Exception import RSAException

def init(_host :str, _user :str, _password :str, _database :str):
    """
    数据库登录 游标获取
    
    Parameters:
        _host - 数据库服务器地址
        _user - 登录用户名
        _password - 已加密登录密码
        _database - 数据库名

    Returns:
        
    """
    global db
    db = pymysql.connect(host = _host,
                         user = _user, 
                         password = __decryptRSA(_password), 
                         database = _database, 
                         cursorclass = pymysql.cursors.DictCursor)
    global cursor
    cursor = db.cursor()

def close():
    """
    关闭数据库连接 关闭游标
    
    Parameters:
        
    Returns:
        
    """
    db.close()
    cursor.close()

def __updateGrade(courseid: int, grade: GradeInfo):
    """
    更新成绩信息
    
    Parameters:
        courseid - 数据库中课程id(主键)
        grade - 成绩类

    Returns:
        
    """
    search_sql = (f"SELECT id FROM class "
                  f"WHERE course_id={courseid} "
                  f"AND teacher='{grade.teacher}' "
                  f"LIMIT 1")
    cursor.execute(search_sql)
    content = cursor.fetchone()
    if (content == None):
        insert_sql = (f"INSERT INTO class "
                      f"VALUES (default, {courseid}, '{grade.name}', "
                      f"'{grade.teacher}', {grade.score}, {grade.number}, "
                      f"{grade.scoreSection[0]}, {grade.scoreSection[1]}, "
                      f"{grade.scoreSection[2]}, {grade.scoreSection[3]}, "
                      f"{grade.scoreSection[4]}, {grade.scoreSection[5]}, "
                      f"{grade.scoreSection[6]}, {grade.scoreSection[7]}, "
                      f"{grade.scoreSection[8]}, {grade.scoreSection[9]}, "
                      f"'{__getDatetime(grade.time)}')")
        cursor.execute(insert_sql)
    else:
        update_sql = (f"UPDATE class "
                      f"SET course_id={courseid}, "
                      f"name='{grade.name}', "
                      f"teacher='{grade.teacher}', "
                      f"score={grade.score}, "
                      f"number={grade.number}, "
                      f"section_9={grade.scoreSection[0]}, "
                      f"section_8={grade.scoreSection[1]}, "
                      f"section_7={grade.scoreSection[2]}, "
                      f"section_6={grade.scoreSection[3]}, "
                      f"section_5={grade.scoreSection[4]}, "
                      f"section_4={grade.scoreSection[5]}, "
                      f"section_3={grade.scoreSection[6]}, "
                      f"section_2={grade.scoreSection[7]}, "
                      f"section_1={grade.scoreSection[8]}, "
                      f"section_0={grade.scoreSection[9]}, "
                      f"time='{__getDatetime(grade.time)}' "
                      f"WHERE id={courseid}")
        cursor.execute(update_sql)

def update(course :CourseInfo):
    """
    更新信息
    
    Parameters:
        course - 课程类信息
    Returns:
        
    """
    search_sql = (f"SELECT id FROM course "
                  f"WHERE code='{course.id}' "
                  f"LIMIT 1")
    cursor.execute(search_sql)
    content = cursor.fetchone()
    try: #创建事物
        if (content == None):
            insert_sql = (f"INSERT INTO course "
                          f"VALUES (default, '{course.id}', "
                          f"'{course.name}', {course.credit}, "
                          f"'{course.category}', '{course.subcategory}', "
                          f"'{course.academy}', '{__getDatetime(course.time)}')")
            cursor.execute(insert_sql)
            id = cursor.lastrowid
        else:
            update_sql = (f"UPDATE course "
                          f"SET name='{course.name}', "
                          f"credit={course.credit}, "
                          f"category='{course.category}', "
                          f"subcategory='{course.subcategory}', "
                          f"academy='{course.academy}', "
                          f"time='{__getDatetime(course.time)}' "
                          f"WHERE code='{course.id}'")
            cursor.execute(update_sql)
            id = content['id']
        for item in course.grade:
            __updateGrade(id,item)
        db.commit()
        print(course.name)
    except Exception: #事物回滚
        db.rollback()