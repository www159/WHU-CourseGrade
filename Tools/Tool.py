#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎2021‎-‎7‎-‎30 8:55:29
# @Author  : NagisaCo
import rsa
import time
import base64

def __divList(ls :list,num :int) -> list:
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

def __decryptRSA(data :str) -> str:
    """
    RSA解密
    
    Parameters:
        data - 待解密数据
    
    Returns:
        str - 已解密数据
    """
    privkey = rsa.PrivateKey.load_pkcs1("-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC8yZpOztMWmzYzvvswTFO/uTaymVG3exS7apoPaABHYI4G1ln6LHqwiL0Zf2aqg0eucPyCYBAr/SvLFzXm/xFCUJQO/EeGOjZeKSUqP8w6n9I488RuEoUS8YeNpLshYAHWbFPBqFuMn2jz70kRb9FqgFwIpLHpBPJ1knw423O5WwIDAQABAoGAVthXB9HVAR09fehpHPq/u/6zzs0A7mrMSrrrTBMHrc4ZB8QreA5mEjeU5dnZnK7vlqubPU57ogDA2JhAz5aelRybBVtx3VWANmHLRVvGrGreAMAxX65ZK0ySZlpuafJWm8sl+ezc0FKGvgJiyf/r8QX+ajBSqYbiErhtFjUaXiECQQDkblMWsWqfCxz8PqgxJLuZsf8uQdbkqVOy3gHJSB0vluSAWbL4UVY1fJMUnFBoXzUbC/X9JUgdNvD22opfsQvtAkEA05JxFVCbdWt8H3hL2yDAmUds58N3WwaQW3Np/H3Qc+/ecclxeFAR8Kxqjw9r2phGs600mNW9uqEc7FX7xVwBZwJAAn/GfvAP9496kLPqySbaupK89PeZb0T++mz9XgNg9l1TQKg6kgbpx4oGXepb4thvz0zxMwTOZitstXasnuFj/QJBALwgANF1JWZZNrs82iZ0jw08R4gldGHKCl5m150dulb8uQzwlCbo+6rHhNDEY6CxulxV7OjhVZ03WWKEaiTpVI0CQQCqKnFmdheJQDzMfKjTo1F45E2O98uSZ0BUiLStWTuGfxDLlcYgytmjjMHBIgGMOL2150PUcMyrWC1Ko3o1rW5/\n-----END RSA PRIVATE KEY-----")

    # 解密数据
    message = rsa.decrypt(base64.b64decode(data), privkey)
    return message.decode('utf8')

def __getTime() -> str:
    """
    获取当前13位时间戳
    
    Parameters:
        
    Returns:
        str - 当前时间戳
    """
    return str(round(time.time() * 1000))

def __getDatetime(timestamp: str) -> str:
    """
    由13位时间戳获取mysql datetime格式时间
    
    Parameters:
        timestamp - 13位时间戳

    Returns:
        str - datetime格式时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp[0:10])))