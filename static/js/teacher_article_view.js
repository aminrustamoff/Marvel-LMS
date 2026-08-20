document.addEventListener("DOMContentLoaded", function () {
/* ---------- 4. Gallery lightbox ---------- */
    const lightbox = document.getElementById("lightbox");
    const lightboxImage = document.getElementById("lightbox-image");
    const lightboxClose = document.getElementById("lightbox-close");

    document.querySelectorAll(".gallery-item").forEach((item) => {
        item.addEventListener("click", () => {
            const src = item.getAttribute("data-lightbox-src");
            if (!src || !lightbox || !lightboxImage) return;
            lightboxImage.src = src;
            lightbox.classList.add("is-open");
        });
    });

    function closeLightbox() {
        lightbox?.classList.remove("is-open");
        if (lightboxImage) lightboxImage.src = "";
    }

    lightboxClose?.addEventListener("click", closeLightbox);
    lightbox?.addEventListener("click", (e) => {
        if (e.target === lightbox) closeLightbox();
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeLightbox();
    });
});