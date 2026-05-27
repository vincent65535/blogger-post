import re
import markdown
from pygments.formatters import HtmlFormatter


def _convert_fenced_to_indented(text):
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s+)(```+|~~~+)(\w*)$', line)
        if m and len(m.group(1)) >= 2:
            indent = m.group(1)
            fence = m.group(2)
            j = i + 1
            while j < len(lines) and not re.match(r'^' + re.escape(indent) + re.escape(fence[0]) + r'+$', lines[j]):
                j += 1
            if j < len(lines):
                code_indent = ' ' * 8
                result.append('')
                for k in range(i + 1, j):
                    cl = lines[k]
                    result.append(code_indent + cl[len(indent):] if cl.startswith(indent) else code_indent + cl)
                result.append('')
                i = j + 1
                continue
        result.append(line)
        i += 1
    return '\n'.join(result)


def markdown_to_html(file_path=None, content=None, inline_css=True, line_width=0):
    if content is not None:
        md_content = content
    elif file_path is not None:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    else:
        raise ValueError('Either file_path or content must be provided')

    md_content = _convert_fenced_to_indented(md_content)

    html = markdown.markdown(
        md_content,
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'extra'
        ]
    )

    if inline_css:
        css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
        html = f'<style>{css}</style>\n{html}'

    if line_width > 0:
        html = f'<div style="max-width:{line_width}ch;margin:0 auto">\n{html}\n</div>'

    return html
