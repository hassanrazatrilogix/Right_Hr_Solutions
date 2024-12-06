/**
 * Template Name: Right HR Solutions - v1.0
 * Template URL: https://zohirs.com
 * Author: Zohir
 */

// Preloader
$(window).on('load', function () {
    "use strict";
    const preloader = $('#preloader'),
        loader = preloader.find('#loading');
    loader.fadeOut();
    preloader.delay(400).fadeOut('slow');
});

$(document).ready(function () {
    "use strict";

    /*----------------------------------------------------*/
    /*  Navigation Menu Toggle
    /*----------------------------------------------------*/
    const hamburger = document.querySelector(".hamburger"),
        navMenu = document.querySelector(".navbar"),
        navMenuOverlay = document.querySelector(".nav-overlay");

    if (hamburger) {
        hamburger.addEventListener("click", () => {
            hamburger.classList.toggle("active");
            navMenu.classList.toggle("active");
            navMenuOverlay.classList.toggle("active");
        });
        document.querySelectorAll(".dropdown-menu").forEach((link) =>
            link.addEventListener("click", () => {
                hamburger.classList.remove("active");
                navMenu.classList.remove("active");
                navMenuOverlay.classList.remove("active");
            })
        );
    }

    /*----------------------------------------------------*/
    /*  Smooth Scroll with Offset for Fixed Menu
    /*----------------------------------------------------*/
    if (window.location.hash) {
        const targetSection = document.querySelector(window.location.hash);
        if (targetSection) {
            setTimeout(() => {
                window.scrollTo({
                    top: targetSection.getBoundingClientRect().top + window.scrollY - 90,
                    behavior: 'smooth'
                });
            }, 200);
        }
    }

    /*----------------------------------------------------*/
    /*  Footer Year Display
    /*----------------------------------------------------*/
    document.getElementById("year").textContent = new Date().getFullYear();

    /*----------------------------------------------------*/
    /*  Video Play & Close
    /*----------------------------------------------------*/
    const videoThumb = document.getElementById("videoThumb"),
        playButton = document.getElementById("playButton"),
        videoPlayer = document.getElementById("videoPlayer"),
        video = document.getElementById("videoControl"),
        videoCloseBtn = document.getElementById("videoCloseBtn");

    // Handle play and close button events
    if (playButton && videoThumb && videoPlayer && video && videoCloseBtn) {
        playButton.addEventListener("click", () => {
            videoThumb.style.display = "none";
            videoPlayer.style.display = "block";
            video.play();
        });

        videoCloseBtn.addEventListener("click", () => {
            videoPlayer.style.display = "none";
            videoThumb.style.display = "block";
            video.pause();
        });
    }

    // IntersectionObserver for pausing and playing video based on visibility
    const videoSectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.play();
            } else {
                video.pause();
            }
        });
    }, { threshold: 0.6 }); // Adjust threshold to control when the video is considered in view (60% in this case)

    // Start observing the video container
    if (videoPlayer) {
        videoSectionObserver.observe(videoPlayer);
    }


    /*----------------------------------------------------*/
    /*  Date and Time Picker
    /*----------------------------------------------------*/
    const dateInput = document.getElementById("pickDate"),
        timeSelect = document.getElementById("pickTime"),
        today = new Date();

    if (dateInput) {
        dateInput.min = today.toISOString().split("T")[0];
        dateInput.max = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 60).toISOString().split("T")[0];

        // Date Formatter
        function formatDateToCustom(date) {
            const options = { day: "2-digit", month: "short", year: "numeric" };
            return new Date(date).toLocaleDateString("en-GB", options).replace(/ /g, " ");
        }

        // Time Formatter to 12-hour format
        function formatTimeTo12Hour(hour, minutes) {
            const period = hour >= 12 ? "PM" : "AM";
            const formattedHour = hour % 12 || 12;
            return `${formattedHour}:${minutes} ${period}`;
        }

        // Populate time options
        function populateTimeOptions(isToday) {
            timeSelect.innerHTML = '<option value="">Select a time</option>';
            const startHour = isToday ? Math.max(8, today.getHours() + (today.getMinutes() < 30 ? 0 : 1)) : 8;

            for (let h = startHour; h <= 18; h++) {
                ["00", "30"].forEach(m => {
                    if (h === 18 && m === "30") return;
                    const time24 = `${h.toString().padStart(2, '0')}:${m}`;
                    const time12 = formatTimeTo12Hour(h, m);
                    timeSelect.innerHTML += `<option value="${time24}">${time12}</option>`;
                });
            }
        }

        // Update date format and time options on date change
        dateInput.addEventListener("change", () => {
            populateTimeOptions(dateInput.value === dateInput.min);
            if (dateInput.value) {
                dateInput.type = "text";
                dateInput.value = formatDateToCustom(dateInput.value);
            }
        });
        dateInput.addEventListener("focus", () => dateInput.type = "date");
    }

    /*----------------------------------------------------*/
    /*  File Uploader Validation
    /*----------------------------------------------------*/
    const uploadFileInput = document.getElementById("uploadFile"),
        fileNameDisplay = document.getElementById("fileName");

    if (uploadFileInput && fileNameDisplay) {
        uploadFileInput.addEventListener("change", () => {
            const file = uploadFileInput.files[0];
            if (file) {
                const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2),
                    allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];

                if (!allowedTypes.includes(file.type)) {
                    uploadFileInput.value = "";
                    fileNameDisplay.textContent = "Invalid file type. Accepted formats: JPG, PNG, PDF.";
                } else if (fileSizeMB > 5) {
                    uploadFileInput.value = "";
                    fileNameDisplay.textContent = "File too large. Maximum size allowed is 5 MB.";
                } else {
                    fileNameDisplay.textContent = `Selected file: ${file.name} (${fileSizeMB} MB)`;
                }
            }
        });
    }

    /*----------------------------------------------------*/
    /*  Bootstrap Form Validation
    /*----------------------------------------------------*/
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    /*----------------------------------------------------*/
    /*  Newsletter Form Validation
    /*----------------------------------------------------*/
    const newsletterEmail = document.getElementById("newsletterEmail"),
        submitNewsletter = document.getElementById("submitNewsletter");

    if (newsletterEmail && submitNewsletter) {
        newsletterEmail.addEventListener("input", () => {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            submitNewsletter.disabled = !emailPattern.test(newsletterEmail.value);
        });

        window.preloadEmail = function () {
            const email = newsletterEmail.value;
            window.location.href = `/contact-us.html?email=${encodeURIComponent(email)}#contact_us_form`;
            return false;
        };
    }

    // /*----------------------------------------------------*/
    // /*  URL-based Email and Category Population
    // /*----------------------------------------------------*/
    // const urlParams = new URLSearchParams(window.location.search),
    //     email = urlParams.get("email"),
    //     emailAddressField = document.getElementById("emailAddress"),
    //     selectedCategory = urlParams.get("category");

    // if (email && emailAddressField) emailAddressField.value = email;
    // if (selectedCategory) {
    //     const radioButton = document.getElementById(selectedCategory);
    //     if (radioButton) radioButton.checked = true;
    // }

    // // Remove query parameters and fragments from the URL in the browser's address bar
    // window.addEventListener('load', function () {
    //     // Get the current base URL without query parameters or fragments
    //     const baseUrl = window.location.origin + window.location.pathname;
    //     // Replace the URL in the address bar without reloading the page
    //     history.replaceState(null, '', baseUrl);
    // });

    /*----------------------------------------------------*/
    /*  Terms and Conditions Checkbox
    /*----------------------------------------------------*/
    const acceptTermsCheckbox = document.getElementById("acceptTermsConditions"),
        submitButton = document.getElementById("submitButton");

    if (acceptTermsCheckbox && submitButton) {
        acceptTermsCheckbox.addEventListener("change", () => {
            submitButton.disabled = !acceptTermsCheckbox.checked;
        });
    }
});

