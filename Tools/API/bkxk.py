#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : 2021‎-‎7‎-‎25 ‏‎19:43:23
# @Author  : NagisaCo
import rsa
import time
import base64
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

_path = "https://bkxk.whu.edu.cn"

class RSAError(Exception):
    """
    RSA解密异常
    """
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class CourseInfo:
    """
    course详情
    """
    def __init__(self):
        self.index = 0 #编号
        self.id = "" #课程代码
        self.name = "" #课程名称
        self.category = "" #课程类别
        self.subcategory = "" #课程归属
        self.academy = "" #开课学院
        self.credit = 0 #学分
        self.time = 0 #查询时间

def decryptRSA(data :str) -> str:
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

def __getEncryptPasswd(session :requests.sessions.Session, passwd :str) -> str:
    """
    获取登录密码加密公钥
    
    Parameters:
        session - 登录会话
        passwd - 配置文件中已加密的密码

    Returns:
        str - 加密的登录密码

    Exceptions:
        RSAError - RSA解密异常
    """
    #获取公钥
    url = _path+"/xtgl/login_getPublicKey.html?time="+__getTime()
    page = session.get(url)
    modulus = int.from_bytes(base64.b64decode(page.json()['modulus']),byteorder='big',signed=False)
    exponent = int.from_bytes(base64.b64decode(page.json()['exponent']),byteorder='big',signed=False)
    pubkey = rsa.PublicKey(modulus,exponent)
    try:
        password = decryptRSA(passwd)#获取配置文件中加密后解密的密码
    except Exception:
        raise RSAError("RSA解密失败", "无法解析encryptedPassword，请确认使用Encryptor.py加密后重试...")
    
    #加密登录密码
    encryptPasswd = base64.b64encode(rsa.encrypt(password.encode('utf8'),pubkey)).decode('utf8')
    return encryptPasswd

def __getToken(session :requests.sessions.Session) -> str:
    """
    获取登录所需token
    
    Parameters:
        session - 登录会话    

    Returns:
        str - token
    """
    #获取token
    url = _path+"/xtgl/login_slogin.html?time="+__getTime()
    page=session.get(url)
    page.encoding = page.apparent_encoding
    soup = BeautifulSoup(page.text,'html.parser')
    token = soup.find("input",attrs={"id":"csrftoken"}).attrs['value']
    return token

def logout(session :requests.sessions.Session) -> requests.sessions.Session:
    """
    登出当前账号
    
    Parameters:
        session - 已登录的会话

    Returns:
        requests.session - 已登出的会话
    """
    url = "https://bkxk.whu.edu.cn/logout?t="+__getTime()+"&login_type="

    payload={}
    headers = {
      'Connection': 'keep-alive',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'sec-ch-ua-mobile': '?0',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'Referer': 'https://bkxk.whu.edu.cn/xtgl/index_initMenu.html',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Cookie': 'route='+session.cookies["route"]+'; JSESSIONID='+session.cookies["JSESSIONID"]
    }

    response = session.request("GET", url, headers=headers, data=payload)

    return session

def login(session :requests.sessions.Session, studentNum :str, password :str, gnmkdm :str) -> requests.sessions.Session:
    """
    登录bkxk
    
    Parameters:
        session - 待登录的会话
        studentNum - 学号
        password - 配置文件加密的密码
        gnmkdm - 配置文件gnmkdm项

    Returns:
        requests.session - 已登录的会话

    Exceptions:
        RSAError - RSA解密异常
    """
    student = studentNum

    passwd = __getEncryptPasswd(session,password)

    token = __getToken(session)
    
    url = _path+"/xtgl/login_slogin.html?time="+__getTime()

    data = {'csrftoken':token,
            'language':'zh_CN',
            'yhm':student,
            'mm':passwd,
            'mm':passwd}
    payload = urlencode(data)

    headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'sec-ch-ua-mobile': '?0',
      'Upgrade-Insecure-Requests': '1',
      'Origin': 'https://bkxk.whu.edu.cn',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'Referer': 'https://bkxk.whu.edu.cn/xtgl/login_slogin.html',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    response = session.request("POST", url, headers=headers, data=payload)
    
    return session

def check(session :requests.sessions.Session) -> bool:
    """
    检测是否登录
    
    Parameters:
        session - 待检测会话

    Returns:
        bool - 检查结果
    """
    url = "https://bkxk.whu.edu.cn/xtgl/index_initMenu.html"
    response = session.request("GET", url)
    if (response.url=="https://bkxk.whu.edu.cn/xtgl/login_slogin.html"):
        return False
    else:
        return True

def getInfo(_in :tuple) -> CourseInfo:
    """
    获取相应课程详情信息
    
    Parameters:
        _in - 打包传入的参数(课程编号, gnmkdm, 已登录会话)

    Returns:
        CourseInfo/False - 返回查询课程详情/False(未成功)
    """
    index, courseId, gnmkdm, session= _in #解包参数
    url = "https://bkxk.whu.edu.cn/xkgl/common_cxKcxxModel.html?time="+__getTime()+"&gnmkdm="+gnmkdm
    payload = "kch_id="+courseId
    headers = {
      'Connection': 'keep-alive',
      'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
      'Accept': 'text/html, */*; q=0.01',
      'X-Requested-With': 'XMLHttpRequest',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      'Origin': 'https://bkxk.whu.edu.cn',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Cookie': 'route='+session.cookies["route"]+'; JSESSIONID='+session.cookies["JSESSIONID"]
    }
    requests.adapters.DEFAULT_RETRIES = 10 #设定默认重试次数
    response = session.request("POST", url, headers=headers, data=payload, timeout=20)
    time.sleep(0.1) #暂停0.1s 防止爬虫速度过快
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text,'html.parser')

    courseInfo = CourseInfo()
    try:
        courseInfo.index = index
        courseInfo.time = __getTime()
        courseInfo.id = soup.find(text='课程代码').parent.next_sibling.next_sibling.text
        courseInfo.name = soup.find(text='课程名称').parent.next_sibling.next_sibling.text
        courseInfo.academy = soup.find(text='开课学院').parent.next_sibling.next_sibling.text
        courseInfo.credit = int("".join(list(filter(str.isdigit, soup.find(text='学分').parent.next_sibling.next_sibling.text))))
        courseInfo.category = soup.find(text='课程类别').parent.next_sibling.next_sibling.text
        courseInfo.subcategory = soup.find(text='课程归属').parent.next_sibling.next_sibling.text
        return courseInfo
    except Exception:
        return False
        

def init(num :str, passwd :str, gn :str) -> requests.sessions.Session:
    """
    初始化登录
    
    Parameters:
        num - 学号
        passwd - 配置文件中已加密的密码
        gn - gnmkdm

    Returns:
        requests.session - 已登录的会话
    """
    global session
    session=requests.session()
    login(session,num,passwd,gn)
    return session
