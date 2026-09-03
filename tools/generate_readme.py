#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import re
from typing import Any
from urllib.parse import unquote

if not os.environ.get("LANG"):
    os.environ["LANG"] = "en_US.UTF-8"

import jsonschema2md

from seetapsych_attributes.schema import schema

ROOT = os.path.dirname(os.path.abspath(__file__))

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/seetapsych/seetapsych-attributes/main/"

_COMPACT_LONG_LIST_THRESHOLD = 16


def _to_absolute_img_url(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return url
    return GITHUB_RAW_BASE + url.lstrip("/")


def _compact_truncate_list(lst: list[Any]) -> str | list[Any]:
    if len(lst) <= _COMPACT_LONG_LIST_THRESHOLD:
        return lst
    return f"[{lst[0]!r}] * {len(lst)}"


def _compact_process_value(value: Any, in_examples: bool = False) -> Any:
    if isinstance(value, dict):
        return {k: _compact_process_value(v, in_examples or (k == "examples")) for k, v in value.items()}
    if isinstance(value, list):
        if in_examples:
            truncated = _compact_truncate_list(value)
            if isinstance(truncated, str):
                return truncated
            return [_compact_process_value(v, in_examples) for v in truncated]
        return [_compact_process_value(v, in_examples) for v in value]
    return value


def compact_examples(schema: dict[str, Any]) -> dict[str, Any]:
    return _compact_process_value(schema, in_examples=False)


def schema2markdown(schema: dict[str, Any]) -> str:
    parser = jsonschema2md.Parser()

    md = parser.parse_schema(schema, fail_on_error_in_defs=False)
    return "".join(md)


def fix_markdown_headers(text: str) -> str:
    lines = text.splitlines()
    result = []

    for i, line in enumerate(lines):
        if line.startswith("#"):
            if i > 0 and lines[i - 1].strip() != "":
                result.append("")
        result.append(line)

    return "\n".join(result)


def sanitize_id(s: str) -> str:
    s = unquote(s)
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def fix_markdown_links_and_anchors(text: str) -> str:
    text = re.sub(r"\[#/\$defs/([^\]]+)\]", r"[\1]", text)

    def link_replacer(m: re.Match[str]) -> str:
        display = m.group(1)
        orig_fragment = m.group(2)
        clean = sanitize_id(orig_fragment)
        if clean == orig_fragment:
            return m.group(0)
        return f"[{display}](#{clean})"

    text = re.sub(r"\[([^\]]+)\]\(#([^)]+)\)", link_replacer, text)

    link_targets = set()
    for m in re.finditer(r"\[[^\]]*\]\(#([^)]+)\)", text):
        link_targets.add(m.group(1))

    added_clean_ids: set[str] = set()

    def anchor_replacer(m: re.Match[str]) -> str:
        orig_id = m.group(1)
        clean_id = sanitize_id(orig_id)
        clean_is_target = clean_id in link_targets
        if not clean_is_target:
            return m.group(0)
        if clean_id == orig_id:
            return m.group(0)
        if clean_id in added_clean_ids:
            return ""
        added_clean_ids.add(clean_id)
        return f'<a id="{clean_id}"></a>'

    text = re.sub(r'<a id="([^"]+)"></a>', anchor_replacer, text)

    return text


_DEFAULT_IMG_STYLE = 'style="max-height: 360px; width: auto;"'


def _strip_md(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s


def _md_to_html(s: str) -> str:
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def _build_img_attrs(fig: dict[str, Any]) -> str:
    width = fig.get("width")
    height = fig.get("height")
    attrs: list[str] = []
    if width is not None:
        attrs.append(f'width="{width}"')
    if height is not None:
        attrs.append(f'height="{height}"')
    if not attrs:
        attrs.append(_DEFAULT_IMG_STYLE)
    return " ".join(attrs)


def _build_figures_html(tag: str, figures: list[dict[str, Any]]) -> str:
    if not figures:
        return ""
    blocks: list[str] = []
    for idx, fig in enumerate(figures, start=1):
        anchor = f"{tag}-figure-{idx}"
        url = _to_absolute_img_url(fig.get("url", ""))
        raw_title = fig.get("title", "")
        alt_title = _strip_md(raw_title)
        caption_title = _md_to_html(raw_title)
        img_attrs = _build_img_attrs(fig)
        blocks.append(
            f'<div align="center" id="{anchor}">\n'
            f'  <img src="{url}" alt="{alt_title}" {img_attrs} />\n'
            f"  <p><em><strong>Figure {idx}.</strong> {caption_title}</em></p>\n"
            f"</div>"
        )
    return "\n\n".join(blocks)


def _insert_figures_before_examples(md: str, figures_html: str) -> str:
    if not figures_html:
        return md
    pattern = r"(\n###\s+Examples\b)"
    if re.search(pattern, md):
        return re.sub(pattern, r"\n\n" + figures_html + r"\1", md, count=1)
    return md.rstrip() + "\n\n" + figures_html + "\n"


def _replace_figure_refs(md: str, tag: str, num_figures: int) -> str:
    if num_figures <= 0:
        return md

    def replacer(m: re.Match[str]) -> str:
        n = m.group(1)
        anchor = f"{tag}-figure-{n}"
        return f"[Fig. {n}](#{anchor})"

    return re.sub(r"(?<!\[)Fig\.\s*(\d+)", replacer, md)


def main():
    output = os.path.join(ROOT, "..", "README.md")

    with open(os.path.join(ROOT, "header.md"), "r", encoding="utf-8") as f:
        header = f.read()

    catalog: list[tuple[str, str, str]] = []
    articles: list[str] = []

    for key, model in schema.items():
        spec = model.model_json_schema()
        figures = spec.get("x-figures", []) or []
        spec = compact_examples(spec)
        md = schema2markdown(spec)

        brief = spec.get("description", "") or spec.get("x-brief", "")
        md = re.sub(r"^#", r"##", md, flags=re.MULTILINE)
        tag = key.lower().replace("/", "").replace(" ", "-")

        figures_html = _build_figures_html(tag, figures)
        md = _insert_figures_before_examples(md, figures_html)
        md = _replace_figure_refs(md, tag, len(figures))

        catalog.append((key, tag, brief))
        articles.append(f'<a id="{tag}"></a>\n{md}')

    neck = "## Catalog\n\n" + "\n".join([f"- [{k}](#{t}) {b}" for k, t, b in catalog])

    joined_articles = "\n\n".join(articles)
    joined_articles = fix_markdown_headers(joined_articles)
    joined_articles = fix_markdown_links_and_anchors(joined_articles)
    content = "\n\n".join([header, neck, joined_articles])

    with open(output, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
