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


document.addEventListener('DOMContentLoaded', function() {
    console.log("here")
  var accordian = document.getElementById("accordionLabels");

  var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
  var checkbox = {
    1 : "", 
    0 : "checked"
  }
  //get default settings from storage
  new Promise((resolve, reject) =>{
    var defaultObject = {}
    chrome.storage.local.get('default', function(result) {
      defaultObject = result.default;
      console.log("contains default object", defaultObject)
      console.log(defaultObject)
      resolve(defaultObject)
    })
  }).then((settings)=>{
    var bar;
  for (var label = 0; label < labels.length ; label++){
      console.log("here2")
      bar = document.createElement('div');
      bar.innerHTML = "   <div class='card z-depth-0 bordered'> \
      <div class='card-header' id='heading"+labels[label].replace(' ', '')+"'>\
        <h5 class='mb-0'>\
        <div class ='row'>\
          <div class='col label'>\
          <button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+labels[label]+"'\
            aria-expanded='false' aria-controls='collapse"+labels[label].replace(' ', '')+"'>\
            " + labels[label]+" \
          </button> </div> \
          <div class='col toggle-site'> \
          <input type='checkbox' " + checkbox[settings[Constants.labels[labels[label]]].status] +" class = 'toggle-script' id='"+labels[label].replace(' ', '') +"' data-offstyle='success' data-onstyle='danger' data-on='Disabled' data-off='Enabled' data-toggle='toggle'> </div>\
        </h5>  \
      </div>  \
      <div> \
      <div id='collapse"+labels[label].replace(' ', '')+"' class='collapse' aria-labelledby='heading"+labels[label]+"' \
        data-parent='#accordionLabels'> \
        <div class='card-body'> \
          description of these kind of scripts and what is recommended\
        </div> \
      </div> \
    </div>"
    accordian.appendChild(bar)

    
  }

  $(document).ready(function () {
    $(".toggle").click(function (){
      var checkbox = this.childNodes[0];
      var status = $('#'+checkbox.id).is(':checked');
      console.log("checkbox " +checkbox.id +" if disabled" ,status)
      if (status) {
        // settings[checkbox.id] = 1;
        for (let ele in settings){
          if (settings[ele].label.replace(' ', '') === checkbox.id){
            console.log("Before: ", settings[ele].label, checkbox.id, settings[ele].status) ; 

            settings[ele].status = 1;
            console.log("After: ",settings[ele].label, checkbox.id, settings[ele].status) ; 
          }
        }
        console.log("enabled");
      }
      else{

        for (let ele in settings){
          // console.log("Before: ", settings[ele].label, checkbox.id, settings[ele].status) ; 

          if (settings[ele].label.replace(' ', '') === checkbox.id){
            console.log("Before: ", settings[ele].label, checkbox.id, settings[ele].status) ; 

            settings[ele].status = 0;
            console.log("After: ", settings[ele].label, checkbox.id, settings[ele].status) ; 
          }
        }
        // console.log("disabled" );

      }
      
      console.log("updated settings", settings)
    })
    //your code here
  });
  $("#saveDefaultSettings").click(function (){
    console.log("clickeed")
    console.log(settings)
    chrome.storage.local.set({default: settings}, function() { })
  })


  }, false)



})








