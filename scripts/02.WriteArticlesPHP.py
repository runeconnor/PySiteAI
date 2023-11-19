"""
Generates ai-written articles for target website.
"""
from concurrent.futures import ThreadPoolExecutor

from pandas import read_excel
from functions.api import *

input_file_path = '../input/input.xlsx'
input_file = read_excel(input_file_path)
relative_paths = input_file['Relative_Paths']
keywords = input_file['Keywords']
slugs = input_file['Slugs']
outline_temperature = OUTLINE_TEMPERATURE
article_temperature = ARTICLE_TEMPERATURE
user_comments_temperature = USER_COMMENTS_TEMPERATURE
num_all_keywords = len(relative_paths)

all_items = []
for i in range(num_all_keywords):
    relative_path = relative_paths[i]
    keyword = keywords[i]
    slug = slugs[i]

    data = (relative_path, keyword, slug, outline_temperature,
            article_temperature, user_comments_temperature, num_all_keywords)

    all_items.append(data)

num_all_items = len(all_items)
avg_len = num_all_items // NUM_THREADS

# Lists to be executed by each thread
sub_lists = [all_items[i:i + avg_len] for i in range(0, num_all_items, avg_len)]

# Execute
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    for sublist in sub_lists:
        executor.map(write_article, sublist)

print(f'\n{ConsoleColors.OKGREEN}ALL DONE!{ConsoleColors.ENDC}')
