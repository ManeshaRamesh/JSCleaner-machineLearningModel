Constants = {};
Constants.labels = {
Advertising : 0,
Analytics : 1, 
Social : 2, 
Video : 3, 
Utilities:4,
Hosting: 5, 
Marketing: 6, 
"Customer Success": 7, 
Content : 8,
CDN : 9,
"Tag Managment": 10,
Others: 11
}
var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']

document.addEventListener('DOMContentLoaded', function() {


  //add the two modes
  var mode = document.getElementById("mode");
  var radio1 = document.createElement("input");
  radio1.type = 'radio';
  radio1.id = 'radioDefault'
  radio1.name = "radioMode";
  radio1.checked = true; 
  

  var radio1Label = document.createElement("label");
  radio1Label.for = 'radioDefault';
  radio1Label.innerText = "default";

  var mode = document.getElementById("mode");
  var radio2 = document.createElement("input");
  radio2.type = 'radio';
  radio2.id = 'radioCustom'
  radio2.name = "radioMode";


  var radio2Label = document.createElement("label");
  radio2Label.for = 'radioCustom';
  radio2Label.innerText = "custom";
  
  mode.appendChild(radio1);
  mode.appendChild(radio1Label)
  mode.appendChild(radio2);
  mode.appendChild(radio2Label)






  $(document).ready(function () {
    $("#radioCustom").click(function (){
      var checkboxDefault = this;
      var status = $('#'+checkboxDefault.id).is(':checked');
      if (status){

      }
      
    })
  })
}, false);

window.addEventListener('DOMContentLoaded', () => {
  // ...query for the active tab...
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, tabs => {
    // ...and send a request for the DOM info...
    browser.tabs.sendMessage(
        tabs[0].id,
        {from: 'popup', subject: 'DOMInfo'}
        // ...also specifying a callback to be called 
        //    from the receiving end (content script).
        ).then((response)=>{
          console.log("Scripts to be displayed", response)
          var accordian = document.getElementById("accordionLabels");
          var div = document.createElement("div");
          div.id = "accordionlabels";
          div.className = "col";
          accordian.appendChild(div);
          // for (let [key, value] of response) {
          for (label of labels) {
            var scriptwrapper = document.createElement("div");
            scriptwrapper.className = "row";
            // scriptwrapper.innerHTML= "<div class='col-6 scriptName'> " + key + "</div> <div class='col-6 status' style='overflow: hidden; '>"+ JSON.stringify(value) + "</div>"
            scriptwrapper.innerHTML =  "<div class='card z-depth-0 bordered'> \
            <div class='card-header' id='heading"+label.replace(' ', '')+"'>\
              <h5 class='mb-0'>\
                <button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+label.replace(' ', '')+"'\
                  aria-expanded='false' aria-controls='collapse"+label.replace(' ', '')+"'>\
                  " + label+" \
                </button>  \
              </h5>  \
            </div>  \
            <div id='collapse"+label.replace(' ', '')+"' class='collapse' aria-labelledby='heading"+label.replace(' ', '')+"' \
            data-parent='#accordionlabels'> \
              <div class='card-body' id ='scriptsListHere"+label.replace(' ', '')+"'> \
             </div> \
            </div> \
          </div>"
          div.appendChild(scriptwrapper);
          var place = document.getElementById('scriptsListHere'+label.replace(' ', ''))
          for (let [key, value] of response) {
            if (value.label === label){
              document.getElementById('collapse'+label.replace(' ', '')).className = "collapse show"
              place.innerText = place.innerText + key +"/n";

            }
          }
            
          }
        });
  });
});