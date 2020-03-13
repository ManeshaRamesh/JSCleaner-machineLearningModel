
import * as Constants from './constants.js';

 var db;

//  var blockScripts = ['']; //array of blocked scripts (based on labels)
 var scripts = []; //array of all scripts

var BlockTheseScripts =[]




function createDatabase(){ 
    return new Promise((resolve) => {
            //create the database

    // Let us open our database
    var DBOpenRequest = window.indexedDB.open("JSCLEANER", 2);

    // these event handlers act on the database being opened.
    DBOpenRequest.onerror = function(event) {
        console.log(window.jscleaner.Error.DATABASEERROR + "Failed to load to database.")
    };

    DBOpenRequest.onupgradeneeded = function(event) {
    var db = this.result;
    
    db.onerror = function(event) {
        console.log(window.jscleaner.ErrorDATABASEERROR + "Failed to load to database.")
    };

        // if (!db.objectStoreNames.contains('scripts')) {
            var scriptsOS = db.createObjectStore("scripts", {keyPath: "scriptsID", autoIncrement:true});
            // scriptsOS.createIndex("scriptsID", "scriptsID", {unique: true});
            scriptsOS.createIndex('name', 'name', {unique: true});
            scriptsOS.createIndex('label', 'label', {unique: false});
            scriptsOS.createIndex('accuracy', 'accuracy', {unique: false});

            console.log("createdObjectStore", scriptsOS)
        // }
        // if (!db.objectStoreNames.contains('urls')) {
            var urlsOS = db.createObjectStore('urls', {keyPath: 'urlsName', autoIncrement:true});
            // urlsOS.createIndex('urlID', 'urlID', {unique: true});
            urlsOS.createIndex('default', 'default', {unique: true});
            urlsOS.createIndex('scripts', 'scripts', {unique: false});
        // }
        // if (!db.objectStoreNames.contains('urlsScripts')) {
        // var urlsscriptsOS = db.createObjectStore('urlsScripts', {keyPath: 'urlsScriptsID', autoIncrement:true});
        // }
    }
    DBOpenRequest.onsuccess = function(event) {
        console.log("Database Initialized")

    //   note.innerHTML += '<li>Database initialised.</li>';
    
    // store the result of opening the database in the db
    // variable. This is used a lot below
    resolve(DBOpenRequest.result);
    
    };


    })


   }

function addItem(newItem, OSName ){
    // console.log("Add Item", newItem)
    // Create a new object ready to insert into the IDB
//   var newItem = [ { taskTitle: "Walk dog", hours: 19, minutes: 30, day: 24, month: "December", year: 2013, notified: "no" } ];

  // open a read/write db transaction, ready for adding the data
  var transaction = db.transaction([OSName], "readwrite");

  // report on the success of the transaction completing, when everything is done
  transaction.oncomplete = function(event) {
    // note.innerHTML += '<li>Transaction completed.</li>';
    // console.log("Transaction Completed (ADD ITEM) - ", newItem)
  };

  transaction.onerror = function(event) {
//   note.innerHTML += '<li>Transaction not opened due to error. Duplicate items not allowed.</li>';
    console.log("Transaction not opened due to error. Duplicate items not allowed - ", newItem)

  };

  // create an object store on the transaction
  var objectStore = transaction.objectStore(OSName);

  // Make a request to add our newItem object to the object store
  var objectStoreRequest = objectStore.add(newItem);

  objectStoreRequest.onsuccess = function(event) {
    // report the success of our request
    // note.innerHTML += '<li>Request successful.</li>';
    console.log("Request to add item was successful- ", newItem)
    loadData(null); 
};

   

 
}


    //read values params - objectstore, key,
function readItem(OSName, key) {
    // open a read/write db transaction, ready for retrieving the data
    var transaction = db.transaction([OSName], "readwrite");
    
    // report on the success of the transaction completing, when everything is done
    transaction.oncomplete = function(event) {
        console.log("Transaction Completed - ", OSName)

    };
    
    transaction.onerror = function(event) {
        console.log("Transaction not opened due to error. Duplicate items not allowed - ", transaction.error)

        // note.innerHTML += '<li>Transaction not opened due to error: ' + transaction.error + '</li>';
    };
    
    // create an object store on the transaction
    var objectStore = transaction.objectStore(OSName);
    
    // Make a request to get a record by key from the object store
    var objectStoreRequest = objectStore.get(key);
    
    objectStoreRequest.onsuccess = function(event) {
        // report the success of our request
        console.log("Request successful - ", OSName)
    
        var myRecord = objectStoreRequest.result;
    };
}