/*----------------------------------------------------*/
/*  Sticky Header and Back-to-Top Button
/*----------------------------------------------------*/
$(window).on('scroll', function () {
    "use strict";
    const scrollY = $(window).scrollTop();
    if (scrollY > 80) {
        $(".main-header").addClass("fixd");
        $(".back-to-top").addClass("active");
    } else {
        $(".main-header").removeClass("fixd");
        $(".back-to-top").removeClass("active");
    }
});

/*----------------------------------------------------*/
/*  Initialize Google Translate
/*----------------------------------------------------*/
function googleTranslateElementInit() {
    new google.translate.TranslateElement(
        {
            pageLanguage: 'en',
            includedLanguages: 'en,fr,es',
            autoDisplay: false,
        },
        'google_translate_element'
    );
}

function translateLanguage(lang) {
    const select = document.querySelector("select.goog-te-combo");
    if (select) {
        select.value = lang;
        select.dispatchEvent(new Event("change"));
    }
}

function handleLanguageChange(lang) {
    // Update the displayed language in the dropdown
    const languageText = { en: 'English', fr: 'Français', es: 'Español' };
    document.getElementById("currentLanguage").textContent = languageText[lang];

    // Store the selected language in localStorage
    localStorage.setItem("selectedLanguage", lang);

    // Perform translation
    translateLanguage(lang);
}

