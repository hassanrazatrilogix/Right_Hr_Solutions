document.addEventListener("DOMContentLoaded", () => {
  // Select all menu items
  const menuItems = document.querySelectorAll(".menu-item");

  menuItems.forEach(item => {
      item.addEventListener("click", function () {
          // Remove 'active' class from all menu items
          menuItems.forEach(menu => menu.classList.remove("active"));

          // Add 'active' class to the clicked menu item
          this.classList.add("active");
      });
  });
});


