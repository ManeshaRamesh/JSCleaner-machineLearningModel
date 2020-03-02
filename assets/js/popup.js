document.addEventListener('DOMContentLoaded', function() {

    var checkPageButton = document.getElementById('home');
    checkPageButton.addEventListener('click', function() {
        window.location.href="popup.html";
    }, false);
    
    var checkPageButton = document.getElementById('settings');
    checkPageButton.addEventListener('click', function() {
        chrome.tabs.create({ url: "settings.html" });
    }, false);

    var checkPageButton = document.getElementById('scripts');
    checkPageButton.addEventListener('click', function() {
        window.location.href="scripts.html";
        // window.location.href="new.html";
        // chrome.browserAction.setPopup({popup: "scripts.html"});
    }, false);
  }, false);