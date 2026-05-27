import argparse
import json
import os
import sys
from oauth import get_credentials
from blogger import BloggerClient
from md_utils import markdown_to_html

CONFIG_FILE = 'config.json'


def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    return config


def extract_title_and_body(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        return '', ''
    title = lines[0].strip().lstrip('#').strip()
    body = ''.join(lines[1:])
    return title, body


def insert_more_tag(html):
    pos = html.find('</style>')
    if pos == -1:
        pos = 0
    else:
        pos = html.find('\n', pos)
        if pos != -1:
            pos += 1
    idx = html.find('\n', pos)
    if idx == -1:
        return html
    return html[:idx] + '\n<!--more-->' + html[idx:]


def main():
    parser = argparse.ArgumentParser(
        description='Publish posts to Blogger via API')
    parser.add_argument('--title', help='Post title (auto-extracted from first line of file if not specified)')
    parser.add_argument('--file', help='Path to a Markdown file for post content')
    parser.add_argument('--content', help='Raw HTML content (use if not using --file)')
    parser.add_argument('--labels', help='Comma-separated labels')
    parser.add_argument('--draft', action='store_true', help='Save as draft instead of publishing')
    parser.add_argument('--blog-id', help='Your Blogger Blog ID (or set in config.json)')

    args = parser.parse_args()

    if not args.file and not args.content:
        parser.error('Either --file or --content is required')

    if args.file and args.content:
        parser.error('Use only one of --file or --content')

    config = load_config()
    blog_id = args.blog_id or config.get('blog_id')
    if not blog_id:
        parser.error('--blog-id is required (or set it in config.json)')
    line_width = config.get('line_width', 0) or 0

    title = args.title
    if args.file:
        if title:
            html_content = markdown_to_html(args.file, line_width=line_width)
        else:
            title, body = extract_title_and_body(args.file)
            if body.strip():
                html_content = markdown_to_html(content=body, line_width=line_width)
            else:
                html_content = ''
    else:
        html_content = args.content

    if html_content:
        html_content = insert_more_tag(html_content)

    labels = [label.strip() for label in args.labels.split(',')] if args.labels else None

    try:
        credentials = get_credentials()
        client = BloggerClient(credentials)
        response = client.publish_post(
            blog_id=blog_id,
            title=title,
            content=html_content,
            labels=labels,
            is_draft=args.draft
        )
        print(f'Published successfully! URL: {response.get("url")}')
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
