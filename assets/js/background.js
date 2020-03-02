
window.jscleaner = {}
window.jscleaner.labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']



chrome.storage.local.get(['default'], function(result) {
    if (result.key ===undefined || result.value === null){ //if installed for the first time or the default settings are cleared
        // console.log("does not exist", result.key)
        var settingDefault = {}
        window.jscleaner.labels.forEach((element) =>{
            settingDefault[element] = "enabled"; // enables all scripts - does not block anything unless set otherwise
        })

        console.log("default setting", settingDefault)
        chrome.storage.local.set({default: settingDefault}, function() { }) //store default settings in chrome storage     
        
    }
    else{
        console.log("exists", result.key)
    }

 
  });

  chrome.storage.local.get(['LabeledScripts'], function(result) {
    if (result.key ===undefined || result.value === null){ //if installed for the first time or the default settings are cleared
        // console.log("does not exist", result.key)
        var labeledScripts = null

        console.log("default setting", labeledScripts)
        chrome.storage.local.set({LabeledScripts: labeledScripts}, function() { }) //store default settings in chrome storage     
        
    }
    else{
        console.log("exists", result.key)
    }

 
  });


chrome.runtime.onInstalled.addListener(function (object) {
    chrome.tabs.create({url: "settings.html"}, function (tab) {
        
    });
});