// Onload function to set default language from stored selection
window.addEventListener('load', function () {
    const savedLanguage = localStorage.getItem("selectedLanguage") || "en";
    handleLanguageChange(savedLanguage);
});

// Load Google Translate Script
(function loadGoogleTranslate() {
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    document.head.appendChild(script);
})();










document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('dynamicForm');
  const subcategoriesSection = document.getElementById('subcategoriesSection');
  const customizeOrderSection = document.getElementById('customizeOrderSection');
  const orderConfirmSection = document.getElementById('orderConfirmSection');

  // URL-based Email and Category Population
  const urlParams = new URLSearchParams(window.location.search);
  const email = urlParams.get("email");
  const emailAddressField = document.getElementById("emailAddress");
  const selectedCategory = urlParams.get("category");

  if (email && emailAddressField) {
    emailAddressField.value = email;
  }

  if (selectedCategory) {
    const radioButton = document.getElementById(selectedCategory);
    if (radioButton) {
      radioButton.checked = true;
    }
  }

  // Remove query parameters from the URL
  window.addEventListener('load', function () {
    const baseUrl = window.location.origin + window.location.pathname;
    history.replaceState(null, '', baseUrl);
  });

  // Initialize form
  function initializeForm() {
    // If a category is preselected via URL, handle it
    const defaultCategory = selectedCategory
      ? document.getElementById(selectedCategory)
      : document.querySelector('input[name="categoriesList"]:checked');

    if (defaultCategory && defaultCategory.dataset.category) {
      updateSubcategories(defaultCategory.dataset.category);
    } else {
      // Fallback to the first category if no default is selected
      const firstCategory = document.querySelector('input[name="categoriesList"]');
      if (firstCategory) {
        firstCategory.checked = true;
        updateSubcategories(firstCategory.dataset.category);
      }
    }

    // Check if there's a preselected service
    // const defaultService = document.querySelector('input[name="servicesList"]:checked');
    // if (defaultService) {
    //   customizeOrderSection.classList.remove('hidden');
    //   orderConfirmSection.classList.remove('hidden');
    // }
  }

  // Show subcategories based on selected category
  function updateSubcategories(categoryValue) {
    // Hide all subcategories initially
    document.querySelectorAll('.service-list-group').forEach((sub) => {
      sub.classList.add('hidden');
    });

    // Show the relevant subcategory
    const relevantSubcategory = document.querySelector(`.service-list-group[data-category="${categoryValue}"]`);
    if (relevantSubcategory) {
      relevantSubcategory.classList.remove('hidden');
      subcategoriesSection.classList.remove('hidden');
    } else {
      subcategoriesSection.classList.add('hidden');
    }

    // // Reset and hide the next sections
    // customizeOrderSection.classList.add('hidden');
    // orderConfirmSection.classList.add('hidden');
  }

  // Handle category and service selection changes
  form.addEventListener('change', (e) => {
    if (e.target.name === 'categoriesList') {
      updateSubcategories(e.target.dataset.category);
    }

    // if (e.target.name === 'servicesList') {
    //   customizeOrderSection.classList.remove('hidden');
    //   orderConfirmSection.classList.remove('hidden');
    // }
  });

  // Initialize form state on page load
  initializeForm();
});


