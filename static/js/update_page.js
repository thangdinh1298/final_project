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
   let delete_form = document.querySelector("#" + div_id + " form")
   
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
   div.insertBefore(form, delete_form)
   tinymce.init({ selector: "#" + div_id + " form textarea"});
}
