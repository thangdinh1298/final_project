function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
}

function updateWithTextArea(div_id, button_id, url) {
   let div = document.getElementById(div_id);
   let button = document.querySelector("#" + div_id + " #" + button_id)
   let delete_button = document.querySelector("#" + div_id + " #delete")
   
   button.remove()

   let form = document.createElement("form");
   form.action=url
   form.method="POST"
   let text_area = document.createElement("textarea");
   text_area.name=div_id //set name of text data the same as that of div id
   button = document.createElement("button");
   button.type = "submit"
   button.textContent = "Update"

   form.appendChild(text_area)
   form.appendChild(button)
   div.insertBefore(form, delete_button)
   var editor = new Simditor({
     textarea: $("#" + div_id + " form textarea")
     //optional options
   });
}

function deleteItem(div_id, url) {
   $.ajax({
      method:'DELETE',
      url: url,
      async: false,
      dataType: 'html'
   }).done(function(data) {
      console.log(data)
   })
}

function submitAnnouncement(text_area_id, url) {
   let text_area = document.querySelector("#"+text_area_id);
   $.ajax({
      method:'POST',
      data:{ 'announcement': text_area.value},
      url: url,
      async: false,
      dataType: 'html',
      success: function(data) {
         let header = document.querySelector("#announcement h2");
         let li = document.createElement("LI");
         let json = $.parseJSON(data)
         li.innerHTML = "Created time: " + json["created_date"] + "\n" + json["description"]
         insertAfter(li ,header)
      },
      error: function(xhr, textStatus, errorThrown) {
         alert("Failed")
      }
   })
}
