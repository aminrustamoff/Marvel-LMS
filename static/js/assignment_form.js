document.addEventListener("DOMContentLoaded", function () {
    const selectConfigs = [
        { id: "id_groups", placeholder: "Search for groups..." },
        { id: "id_articles", placeholder: "Search for articles..." },
        { id: "id_passages", placeholder: "Search for passages..." },
        { id: "id_listenings", placeholder: "Search for listening tests..." },
        { id: "id_podcasts", placeholder: "Search for podcasts..." },
    ];

    selectConfigs.forEach(({ id, placeholder }) => {
        const el = document.getElementById(id);
        if (!el) return;

        new Choices(el, {
            removeItemButton: true,
            placeholder: true,
            placeholderValue: placeholder,
            noResultsText: "No results found",
            noChoicesText: "Nothing left to select",
            itemSelectText: "Click to select",
            searchResultLimit: 20,
            shouldSort: false,
        });

        el.addEventListener("change", () => updateCount(id));
        updateCount(id);
    });

    function updateCount(selectId) {
        const el = document.getElementById(selectId);
        const badge = document.querySelector(`[data-count-for="${selectId}"]`);
        if (!el || !badge) return;
        badge.textContent = el.selectedOptions ? el.selectedOptions.length : 0;
    }

    // Tab switching
    const tabs = document.querySelectorAll(".task-tab");
    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            tabs.forEach((t) => t.classList.remove("active"));
            document.querySelectorAll(".task-tabs__panel").forEach((panel) => {
                panel.hidden = true;
            });
            tab.classList.add("active");
            document.getElementById(tab.dataset.target).hidden = false;
        });
    });
});