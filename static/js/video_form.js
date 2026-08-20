document.addEventListener("DOMContentLoaded", function () {
    const urlInput = document.getElementById("id_url");
    const preview = document.getElementById("video-preview");
    const previewFrame = document.getElementById("video-preview-frame");

    if (!urlInput || !preview || !previewFrame) return;

    function extractYouTubeId(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=)([^&]+)/,
            /(?:youtu\.be\/)([^?]+)/,
            /(?:youtube\.com\/embed\/)([^?]+)/,
        ];
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        return null;
    }

    function updatePreview() {
        const videoId = extractYouTubeId(urlInput.value.trim());
        if (videoId) {
            previewFrame.src = `https://www.youtube.com/embed/${videoId}`;
            preview.hidden = false;
        } else {
            previewFrame.src = "";
            preview.hidden = true;
        }
    }

    urlInput.addEventListener("input", updatePreview);
    updatePreview(); // run once on load, in case editing an existing video
});