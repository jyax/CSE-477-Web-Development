// Get references to the menu icon and mobile menu elements
const menuIcon = document.getElementById('menu-icon');
const mobileMenu = document.getElementById('mobile-menu');

// Function to toggle the visibility of the mobile menu
function toggleMobileMenu() {
    mobileMenu.classList.toggle('show-menu');
}

// Add a click event listener to the menu icon to toggle the mobile menu
menuIcon.addEventListener('click', toggleMobileMenu);

// Add a window resize event listener to handle responsive behavior
window.addEventListener('resize', () => {
    // Check if the window width is less than 650 pixels
    if (window.innerWidth < 650) {
        // Display the menu icon and hide the mobile menu
        menuIcon.style.display = 'block';
        mobileMenu.style.display = 'none';
    } else {
        // Hide the menu icon and display the mobile menu
        menuIcon.style.display = 'none';
        mobileMenu.style.display = 'block';
    }
});

// Initialize the menu icon and mobile menu visibility based on the initial window width
if (window.innerWidth < 650) {
    // Display the menu icon and hide the mobile menu initially
    menuIcon.style.display = 'block';
    mobileMenu.style.display = 'none';
} else {
    // Hide the menu icon and display the mobile menu initially
    menuIcon.style.display = 'none';
    mobileMenu.style.display = 'block';
}

// Get reference to the feedback button
const feedbackButton = document.getElementById('toggle-feedback-btn');
const feedbackFormContainer = document.querySelector('.feedback-form-container');
// Function to toggle the visibility of the feedback form
function toggleFeedbackForm() {
    // Assuming you have a feedback form with a specific ID
    feedbackFormContainer.style.display = feedbackFormContainer.style.display === 'block' ? 'none' : 'block';

    const blurBackDrop = document.getElementById('blur-backdrop');
    if (feedbackFormContainer.style.display === 'block') {
        feedbackFormContainer.classList.add('above-blur');
        blurBackDrop.style.display = 'block';
    } else {
        feedbackFormContainer.classList.remove('above-blur');
        blurBackDrop.style.display = 'none'
    }
}

// Add a click event listener to the feedback button to toggle the feedback form
feedbackButton.addEventListener('click', toggleFeedbackForm);

document.querySelector('.feedback-form-container form').addEventListener('submit', function()  {
    toggleFeedbackForm();
})