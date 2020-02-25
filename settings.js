document.addEventListener('DOMContentLoaded', function() {
    console.log("here")
var accordian = document.getElementById("accordionLabels");

var labels = ['Advertising','Analytics', 'Social', 'Video', 'Utilities', 'Hosting', 'Marketing', 'Customer Success', 'Content', 'CDN', 'Tag Managment', 'Others']
var bar;
for (var label = 0; label < labels.length ; label++){
    console.log("here2")
    bar = document.createElement('div');
    bar.innerHTML = "   <div class='card z-depth-0 bordered'> \
    <div class='card-header' id='heading"+labels[label]+"'>\
      <h5 class='mb-0'>\
      <div class ='row'>\
        <div class='col label'>\
        <button class='btn btn-link collapsed' type='button' data-toggle='collapse' data-target='#collapse"+labels[label]+"'\
          aria-expanded='false' aria-controls='collapse"+labels[label]+"'>\
          " + labels[label]+" \
        </button> </div> \
        <div class='col toggle-site'> \
        <input type='checkbox' class = 'toggle-script' data-offstyle='success' data-onstyle='danger' data-on='Disabled' data-off='Enabled' data-toggle='toggle'> </div>\
      </h5>  \
    </div>  \
    <div> \
    <div id='collapse"+labels[label]+"' class='collapse' aria-labelledby='heading"+labels[label]+"' \
      data-parent='#accordionLabels'> \
      <div class='card-body'> \
        description of these kind of scripts and what is recommended\
      </div> \
    </div> \
  </div>"
   accordian.appendChild(bar)
}}, false);