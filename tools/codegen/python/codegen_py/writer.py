"""C emission DSL — tiny writer for generating C/C++ header files."""
from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Hashable, Iterable, Iterator, Sequence


class CValue(ABC):
    """Expression-level C syntax that can be embedded by the writer."""

    @abstractmethod
    def render(self) -> str: ...

    def __str__(self) -> str:
        return self.render()


@dataclass(frozen=True, slots=True)
class CSymbol(CValue):
    """A C symbol like TYPE_GRASS or ABILITY_STENCH."""
    value: str
    def render(self) -> str: return self.value


@dataclass(frozen=True, slots=True)
class CExpr(CValue):
    """An explicitly raw C expression."""

    value: str

    def render(self) -> str: return self.value


@dataclass(frozen=True, slots=True)
class CString(CValue):
    """A C string literal — will be quoted."""
    value: str
    def render(self) -> str: return f'"{self.value}"'


@dataclass(frozen=True, slots=True)
class CGuiString(CValue):
    """A GBA gettext-style string — wrapped in _(...)."""
    value: str
    def render(self) -> str: return f'_("{self.value}")'


@dataclass(frozen=True, slots=True)
class CDollarString(CValue):
    """A GBA dollar-string — wrapped in $(...)."""
    value: str
    def render(self) -> str: return f'$("{self.value}")'


@dataclass(frozen=True, slots=True)
class CBraceList(CValue):
    """A compact positional initializer such as `{a, b, c}`."""

    values: Sequence[Any]

    def render(self) -> str:
        return "{" + ", ".join(c_value(value) for value in self.values) + "}"


@dataclass(frozen=True, slots=True)
class LookupTable:
    """A C lookup table whose string values share deduplicated declarations."""

    signature: str
    entries: Sequence[tuple[Hashable, str | None]]
    render_entry: Callable[[Hashable, str], str] = lambda key, name: f"[{key}] = {name}"


def c_value(val: Any) -> str:
    """Render a Python value as a C literal."""
    match val:
        case CValue(): return val.render()
        case bool(): return "TRUE" if val else "FALSE"
        case int(): return str(val)
        case float(): return f"{val}"
        case str(): return val  # raw C code fragment
        case None: return "0"
        case list(): return "{" + ", ".join(c_value(x) for x in val) + "}"
        case _: return str(val)


IND = "    "


