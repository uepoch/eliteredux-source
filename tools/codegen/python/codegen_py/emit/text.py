"""Text generators — ability text, help articles."""
from __future__ import annotations
from ..writer import CDollarString, CWriter, java_hash_code
from ..font import Font, break_string
from ..protobuf import enum_name


def _ordered_unique(*groups):
    seen = set()
    for group in groups:
        for value in group:
            if value not in seen:
                seen.add(value)
                yield value


def gen_abilitytext(data, w: CWriter):
    PREFIX = "__sAbilityText_"
    base = data.proto_dir.parent

    short_descs = {}
    expanded_descs = {}

    for ab in data.abilities:
        short_descs[ab.id] = break_string(ab.description, Font.SMALL_NARROW, 150, 2, base)

    for ab in data.abilities:
        src = ab.expanded_description if ab.expanded_description else ab.description
        expanded_descs[ab.id] = break_string(src, Font.SMALL_NARROW, 150, 11, base)

    all_strings = _ordered_unique(short_descs.values(), expanded_descs.values())

    for s in all_strings:
        h = java_hash_code(s)
        w.line(f'constexpr u8 {PREFIX}{h}[] = _("{s}");')

    w.line("template <AbilityEnum Id>")
    w.line("constexpr Ability AbilityStrings = {0};")
    w.blank()

    for ab in data.abilities:
        w.line("template <>")
        with w.array(f"constexpr Ability AbilityStrings<{ab.id}>", blank_after=True):
            w.field("name", CDollarString(ab.name))
            w.field("description", f"{PREFIX}{java_hash_code(short_descs[ab.id])}")
            w.field("expandedDescription", f"{PREFIX}{java_hash_code(expanded_descs[ab.id])}")


def gen_helparticles(data, w: CWriter):
    base = data.proto_dir.parent
    categories = data.help_articles.help_category

    w.line(f"#define NUM_HELP_ARTICLES {len(categories)}")
    w.blank()
    with w.array("const HelpCategory gHelpArticles[NUM_HELP_ARTICLES]"):
        for cat in categories:
            title = cat.title
            color = enum_name(cat, "color")
            articles = cat.help_article
            with w.initializer():
                w.field("title", CDollarString(title))
                w.field("color", f"MENU_COLOR_{color}")
                w.field("numEntries", len(articles))
                with w.block(".entries = (const HelpArticle[]) {", "}"):
                    for article in articles:
                        art_title = article.title
                        pages = article.page
                        with w.initializer():
                            w.field("title", CDollarString(art_title))
                            w.field("numPages", len(pages))
                            with w.block(".pages = (const u8* const[]) {", "}"):
                                for page in pages:
                                    wrapped = break_string(page, Font.SMALL_NARROW, 210, 9, base)
                                    w.entry(CDollarString(wrapped))
