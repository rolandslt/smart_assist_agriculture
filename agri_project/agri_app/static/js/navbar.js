document.addEventListener('DOMContentLoaded', function() {
    const icon = document.getElementById('profile-icon-trigger');
    const menu = document.getElementById('profile-dropdown-menu');

    if (icon && menu) {
        icon.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevents the document click listener from firing immediately
            // Toggle visibility using the Tailwind 'hidden' class
            menu.classList.toggle('hidden');
        });
        
        // Hide menu if user clicks anywhere outside the menu or icon
        document.addEventListener('click', function(event) {
            if (!menu.contains(event.target) && !icon.contains(event.target)) {
                menu.classList.add('hidden');
            }
        });
    }
});