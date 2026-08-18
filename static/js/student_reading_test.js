/* ═══════════════════════════════════════════════════
   INPUT LISTENERS → refresh pip status
   ═══════════════════════════════════════════════════ */
function attachInputListeners() {
    document.querySelectorAll('.fill-input, .drop-select').forEach(el => {
        el.addEventListener('input',  renderTabBar);
        el.addEventListener('change', renderTabBar);
        el.addEventListener('focus', () => {
            const num = parseInt((el.id || '').replace('question', ''));
            if (!isNaN(num)) { activeSub = num; renderTabBar(); }
        });
    });

    document.querySelectorAll('.mchq input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', renderTabBar);
        radio.addEventListener('focus', () => {
            const group = radio.closest('.mchq');
            if (group && group.id) {
                const num = parseInt(group.id.replace('question', ''));
                if (!isNaN(num)) { activeSub = num; renderTabBar(); }
            }
        });
    });

    document.querySelectorAll('.mchm input[type="checkbox"]').forEach(cb => {
        cb.addEventListener('change', renderTabBar);
    });

    // mchm max-selection enforcement
    document.addEventListener('change', function (e) {
        const cb = e.target;
        if (!cb.matches('.mchm-option input[type="checkbox"]')) return;
        const group      = cb.closest('.mchm');
        const allCBs     = group.querySelectorAll('input[type="checkbox"]');
        const maxAllowed = (cb.dataset.questionIds || '').trim().split(/\s+/).length;
        const checked    = [...allCBs].filter(c => c.checked).length;
        allCBs.forEach(c => { if (!c.checked) c.disabled = checked >= maxAllowed; });
    });
}


/* ═══════════════════════════════════════════════════
   DRAG-AND-DROP (match blocks)
   ═══════════════════════════════════════════════════ */
let _draggedChip = null;

function matchDragStart(e) {
    _draggedChip = e.currentTarget;
    _draggedChip.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', _draggedChip.dataset.value);
}
function matchDragOver(e)  { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; e.currentTarget.classList.add('drag-over'); }
function matchDragLeave(e) { e.currentTarget.classList.remove('drag-over'); }
function matchDrop(e) {
    e.preventDefault();
    const zone = e.currentTarget;
    zone.classList.remove('drag-over');
    if (!_draggedChip) return;

    const existing = zone.querySelector('.match-chip');
    if (existing) { document.querySelector('.match-right')?.appendChild(existing); existing.setAttribute('draggable', true); }

    zone.appendChild(_draggedChip);
    _draggedChip.classList.remove('dragging');
    zone.classList.add('filled');
    const hint = zone.querySelector('.drop-hint');
    if (hint) hint.style.display = 'none';

    let hidden = zone.querySelector('input[type=hidden]');
    if (!hidden) { hidden = document.createElement('input'); hidden.type = 'hidden'; hidden.name = zone.id; zone.appendChild(hidden); }
    hidden.value = _draggedChip.dataset.value;
    _draggedChip  = null;
    renderTabBar();
}
document.addEventListener('dragend', () => { if (_draggedChip) { _draggedChip.classList.remove('dragging'); _draggedChip = null; } });


/* ═══════════════════════════════════════════════════
   SUBMIT
   ═══════════════════════════════════════════════════ */
function collectAnswers() {
    const answers = { id: document.getElementById('test_id').innerText };

    document.querySelectorAll('.fill-input').forEach(el => { answers[el.id] = el.value.trim(); });
    document.querySelectorAll('.mchq').forEach(g => {
        const sel = g.querySelector('input[type="radio"]:checked');
        answers[g.id] = sel ? sel.value : null;
    });
    document.querySelectorAll('.mchm').forEach(g => {
        const ids     = (g.dataset.questionIds || '').trim().split(/\s+/);
        const checked = [...g.querySelectorAll('input[type="checkbox"]:checked')].map(c => c.value);
        ids.forEach((qid, i) => { answers[qid] = checked[i] ?? null; });
    });
    document.querySelectorAll('.match-drop-zone').forEach(z => {
        const h = z.querySelector('input[type="hidden"]');
        answers[z.id] = h ? h.value : null;
    });
    document.querySelectorAll('.drop-select').forEach(s => { answers[s.id] = s.value; });

    return answers;
}

async function submitAnswers() {
    try {
        const res = await fetch('/api/submit/listening/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(collectAnswers()),
        });
        await res.json();
        window.onbeforeunload = null;
        window.location.href  = '/main/';
    } catch (err) {
        console.error('Submission failed:', err);
        window.location.href = '/main/';
    }
}

function getCookie(name) {
    const parts = (`; ${document.cookie}`).split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}



document.addEventListener("DOMContentLoaded", function () {

    /* ---------- Matnni highlight qilish ---------- */
    const HIGHLIGHT_COLORS = ["#fef08a", "#bbf7d0", "#bfdbfe", "#fbcfe8", "#fed7aa"];
    const content = document.getElementById("test-content");

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

/* ═══════════════════════════════════════════════════
   RESIZABLE SPLIT PANELS
   ═══════════════════════════════════════════════════ */
document.querySelectorAll('.resizer').forEach(resizer => {
    const panelNum = resizer.dataset.panel;
    resizer.addEventListener('mousedown', e => {
        e.preventDefault();
        resizer.classList.add('active');
        document.body.style.cursor    = 'col-resize';
        document.body.style.userSelect = 'none';
        const leftEl    = document.getElementById('left' + panelNum);
        const container = leftEl.closest('.split-container');
        function onMove(e) {
            const rect    = container.getBoundingClientRect();
            const pct     = ((e.clientX - rect.left) / rect.width) * 100;
            const clamped = Math.min(Math.max(pct, 15), 85);
            leftEl.style.flex  = 'none';
            leftEl.style.width = clamped + '%';
        }
        function onUp() {
            resizer.classList.remove('active');
            document.body.style.cursor    = '';
            document.body.style.userSelect = '';
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup',   onUp);
        }
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup',   onUp);
    });
});


document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.mchm').forEach(initMCHM);
});

function initMCHM(container) {
  const qids = container.dataset.questionIds.trim().split(/\s+/); // ["question18","question19","question20"]
  const maxSelect = qids.length;
  const checkboxes = container.querySelectorAll('input[type="checkbox"]');
  let orderCounter = 0;

  function getCheckedInOrder() {
    return Array.from(checkboxes)
      .filter(cb => cb.checked)
      .sort((a, b) => Number(a.dataset.selOrder) - Number(b.dataset.selOrder));
  }

  function update() {
    const checked = getCheckedInOrder();

    // Tanlash tartibiga qarab to'g'ri question id (name) beriladi
    checked.forEach((cb, idx) => {
      cb.name = qids[idx];
    });

    // Belgilanmagan checkboxlarda name bo'lmasin (formaga noto'g'ri qiymat ketmasin)
    checkboxes.forEach(cb => {
      if (!cb.checked) {
        cb.removeAttribute('name');
        delete cb.dataset.selOrder;
      }
    });

    // Limitga yetganda qolganlarini disable, aks holda hammasini enable qilish
    const limitReached = checked.length >= maxSelect;
    checkboxes.forEach(cb => {
      cb.disabled = limitReached && !cb.checked;
    });
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', function () {
      if (this.checked) {
        orderCounter++;
        this.dataset.selOrder = orderCounter;
      } else {
        delete this.dataset.selOrder;
      }
      update();
    });
  });
}