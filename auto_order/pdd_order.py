# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : pdd_order.py
@Author   :wangmaosheng
@Date     : 2025/3/23 23:23
@Desc:    : 模拟下单的主入口
"""



import time
from appium import webdriver
from appium.options.android import UiAutomator2Options

# 配置 Appium 所需的参数
desired_caps = {
    "platformName": "Android",  # 平台名称，这里以 Android 为例
    "platformVersion": "15",  # 替换为你的安卓版本号
    "deviceName": "83b56737",  # 替换为你的设备名称
    "appPackage": "com.xunmeng.pinduoduo",  # 拼多多的包名
    "appActivity": ".ui.activity.MainActivity",  # 拼多多的启动 Activity
    "noReset": True,  # 不重置应用状态
    "skipDeviceInitialization": True,  # 跳过设备初始化步骤
    "automationName": "UiAutomator2"  # 明确指定使用 UiAutomator2 驱动
}

options = UiAutomator2Options()
options.load_capabilities(desired_caps)

# 连接到 Appium 服务器
driver = webdriver.Remote('http://localhost:4723', options=options)

try:
    # 等待应用启动
    time.sleep(10)

    # 这里可以添加页面跳转的代码，例如点击某个元素跳转到其他页面
    # 假设我们要点击搜索框，你需要根据实际的元素定位方式进行修改
    # search_box = driver.find_element("id", "com.xunmeng.pinduoduo:id/你的搜索框 ID")
    # search_box.click()
    #
    # # 等待一段时间以便观察效果
    # time.sleep(5)

except Exception as e:
    print(f"发生错误: {e}")
finally:
    # 关闭应用
    driver.quit()
