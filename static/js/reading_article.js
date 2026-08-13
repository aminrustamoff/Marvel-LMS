document.addEventListener("DOMContentLoaded", function () {
    const article = document.querySelector(".reading-article");
    const content = document.getElementById("article-content");
    if (!article || !content) return;

    /* ---------- 1. O'qish vaqtini hisoblash ---------- */
    const words = content.innerText.trim().split(/\s+/).filter(Boolean).length;
    const wordsPerMinute = 180;
    const minutes = Math.max(1, Math.round(words / wordsPerMinute));
    const timeEl = document.getElementById("reading-time");
    if (timeEl) timeEl.textContent = minutes;

    /* ---------- 2. Shrift o'lchamini boshqarish ---------- */
    const STORAGE_KEY = "reading_article_font_scale";
    const minScale = 0.8;
    const maxScale = 1.6;
    const step = 0.1;

    let scale = parseFloat(localStorage.getItem(STORAGE_KEY)) || 1;

    function applyScale() {
        scale = Math.min(maxScale, Math.max(minScale, scale));
        article.style.setProperty("--ra-font-scale", scale.toFixed(2));
        localStorage.setItem(STORAGE_KEY, scale.toFixed(2));
    }
    applyScale();

    document.getElementById("font-increase")?.addEventListener("click", () => {
        scale += step;
        applyScale();
    });
    document.getElementById("font-decrease")?.addEventListener("click", () => {
        scale -= step;
        applyScale();
    });
    document.getElementById("font-reset")?.addEventListener("click", () => {
        scale = 1;
        applyScale();
    });

    /* ---------- 3. O'qish progress bar ---------- */
    const progressBar = document.getElementById("reading-progress-bar");
    if (progressBar) {
        window.addEventListener("scroll", () => {
            const rect = content.getBoundingClientRect();
            const contentHeight = content.offsetHeight - window.innerHeight;
            const scrolled = Math.min(
                Math.max(-rect.top, 0),
                Math.max(contentHeight, 1)
            );
            const percent = (scrolled / Math.max(contentHeight, 1)) * 100;
            progressBar.style.width = `${Math.min(100, Math.max(0, percent))}%`;
        });
    }

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

    /* ---------- 5. Matnni highlight qilish ---------- */
    const HIGHLIGHT_COLORS = ["#fef08a", "#bbf7d0", "#bfdbfe", "#fbcfe8", "#fed7aa"];

    const popup = document.createElement("div");
    popup.className = "highlight-popup";
    HIGHLIGHT_COLORS.forEach((color) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "highlight-popup__swatch";
        btn.style.background = color;
        btn.addEventListener("mousedown", (e) => {
            e.preventDefault();
            applyHighlight(color);
        });
        popup.appendChild(btn);
    });
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "highlight-popup__remove";
    removeBtn.textContent = "×";
    removeBtn.addEventListener("mousedown", (e) => {
        e.preventDefault();
        removeHighlight();
    });
    popup.appendChild(removeBtn);
    document.body.appendChild(popup);

    let savedRange = null;

    function showPopup(x, y) {
        popup.style.left = `${x}px`;
        popup.style.top = `${y}px`;
        popup.classList.add("is-open");
    }

    function hidePopup() {
        popup.classList.remove("is-open");
    }

    content.addEventListener("mouseup", () => {
        const selection = window.getSelection();
        if (!selection || selection.isCollapsed || selection.toString().trim() === "") {
            hidePopup();
            return;
        }
        const range = selection.getRangeAt(0);
        if (!content.contains(range.commonAncestorContainer)) {
            hidePopup();
            return;
        }
        savedRange = range.cloneRange();
        const rect = range.getBoundingClientRect();
        showPopup(
            rect.left + window.scrollX + rect.width / 2 - 70,
            rect.top + window.scrollY - 44
        );
    });

    document.addEventListener("mousedown", (e) => {
        if (!popup.contains(e.target)) hidePopup();
    });

    function applyHighlight(color) {
        if (!savedRange) return;
        const mark = document.createElement("mark");
        mark.className = "ra-highlight";
        mark.style.backgroundColor = color;
        try {
            savedRange.surroundContents(mark);
        } catch (err) {
            // Bir nechta elementga tarqalgan selection uchun fallback
            const contents = savedRange.extractContents();
            mark.appendChild(contents);
            savedRange.insertNode(mark);
        }
        window.getSelection().removeAllRanges();
        hidePopup();
    }

    function removeHighlight() {
        if (!savedRange) return;
        const selection = window.getSelection();
        let node = selection.anchorNode;
        while (node && node !== content) {
            if (node.nodeType === 1 && node.tagName === "MARK" && node.classList.contains("ra-highlight")) {
                const parent = node.parentNode;
                while (node.firstChild) parent.insertBefore(node.firstChild, node);
                parent.removeChild(node);
                break;
            }
            node = node.parentNode;
        }
        window.getSelection().removeAllRanges();
        hidePopup();
    }

    // Mavjud highlight ustiga bosilganda ham popup chiqishi uchun
    content.addEventListener("click", (e) => {
        if (e.target.tagName === "MARK" && e.target.classList.contains("ra-highlight")) {
            const range = document.createRange();
            range.selectNodeContents(e.target);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            savedRange = range.cloneRange();
            const rect = e.target.getBoundingClientRect();
            showPopup(
                rect.left + window.scrollX + rect.width / 2 - 70,
                rect.top + window.scrollY - 44
            );
        }
    });

    
});

