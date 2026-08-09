"""Font width mapping and pixel-width word wrapping (port of FontMapping.kt)."""
from __future__ import annotations
from enum import IntEnum
from pathlib import Path
import re


class Font(IntEnum):
    SMALL = 0
    NORMAL = 1
    SHORT = 2
    SHORT_COPY_1 = 3
    SHORT_COPY_2 = 4
    SHORT_COPY_3 = 5
    BRAILLE = 6
    NARROW = 7
    SMALL_NARROW = 8
    BOLD = 9


_FONT_WIDTHS_CACHE: dict[int, list[int]] = {}


def _load_widths(font_id: int, base_path: Path) -> list[int]:
    if font_id in _FONT_WIDTHS_CACHE:
        return _FONT_WIDTHS_CACHE[font_id]
    path = base_path / "graphics" / "fonts" / f"font{font_id}_latin_widths.inc"
    text = path.read_text()
    widths = [int(m.group()) for m in re.finditer(r'\d+', text)]
    _FONT_WIDTHS_CACHE[font_id] = widths
    return widths


CHAR_INDICES: dict[str, int] = {
    ' ': 0x00, 'À': 0x01, 'Á': 0x02, 'Â': 0x03, 'Ç': 0x04, 'È': 0x05,
    'É': 0x06, 'Ê': 0x07, 'Ë': 0x08, 'Ì': 0x09, 'Î': 0x0B, 'Ï': 0x0C,
    'Ò': 0x0D, 'Ó': 0x0E, 'Ô': 0x0F, 'Œ': 0x10, 'Ù': 0x11, 'Ú': 0x12,
    'Û': 0x13, 'Ñ': 0x14, 'ß': 0x15, 'à': 0x16, 'á': 0x17, 'ç': 0x19,
    'è': 0x1A, 'é': 0x1B, 'ê': 0x1C, 'ë': 0x1D, 'ì': 0x1E, 'î': 0x20,
    'ï': 0x21, 'ò': 0x22, 'ó': 0x23, 'ô': 0x24, 'œ': 0x25, 'ù': 0x26,
    'ú': 0x27, 'û': 0x28, 'ñ': 0x29, 'º': 0x2A, 'ª': 0x2B, '&': 0x2D,
    '+': 0x2E, '=': 0x35, ';': 0x36, '¿': 0x51, '¡': 0x52, 'Í': 0x5A,
    '%': 0x5B, '(': 0x5C, ')': 0x5D, 'â': 0x68, 'í': 0x6F, '<': 0x85,
    '>': 0x86, '0': 0xA1, '1': 0xA2, '2': 0xA3, '3': 0xA4, '4': 0xA5,
    '5': 0xA6, '6': 0xA7, '7': 0xA8, '8': 0xA9, '9': 0xAA, '!': 0xAB,
    '?': 0xAC, '.': 0xAD, '-': 0xAE, '·': 0xAF, '…': 0xB0, '\u201c': 0xB1,
    '\u201d': 0xB2, '\u2018': 0xB3, "'": 0xB4, '♂': 0xB5, '♀': 0xB6,
    '¥': 0xB7, ',': 0xB8, '×': 0xB9, '/': 0xBA, 'A': 0xBB, 'B': 0xBC,
    'C': 0xBD, 'D': 0xBE, 'E': 0xBF, 'F': 0xC0, 'G': 0xC1, 'H': 0xC2,
    'I': 0xC3, 'J': 0xC4, 'K': 0xC5, 'L': 0xC6, 'M': 0xC7, 'N': 0xC8,
    'O': 0xC9, 'P': 0xCA, 'Q': 0xCB, 'R': 0xCC, 'S': 0xCD, 'T': 0xCE,
    'U': 0xCF, 'V': 0xD0, 'W': 0xD1, 'X': 0xD2, 'Y': 0xD3, 'Z': 0xD4,
    'a': 0xD5, 'b': 0xD6, 'c': 0xD7, 'd': 0xD8, 'e': 0xD9, 'f': 0xDA,
    'g': 0xDB, 'h': 0xDC, 'i': 0xDD, 'j': 0xDE, 'k': 0xDF, 'l': 0xE0,
    'm': 0xE1, 'n': 0xE2, 'o': 0xE3, 'p': 0xE4, 'q': 0xE5, 'r': 0xE6,
    's': 0xE7, 't': 0xE8, 'u': 0xE9, 'v': 0xEA, 'w': 0xEB, 'x': 0xEC,
    'y': 0xED, 'z': 0xEE, '▶': 0xEF, ':': 0xF0, 'Ä': 0xF1, 'Ö': 0xF2,
    'Ü': 0xF3, 'ä': 0xF4, 'ö': 0xF5, 'ü': 0xF6,
}


_OCTAL_ESCAPES_RE = re.compile(r'(?:\\[0-7]{1,3})+')


def _decode_escapes(s: str) -> str:
    """Decode any source-level octal escape sequences that remain in game text."""
    def _replace(m: re.Match) -> str:
        raw = m.group(0)
        octals = re.findall(r'\\([0-7]{1,3})', raw)
        raw_bytes = bytes(int(o, 8) for o in octals)
        try:
            return raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return raw
    return _OCTAL_ESCAPES_RE.sub(_replace, s)


def _char_width(ch: str, widths: list[int], accept_newline: bool = False) -> int:
    if accept_newline and ch == '\n':
        return 0
    idx = CHAR_INDICES.get(ch)
    if idx is None:
        raise ValueError(f"No index present for character {ch!r}")
    return widths[idx]


def _pixel_length(s: str, widths: list[int]) -> int:
    cleaned = s.replace("{PKMN}", "")
    total = sum(_char_width(c, widths, True) for c in cleaned)
    pkmn_count = len(re.findall(r'\{PKMN\}', s))
    total += pkmn_count * (widths[0x53] + widths[0x54])
    return total


def break_string(string: str, font: Font, max_length: int, max_lines: int,
                 base_path: Path) -> str:
    """Word-wrap a string using pixel-width measurement (port of breakString)."""
    string = _decode_escapes(string)
    widths = _load_widths(int(font), base_path)

    result: list[str] = []
    cur_length = 0
    pieces = re.split(r'((?= )|(?<=-)|(?=\n))', string)

    for piece in pieces:
        if not piece:
            continue
        piece_length = _pixel_length(piece, widths)
        if piece.startswith('\n') or cur_length + piece_length > max_length:
            result.append('\\n')
            trimmed = piece.strip()
            cur_length = _pixel_length(trimmed, widths)
            result.append(trimmed)
        else:
            result.append(piece)
            cur_length += piece_length

    output = ''.join(result)
    line_count = output.count('\\n') + 1
    if line_count > max_lines:
        raise ValueError(f"String {output!r} exceeds max line length of {max_lines}.")

    return output
