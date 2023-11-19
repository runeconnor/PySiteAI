from includes.constants import EXCLUDED_DIRS
from functions.util import get_all_dirs_from_xml_sitemap

sitemap_path = r'D:\wamp64\www\sitemap.xml'
site_url = 'https://productsearch.pw/'
dst_path = 'all_dirs.txt'

dirs = get_all_dirs_from_xml_sitemap(sitemap_path, site_url, dst_path, EXCLUDED_DIRS)

print(dirs)

