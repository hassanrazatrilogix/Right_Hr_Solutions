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


document.addEventListener('DOMContentLoaded', function () {
  const arrowIcon = document.getElementById('arrow-icon');
  const dropdown = document.querySelector('.dropdown');

  arrowIcon.addEventListener('click', function (event) {
      event.stopPropagation(); // Prevent click from propagating
      dropdown.classList.toggle('active');
  });

  document.addEventListener('click', function (event) {
    
      if (!dropdown.contains(event.target)) {
          dropdown.classList.remove('active');
      }
  });
});


function toggleSubmenu(event) {
    event.preventDefault();
    const submenu = event.target.nextElementSibling;
    if (submenu) {
        submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
    }
}

function toggleDropdown(event) {
    event.stopPropagation();
    const dropdownContent = event.target.closest('.dropdown').querySelector('.dropdown-content');
    if (dropdownContent) {
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    }
}

document.addEventListener('click', function () {
    document.querySelectorAll('.dropdown-content').forEach(content => {
        content.style.display = 'none';
    });
});

const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      const arrow = item.querySelector('.arrow');

      question.addEventListener('click', () => {
        const isOpen = answer.classList.contains('open');

        // Close all open answers
        document.querySelectorAll('.faq-answer').forEach(a => a.classList.remove('open'));
        document.querySelectorAll('.arrow').forEach(a => a.classList.remove('open'));

        // Toggle current item
        if (!isOpen) {
          answer.classList.add('open');
          arrow.classList.add('open');
        }
      });
    });