function updateItem(OSName, key, data){
    // var title = "Walk dog";

// Open up a transaction as usual
    var objectStore = db.transaction([OSName], "readwrite").objectStore(OSName);

    // Get the to-do list object that has this title as it's title
    var objectStoreKeyRequest = objectStore.get(key);

    objectStoreKeyRequest.onsuccess = function() {
    // Grab the data object returned as the result    

        // Create another request that inserts the item back into the database
        var updateItemRequest = objectStore.put(data);

        // Log the transaction that originated this request
        console.log("The transaction that originated this request is " + updateItemRequest.transaction);
        // When this new request succeeds, run the displayData() function again to update the display
        objectStoreRequest.onsuccess = function(event) {
            // report the success of our request
            // note.innerHTML += '<li>Request successful.</li>';
            console.log("Request to update item was successful- ", data)
            loadData(null); 
        };
    };

}
 function removeItem(OSName, key){
       // open a read/write db transaction, ready for deleting the data
    var transaction = db.transaction([OSName], "readwrite");

    // report on the success of the transaction completing, when everything is done
    transaction.oncomplete = function(event) {
        // console.log('Transaction completed');
    };

    transaction.onerror = function(event) {
        console.log('Transaction not opened due to error: ' + transaction.error );
    };

    // create an object store on the transaction
    var objectStore = transaction.objectStore(OSName);

    // Make a request to delete the specified record out of the object store
    var objectStoreRequest = objectStore.delete(key);

    objectStoreRequest.onsuccess = function(event) {
        // report the success of our request
        // note.innerHTML += '<li>Request successful.</li>';
        console.log("Request to remove item was successful- ", key)
        loadData(null); 
    };
 }
 function searchItem(OSName, attribute, item){
       // first clear the content of the task list so that you don't get a huge long list of duplicate stuff each time
    //the display is updated.
  

    // Open our object store and then get a cursor list of all the different data items in the IDB to iterate through
    let objectStore = db.transaction(OSName).objectStore(OSName);
    objectStore.openCursor().onsuccess = function(event) {
      let cursor = event.target.result;
        // if there is still another cursor to go, keep runing this code
        if(cursor) {
            if (cursor.value[attribute] == item) { return cursor.value;};

          // continue on to the next item in the cursor
          cursor.continue();

        // if there are no more cursor items to iterate through, say so, and exit the function
        } else {
            console.log("reached end of table")
            return null;
        }
      }

 }

 function ifExists(OSName, attribute, item){

    return new Promise((resolve,reject) =>{
        let objectStore = db.transaction(OSName).objectStore(OSName);
        objectStore.openCursor().onsuccess = function(event) {
        let cursor = event.target.result;
        // if there is still another cursor to go, keep runing this code
            if(cursor) {
                if (cursor.value[attribute] == item) {resolve(true);};

            // continue on to the next item in the cursor
            cursor.continue();

            // if there are no more cursor items to iterate through, say so, and exit the function
            } else {
                console.log("reached end of table")
                resolve(false);
            }
        }
    })
    


 }

function iterate(OSName, callback){
    if (!db) return;
    let objectStore = db.transaction(OSName).objectStore(OSName);
    objectStore.openCursor().onsuccess = function(event) {
      let cursor = event.target.result;
        // if there is still another cursor to go, keep runing this code
        if(cursor) {
            callback(cursor.value)
            // .then((result)=>{
            //     if (result){
            //         console.log(result); 
            //         return result;
            //     }
            //     else if (result === null){
            //         cursor.continue();
            //     }
            // })
            // if (cursor.value[attribute] == item) {console.log(cursor.value); return true;};
            
            // continue on to the next item in the cursor
          
            cursor.continue();
        // if there are no more cursor items to iterate through, say so, and exit the function
        } else {
            console.log("reached end of table")
            return;
        }
      }

 }


 function blockURLS(OSName, details){
     return new Promise((resolve, reject)=>{
        let objectStore = db.transaction(OSName).objectStore(OSName);
        objectStore.openCursor().onsuccess = function(event) {
          let cursor = event.target.result;
            // if there is still another cursor to go, keep runing this code
            if(cursor) {
                if(cursor.value.name === details.url){
                    if (cursor.value.label === "Social"){
    
                        console.log("Should be blocked", cursor.value)
                        var scheme = /^https/.test(details.url) ? "https" : "http";
                        // chrome.tabs.update(details.tabId, {
                        //     url: scheme + "://robwu.nl/204"
                        // });
                        resolve({redirectUrl: scheme + "://robwu.nl/204" });
                    }
                }
                cursor.continue();
                // if (cursor.value[attribute] == item) {console.log(cursor.value); return true;};
                
                // continue on to the next item in the cursor
              
    
            // if there are no more cursor items to iterate through, say so, and exit the function
            } else {
                console.log("reached end of table")
                resolve(undefined);
            }
          }


     })


 }

 function blockRequests(){
    var label;
    var disabledLabels = [];
    var blockScripts = [];
    for(label of Constants.defaultLabels){
        if (!label.status){
            disabledLabels.push(label.label);
        }
    }
    iterate('scripts', function(value){
        if(disabledLabels.includes(value.label)){
            blockScripts.push(value.name); 
        }
    })
    console.log("Scripts that are being blocked", blockScripts); 
    BlockTheseScripts = blockScripts;
    // return blockScripts;

 }

 function loadData(openedDB){
 
    return new Promise(()=>{
        if (openedDB !==null){
            db = openedDB;
        }
        
        blockRequests();
        // console.log('Scripts that need to be blocked; ', blockScripts)

        
        var transaction = db.transaction(['scripts'], "readwrite");
        
        // report on the success of the transaction completing, when everything is done
        transaction.oncomplete = function(event) {
            // console.log("Transaction Completed - ", OSName)

        };
        
        transaction.onerror = function(event) {
            // console.log("Transaction not opened due to error. Duplicate items not allowed - ", transaction.error)

            // note.innerHTML += '<li>Transaction not opened due to error: ' + transaction.error + '</li>';
        };
        
        // create an object store on the transaction
        var objectStore = transaction.objectStore('scripts');
        
        // Make a request to get a record by key from the object store
        var objectStoreRequest = objectStore.getAll();
        
        objectStoreRequest.onsuccess = function(event) {
            // report the success of our request
            scripts = objectStoreRequest.result;

            console.log("Request successful - ", scripts)
        
        };

    })
    
}


export  {
    createDatabase,
    readItem,
    addItem, 
    removeItem,
    updateItem, 
    searchItem, 
    ifExists, 
    iterate, 
    blockURLS,
    scripts, 
    loadData, 
    blockRequests


};
