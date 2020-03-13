document.addEventListener('DOMContentLoaded', function() {



var contentScripts = function(object, label){
  // return JSON.stringify(object.scripts[label]) 
  var array = object.scripts[label]
  var string = '<ul style="list-style-type:none;">';
  if (array.length){
    for (element of array){
      string = string + '<li><div style="overflow: hidden;">' +JSON.stringify(Object.keys(element)[0]).split('"').join('').split('\\').pop().split('/').pop();; + " </div> </li>";
    }
  }
  else {
    return "none"
  }
  string = string + '</ul>'
  return string;
  
}  



// var accordian = document.getElementById("accordionLabels");
var checkbox = {
  enabled : "", 
  disabled : "checked"
}

var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
chrome.tabs.query({active:true,currentWindow:true},function(tabArray){
  // console.log("window url",tabArray[0].url);
  windowURL = tabArray[0].url;
  //check if url is in chrome storage
  chrome.storage.local.get([windowURL], function(result) {
    var bar;
    var defaultFlag = false;
    // console.log("result",  result,  result.value , result.key)
    // if (result.key ===undefined || result.value === null){ //if installed for the first time or the default settings are cleared
    if (!result.hasOwnProperty (windowURL)){
    //if the website is not in chrome storage ask user to reload the page
      bar = document.createElement('div');
      bar.innerHTML = " <div> Please reload the page </div> " 
      accordian.appendChild(bar)
    }
    else { // if it is in chrhome storage
      var scriptsObject = result[windowURL];
       new Promise((resolve, reject)=>{
        if (scriptsObject.default == true){ //if the website's setting is default

        if (scriptsObject.default = true){
          chrome.storage.local.get(['default'], function(result) {
            resolve(result.default) //resolve the default object
          })
  
        }

        else{
          resolve(null);
        }
      }
      else{
        resolve (null); //resolve null if the website's default is false
      }

       }).then((defaultObject)=>{
                defaultFlag = true;
               console.log("Object: ", defaultObject);
               if (defaultObject === null) {
                var body =  document.getElementById("body");
                var mode = document.createElement('div');
                mode.className = "row setting center";
                mode.innerHTML = '  <div class="col">  <label class="container"> Default \
                  <input type="checkbox"> \
                  <span class="checkmark" id="defaultCheckbox"></span> \
                  </label> </div>   '
                body.appendChild(mode);
                
                
               }
               else{
                 defaultFlag = false;
                  var body =  document.getElementById("body");
                  var mode = document.createElement('div');
                  mode.className = "row setting center";
                  mode.innerHTML = '  <div class="col">  <label class="container"> Default \
                    <input type="checkbox" checked="checked" > \
                    <span class="checkmark" id="defaultCheckbox"></span> \
                    </label> </div>   '
                  body.appendChild(mode);
      for (var label = 0; label < labels.length ; label++){
        console.log("here2")

        // if default == true
        // this is the button with the default and the custom mode
        

        bar = document.createElement('div');
        bar.className = "row body scriptLabels";
        bar.innerHTML = "                      <div class='accordion' id='accordionLabels' data-content-type='scripts'>  <div class='card z-depth-0 bordered'> \
        <div class='card-header' id='heading"+labels[label]+"'>\
          <h5 class='mb-0'>\
          <div class ='row'>\
            <div class='col label'>\
            <button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+labels[label].replace(' ', '')+"'\
              aria-expanded='false' aria-controls='collapse "+labels[label].replace(' ', '')+"'>\
              " + labels[label]+" \
            </button> </div> \
            <div class='col toggle-site'> \
            <label class='switch'>\
              <input type='checkbox' " + checkbox[defaultObject[labels[label]]]+">\
              <span class='slider'></span>\
            </label> \
          </h5>  \
        </div>  \
        <div> \
        <div id='collapse"+labels[label].replace(' ', '')+"' class='collapse' aria-labelledby='heading"+labels[label].replace(' ', '')+"' \
          data-parent='#accordionLabels'> \
          <div class='card-body'> \
            "+ contentScripts(scriptsObject, labels[label])
            
            +" \
          </div> \
        </div> \
      </div> \
      </div>"
      body.appendChild(bar)
    }

  }

  $(document).ready(function () {
    $("#defaultCheckbox").click(function (){
      console.log("before", defaultFlag)

      if (defaultFlag){
        defaultFlag = false;
      }
      else{
        defaultFlag = true
      }
      console.log("after", defaultFlag)
      
      
      chrome.storage.local.get([windowURL], function(result) {
        result[windowURL].default = defaultFlag;
        console.log("after", result)
        var tempObject = {}
        tempObject[windowURL] = result[windowURL]
        // chrome.storage.local.set({default: settings}, function() { })
      })
    })

  })


       })


    }
  
  })
});
//  window.location.href)




}, false);
