
import * as Database from './database.js';
import * as Constants from './constants.js';


var timedout = false;
window.jscleaner = {}
window.jscleaner.tabs = [];

window.jscleaner.labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
window.jscleaner.Error = {
    DATABASEERROR: "Database error: ", 

}


//////GETTING ALL TABS///////
// function getAllTabs(){
//     chrome.windows.getAll({populate : true}, function (result) {
//         window.jscleaner.tabs = [];
//         var wind;
//         for (wind of result){
//             for(var i = 0; i < wind.tabs.length; i++){
//                 window.jscleaner.tabs.push(wind.tabs[i].url);
//             }
//         }
//         console.log("All tabs", window.jscleaner.tabs)

//     })
// }

// getAllTabs();

// chrome.tabs.onCreated.addListener(getAllTabs);

// chrome.tabs.onRemoved.addListener(getAllTabs);

// chrome.windows.onCreated.addListener(getAllTabs);

// chrome.windows.onRemoved.addListener(getAllTabs);

//////GETTING ALL TABS///////








//if they are there get disbaleds scripts
//if not add to database




//gest the default setting ands tores 

// chrome.storage.local.get(['default'], function(result) {
//     var obj;
//     if (result.key ===undefined || result.value === null){ //if not in google storage 

//         // console.log("does not exist", result.key)
//         var settingDefault = []
//         window.jscleaner.labels.forEach((element) =>{
//             obj ={
//                 label: element,
//                 status: 1
//             }
//             settingDefault.push(obj)// enables all scripts - does not block anything unless set otherwise
//         })


//         console.log("default setting", settingDefault)
//         chrome.storage.local.set({default: settingDefault}, function() { }) //store default settings in chrome storage     
//         Constants.defaultLabels = settingDefault;
//     }
//     else{
//         console.log("exists", result.key)
//         Constants.defaultLabels = result.value;
//     }

 
//   });



//   chrome.storage.local.get(['LabeledScripts'], function(result) {
//     if (result.key ===undefined || result.value === null){  //if there are no labelled scripts 
//         // console.log("does not exist", result.key)
//         var labeledScripts = null

//         // console.log("default setting", labeledScripts)
//         chrome.storage.local.set({LabeledScripts: labeledScripts}, function() { }) //set null value  
        
//     }
//     else{
//         console.log("exists", result.key)
//     }

 
//   });


  chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {

      console.log(request.url)
        
    });
chrome.runtime.onInstalled.addListener(function (object) {
    // chrome.tabs.create({url: "settings.html"}, function (tab) {
        
    // });
    
    // chrome.storage.local.remove(['default']);

 
    
});


// var storedScript = []; //scripts are alreadys stored
var scripts = []; //scripts names extracted
var labeledScripts = []; //labaled scripts
window.jscleaner.Constants = {}
window.jscleaner.Constants.labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
Database.createDatabase().then((result) =>{
    
    Database.loadData(result).then(()=>{


        // console.log("The scripts that need to be bocked", Database.BlockTheseScripts)
        
        setInterval(() => {
            // console.log("Labelled Scripts size", Database.labelledScript)

            // console.log('Timed Out', timedout);
            // timedout = true;

            //every 3 seconds is checks if there any scripts that need to be sent to the eproxy 
            if(scripts.length){
                ////////////////////////Proxy replacement//////////////////////////
                var script;
                var tempObj = {};
                //get response say in labeled scripts
                for (script of scripts){
            
                    tempObj = {
                        name: script, 
                        label: window.jscleaner.Constants.labels[Math.floor(Math.random() * window.jscleaner.Constants.labels.length)], 
                        accuracy: 0.1
                    }
                    labeledScripts.push(tempObj); //teh proxy returns an array of objects
                }
    
            ////////////////////////Proxy replacement//////////////////////////
                //add labelled scripts to the database.
                // console.log("print add item - here2")

                var script;
                for (script of labeledScripts){
                    Database.addItem(script,'scripts');
                }
            scripts = [];
            labeledScripts = [];
        }
        }, 5000);

        browser.storage.onChanged.addListener(Database.logStorageChange);

        chrome.webRequest.onBeforeSendHeaders.addListener(
            
            function(details) {
                // console.log(details.url)
                
                if (details.type == "script"){ //check if url is of type script
                    //only adds those scripts that have not been labelled
                    var found = false;
                    //check if the scripts can be found

                    if (Database.labelledScript.get(details.url)){
                        found = true;
                    }
                    // for(var i = 0; i < Database.scripts.length; i++) {
                    //     if (Database.scripts[i].name == details.url) {
                    //         found = true;
                    //         break;
                    //     }
                    // }
                    console.log("Should script be labelled?: ", details.url, !found  , !scripts.includes(details.url) )
                    if (!found && !scripts.includes(details.url)) {//if is script is in database
            
                        // console.log('Needs to be sent to proxy server')
                        //check if teh url is already in local storage
                        scripts.push(details.url)
                        // console.log ("pushed", details.url,scripts.length)
                    }


                }
                console.log("conditions: scriptlength and timeout", scripts.length)

            
                if(scripts.length == 5) {//add a timer
                    // console.log("print add item - here1")
                    // timedout = false;
                    
                    //send an ajax request
                    
                     
                            ////////////////////////Proxy replacement//////////////////////////
                            var script;
                            var tempObj = {};
                            //get response say in labeled scripts
                            for (script of scripts){
                        
                                tempObj = {
                                    name: script, 
                                    label: window.jscleaner.Constants.labels[Math.floor(Math.random() * window.jscleaner.Constants.labels.length)], 
                                    accuracy: 0.1
                                }
                                labeledScripts.push(tempObj); //teh proxy returns an array of objects
                            }
                
                        ////////////////////////Proxy replacement//////////////////////////
                            //add labelled scripts to the database.
                            // console.log("print add item - here2")

                            var script;
                            for (script of labeledScripts){
                                Database.addItem(script,'scripts');
                            }
                        scripts = [];
                        labeledScripts = [];
                

                }



                    // console.log("These are the Labeled Scripts: ",labeledScripts);
                    // chrome.storage.local.set({LabeledScripts: labeledScripts}, function() { })

                // }
            //   return {requestHeaders: details.requestHeaders};
            },
            {urls: ["<all_urls>"]},["requestHeaders"]);

    // create and event and event listener for the timer

    
    
  
        




    })
});

