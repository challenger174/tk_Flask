## serve项目结构

load_1688_data_parse为当前页面的主入口，包含内容为读取多线程队列，并进行数据格式转换为的主体,
其中parse_util文件夹下存放的是较为复杂的每个模块的解析逻辑和任务

```
serve:
    load_1688_data_parse: 解析1688获取到的原始数据，并作为parse_util的上游聚合类，整体的处理逻辑在当前逻辑当中展示，
                          其中title 、 等简单逻辑在当前python当中实现
                     
parse_util：
    - get_description: 商品的描述信息数据，最终生成html嵌入到前端网页当中，其中通过gpt生成动态的网页html,并且通过gpt识别图片是否可用，并且将商品的一些描述信息添加到html当中
    - main_imgs: 处理商品的主图的函数
    - get_property: 商品重量和尺寸信息
    - get_product_attributes: 获取并上传商品属性
    - get_skus: 获取sku信息，并构建json

```
关注这个： certifications： FDA认知相关  

https://partner.tiktokshop.com/docv2/page/6509de61bace3e02b7489cba?external_id=6509de61bace3e02b7489cba#%E5%9B%9E%E5%88%B0%E9%A1%B6%E9%83%A8

```markdown
- publish_product：进行商品发布的主任务
```