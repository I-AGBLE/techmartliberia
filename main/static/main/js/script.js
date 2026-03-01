// Google Recapture Script For Callback 
function enableSubmit() {
    document.getElementById("submit").disabled = false;
}

function disableSubmit() {
    document.getElementById("submit").disabled = true;
}



// Menu Icon Button Toggle Functionconst menuButton = document.querySelector('.nav_menu_button');
const openMenu = document.querySelector('.open_menu');
const closeMenu = document.querySelector('.close_menu');
const menuItems = document.querySelector('.menu_items');

// Open menu
openMenu.addEventListener('click', (e) => {
  menuItems.classList.add('active');
  openMenu.style.display = 'none';
  closeMenu.style.display = 'block';
  e.stopPropagation(); // prevent triggering document click
});

// Close menu (close button)
closeMenu.addEventListener('click', (e) => {
  menuItems.classList.remove('active');
  openMenu.style.display = 'block';
  closeMenu.style.display = 'none';
  e.stopPropagation(); // prevent triggering document click
});

// Close menu when clicking a link
document.querySelectorAll('.menu_items a').forEach(link => {
  link.addEventListener('click', () => {
    menuItems.classList.remove('active');
    openMenu.style.display = 'block';
    closeMenu.style.display = 'none';
  });
});

// Close menu when clicking outside the menu
document.addEventListener('click', (event) => {
  // Only if menu is active
  if (menuItems.classList.contains('active')) {
    // Check if click is NOT inside menu or button
    if (!event.target.closest('.menu_items') && !event.target.closest('.nav_menu_button')) {
      menuItems.classList.remove('active');
      openMenu.style.display = 'block';
      closeMenu.style.display = 'none';
    }
  }
});



