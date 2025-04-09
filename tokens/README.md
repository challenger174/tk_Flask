该文件夹下的内容为token相关的任务，包含：token获取和续签的任务：

目前设置参数为token过期前3天的时候会自动续签token，并将数据update到mysql当中，
对应的参数为：conf.yml下的

token注册获取的任务：
    

```markdown
token续签的任务：refresh_token.py：
tk_util.refresh_frequency： 来控制刷新时间间隔
refresh_token：来进行判断任务启动后是否进行刷新
get_token: 获取token信息，通过配置文件当中的shop_id获取，观察mysql数据库进行选择
```
