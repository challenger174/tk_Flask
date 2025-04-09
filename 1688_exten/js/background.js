// (function(){chrome.runtime.onInstalled.addListener((()=>{console.log("插件已安装")}))})();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "messgae_detail_to_flask") {
        console.log("Data to send:", message.data);
        fetch("http://127.0.0.1:5001/1688/commodity_msg", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(message.product_msg)
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Data synced successfully:", data);
            sendResponse({ status: "success", data });
        })
        .catch((error) => {
            console.error("Error syncing data:", error);
            sendResponse({ status: "error", error: error.message });
        });

    // 表示响应是异步的
    return true;
    }
});