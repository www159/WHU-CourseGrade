#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : 2021‎-‎7‎-‎25 ‏‎21:03:38
# @Author  : NagisaCo
import configparser
from copy import deepcopy
from Tools.Exception import LoadConfigException
configFile = configparser.ConfigParser()
configFile.read("config.ini",encoding="gbk")

CONFIG_DICT = {  "base": 
                {"htmlsource": ""}, 
            "bkxk": 
                {"gnmkdm": "N253512", 
                 "studentnum": "", 
                 "encryptedpassword": ""}, 
            "mxj": 
                {"token": ""}, 
            "db": 
                {"server": "", 
                 "username": "", 
                 "encryptedpassword": "", 
                 "database": ""}
         }

def init():
    """
    初始化配置文件
    
    Parameters:
        
    Returns:
        
    """
    configNew = configparser.ConfigParser() #重置配置文件

    for section in CONFIG_DICT:
        configNew.add_section(section)
        for option in CONFIG_DICT[section]:
            if (configFile.has_option(section, option)):
                configNew.set(section, option, configFile.get(section, option)) #恢复已配置的项目内容
            else:
                configNew.set(section, option, CONFIG_DICT[section][option])

    with open("config.ini","w+") as f:
        f.writelines("#config.ini\n")
        configNew.write(f)
        f.writelines("#[bkxk]和[db]中的encryptedPassword项为经过Encryptor.py加密后的密码\n")
        f.writelines("#[db]不填写自动关闭数据库存储任务\n")

def load() ->dict:
    """
    获取配置文件
    
    Parameters:
        
    Returns:
        dict - 读取的配置文件

    Exceptions:
        LoadConfigError - 配置错误
    """
    config = deepcopy(CONFIG_DICT)

    try:
        for section in config:
            for option in config[section]:
                config[section][option] = configFile.get(section, option) #读取文件
                print(f"已加载配置{section}.{option}: {config[section][option]}")
                if (section != "db"): #不检查空值的section
                    if (config[section][option] == ""): #检查空值
                        raise LoadConfigException("配置读取错误", 
                                                  f"{section}中{option}为空，请检查config.ini后重试...")
    except (configparser.NoSectionError, configparser.NoOptionError):
        init()
        raise LoadConfigException("配置读取错误", "配置缺少项目，请检查config.ini后重试...")

    for section in config:
        if (section != "db"): #不检查空值的section
            for option in config[section]:
                if (config[section][option] == ""): #检查空值
                    raise LoadConfigException("配置读取错误", 
                                              f"{section}中{opntion}为空，请检查config.ini后重试...")

    return config