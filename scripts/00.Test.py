from functions.util import count_files
from includes.constants import ROOT_PATH, PROFILE_IMAGE_DIR_PATH, PROFILE_IMAGE_FILE_EXTENSION

profile_image_dir_local = ROOT_PATH + PROFILE_IMAGE_DIR_PATH
g = 'm'
ext = PROFILE_IMAGE_FILE_EXTENSION
print(count_files(profile_image_dir_local + f'/{g}', ext))
