## 武汉大学课程历史给分批量获取脚本

* Author：[NagisaCo](https://github.com/NagisaCo)
* Github：https://github.com/NagisaCo/CourseGrade

> 如有侵权，请联系我删除
>
> 禁止用于非法用途，违者后果自负

## 环境要求

* python3.7及以上
* MySQL数据库(可选)

## 使用方法

### 1. 下载项目
```shell
git clone https://github.com/NagisaCo/CourseGrade.git
cd CourseGrade
pip install -r requirements.txt
```

如果执行`pip install`时提示`-bash: pip: command not found`
就是`pip`命令没有安装，执行下方命令安装即可，然后再执行即可

```shell
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

### 2. 填写配置文件

若目录下不存在`config.ini`配置文件，请先执行`python CourseGrade.py`或双击`CourseGrade.py`后获取配置文件模板

![WL3BIU.png](https://z3.ax1x.com/2021/07/30/WL3BIU.png)

根据个人实际填写配置文件，详细填写方法请见[配置文件填写](#配置文件填写)

![WL86k8.png](https://z3.ax1x.com/2021/07/30/WL86k8.png)

### 3. 执行程序

运行`CourseGrade.py`得到运行结果，结果保存至`result`文件中，可使用`__loadFile()`函数加载。若配置数据库属性，则可以从数据库中查看结果

![WLGx2Q.png](https://z3.ax1x.com/2021/07/30/WLGx2Q.png)

## 配置文件填写

```ini
#config.ini
[base]
htmlsource = 

[bkxk]
gnmkdm = N253512
studentnum = 
encryptedpassword = 

[mxj]
token = 

[db]
server = 
username = 
encryptedpassword = 
database = 

#[bkxk]和[db]中的encryptedPassword项为经过Encryptor.py加密后的密码
#[db]不填写自动关闭数据库存储任务
```

| 参数                       | 注释                        |   值                 |
|---------------------------|-----------------------------|---------------------|
| base.htmlsource           | 课程id获取来源                | 本地html路径或者url   |   
| bkxk.gnmkdm               | 暂不清楚该项的作用             | 默认值为N253512      |  
| bkxk.studentnum           | 学号，登录选课网页的用户名      | 13位数字             |  
| bkxk.encryptedpassword    | 加密后的登录选课网页密码        | Base64              | 
| mxj.token                 | 小程序梦想珈登录token       | 32位token            |
| db.server                 | 数据库服务器地址              | 域名或ip地址          |  
| db.username               | 数据库登录用户名              | 字符串                |   
| db.encryptedpassword      | 加密后的数据库登录密码         | Base64               |
| db.database               | 数据库名称                   | 字符串                |

### base
- htmlsource

  > `htmlsource`为课程id获取来源
  
  在选课界面，使用`F12`调出浏览器(以Chrome为例)的`Console(控制台)`界面，执行以下代码加载全部可选课程

  ```js
  while(document.getElementById("isEnd").value!=="true") {loadCoursesByPaged();}
  ```

  ![WLNTW8.png](https://z3.ax1x.com/2021/07/30/WLNTW8.png)

  将静态页面另存为html保存至本地，或者http服务器上

  > 在网页空白处 `右键`
  > 选择 `另存为`
  > 选择 `保存类型：网页，全部` 
  
  在`htmlsource`中填写文件路径或url地址
  
```ini
[base]
htmlsource = ./自主选课.html
```

### bkxk
- gnmkdm

  > 暂不清楚该项的作用，猜测为区分课程表，默认值为`N253512`，请在选课页面的url中获取相应值

  ![WLdRL4.png](https://z3.ax1x.com/2021/07/30/WLdRL4.png)

- studentnum

  > 学号，即登录选课网页的用户名

- encryptedpassword

  > 登录选课网页的密码

  为避免明文保存密码，请使用`Encryptor.py`加密登录密码后填写加密后的密码

  执行`python Encryptor.py`或双击`Encryptor.py`，在窗口中输入登录密码，回车提交后获取加密后密码。加密密码同时也存储在剪贴板中，可使用`Ctrl+V`直接粘贴至`encryptedpassword`中

  ![WLwDne.png](https://z3.ax1x.com/2021/07/30/WLwDne.png)

```ini
[bkxk]
gnmkdm = N25xxxx
studentnum = 20xxxxxxxxxxx
encryptedpassword = CB3mBPjM5h4ly3IHcu3aGj+2vYE/FX6N/QNgr4FkBwdw+mDVmCboXCbGm3j//dNVWx8A5wknKsLrx/ZoHpGbGLmlQNd6EZ/Ip5lHRXcbfwH94LRApu8GaIk/X+ngUG3b1tK7cwiE05r0sTIMoJ16ysIXb6V/rnVj7pwZVHvw414=
```

### mxj
- token

  > 小程序`梦想珈`登录token

  该值需要对微信小程序抓包获得，以下简要介绍使用Mumu模拟器抓包的过程。已安装xposed框架的安卓手机可采用类似步骤进行抓包。

  1. 打开root权限，安装xposed框架，安装并激活JustTrustMe模块<https://www.jianshu.com/p/dfea1a84bb3b>
  2. 配置代理，安装Charles证书，设置SSL抓包<https://blog.csdn.net/weixin_38863166/article/details/104941825>
  3. 安装32位版本微信<https://dldir1.qq.com/weixin/android/weixin809android1940.apk>
  4. 登录微信，开启抓包，打开`梦想珈`小程序，在`Structure`中找到`https://www.campuses.cn`域下的任意一个请求，点击`Contents`选项卡，选择上半区域的`Headers`，复制`token`
   
   ![WLHGHH.png](https://z3.ax1x.com/2021/07/30/WLHGHH.png)

```ini
[mxj]
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
### db

当db项目为空时，自动关闭更新数据库操作  

数据库格式可通过`course_grade.sql`导入

1. 登录数据库

  ```shell
  mysql -u root -p
  ```

2. 新建数据库并导入sql文件
  
  ```sql
  CREATE DATABASE course_grade;
  USE course_grade;
  SOURCE ./course_grade.sql;
  ```
或者使用`Navicat`等GUI界面操作

![WLLAu8.png](https://z3.ax1x.com/2021/07/30/WLLAu8.png)]

- server

  > 数据库服务器地址

- username

  > 数据库登录用户名

- encryptedpassword

  > 数据库登录密码，经过`Encryptor.py`加密

- database
  
  > 数据库名称

```ini
[db]
server = localhost
username = course_grade
encryptedpassword = pZE7DFk4Ral78riF7bwt3u5wk8Xf34RZw0/ZEx3OtdxoXXK6rXm+xaCut3Dvr54W6u+KrmhjwlrID19WBLd4+AIDEQKZo4LofRWCPdUJdAV8qmkFpV7OoqXJY6KykYHu5saH9Saq5cLVCyHQe0pVieYYePkALjB75jvoPZDtiR4=
database = course_grade
```

## 结果
- 本地Result保存

  查询结果由`__storeFile()`函数将`CourseInfo`类的`List`存储至本地，可由`__loadFile()`重新加载，无需再次进行爬虫操作。

- 数据库保存
  
  当配置文件中db项目填写有效后，会自动更新数据库中的内容。

  ![WOVLvT.png](https://z3.ax1x.com/2021/07/30/WOVLvT.png)