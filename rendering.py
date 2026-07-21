import unicodedata

def display_len(text: str) -> int:
    """Calculates the visual width of a string, accounting for wide emojis."""
    width = 0
    for char in text:
        # 'W' (Wide) and 'F' (Fullwidth) take up 2 terminal spaces
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width

def print_table(table: list[list[str]], sep: str = ""):
    max_columns = 0
    if table:
        max_columns = max(len(line) for line in table)

    col_widths: list[int] = []
    for i in range(max_columns):
        col_width = 0
        col_width = max(display_len(line[i]) if len(line) > i else 0 for line in table)
        col_widths.append(col_width)

    for line in table:
        text = ''.join(
            (sep if i != 0 else '') +
            t + ' ' * (col_widths[i] - display_len(t))
            for i, t in enumerate(line)
        )
        print(text)
