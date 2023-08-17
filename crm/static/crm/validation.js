document.addEventListener("DOMContentLoaded", function() {
    const isMixedSizeCheckbox = document.querySelector("#is_mixed_size");
    const sizeSelect = document.querySelector("#size");

    isMixedSizeCheckbox.addEventListener("change", function() {
        sizeSelect.disabled = this.checked;
    });

    // Initialize the disabled state based on the initial checkbox value
    sizeSelect.disabled = isMixedSizeCheckbox.checked;

    // Enable the sizeSelect dropdown when the checkbox is unchecked
    isMixedSizeCheckbox.addEventListener("change", function() {
        if (!this.checked) {
            sizeSelect.disabled = false;
        }
    });
});

let saveButton = document.getElementById('submitButton');
saveButton.onclick = function() {
    let accepted = confirm("Are you sure you want to save?");
    if (accepted) {
        document.getElementById('form').submit();
    }
}
