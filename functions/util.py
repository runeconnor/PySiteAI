from includes.constants import *


def addslashes_php(data: str) -> str:
    return data.replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")


def combine_section_texts(section_texts: dict) -> str:
    php = '$section_texts = [\n'
    num_sections = len(section_texts)
    for idx in range(1, num_sections + 1):
        text = section_texts[idx]
        php += f'"{text}"'
        if idx == num_sections:
            php += '\n'
        else:
            php += ',\n'
    php += '];\n'
    return php


def convert_image_to_webp(full_path: str) -> None:
    from PIL import Image
    from pathlib import Path

    allowed_extensions = ['.jpg', '.jpeg', '.png']
    full_path = Path(full_path)

    if full_path.suffix in allowed_extensions:
        print('Converting:', full_path)
        img = Image.open(full_path)
        new_file_path = full_path.with_suffix('.webp')
        img.save(new_file_path)
        print('Done:', full_path)


def count_files(full_path: str, file_extension: str='') -> int:
    from pathlib import Path

    cnt = 0
    for item in Path(full_path).iterdir():
        if item.is_file():
            if file_extension:
                if item.suffix == file_extension:
                    cnt += 1
            else:
                cnt += 1

    return cnt


def count_folders(full_path: str) -> int:
    from pathlib import Path

    cnt = 0
    for item in Path(full_path).iterdir():
        if item.is_dir():
            cnt += 1

    return cnt