// chrome.webRequest.onHeadersReceived.addListener(function(details){

//     for (item of labeledScripts){
//         if (item.name === details.url){
//             console.log("Reponse stuff: ", details)
//             console.log ("Print the url and the label", details.url, item.label)
//             // console.log("Print shit: ",details.responseHeaders[5].name, details.responseHeaders[5].value);
//             let header = details.responseHeaders.find(e => e.name.toLowerCase() === "access-control-allow-origin") ;
//             details.responseHeaders.pop (headers)
            
//             return {responseHeaders: details.responseHeaders};
//         }
//         else{

//         }
//     }

// }, {urls: ["<all_urls>"]}, ["blocking", "responseHeaders"])


  
  /////////////////////////////////Blocking after receiving the response
  
    //   browser.webRequest.onHeadersReceived.addListener( function(details) {
    //     // ... your code that checks whether the request should be blocked ...
    //     // console.log("onHeadersRecieved")
    //     var item;
    //     // console.log("The URLss : ", details.url, labeledScripts)
    //     // console.log("headers recieved", labeledScripts)
    //     // return Database.iterate('scripts',function(value){
    //     //     return new Promise((resolve, reject) =>{
    //     //         if(value.name === details.url){
    //     //             if (value.label === "Social"){

    //     //                 // console.log(value)
    //     //                 var scheme = /^https/.test(details.url) ? "https" : "http";
    //     //                 chrome.tabs.update(details.tabId, {
    //     //                     url: scheme + "://robwu.nl/204"
    //     //                 });
    //     //                 resolve({cancel: true});
    //     //             }
    //     //             else{
    //     //                 resolve(null); 
    //     //             }
    
    //     //         }
    //     //         else{
    //     //             resolve(null); 
    //     //         }

    //     //     })

    //     // } )

    //     // if (details.frameId === 0) { // Top frame, yay!
    //     //     var scheme = /^https/.test(details.url) ? "https" : "http";
    //     //     chrome.tabs.update(details.tabId, {
    //     //         url: scheme + "://robwu.nl/204"
    //     //     });
    //     //     return;
    //     // }
    //     // return {cancel: true};
    //     // var result = await Database.blockURLS('scripts', details);        
    //     // return result;
    //     for (item of Database.scripts){
    //         // console.log(details.url, item)

    //         if (details.url ===  item.name) { // Top frame, yay!
    //             // if (item.label == "Video"){
    //                 console.log('should be blocked', details.url)
    //             var scheme = /^https/.test(details.url) ? "https" : "http";
    //             chrome.tabs.update(details.tabId, {
    //                 url: scheme + "://robwu.nl/204"
    //             });
    //             return {cancel: true};
    //             // var scheme = /^https/.test(details.url) ? "https" : "http";
    //             // return {redirectUrl: scheme + "://robwu.nl/204" };
                
    //         }
    //     }
    //     return;
    // }, { urls: ["<all_urls>"]}, ["responseHeaders", "blocking"]);



    // ////DATABASE SHIT


