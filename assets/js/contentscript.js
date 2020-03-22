
   
    browser.runtime.sendMessage({URL : window.location.href}, function(response) {
       
        console.log("Response from Background script: ", response);
    });



// // document.addEventListener('DOMContentLoaded', (event) => {
//     window.performance.mark('Begin');
//     window.performance.mark('End');
//     var resources = window.performance.getEntries();
//     console.log("Resources: ", resources)
//     for (i = 0; i < resources.length; i++){
//         if (resources[i].initiatorType == "script"){
//             console.log ("script: ", resources[i].name)
//         }
//     }
    
// //   });