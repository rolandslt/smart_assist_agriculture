// static/js/notifications.js
function closeModal() {
    // This ID must match the ID of your outermost modal div
    const modal = document.getElementById('reviewModal');
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error("Could not find element with ID 'reviewModal'");
    }
}

// Optional: Close modal if user clicks outside of the white box
window.onclick = function(event) {
    const modal = document.getElementById('reviewModal');
    if (event.target == modal) {
        closeModal();
    }
}