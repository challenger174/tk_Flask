# 自动化下单工具根目录
技术：appium + mysql + python + 

### 前提：
- 需提前配置好android sdk：
  

```shell
# 查看当前版本
appium -v 
# adb的版本
adb -v 
# 查看当前电脑链接设备数量以及状态，如果显示 "unauthorized"，说明手机上还没点确认授权，解锁手机点击“允许调试” device" 表示连接成功
adb devices 

# 确认连接的设备信息
adb shell getprop ro.product.model

# 获取拼多多App的包和启动Activity
adb shell pm list packages | grep pinduoduo
# 给排毒多发送一组随机数，检测当前App
adb shell monkey -p com.xunmeng.pinduoduo -v 1
# 查看当前系统的版本号
adb shell getprop ro.build.version.release
# 获取服务状态信息，window会输出窗口相关的信息
adb shell dumpsys window | grep mCurrentFocus
```
当前窗口为拼多多软件
![img.png](img/img.png)

```shell

# (启动appium)
appium -a <主机地址> -p <端口号>
#简洁模式只需要appium server 即可

# 启动服务的时候放宽一些安全权限
appium --relaxed-security

```