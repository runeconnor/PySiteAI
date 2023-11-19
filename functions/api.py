import time

from functions.util import *
from includes.config import *
from includes.constants import *
from includes.prompts import *

global_cnt = 0
api_delay_cnt = 0


def call_openai_api(system_prompt: str, user_prompt: str, model: str, temperature: float) -> str:
    """
    Calls OpenAI API and returns the response.
    :param system_prompt: The system prompt - Use this to describe how you want the AI model to behave.
    :param user_prompt: The user prompt - Use this to describe what you want the AI model to do.
    :param model: The AI model that will be used.
    :param temperature: How creative do you want the AI to be? Values between 0.0 (deterministic) and 2.0 (crazy).
    :return: The response of the AI model.
    """
    from os import environ
    import openai

    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
    else:
        openai.api_key = environ["OPENAI_API_KEY"]

    system_msg = [{"role": "system", "content": system_prompt}]
    user_msg = [{"role": "user", "content": user_prompt}]

    msgs = system_msg + user_msg
    response = openai.ChatCompletion.create(model=model,
                                            messages=msgs,
                                            temperature=temperature)
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."

    return response["choices"][0]["message"]["content"]


def write_article(data: tuple) -> None:
    from time import sleep
    from os import path
    from pathlib import Path
    from bs4 import BeautifulSoup

    relative_path, keyword, slug, outline_temperature, \
        article_temperature, user_comments_temperature, num_all_keywords = data

    global global_cnt
    global api_delay_cnt

    while LOCKS['api_delay_cnt'].locked():
        time.sleep(0.01)
    with LOCKS['api_delay_cnt']:
        api_delay_cnt += API_CALL_DELAY

    sleep(api_delay_cnt)

    relative_path = Path(relative_path)
    full_path = Path(ROOT_PATH).joinpath(relative_path)
    index_php_path = full_path.joinpath('index.php')
    index_php = ''

    dirs = relative_path.parts
    home_path = '../' * len(dirs)

    if not path.exists(index_php_path):
        article_generated = False
        article_outline_generated = False
        section_texts_generated = {}
        for idx in range(1, NUMBER_OF_ARTICLE_SECTIONS + 1):
            section_texts_generated[idx] = False
        article_text_generated = False
        author_info_box_generated = False
        user_comments_generated = False

        outline = {}
        section_texts = {}

        print(f'Writing: {relative_path}\n')

        while not article_generated:
            try:
                # ARTICLE OUTLINE
                while not article_outline_generated:
                    try:
                        prompt = 'Topic: products in ' + keyword + ' in online marketplaces.'
                        ai_response_json = call_openai_api(SYSTEM_PROMPT_ARTICLE_OUTLINE, prompt,
                                                           MODEL, outline_temperature)

                        ai_response_dict = decode_json(ai_response_json, relative_path)

                        # (dict) - outline['php'] will give you the php code
                        # you can also do outline['title'], outline['section titles'], and outline['section summaries']
                        outline = write_article_outline(ai_response_dict, home_path, slug, relative_path, full_path)
                        index_php += outline['php']

                    except Exception as err:
                        print(f"{ConsoleColors.FAIL}- OUTLINE: FAILED {relative_path}\n{err=},"
                              f"{type(err)=}{ConsoleColors.ENDC}")
                    else:
                        article_outline_generated = True
                        print(f'Outline generated for: {relative_path}\n')

                # ARTICLE SECTION TEXTS
                while (not article_text_generated) and article_outline_generated:
                    while False in section_texts_generated.values():
                        section_id = '!ERROR!'
                        try:
                            for idx in range(1, NUMBER_OF_ARTICLE_SECTIONS + 1):
                                if not section_texts_generated[idx]:
                                    section_id = idx

                            section_title = outline['section titles'][section_id]
                            section_summary = outline['section summaries'][section_id]
                            prompt = f'section title: {section_title}, section summary: {section_summary}'
                            ai_response_json = call_openai_api(SYSTEM_PROMPT_ARTICLE_SECTION, prompt,
                                                               MODEL, article_temperature)

                            ai_response_list = list(decode_json(ai_response_json, relative_path))
                            paragraphs = ai_response_list

                            section_text = ''
                            for paragraph in paragraphs:
                                paragraph = BeautifulSoup(paragraph, "html.parser").text
                                section_text += f'<p>{paragraph}</p>\\n'

                            section_texts[section_id] = section_text

                        except Exception as err:
                            print(f"{ConsoleColors.FAIL}- SECTION TEXT {section_id}: FAILED {relative_path}\n{err=},"
                                  f"{type(err)=}{ConsoleColors.ENDC}")
                        else:
                            section_texts_generated[section_id] = True
                            print(f'Section {section_id} generated for: {relative_path}\n')

                    index_php += combine_section_texts(section_texts)
                    article_text_generated = True
                    print(f'All section texts generated for: {relative_path}\n')

                # TODO: AUTHOR INFO BOX
                # generate 200 author images and add them to _img/author/[slug].webp
                # write a script to replace the images in author bios with these new images
                author_root_folder_full_path = ROOT_PATH + AUTHOR_DIR_PATH
                index_php += generate_random_author_info_box(author_root_folder_full_path)
                author_info_box_generated = True
                print(f'Author info box generated for: {relative_path}\n')

                # USER COMMENTS
                while (not user_comments_generated) and article_outline_generated:
                    try:
                        article_title = outline['title']
                        section_titles = outline['section titles']
                        section_summaries = outline['section summaries']
                        prompt = (f'article title: {article_title}\n'
                                  f'article subheadings: {section_titles}\n'
                                  f'section summaries: {section_summaries}')
                        ai_response_json = call_openai_api(SYSTEM_PROMPT_USER_COMMENTS, prompt,
                                                           MODEL, user_comments_temperature)

                        ai_response_dict = decode_json(ai_response_json, relative_path)
                        index_php += parse_user_comments(ai_response_dict)

                    except Exception as err:
                        print(f"{ConsoleColors.FAIL}- USER COMMENTS: FAILED {relative_path}\n{err=},"
                              f"{type(err)=}{ConsoleColors.ENDC}")
                    else:
                        user_comments_generated = True
                        print(f'User comments generated for: {relative_path}\n')

            except Exception as err:
                print(f"{ConsoleColors.FAIL}FAILED TO GENERATE ARTICLE! {relative_path}\n{err=},"
                      f"{type(err)=}{ConsoleColors.ENDC}")

            else:
                conditions = [
                    article_outline_generated,
                    article_text_generated,
                    author_info_box_generated,
                    user_comments_generated
                ]
                if not (False in conditions):
                    article_generated = True

                    # ADD FINISHING TOUCHES
                    index_php += finish_up_index_php()

                    # WRITE TO FILES
                    while LOCKS['write'].locked():
                        time.sleep(0.01)
                    with LOCKS['write']:
                        with open(index_php_path, 'w', encoding='utf-8') as f:
                            f.write(index_php)

                    while LOCKS['global_cnt'].locked():
                        time.sleep(0.01)
                    with LOCKS['global_cnt']:
                        global_cnt += 1

                    print(f'{ConsoleColors.OKCYAN}DONE | KEYWORD: {keyword}{ConsoleColors.ENDC}')
                    percentage = round(global_cnt / num_all_keywords * 100, 1)
                    print(relative_path, '--', f"{global_cnt}/{num_all_keywords} ({percentage}%)\n")
    else:
        print(f'{ConsoleColors.WARNING}Article exists, skipping...{relative_path}{ConsoleColors.ENDC}\n')
        while LOCKS['global_cnt'].locked():
            time.sleep(0.01)
        with LOCKS['global_cnt']:
            global_cnt += 1


