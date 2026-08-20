document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("add-image-form");
    const formsetContainer = document.getElementById("image-formset");
    const totalFormsInput = document.querySelector("#id_images-TOTAL_FORMS");

    if (!addButton || !formsetContainer || !totalFormsInput) return;

    addButton.addEventListener("click", function () {
        const formNum = parseInt(totalFormsInput.value, 10);
        const rows = formsetContainer.querySelectorAll(".image-formset__row");
        const lastRow = rows[rows.length - 1];

        const newRow = lastRow.cloneNode(true);

        newRow.innerHTML = newRow.innerHTML.replace(
            new RegExp(`images-${formNum - 1}-`, "g"),
            `images-${formNum}-`
        );

        newRow.querySelectorAll("input[type='text'], input[type='file']").forEach((input) => {
            input.value = "";
        });
        newRow.querySelectorAll("input[type='checkbox']").forEach((input) => {
            input.checked = false;
        });
        const preview = newRow.querySelector(".image-formset__preview");
        if (preview) {
            preview.outerHTML = '<div class="image-formset__preview image-formset__preview--empty">No image</div>';
        }

        formsetContainer.appendChild(newRow);
        totalFormsInput.value = formNum + 1;
    });
});