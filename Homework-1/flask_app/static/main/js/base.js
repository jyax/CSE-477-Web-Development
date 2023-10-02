const menuIcon = document.getElementById('menu-icon');
const mobileMenu = document.getElementById('mobile-menu');

function toggleMobileMenu() {
    mobileMenu.classList.toggle('show-menu');
}

menuIcon.addEventListener('click', toggleMobileMenu);

window.addEventListener('resize', () => {
    if (window.innerWidth < 650) {
        menuIcon.style.display = 'block'; // Display the menu icon
        mobileMenu.style.display = 'none'; // Hide the mobile menu
    } else {
        menuIcon.style.display = 'none'; // Hide the menu icon
        mobileMenu.style.display = 'block'; // Display the mobile menu
    }
});

if (window.innerWidth < 650) {
    menuIcon.style.display = 'block'; // Display the menu icon
    mobileMenu.style.display = 'none'; // Hide the mobile menu
} else {
    menuIcon.style.display = 'none'; // Hide the menu icon
    mobileMenu.style.display = 'block'; // Display the mobile menu
}