def write_article_outline(ai_response: dict, home_path: str, slug: str,
                          relative_path, full_path) -> dict[str, str | dict[int, str]]:
    from bs4 import BeautifulSoup

    page_title = ai_response['article title']
    page_title = BeautifulSoup(page_title, "html.parser").text
    section_titles = {}
    section_summaries = {}

    php = f'<?php\n$root = \"{home_path}\";\n'
    php += f'$title = "{page_title}";\n'
    php += f'$slug = "{slug}";\n'
    php += f'$breadcrumbs = "{generate_breadcrumbs(relative_path)}";\n'
    php += f'$child_links = "{generate_child_links(full_path)}";\n'
    php += f'$same_level_links = "{generate_same_level_links(full_path)}";\n'
    php += f'$number_of_sections = {NUMBER_OF_ARTICLE_SECTIONS};\n'
    php += f'$h1 = "<h1>{page_title}</h1>\\n";\n'
    php += f'$img_below_h1 = "";\n'
    php += '$section_titles = [\n'
    for idx in range(1, NUMBER_OF_ARTICLE_SECTIONS + 1):
        section_title = ai_response[f'section {idx}'][0]
        section_title = BeautifulSoup(section_title, "html.parser").text
        section_summary = ai_response[f'section {idx}'][1]
        section_summary = BeautifulSoup(section_summary, "html.parser").text
        section_titles[idx] = section_title
        section_summaries[idx] = section_summary
        php += f'"<h2>{section_title}</h2>\\n"'
        if idx == NUMBER_OF_ARTICLE_SECTIONS:
            php += '\n'
        else:
            php += ',\n'
    php += '];\n'
    php += '$section_images = [\n'
    for idx in range(1, NUMBER_OF_SECTION_IMAGES + 1):
        php += '"<img class=\\"ibh2\\" alt=\\"{$title} '
        php += f'{idx}' + '\\" src=\\"{$slug}-' + f'{idx}.webp\\">"'
        if idx == NUMBER_OF_SECTION_IMAGES:
            php += '\n'
        else:
            php += ',\n'
    php += '];\n'

    result = {
        'title': page_title,
        'section titles': section_titles,
        'section summaries': section_summaries,
        'php': php
    }

    return result