def create_subfolders_from_keywords(parent_dir_full_path: str, keywords_file_full_path: str) -> list[tuple[str, str]]:
    """
    Creates the subfolders where each item returned by the API call will be stored.
    Returns the list of keywords used and the folders created as a list of (folder, keyword) tuples.
    :param parent_dir_full_path: Full path to the parent directory where subfolders will be created.
    :param keywords_file_full_path: Full path to the keywords file, where each keyword is given in its own line.
    :return: Returns the list of keywords used and the folders created as a list of (folder, keyword) tuples.
    """
    from os import path, mkdir
    from re import sub
    from pathlib import Path
    parent_dir_full_path = Path(parent_dir_full_path)
    keywords_file_full_path = Path(keywords_file_full_path)

    folders_and_keywords = []
    with open(keywords_file_full_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.lower().strip()
            removed = line.replace(' &', '')
            folder_name = sub(r'[^a-z0-9\s+]', '', removed).replace(' ', '-')
            folders_and_keywords.append((folder_name, line))

    for folder, _ in folders_and_keywords:
        path_full = path.join(parent_dir_full_path, folder)
        if not path.exists(path_full):
            mkdir(path_full)

    # returns a list of (folder, keyword) tuples
    return folders_and_keywords


def decode_json(ai_response_json: str, relative_path):
    ai_response = None
    from json import loads, decoder
    try:
        ai_response = loads(ai_response_json)
    except decoder.JSONDecodeError:
        print(f"{ConsoleColors.WARNING}- JSON DECODE: FAILED {relative_path} -- "
              f"Invalid JSON, trying dirtyjson package to decode...{ConsoleColors.ENDC}")
        from dirtyjson import loads
        ai_response = loads(ai_response_json)
        ai_response = str(ai_response[0]).split('\n\n')
    finally:
        return ai_response


def finish_up_index_php() -> str:
    php = """$contents = $h1.$img_below_h1;
for ($i = 0; $i < $number_of_sections; $i++) {
    if (count($section_images) < $i + 1) {
        $section_images[$i] = "";
    }
    $contents .= $section_titles[$i].$section_images[$i].$section_texts[$i];
}
$contents .= $author.$comments;

include_once("{$root}_inc/template_v2.php");"""
    return php


def generate_breadcrumbs(relative_path: str) -> str:
    from pathlib import Path

    dirs = str(Path(relative_path)).split('\\')
    home_path = '../' * len(dirs)
    breadcrumbs = (r'<div class=\"breadcrumb\">\n<ul>\n<li>'
                   + f'<a href=\\"{home_path}\\">Home</a></li>\\n')
    link = home_path
    for slug in dirs:
        link_text = slug.replace('-', ' ').title()
        link += slug + '/'
        if slug != dirs[-1]:
            breadcrumbs += (r'<li><a href=\"' + link + r'\">'
                            + link_text + r'</a></li>\n')
        else:
            breadcrumbs += (r'<li>' + link_text + r'</li>\n')
    breadcrumbs += r'</ul>\n</div>'
    return breadcrumbs


def generate_child_links(full_path: str) -> str:
    from pathlib import Path

    child_links = ''
    for subdir in Path(full_path).iterdir():
        if subdir.is_dir():
            slug = subdir.name
            if (slug not in EXCLUDED_DIRS) and (slug[0] != '_'):
                text = slug.replace('-', ' ').title()
                child_links += f'<a href=\\"{slug}\\">{text}</a><br />\n'
    return child_links


def generate_random_author_info_box(author_root_folder_full_path: str) -> str:
    from random import randint
    from includes.config import DATE_START

    author_bio_snippet = '!ERROR!'
    author_gender = '!ERROR!'
    author_img = '!ERROR!'
    author_name = '!ERROR!'
    author_slug = '!ERROR!'

    author_folders = get_subfolders(author_root_folder_full_path)
    idx = randint(1, len(author_folders))
    author_link = author_folders[idx - 1]

    index_php_path = author_link + '\\index.php'

    with open(index_php_path, 'r', encoding='utf-8') as f:
        index_php = f.readlines()

    cnt = 1
    for line in index_php:
        if cnt == 3:
            s = line.strip()
            if s.startswith('$title'):
                author_name = s.lstrip('$title = "').rstrip(' Author Bio";')
            else:
                raise Exception(f"Err: $title not found on line 3 at:\n{index_php_path}")
        elif cnt == 4:
            s = line.strip()
            if s.startswith('$slug'):
                author_slug = s.lstrip('$slug = "').rstrip('";')
            else:
                raise Exception(f"Err: $slug not found on line 4 at:\n{index_php_path}")
            author_slug_from_name = author_name.lower().replace(' ', '-')
            if author_slug != author_slug_from_name:
                author_slug = author_slug_from_name
                print('Error: Author slug is different from slug generated from author name. Please check!')
                print('--Author Name:', author_name)
        elif cnt == 10:
            s = line.strip()
            if s.startswith('$img_author'):
                author_img = s.lstrip('$img_author = "').rstrip('";')
                if author_img.endswith(r'female.jpg\">\n'):
                    author_gender = 'female'
                elif author_img.endswith(r'male.jpg\">\n'):
                    author_gender = 'male'
                else:
                    raise Exception(f"Err: Cannot determine gender on line 10 at:\n{index_php_path}")
            else:
                raise Exception(f"Err: $img_author not found on line 10 at:\n{index_php_path}")
        elif cnt == 11:
            s = line.strip()
            if s.startswith('$bio'):
                author_bio_snippet = s.lstrip('$bio = "')[:100]
            else:
                raise Exception(f"$bio not found on line 11 at:\n{index_php_path}")
        cnt += 1

    info_box_html = r'<div class=\"author\">\n'
    info_box_html += f'Published: {generate_random_date(DATE_START)}<br><br>\\n'
    info_box_html += author_img
    info_box_html += r'Author: <a href=\"{$root}author/'
    info_box_html += author_slug + r'\">' + author_name + r'</a>\n'
    info_box_html += author_bio_snippet + r'...\n'
    info_box_html += r'</div>\n'

    php = '$author = \"'
    php += info_box_html
    php += '\";\n'

    return php


def generate_random_date(start: str, time_format: str = '%m/%d/%Y'):
    from random import random
    from time import mktime, strptime, strftime, localtime

    start = mktime(strptime(start, time_format))
    end = mktime(localtime())
    multiplier = random()
    random_date = start + multiplier * (end - start)

    return strftime(time_format, localtime(random_date))


def generate_same_level_links(full_path: str) -> str:
    from pathlib import Path
    full_path = Path(full_path)

    this = full_path.name
    same_level_links = ''
    for subdir in full_path.parent.iterdir():
        if subdir.is_dir():
            slug = subdir.name
            if (slug not in EXCLUDED_DIRS) and (slug[0] != '_') and (slug != this):
                text = slug.replace('-', ' ').title()
                same_level_links += f'<a href=\\"../{slug}\\">{text}</a><br />\n'
    return same_level_links


def get_all_dirs_from_xml_sitemap(sitemap_path: str, site_url: str, dst_path: str, exclude_dirs: list) -> list:
    import xml.etree.ElementTree

    tree = xml.etree.ElementTree.parse(sitemap_path)
    root = tree.getroot()

    all_dirs = []
    for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text.replace(site_url, '')
        skip = False
        for xdir in exclude_dirs:
            if loc.startswith(xdir) or loc == '':
                skip = True
                break
        if not skip:
            all_dirs.append(loc)
    with open(dst_path, 'w', encoding='utf-8') as f:
        cnt = 1
        for loc in all_dirs:
            if cnt < len(all_dirs):
                f.write(loc + '\n')
            else:
                f.write(loc)
            cnt += 1
    return all_dirs


def get_list_of_all_files_in_folder(full_path: str) -> list:
    from pathlib import Path
    full_path = Path(full_path)
    list_of_files = [x for x in full_path.iterdir() if x.is_file()]
    return list_of_files


def get_subfolders(full_path: str) -> list[str]:
    from os import scandir
    subfolders = [f.path for f in scandir(full_path) if f.is_dir()]
    return subfolders


def get_user_confirmation(message: str) -> bool:
    valid_responses = ('y', 'yes', 'n', 'no')
    negative_responses = ('n', 'no')
    while True:
        user_response = input(message)
        user_response = user_response.lower()
        if user_response not in valid_responses:
            print('Error: Please type either "y" or "n".')
        elif user_response in negative_responses:
            return False
        else:
            return True


def initialize_error_log():
    import logging
    from datetime import datetime

    now = datetime.now().strftime("%Y_%m_%d_%Hh_%Mm_%Ss")
    logfile = f'error_log_{now}.log'
    logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')


def make_dirs(dir_paths: list = None, file_path: str = None) -> None:
    """
    Creates directories based on given list of paths. or file containing a list of paths.
    :param dir_paths:
    :param file_path:
    :return:
    """
    from pathlib import Path

    if dir_paths is not None:
        for d in dir_paths:
            d = Path(d.strip())
            d.mkdir(exist_ok=True)
    elif file_path is not None:
        with open(file_path, 'r', encoding='utf-8') as f:
            for d in f:
                d = Path(d.strip())
                d.mkdir(exist_ok=True)


def rename_and_move_profile_images(next_num: int, src_full_path: str, dst_full_path: str) -> None:
    from os import listdir
    from shutil import move

    src_files = listdir(src_full_path)

    for idx, name in enumerate(src_files):
        num = next_num + idx
        src = f'{src_full_path}\\{name}'
        dst = f'{dst_full_path}\\{num}.jpg'

        move(src, dst)


def parse_user_comments(ai_response_dict: dict) -> str:
    """
    Changes user comments from JSON to HTML format.
    :param ai_response_dict: User comments in dict format.
    :return: User comments in HTML format.
    """
    from random import randint
    from bs4 import BeautifulSoup

    user_comments_html = '<h2>User Comments</h2>\n<div class=\\"comments\\">\n<ul>\n'
    for i in range(len(ai_response_dict)):
        name = ai_response_dict[i]['full name']
        name = BeautifulSoup(name, "html.parser").text
        gender = ai_response_dict[i]['gender']
        gender = BeautifulSoup(gender, "html.parser").text
        comment = ai_response_dict[i]['comment']
        comment = BeautifulSoup(comment, "html.parser").text
        profile_image_dir_local = ROOT_PATH + PROFILE_IMAGE_DIR_PATH
        profile_image_dir_server = addslashes_php(r'{$root}' + PROFILE_IMAGE_DIR_PATH)
        ext = PROFILE_IMAGE_FILE_EXTENSION
        g = 'm'
        if gender == 'female':
            g = 'f'
        profile_image_id = randint(1, count_files(profile_image_dir_local + f'/{g}', ext))
        user_comments_html += '<li>' \
                              f'<img src=\\"{profile_image_dir_server}{g}/{profile_image_id}{ext}\\">' \
                              f'<b>{name}</b>: {comment}</li>\n'
    user_comments_html += '</ul>\n</div>\n'

    php = '$comments = "'
    php += user_comments_html
    php += '";\n'

    return php
