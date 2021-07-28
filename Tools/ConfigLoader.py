#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : 2021‎-‎7‎-‎25 ‏‎21:03:38
# @Author  : NagisaCo
import configparser

config = configparser.ConfigParser()
config.read("config.ini",encoding="gbk")

class LoadConfigError(Exception):
    """
    配置文件加载异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class Config:
    """
    配置文件内容
    """
    def __init__(self):
        self.htmlSource = ""
        self.gnmkdm = ""
        self.studentNum = ""
        self.encryptedPassword = ""
        self.token = ""

def init():
    """
    初始化配置文件
    
    Parameters:
        
    Returns:
        
    """
    config_new = configparser.ConfigParser() #重置配置文件

    config_new.add_section("base")
    if (config.has_option("base", "html_source")):
        config_new.set("base", "html_source", config.get("base", "html_source")) #恢复已配置的项目内容
    else:
        config_new.set("base", "html_source", "")

    config_new.add_section("bkxk")
    if (config.has_option("bkxk", "gnmkdm")):
        config_new.set("bkxk", "gnmkdm", config.get("bkxk", "gnmkdm"))
    else:
        config_new.set("bkxk", "gnmkdm", "N253512")
    if (config.has_option("bkxk", "studentNum")):
        config_new.set("bkxk", "studentNum", config.get("bkxk", "studentNum"))
    else:
        config_new.set("bkxk", "studentNum", "")
    if (config.has_option("bkxk", "encryptedPassword")):
         config_new.set("bkxk", "encryptedPassword", config.get("bkxk", "encryptedPassword"))
    else:
        config_new.set("bkxk", "encryptedPassword", "")

    config_new.add_section("mxj")
    if (config.has_option("mxj", "token")):
        config_new.set("mxj", "token", config.get("mxj", "token"))
    else:
        config_new.set("mxj", "token", "")
    
    note = "#[bkxk]中encryptedPassword项为经过Encryptor.py加密后的密码"

    with open("config.ini","w+") as f:
        config_new.write(f)
        f.writelines(note)

def load() -> Config:
    """
    获取配置文件
    
    Parameters:
        
    Returns:
        Config - 读取的配置文件

    Exceptions:
        LoadConfigError - 配置错误
    """
    try:
        htmlSource = config.get("base", "html_source")
        gnmkdm = config.get("bkxk", "gnmkdm")
        studentNum = config.get("bkxk", "studentNum")
        encryptedPassword = config.get("bkxk", "encryptedPassword")
        token = config.get("mxj", "token")
    except Exception:
        init()
        raise LoadConfigError("配置读取错误", "配置缺少项目，请检查config.ini后重试...")

    if (htmlSource==""):
        raise LoadConfigError("配置读取错误", "html_source为空，请检查config.ini后重试...")
    if (gnmkdm==""):
        raise LoadConfigError("配置读取错误", "gnmkdm为空，请检查config.ini后重试...")
    if (studentNum==""):
        raise LoadConfigError("配置读取错误", "studentNum为空，请检查config.ini后重试...")
    if (encryptedPassword==""):
        raise LoadConfigError("配置读取错误", "encryptedPassword为空，请检查config.ini后重试...")
    if (token==""):
        raise LoadConfigError("配置读取错误", "token为空，请检查config.ini后重试...")

    config_out = Config()
    config_out.encryptedPassword = encryptedPassword
    config_out.gnmkdm = gnmkdm
    config_out.htmlSource = htmlSource
    config_out.studentNum = studentNum
    config_out.token = token

    return config_out