def write_author_bio(data: tuple) -> None:
    from time import sleep
    from os import path
    from pathlib import Path

    relative_path, author_name, slug, gender, temperature, num_authors = data

    global global_cnt
    global api_delay_cnt

    while LOCKS['api_delay_cnt'].locked():
        time.sleep(0.01)
    with LOCKS['api_delay_cnt']:
        api_delay_cnt += API_CALL_DELAY

    sleep(api_delay_cnt)

    full_path = ROOT_PATH + relative_path
    contents_php_path = full_path + '/contents.php'
    contents_php = ''
    index_php_path = full_path + '/index.php'
    index_php = ''

    dirs = str(Path(relative_path)).split('\\')
    home_path = '../' * len(dirs)

    if not path.exists(contents_php_path):
        bio_generated = False
        while not bio_generated:
            try:
                print(f'Writing: {relative_path}\n')
                author_bio_html = call_openai_api(SYSTEM_PROMPT_AUTHOR_BIO, author_name,
                                                  MODEL, temperature)

                index_php = f'<?php\n$root = \"{home_path}\";\n'
                index_php += f'$title = "{author_name} Author Bio";\n'
                index_php += f'$slug = "{slug}";\n'
                index_php += f'$breadcrumbs = "{generate_breadcrumbs(relative_path)}";\n'
                index_php += f'$child_links = "";\n'
                index_php += f'$same_level_links = "";\n'
                index_php += 'include_once("{$root}_inc/template_v2.php");\n'

                contents_php = '<?php\n'
                contents_php += f'$h1 = "<h1>{author_name} Author Bio</h1>\\n";\n'
                contents_php += ('$img_author = "<img alt=\\"Author Profile Image\\"'
                                 'class=\\"img_author\\" src=\\"{$root}_img/profiles/'
                                 f'{gender}.jpg\\">\\n";\n')
                contents_php += f'$bio = "{addslashes_php(author_bio_html)}";\n'
                contents_php += '$contents = $h1.$img_author.$bio;\n'
                contents_php += 'echo $contents;\n'

            except Exception as err:
                print(f"{ConsoleColors.FAIL}- WRITING BIO: FAILED {relative_path}\n{err=},"
                      f"{type(err)=}{ConsoleColors.ENDC}")
            else:
                bio_generated = True

        if bio_generated:
            # WRITE TO FILES
            while LOCKS['write'].locked():
                time.sleep(0.01)
            with LOCKS['write']:
                with open(contents_php_path, 'w', encoding='utf-8') as f:
                    f.write(contents_php)

                with open(index_php_path, 'w', encoding='utf-8') as f:
                    f.write(index_php)

            while LOCKS['global_cnt'].locked():
                time.sleep(0.01)
            with LOCKS['global_cnt']:
                global_cnt += 1

            while LOCKS['api_delay_cnt'].locked():
                time.sleep(0.01)
            with LOCKS['api_delay_cnt']:
                api_delay_cnt -= API_CALL_DELAY

            print(f'{ConsoleColors.OKCYAN}DONE | KEYWORD: {author_name}{ConsoleColors.ENDC}')
            percentage = round(global_cnt / num_authors * 100, 1)
            print(relative_path, '--', f"{global_cnt}/{num_authors} ({percentage}%)")
    else:
        print(f'{ConsoleColors.WARNING}Biography exists, skipping...{relative_path}{ConsoleColors.ENDC}')
