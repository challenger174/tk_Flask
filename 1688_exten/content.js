function sleep(min, max) {
  const randomDelay = Math.floor(Math.random() * (max - min + 1)) + min;  // 生成 3 到 10 秒之间的随机数
  return new Promise(resolve => setTimeout(resolve, randomDelay * 1000));  // 延迟时间以毫秒为单位
}

async function wait_load(path){
  while(!document.querySelector(path)){
    await sleep(1);
  }
}

function add_button(){
  const start = document.querySelector("#submitOrder.module-od-submit-order > .action-button-list");
  const div_button = document.createElement("div");
  div_button.className = "action-button v-button";
  const inner_str = `
    数据采集
  `
  div_button.style.backgroundColor='#ffe4db';
  div_button.style.border="none";
  div_button.style.padding="10px 20px";
  div_button.style.borderRadius="20px";
  div_button.style.fontSize="16px";
  div_button.style.cursor="pointer";
  div_button.style.width="120px";
  div_button.style.textAlign="center";
  div_button.style.color='#ff4000';
  div_button.innerHTML=inner_str;
  div_button.style.marginLeft="10px";
  // div_button.style.marginTop="10px";
  start.appendChild(div_button);
  return div_button;
}

function listener(div_button){
  div_button.addEventListener("click", crawl_script);
}

function crawl_script(){
  // 进行数据的抓取
  console.log("监听点击之前");
  commodity_msg();
  console.log("监听点击之后");
  // 网络传输给对应的服务器当中
}


