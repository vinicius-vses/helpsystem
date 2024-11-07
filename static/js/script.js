document.addEventListener("DOMContentLoaded", function () {
    const dropdownToggle = document.getElementById("user-dropdown-toggle");
    const dropdownMenu = document.getElementById("user-dropdown");
  
    dropdownToggle.addEventListener("click", function (event) {
      event.stopPropagation();
      dropdownMenu.style.display = dropdownMenu.style.display === "none" ? "block" : "none";
    });
  
    document.addEventListener("click", function () {
      dropdownMenu.style.display = "none";
    });
  });
  