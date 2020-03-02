getScripts = async function(){
    var scripts = await document.scripts;  
}

chrome.webRequest.onBeforeRequest.addListener(function(details){
    console.log("request", details)
})