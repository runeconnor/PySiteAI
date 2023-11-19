"""
Reduces the website PHP files to index.php only from separate index.php and contents.php files.
This is to reduce the inodes limited by some hosting providers.
"""
from os import remove, path

from functions.util import get_subfolders

full_path = r'D:\wamp64\www\author'
folders = get_subfolders(full_path)

for folder in folders:
    index_php_path = folder + '\\index.php'
    contents_php_path = folder + '\\contents.php'

    if path.exists(contents_php_path):

        with open(index_php_path, 'r', encoding='utf-8') as f:
            index_php = f.read()

        with open(contents_php_path, 'r', encoding='utf-8') as f:
            contents_php = f.read()

        index_php = index_php.replace('include_once("{$root}_inc/template.php");\n', '')
        index_php = index_php.replace('$page_title', '$title').replace('$page_slug', '$slug')

        contents_php = contents_php.replace('<?php\n', '').replace('echo $contents;\n', '')

        index_php += contents_php
        index_php += 'include_once("{$root}_inc/template_v2.php");\n'

        with open(index_php_path, 'w', encoding='utf-8') as f:
            f.write(index_php)

        remove(contents_php_path)
