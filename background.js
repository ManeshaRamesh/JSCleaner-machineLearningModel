chrome.runtime.onInstalled.addListener(function (object) {
    chrome.tabs.create({url: "firstrun.html"}, function (tab) {
        
    });
});