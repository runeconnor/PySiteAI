"""
Generates an XML sitemap fot the target website that has a folder structure for pages.
"""

import os

from includes.constants import EXCLUDED_DIRS

root = r"D:\wamp64\www"
site = "https://productsearch.pw"


def generate_sitemap_xml(root_dir, site_url):
    size = len(root_dir)
    sitemap_filename = 'sitemap.xml'
    sitemap_xml_contents = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""
    for dirpath, dirnames, _ in os.walk(root_dir):
        dirs = dirpath.split('\\')
        if len(dirs) > 3 and dirs[3] in EXCLUDED_DIRS:   # Exclude special dirs
            continue
        url = dirpath.replace(r'D:\wamp64\www', site_url).replace('\\', '/') + '/'
        print(url)
        sitemap_xml_contents += '    <url>\n        <loc>'
        sitemap_xml_contents += url
        sitemap_xml_contents += '</loc>\n    </url>\n'
    sitemap_xml_contents += '</urlset>'

    with open(f'{root_dir}\\{sitemap_filename}', 'w', encoding='utf-8') as f:
        f.write(sitemap_xml_contents)


generate_sitemap_xml(root, site)
