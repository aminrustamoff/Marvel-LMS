"""
table_parser.py
----------------
Raw sintaksis:

[table
(
{Col 1}
{Item1}
{Item2}
{Item3}
)
(
{Col 2}
{Item4}
{Item5}
{Item6}
)
]

- [table ... ]      -> butun jadval bloki
- ( ... )            -> bitta ustun
- {...} ichidagi birinchi element -> ustun sarlavhasi (<th>)
- qolgan {...} lar    -> shu ustundagi qatorlar (<td>)

Boshqa [context] sintaksisli parserlar bilan to'qnashmasligi uchun
`protect_tables()` / `restore_tables()` juftligidan foydalaning:

    text, store = protect_tables(raw_text)
    text = your_other_context_parser(text)   # endi ( ) { } ko'rmaydi
    final_html = restore_tables(text, store)
"""

import re
import uuid

TABLE_TAG_RE = re.compile(r'\[table\b')


# ---------------------------------------------------------------------------
# 1) Balanslangan qavslarni topish (ichma-ich [ ] bo'lsa ham to'g'ri ishlaydi)
# ---------------------------------------------------------------------------
def _find_blocks(text):
    """[table ... ] bloklarini (matn, start, end) shaklida qaytaradi."""
    blocks = []
    for m in TABLE_TAG_RE.finditer(text):
        start = m.start()
        depth = 0
        end = -1
        for i in range(start, len(text)):
            ch = text[i]
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end != -1:
            blocks.append((text[start:end + 1], start, end))
        # agar end == -1 bo'lsa, bloк yopilmagan -> e'tiborsiz qoldiramiz
    return blocks


# ---------------------------------------------------------------------------
# 2) Bitta [table ... ] blokini ustunlarga ajratish
# ---------------------------------------------------------------------------
def _parse_columns(block_text):
    inner = block_text.strip()
    inner = re.sub(r'^\[table\s*', '', inner)
    inner = re.sub(r'\]\s*$', '', inner)

    columns = []
    i, n = 0, len(inner)
    while i < n:
        if inner[i] == '(':
            depth = 0
            start = i
            j = i
            for j in range(i, n):
                if inner[j] == '(':
                    depth += 1
                elif inner[j] == ')':
                    depth -= 1
                    if depth == 0:
                        break
            group_text = inner[start + 1:j]
            columns.append(_extract_items(group_text))
            i = j + 1
        else:
            i += 1
    return columns


def _extract_items(text):
    """
    Bitta ustun (...) ichidan itemlarni ketma-ket ajratadi. Ikkita
    ko'rinishni tushunadi:
      {...}   -> oddiy katakcha, {} olib tashlanadi, ichidagi matn qaytadi
      [...]   -> {} ga o'ralmagan boshqa parser bloki (masalan [bold]...[/bold]
                 yoki [context]...[/context]) - qavslari SAQLANGAN holda,
                 xom matn sifatida alohida item bo'lib qaytadi, shunda uni
                 item_parser (boshqa parseringiz) keyin to'g'ri taniy oladi.
    Har ikkisi ham ichma-ich qavslarni balans bo'yicha hisoblab topadi,
    shu sababli hech qanday blok tashlab ketilmaydi.
    """
    items = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == '{':
            depth, start, j = 1, i, i + 1
            while j < n and depth > 0:
                if text[j] == '{':
                    depth += 1
                elif text[j] == '}':
                    depth -= 1
                j += 1
            items.append(text[start + 1:j - 1].strip())
            i = j
        elif ch == '[':
            depth, start, j = 1, i, i + 1
            while j < n and depth > 0:
                if text[j] == '[':
                    depth += 1
                elif text[j] == ']':
                    depth -= 1
                j += 1
            items.append(text[start:j].strip())  # qavslari bilan birga saqlanadi
            i = j
        else:
            i += 1
    return items


def _escape(s):
    return (
        s.replace('&', '&amp;')
         .replace('<', '&lt;')
         .replace('>', '&gt;')
         .replace('"', '&quot;')
    )


# ---------------------------------------------------------------------------
# 3) Ustunlarni transpose qilib HTML jadval qurish
# ---------------------------------------------------------------------------
def columns_to_html(columns, css_class="parsed-table", item_parser=None):
    """
    item_parser: har bir katakcha matnini (masalan ichida boshqa
    [context] blok bo'lsa) qayta ishlab, joylashtirishga tayyor
    HTML/matn qaytaruvchi funksiya. Berilmasa, oddiy escape qilinadi
    (xavfsiz, lekin ichidagi [context] bloklar xom holicha qoladi).
    """
    if not columns:
        return ""

    def render(v):
        return item_parser(v) if item_parser else _escape(v)

    headers = [col[0] if col else "" for col in columns]
    rows_data = [col[1:] for col in columns]
    max_rows = max((len(r) for r in rows_data), default=0)

    html = [f'<table class="{css_class}">', '  <thead>', '    <tr>']
    for h in headers:
        html.append(f'      <th>{render(h)}</th>')
    html += ['    </tr>', '  </thead>', '  <tbody>']

    for r in range(max_rows):
        html.append('    <tr>')
        for col in rows_data:
            val = col[r] if r < len(col) else ''
            html.append(f'      <td>{render(val)}</td>')
        html.append('    </tr>')

    html += ['  </tbody>', '</table>']
    return '\n'.join(html)


