#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Time    : ‎‎‎2021-‎7‎-‎26 ‏‎10:38:55
# @Author  : NagisaCo
import rsa
import sys
import base64
import pyperclip
pubkey = rsa.PublicKey.load_pkcs1_openssl_pem("-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8yZpOztMWmzYzvvswTFO/uTaymVG3exS7apoPaABHYI4G1ln6LHqwiL0Zf2aqg0eucPyCYBAr/SvLFzXm/xFCUJQO/EeGOjZeKSUqP8w6n9I488RuEoUS8YeNpLshYAHWbFPBqFuMn2jz70kRb9FqgFwIpLHpBPJ1knw423O5WwIDAQAB\n-----END PUBLIC KEY-----")



def __getch():
    import termios
    import tty
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def __getpass_linux(maskchar="*") -> str:
    """
    获取密码 linux
    
    Parameters:
        maskchar - 替换符号 默认为*

    Returns:
        str - 输入内容
    """
    password = ""
    while True:
        ch = __getch()
        if ch == "\r" or ch == "\n":
            print
            return password
        elif ch == "\b" or ord(ch) == 127:
            if len(password) > 0:
                sys.stdout.write("\b \b")
                password = password[:-1]
        elif ch.isprintable():
            if maskchar != None:
                sys.stdout.write(maskchar)
            password += ch

def __getpass_win() -> str:
    """
    获取密码 win
    
    Parameters:
    
    Returns:
        str - 输入内容
    """
    import msvcrt
    chars = []   
    while True:
        try:
            newChar = msvcrt.getch().decode(encoding="utf-8")  
        except:
            continue
        if newChar in '\r\n': # 如果是换行，则输入结束               
            break   
        elif newChar == '\b': # 如果是退格，则删除密码末尾一位并且删除一个星号   
            if chars:    
                del chars[-1]   
                msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格  
                msvcrt.putch( ' '.encode(encoding='utf-8')) # 输出一个空格覆盖原来的星号  
                msvcrt.putch('\b'.encode(encoding='utf-8')) # 光标回退一格准备接受新的输入                   
        elif newChar.isprintable():  
            chars.append(newChar)  
            msvcrt.putch('*'.encode(encoding='utf-8')) # 显示为星号  
    return (''.join(chars) )  

def input_passwd() -> str:
    """
    获取密码输入 将输入的字符替换为*
    
    Parameters:
    
    Returns:
        str - 输入内容
    """
    import platform
    sys = platform.system()
    if sys == "Windows":
        return __getpass_win()
    elif sys == "Linux":
        return __getpass_linux("*")

if __name__ == "__main__":
    print("Please input your password: ")
    passwd=input_passwd()
    # 加密数据
    crypto = base64.b64encode(rsa.encrypt(passwd.encode('utf8'), pubkey)).decode('utf8')
    pyperclip.copy(crypto) #存入剪贴板
    print("\n==============================")
    print("Your encryptedPassword (also in your clipboard): \n")
    print(crypto)
    print("\n")
    input() #pause