from functions.util import *
from includes.constants import *

full_path_to_the_folder_containing_the_images = ROOT_PATH + '_img\logo'
list_of_files = get_list_of_all_files_in_folder(full_path_to_the_folder_containing_the_images)
for file_path in list_of_files:
    convert_image_to_webp(file_path)