function commodity_msg(){
  product_msg={};
  const imgs = document.querySelector(".od-gallery-turn > .od-gallery-turn-outter-wrapper");
  const img_tags = imgs.querySelectorAll(".od-gallery-turn-item-wrapper > img");
  img_urls = []
  for(let img_tag of img_tags){
    const img_url = img_tag.getAttribute("src");
    img_urls.push(img_url);
  }
  product_msg.img_urls = img_urls;
  const title = document.querySelector("#productTitle > .module-od-title > .title-content > h1").innerText;
  product_msg.title = title;
  product_msg.page_url=window.location.href; // 当前页面的url
  console.log("标题,照片OK")

// sku列表信息
  const skus_format = {}; 
  const skus = []
  const skus_list = document.querySelector("#skuSelection > div.module-od-sku-selection.cart-gap");
  if(skus_list.children.length >2){
    console.log("sku的分类大于两种");
    const labels = skus_list.querySelectorAll("div.feature-item")[0];
    // const laber_name = labels.querySelector(".feature-item-label > h3").innerText;
    const skus_button = labels.querySelectorAll(".transverse-filter > .sku-filter-button.v-flex");
    for(let button of skus_button){
      console.log(button.innerHTML);
      const img_doc =  button.querySelector("div.ant-image.label-image-wrap.v-image-wrap > img");
      let img_url = '';
      if(img_doc === null){
        img_url = '';
      }
      else{
        img_url = img_doc.getAttribute("src");
      }
      const name = button.querySelector("span").innerText;
      console.log("点击之前");
      button.click();
      sleep(1);
      console.log("点击成功");
      const prices = skus_list.querySelectorAll("div.feature-item")[1];
      const label_name = prices.querySelectorAll(".expand-view-list > .expand-view-item.v-flex");
      const spec = [];
      for (let label of label_name){
        const name = label.querySelector(".v-flex > span").innerText;
        const sku_price = label.querySelector("span.item-price-stock").innerText;
        const child = {
          "name": name,
          "sku_price": sku_price
        };
        spec.push(child)
      }
      const one_tag = {
        "img_url": img_url,
        "name": name,
        "child_skus": spec
      };
      skus.push(one_tag);
    }
    skus_format['skus'] = skus;
    skus_format['data_stye'] = '2';
  }
  else{
    console.log("sku的label小于两种")
    const formats = document.querySelectorAll(".module-od-sku-selection.cart-gap > .feature-item > .expand-view-list > .expand-view-item.v-flex");
    for(format of formats){
      const img_v1 = format.querySelector(".v-flex > .ant-image.v-image-wrap.item-image-icon > img");
      let current_sku_img = '';
      if(img_v1){
        current_sku_img=img_v1.getAttribute("src"); 
      }
      const sku_name = format.querySelector(".v-flex > span").innerText;
      const sku_price = format.querySelector("span.item-price-stock").innerText;
      sku_data={
        "sku_img": current_sku_img,
        "sku_name": sku_name,
        "sku_price": sku_price
      }
      skus.push(sku_data);
    }
    skus_format['data_stye'] = '1' // 相当于sku不是交叉的，比较方便获取,这种有图
    skus_format['skus'] = skus
  }

  product_msg.skus_format=skus_format;
  console.log("sku OK")
  // 快递相关信息：
  const send = document.querySelector(".module-od-shipping-services.cart-gap > .cart-content > span.location").innerText; // 发货地址
  const to = document.querySelector(".module-od-shipping-services.cart-gap > .cart-content > span.service-item > a.recieve-address.v-flex").innerText; // 收货地址
  const courier_fee = document.querySelectorAll(".module-od-shipping-services.cart-gap > .cart-content > .service-item")[1].innerText; // 快递费
  let fee = '';
  if(courier_fee){
    fee = courier_fee;
  }else{
    fee = '包邮';
  }
  const express ={
    "send": get_or_default(send),
    "to": get_or_default(to),
    "courier_fee": get_or_default(fee)
  }
  product_msg.express = express;
  console.log("快递信息 oK");
  // detail 描述：商品属性：如果有的话就采集，没有就放过：
  attribute = {};
  const attributes = document.querySelectorAll("#productAttributes .antd-external-collapse.collapse-body tr.ant-descriptions-row");
  if(attributes){
    for(let attr of attributes){
        const key = attr.querySelectorAll("th.ant-descriptions-item-label > span");
        const value = attr.querySelectorAll("td.ant-descriptions-item-content .field-value")
        for(let i = 0; i<key.length; i++){
          attribute[key[i].innerText] = value[i].innerText;
        }
    }
   product_msg.attribute=JSON.stringify(attribute);
}

  // 商品重量体积：
  const size_weight = document.querySelector(".module-od-product-pack-info.od-collapse-module > .collapse-body")
  if(size_weight){
    // 有相关的信息
    size = {};
    console.log("有重量相关信息");
    const title = size_weight.querySelectorAll("table > thead > tr > th.field-value");
    const value = size_weight.querySelectorAll("table > tbody > tr > td.field-value");
    for(let i = 0; i< title.length; i++){
        size[title[i].innerText] = value[i].innerText;
    }
    // console.log("size: "+JSON.stringify(size));
    product_msg.size=size;
  }
  //商品详情
  const detail = document.querySelectorAll(".module-od-product-description > .od-collapse-module > .collapse-body")
  if(detail){
    // 只保留详情里的图片信息：
    detail_img = msg_detail_parse();
    if(detail_img!==null){
      product_msg.detail_img=detail_img;
    }
  }
  console.log(product_msg);

  chrome.runtime.sendMessage(
    { action: "messgae_detail_to_flask", product_msg},
    (response) => {
        if (response.status === "success") {
            console.log("Data synced successfully:", response.data);
        } else {
            console.error("Data sync failed:", response.error);
        }
    }
);
}


function msg_detail_parse(){
  // 解析详情当中的数据到页面当中:
  let element = document.querySelector('.html-description');
  if(element.shadowRoot){
    detail = {};
    let shadowRoot = element.shadowRoot;  // 获取 Shadow DOM
    detial_img = shadowRoot.querySelectorAll("img");
    imgs=[];
    for(let each_img of detial_img){
       imgs.push(each_img.getAttribute('src'));
    }
    detail.imgs=imgs;
    return detail;
  }
  return null;
}

function get_or_default(dom_data, default_data=''){
  if(dom_data)
  {
    return dom_data;
  }else{
    return default_data;
  }
}

const current_path = window.location.href;
const interval = setInterval(function() {
  const label_father = document.querySelector(".module-od-title > .title-content > h1");
  if(label_father){
  //  加载完成
    console.log("路径匹配");
    clearInterval(interval);
    // 添加任务启动按钮
    const start_div = add_button();
    // 监听按钮
    listener(start_div);
  }else{
    console.log("未完成加载,进行重试");
  }
}, 300);  // 每100毫秒检查一次

