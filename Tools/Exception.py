#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎2021‎-‎7‎-‎30‎ 8:47:23
# @Author  : NagisaCo

class RSAException(Exception):
    """
    RSA解密异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class TokenException(Exception):
    """
    Token异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class LoadConfigException(Exception):
    """
    配置文件加载异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class LoadException(Exception):
    """
    读取异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class DBException(Exception):
    """
    数据库操作异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason