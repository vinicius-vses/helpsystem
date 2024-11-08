document.addEventListener("DOMContentLoaded", function () {
    const dropdowns = [
        { toggleId: "user-dropdown-toggle", menuId: "user-dropdown" },
        { toggleId: "filters-dropdown-toggle", menuId: "filters-dropdown" }
    ];

    dropdowns.forEach(({ toggleId, menuId }) => {
        const dropdownToggle = document.getElementById(toggleId);
        const dropdownMenu = document.getElementById(menuId);

        dropdownMenu.style.display = "none";

        dropdownToggle.addEventListener("click", function (event) {
            event.stopPropagation();
            const isVisible = dropdownMenu.style.display === "block";
            dropdownMenu.style.display = isVisible ? "none" : "block";
        });
        
        document.addEventListener("click", function () {
            dropdownMenu.style.display = "none";
        });
    
        dropdownMenu.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    });
});
