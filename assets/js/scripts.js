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

var accordian = document.getElementById("accordionLabels");
var content = null;
var script = "scripts go here";
var description = "description goes here"
var contentType = accordian.getAttribute('data-content-type');
if ( contentType == "scripts"){
    content = script;
}
else if (contentType =="description")  {
    content = description
}
var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
chrome.tabs.query({active:true,currentWindow:true},function(tabArray){
  // console.log("window url",tabArray[0].url);
  windowURL = tabArray[0].url;
  chrome.storage.local.get([windowURL], function(result) {
    var bar;
    // console.log("result",  result,  result.value , result.key)
    // if (result.key ===undefined || result.value === null){ //if installed for the first time or the default settings are cleared
    if (!result.hasOwnProperty (windowURL)){
    console.log("yess")
      bar = document.createElement('div');
      bar.innerHTML = " <div> Please reload the page </div> " 
      accordian.appendChild(bar)
    }
    else {
      var scriptsObject = result[windowURL];
      
      for (var label = 0; label < labels.length ; label++){
          console.log("here2")
          bar = document.createElement('div');
          bar.innerHTML = "   <div class='card z-depth-0 bordered'> \
          <div class='card-header' id='heading"+labels[label]+"'>\
            <h5 class='mb-0'>\
            <div class ='row'>\
              <div class='col label'>\
              <button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+labels[label].replace(' ', '')+"'\
                aria-expanded='false' aria-controls='collapse "+labels[label].replace(' ', '')+"'>\
                " + labels[label]+" \
              </button> </div> \
              <div class='col toggle-site'> \
              <input type='checkbox' class = 'toggle-script' data-offstyle='success' data-onstyle='danger' data-on='Disabled' data-off='Enabled' data-toggle='toggle'> </div>\
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
        </div>"
        accordian.appendChild(bar)
      }
    }
  
  })
});
//  window.location.href)




}, false);

