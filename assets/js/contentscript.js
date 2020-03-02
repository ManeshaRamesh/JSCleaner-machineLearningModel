

var Constants = {}

Constants.labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']



new Promise((resolve, reject) =>{
    scriptLabels = {}
    performance.mark('Begin');
    performance.mark('End');
    var scriptNames = new Array(); 
    var webObjects = window.performance.getEntries();
    console.log("List of JS scripts: ")
    for (i = 0; i < webObjects.length; i++){
            
        if (webObjects[i].initiatorType == "script"){
            scriptNames.push(webObjects[i].name);
            scriptLabels[webObjects[i].name] = null;
            //assigns random labels
            //dummy assignment of labels - should make an ajax request to the proxy
            scriptLabels[webObjects[i].name] = Constants.labels[Math.floor(Math.random() * Constants.labels.length)];
            // console.log(webObjects[i].name);
        }
    }
    // console.log("All the scripts in this page: ",scriptLabels);
    resolve(scriptLabels)


}).then((result)=>{
    var LabeledScriptsObject = {}
    console.log(result)
    var tempObj = {}; 
    for (label of Constants.labels){
        LabeledScriptsObject[label] = []
        for (script in result){
            
    //         console.log("Debug",script, script[0], script[1])
            if (result[script] === label){
                // console.log("script?? ", script, label, result[script], result[script] === label)

                tempObj[script] =  "enabled";
                // console.log("tempObject", tempObj)
                LabeledScriptsObject[label].push(tempObj)
                tempObj = {}
            }
    //     // }
        }
    }
    var urlObj = {}; 
    urlObj[window.location.href] = {
        default: true,
        scripts:  LabeledScriptsObject
    };
    // console.log("Print the Obj: ", urlObj)
    chrome.storage.local.set(urlObj, function() { })
    chrome.storage.local.get([window.location.href], function(result) {
        // console.log("stored??", result)
    })
})




/*
List of things a content script does:
1) checks if the url is in local storage
2) if it is not there, it makes an ajax request to the proxy and sends the the url and list of scripts
3) if it is there it will load the lables


*/