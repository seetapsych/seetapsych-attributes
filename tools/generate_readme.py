#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import os.path
from typing import Any

if not os.environ.get('LANG'):
    os.environ['LANG'] = 'en_US.UTF-8'

import jsonschema2md

from fabopsy_attributes.schema import schema


ROOT = os.path.dirname(os.path.abspath(__file__))


def schema2markdown(schema: dict[str, Any]) -> str:
    parser = jsonschema2md.Parser()

    md = parser.parse_schema(schema, fail_on_error_in_defs=False)
    return ''.join(md)


def fix_markdown_headers(text: str) -> str:
    lines = text.splitlines()
    result = []

    for i, line in enumerate(lines):
        if line.startswith('#'):
            if i > 0 and lines[i - 1].strip() != '':
                result.append('')
        result.append(line)

    return '\n'.join(result)


def main():
    output = os.path.join(ROOT, '..', 'README.md')

    with open(os.path.join(ROOT, 'header.md'), 'r', encoding='utf-8') as f:
        header = f.read()

    catalog: list[tuple[str, str, str]] = []
    articles: list[str] = []

    for key, model in schema.items():
        spec = model.model_json_schema()
        md = schema2markdown(spec)

        brief = spec.get('x-brief', '')
        md = re.sub(r'^#', r'##', md, flags=re.MULTILINE)
        tag = key.lower().replace('/', '').replace(' ', '-')

        catalog.append((key, tag, brief))
        articles.append(f'<a id="{tag}"></a>\n{md}')

    neck = '## Catalog\n\n' + '\n'.join([
        f'- [{k}](#{t}) {b}' for k, t, b in catalog
    ])

    content = '\n\n'.join([header, neck, *articles])
    content = fix_markdown_headers(content)

    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    main()
