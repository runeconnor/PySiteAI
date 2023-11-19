"""
Generates ai-written biographies from a list of author names.
"""

from os import path, mkdir

from includes.config import NUM_THREADS
from includes.constants import ConsoleColors, ROOT_PATH, TEMPERATURE
from functions.util import write_author_bio
from concurrent.futures import ThreadPoolExecutor

num_authors = 200
num_sections = 5

src_path = f'names/100_female_author_names.txt'
with open(src_path, 'r', encoding='utf-8') as f:
    female = f.readlines()

src_path = f'names/100_male_author_names.txt'
with open(src_path, 'r', encoding='utf-8') as f:
    male = f.readlines()

all_items = []
for item in female:
    author_name = item.strip()
    slug = author_name.lower().replace(' ', '-')
    gender = 'female'
    relative_path = 'author/' + slug
    full_path = ROOT_PATH + relative_path

    if not path.exists(full_path):
        mkdir(full_path)

    all_items.append((relative_path, author_name, slug, gender,
                     TEMPERATURE['creative'], num_authors))

for item in male:
    author_name = item.strip()
    slug = author_name.lower().replace(' ', '-')
    gender = 'male'
    relative_path = 'author/' + slug
    full_path = ROOT_PATH + relative_path

    if not path.exists(full_path):
        mkdir(full_path)

    all_items.append((relative_path, author_name, slug, gender,
                     TEMPERATURE['creative'], num_authors))

num_all_items = len(all_items)
avg_len = num_all_items // NUM_THREADS

# Lists to be executed by each thread
sub_lists = [all_items[i:i + avg_len] for i in range(0, num_all_items, avg_len)]

# Add any remaining items to sub_lists
if num_all_items % NUM_THREADS != 0:
    sub_lists[-1].extend(all_items[NUM_THREADS * avg_len:])

# Execute
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    for sublist in sub_lists:
        executor.map(write_author_bio, sublist)

print(f'\n{ConsoleColors.OKGREEN}ALL DONE!{ConsoleColors.ENDC}')