class CWriter:
    """Line-based C code writer with indentation and block support."""

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._indent = 0

    # ── Basic emission ──────────────────────────────────────────────

    def raw(self, text: str = "") -> None:
        """Emit verbatim text without applying indentation."""
        self._lines.extend(text.split("\n"))

    def line(self, text: str = "", indent: int = 0) -> None:
        """Emit a line at the current indentation plus an optional offset."""
        self._lines.append(IND * (self._indent + indent) + text if text else "")

    def blank(self, n: int = 1) -> None:
        """Emit blank line(s)."""
        self._lines.extend([""] * n)

    @contextmanager
    def indented(self, levels: int = 1) -> Iterator[None]:
        """Temporarily increase indentation for nested syntax."""
        self._indent += levels
        try:
            yield
        finally:
            self._indent -= levels

    # ── Preprocessor ────────────────────────────────────────────────

    def define(self, name: str, value: Any = "", indent: int = 0) -> None:
        v = c_value(value)
        self.line(f"#define {name} {v}" if v else f"#define {name}", indent)

    def macro(self, name: str, lines: Iterable[str], indent: int = 0) -> None:
        """Emit a continued macro, adding continuations to all non-final lines."""
        lines = list(lines)
        if not lines:
            self.define(name, indent=indent)
            return
        self.line(f"#define {name} \\", indent)
        for index, line in enumerate(lines):
            continuation = " \\" if index < len(lines) - 1 else ""
            self.line(f"{line}{continuation}", indent)

    @contextmanager
    def ifdef(self, condition: str) -> Iterator[None]:
        self.line(f"#ifdef {condition}")
        yield
        self.line("#endif")

    @contextmanager
    def ifndef(self, condition: str) -> Iterator[None]:
        self.line(f"#ifndef {condition}")
        yield
        self.line("#endif")

    # ── Structured C ────────────────────────────────────────────────

    def field(
        self,
        name: str,
        value: Any,
        indent: int = 0,
        *,
        comma: bool = True,
        comment: str | None = None,
    ) -> None:
        """Emit `.name = value,`"""
        separator = "," if comma else ""
        suffix = f" // {comment}" if comment else ""
        self.line(f".{name} = {c_value(value)}{separator}{suffix}", indent)

    def entry(
        self,
        value: Any,
        *,
        designator: Any | None = None,
        indent: int = 0,
        comma: bool = True,
        comment: str | None = None,
    ) -> None:
        """Emit a scalar initializer entry with optional designator and comment."""
        prefix = f"[{c_value(designator)}] = " if designator is not None else ""
        separator = "," if comma else ""
        suffix = f" // {comment}" if comment else ""
        self.line(f"{prefix}{c_value(value)}{separator}{suffix}", indent)

    @contextmanager
    def designated(self, designator: str, indent: int = 0) -> Iterator[None]:
        """`[DESIGNATOR] = {` ... `},` block."""
        with self.initializer(designator=designator, indent=indent):
            yield

    @contextmanager
    def initializer(
        self,
        designator: str | None = None,
        *,
        indent: int = 0,
        close: str = "},",
    ) -> Iterator[None]:
        """Emit a multiline initializer, optionally with an array designator."""
        opening = f"[{designator}] = {{" if designator is not None else "{"
        self.line(opening, indent)
        with self.indented(indent + 1):
            yield
        self.line(close, indent)

    @contextmanager
    def array(
        self,
        declaration: str,
        *,
        indent: int = 0,
        close: str = "};",
        blank_after: bool = False,
    ) -> Iterator[None]:
        """Emit `<declaration> = { ... };`."""
        self.line(f"{declaration} = {{", indent)
        with self.indented(indent + 1):
            yield
        self.line(close, indent)
        if blank_after:
            self.blank()

    @contextmanager
    def function(
        self,
        signature: str,
        *,
        indent: int = 0,
        close: str = "}",
        blank_after: bool = False,
    ) -> Iterator[None]:
        """Emit a function definition."""
        self.line(f"{signature} {{", indent)
        with self.indented(indent + 1):
            yield
        self.line(close, indent)
        if blank_after:
            self.blank()

    @contextmanager
    def switch(self, expression: str, *, indent: int = 0) -> Iterator[None]:
        """Emit a switch and indent its cases."""
        self.line(f"switch ({expression}) {{", indent)
        with self.indented(indent + 1):
            yield
        self.line("}", indent)

    def case(self, value: Any, statement: str, indent: int = 0) -> None:
        self.line(f"case {c_value(value)}: {statement}", indent)

    def default(self, statement: str, indent: int = 0) -> None:
        self.line(f"default: {statement}", indent)

    @contextmanager
    def block(self, open_text: str, close_text: str = "};", indent: int = 0) -> Iterator[None]:
        """Generic `{ ... } block."""
        self.line(open_text, indent)
        with self.indented(indent + 1):
            yield
        self.line(close_text, indent)

    # ── Output ──────────────────────────────────────────────────────

    def text(self) -> str:
        return "\n".join(self._lines)

    def assembly_enum(
        self,
        enum_name: str,
        values: Iterable[Any],
        *,
        count_name: str | None = None,
        count: int | None = None,
        extra_defines: Sequence[str] = (),
        extra_values: Sequence[str] = (),
    ) -> None:
        """Emit matching assembler defines and a C typedef enum."""
        values = list(values)
        if count_name and count is None:
            count = max(value.number for value in values) + 1

        self.line("#ifdef __assembly__")
        self.blank()
        for value in values:
            self.define(value.name, value.number)
        if count_name:
            self.blank()
            self.define(count_name, count)
        if extra_defines:
            self.blank()
            for line in extra_defines:
                self.line(line)

        self.blank()
        self.line("#else")
        self.blank()
        self.line(f"typedef enum {enum_name} {{")
        for value in values:
            self.line(f"{value.name} = {value.number},", 1)
        if count_name:
            self.line(f"{count_name} = {count},", 1)
        for line in extra_values:
            self.line(line)
        self.line(f"}} {enum_name};")
        self.blank()
        self.line("#endif")


def java_hash_code(s: str) -> int:
    """Reproduce Java/Kotlin String.hashCode().toUInt()."""
    h = 0
    for ch in s:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    if h & 0x80000000:
        h -= 0x100000000
    return h & 0xFFFFFFFF


def file_id(s: str) -> str:
    """Kotlin String.fileID() — sanitize path to valid C identifier."""
    import re
    return re.sub(
        r'[^a-z0-9_]',
        lambda m: f"E{ord(m.group(0).replace('\\\\', '/')[0])}",
        s.lower(),
    )


def create_dedup_maps(pairs: list[tuple[Any, Any]]) -> tuple[dict, dict]:
    """Kotlin createDedupMaps — deduplicate key→value pairs into indexed maps.

    Returns (key_to_index, value_to_index).
    """
    groups: dict[Any, list[Any]] = {}
    for key, val in pairs:
        groups.setdefault(key, []).append(val)

    key_ids = {k: i for i, k in enumerate(groups.keys())}
    value_ids: dict[Any, int] = {}
    for key, values in groups.items():
        for val in values:
            value_ids[val] = key_ids[key]

    return key_ids, value_ids


def emit_file_lookup_tables(
    writer: CWriter,
    prefix: str,
    render_value: Callable[[str, str], str],
    tables: Sequence[LookupTable],
) -> None:
    """Emit FILE-mode lookup tables with first-seen string deduplication."""
    dedup: dict[str, str] = {}
    for table in tables:
        for _, value in table.entries:
            if value and value.strip():
                dedup[prefix + file_id(value)] = value

    for name, value in dedup.items():
        writer.line(f"static const {render_value(name, value)};")

    for table in tables:
        with writer.array(f"const {table.signature}", blank_after=True):
            for key, value in table.entries:
                if value and value.strip():
                    name = prefix + file_id(value)
                    writer.line(f"{table.render_entry(key, name)},")
