var defaultLabels = [];
var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
chrome.storage.local.get(['default'], function(result) {
    var obj;
    if (result.key ===undefined || result.value === null){ //if not in google storage 

        // console.log("does not exist", result.key)
        var settingDefault = []
        labels.forEach((element) =>{
            obj ={
                label: element,
                status: Math.round(Math.random())
            }
            settingDefault.push(obj)// enables all scripts - does not block anything unless set otherwise
        })


        console.log("default setting", settingDefault)
        chrome.storage.local.set({default: settingDefault}, function() { }) //store default settings in chrome storage     
        defaultLabels = settingDefault;
    }
    else{
        console.log("exists", result.key)
        defaultLabels = result.value;
    }

 
  });


export {
    defaultLabels
};
