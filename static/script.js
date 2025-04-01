// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMenuButton = document.getElementById('close-menu');
    const mobileMenu = document.getElementById('mobile-menu');
    const body = document.body;

    function openMenu() {
        mobileMenu.classList.remove('translate-x-full');
        body.style.overflow = 'hidden';
        // Reset all dropdowns when opening menu
        document.querySelectorAll('.mobile-dropdown div').forEach(dropdown => {
            dropdown.classList.add('hidden');
        });
        document.querySelectorAll('.mobile-dropdown i').forEach(icon => {
            icon.classList.remove('rotate-180');
        });
    }

    function closeMenu() {
        mobileMenu.classList.add('translate-x-full');
        body.style.overflow = '';
    }

    // Event Listeners
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', openMenu);
    }

    if (closeMenuButton) {
        closeMenuButton.addEventListener('click', closeMenu);
    }

    // Close menu when clicking outside
    if (mobileMenu) {
        mobileMenu.addEventListener('click', function(e) {
            if (e.target === mobileMenu) {
                closeMenu();
            }
        });
    }

    // Close menu when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu && !mobileMenu.classList.contains('translate-x-full')) {
            closeMenu();
        }
    });

    // Mobile Dropdowns
    const dropdowns = document.querySelectorAll('.mobile-dropdown');
    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('button');
        const content = dropdown.querySelector('div');
        const icon = button.querySelector('i');

        if (button && content && icon) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Close other dropdowns
                dropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        const otherContent = otherDropdown.querySelector('div');
                        const otherIcon = otherDropdown.querySelector('i');
                        if (otherContent) otherContent.classList.add('hidden');
                        if (otherIcon) otherIcon.classList.remove('rotate-180');
                    }
                });
                
                content.classList.toggle('hidden');
                icon.classList.toggle('rotate-180');
            });
        }
    });
}); 