def parse_table_block(block_text, css_class="parsed-table", item_parser=None):
    """
    Bitta [table ... ] blokini HTML ga aylantiradi.

    item_parser berilsa, har bir katakcha matni (masalan ichidagi
    boshqa [context] blok) shu funksiyadan o'tkazilib, natija
    escape qilinmasdan to'g'ridan-to'g'ri joylashtiriladi — chunki
    item_parser javobi allaqachon xavfsiz/tayyor HTML deb hisoblanadi.
    Agar item_parser ichida oddiy matn (hech qanday maxsus blok bo'lmasa)
    qaytsa, o'zingiz uni escape qilishga mas'ulsiz (masalan
    `html.escape(text)` qaytarish orqali).
    """
    columns = _parse_columns(block_text)
    return columns_to_html(columns, css_class=css_class, item_parser=item_parser)


# ---------------------------------------------------------------------------
# 4A) Oddiy usul: darhol almashtirish (agar boshqa parser [table] bloklarini
#      hech qachon ko'rmasa, shu yetarli)
# ---------------------------------------------------------------------------
def parse_tables_in_text(full_text, css_class="parsed-table", item_parser=None):
    blocks = _find_blocks(full_text)
    for block_text, start, end in reversed(blocks):  # oxiridan boshlab, offsetlar buzilmasin
        html = parse_table_block(block_text, css_class=css_class, item_parser=item_parser)
        full_text = full_text[:start] + html + full_text[end + 1:]
    return full_text


# ---------------------------------------------------------------------------
# 4B) Tavsiya etiladigan usul: placeholder bilan himoyalash
#      Boshqa [context] parserlaringiz orasiga xavfsiz joylashadi.
# ---------------------------------------------------------------------------
def protect_tables(full_text, css_class="parsed-table", item_parser=None):
    """
    [table ... ] bloklarini noyob tokenlarga almashtiradi va
    (token -> tayyor HTML) lug'atini qaytaradi.

    item_parser: katakcha ichidagi matnni (nested [context] bloklarni
    hal qilish uchun) sizning boshqa context-parseringizdan o'tkazadi.
    Odatda shu yerga aynan o'sha "boshqa parserlar" funksiyangizni
    beriladi — shunda [table] ichidagi bloklar ham qoldirilmay
    parse qilinadi.

    Foydalanish:
        text, store = protect_tables(raw_text, item_parser=your_context_parser)
        text = your_context_parser(text)    # tashqaridagi [context] bloklar uchun
        final_html = restore_tables(text, store)
    """
    store = {}
    blocks = _find_blocks(full_text)
    for block_text, start, end in reversed(blocks):
        token = f'\x00TABLE_{uuid.uuid4().hex}\x00'
        store[token] = parse_table_block(block_text, css_class=css_class, item_parser=item_parser)
        full_text = full_text[:start] + token + full_text[end + 1:]
    return full_text, store


def restore_tables(text, store):
    """protect_tables() dan olingan tokenlarni tayyor HTML bilan almashtiradi."""
    for token, html in store.items():
        text = text.replace(token, html)
    return text


# ---------------------------------------------------------------------------
# Tezkor test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    raw = """
    Bu yerda oddiy matn bor.

    [table
    (
    {Col 1}
    {Item1}
    [bold]muhim so'z[/bold]
    {Item3}
    )
    (
    {Col 2}
    {Item4}
    {Item5}
    {Item6}
    )
    ]

    Matn davom etadi, boshqa [context] blok ham bo'lishi mumkin.
    """

    # Bu sizning haqiqiy "boshqa parserlar" funksiyangizning o'rnini bosuvchi
    # juda sodda misol: [bold]...[/bold] ni <strong> ga aylantiradi va
    # qolgan matnni escape qiladi.
    def demo_context_parser(text):
        out = _escape(text)
        out = out.replace('[bold]', '<strong>').replace('[/bold]', '</strong>')
        return out

    print("--- item_parser BILAN (nested [context] hal qilinadi) ---")
    print(parse_tables_in_text(raw, item_parser=demo_context_parser))

    print("\n--- item_parser SIZ (nested [context] xom qoladi) ---")
    print(parse_tables_in_text(raw))