from includes.constants import ROOT_PATH, TEMPERATURE

# CHANGE THESE AS NEEDED
DIR_PATH = ROOT_PATH + "automotive"  # Directory under which we are generating articles
KEYWORDS_FILE_PATH = "automotive.txt"
NUMBER_OF_ARTICLE_SECTIONS = 5
NUMBER_OF_SECTION_IMAGES = 4
NUMBER_OF_SECTION_PARAGRAPHS = 4
NUMBER_OF_USER_COMMENTS = 4

NUM_THREADS = 20
API_CALL_DELAY = 1  # seconds

MODEL = 'gpt-3.5-turbo'
OUTLINE_TEMPERATURE = TEMPERATURE['balanced']
ARTICLE_TEMPERATURE = TEMPERATURE['code']
USER_COMMENTS_TEMPERATURE = TEMPERATURE['balanced']

DATE_START = '8/1/2023'  # This is used for generating random dates for articles
