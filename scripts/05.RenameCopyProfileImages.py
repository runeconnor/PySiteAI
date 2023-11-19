"""
Renames and copies profile images generated manually using generative ai (like Leonardo.ai)
to appropriate folder in the target website.
"""
from functions.util import rename_and_move_profile_images, count_files

src_path_full_female = r'D:\Yedek\__temp\f'
src_path_full_male = r'D:\Yedek\__temp\m'
dst_path_full_female = r'G:\My Drive\Web\ProductSearch.pw\assets\Images\ai_generated\profiles\f'
dst_path_full_male = r'G:\My Drive\Web\ProductSearch.pw\assets\Images\ai_generated\profiles\m'
next_num_female = count_files(dst_path_full_female) + 1
next_num_male = count_files(dst_path_full_male) + 1
rename_and_move_profile_images(next_num_female, src_path_full_female, dst_path_full_female)
rename_and_move_profile_images(next_num_male, src_path_full_male, dst_path_full_male)

print('Done.')
