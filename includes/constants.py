from threading import Lock

OPENAI_API_KEY = ""  # Set your OpenAI API key here or as an environment variable called API_KEY
BACKUP_PATH = "G:/My Drive/Web/_Backup/"  # All AI responses are backed up here as files
ROOT_PATH = "D:/wamp64/www/"  # Where your website is stored on your local machine
IMAGE_DIR_PATH = "_img/"
PROFILE_IMAGE_DIR_PATH = IMAGE_DIR_PATH + "profiles/"
PROFILE_IMAGE_FILE_EXTENSION = ".webp"
AUTHOR_DIR_PATH = "author/"
AUTHOR_IMAGE_DIR_PATH = IMAGE_DIR_PATH + "author/"

LANGUAGES = [
    ('English', 'en'),
    ('German', 'de'),
    ('French', 'fr'),
    ('Spanish', 'es'),
    ('Russian', 'ru'),
    ('Portuguese', 'pt'),
    ('Chinese', 'zh'),
    ('Italian', 'it'),
    ('Polish', 'pl'),
    ('Arabic', 'ar'),
    ('Dutch', 'nl'),
    ('Ukrainian', 'uk'),
    ('Hebrew', 'he'),
    ('Indonesian', 'id'),
    ('Turkish', 'tr'),
    ('Vietnamese', 'vi'),
    ('Czech', 'cs'),
    ('Swedish', 'sv'),
    ('Korean', 'ko'),
    ('Finnish', 'fi'),
    ('Persian', 'fa'),
    ('Japanese', 'ja'),
    ('Hungarian', 'hu'),
    ('Hindi', 'hi'),
    ('Bangla', 'bn'),
    ('Thai', 'th'),
    ('Norwegian', 'no'),
    ('Catalan', 'ca'),
    ('Greek', 'el'),
    ('Romanian', 'ro'),
    ('Danish', 'da'),
    ('Serbian', 'sr'),
    ('Bulgarian', 'bg'),
    ('Malay', 'ms'),
    ('Azerbaijani', 'az'),
    ('Slovak', 'sk'),
    ('Estonian', 'et'),
    ('Armenian', 'hy'),
    ('Croatian', 'hr'),
    ('Uzbek', 'uz')
]

TEMPERATURE = {
    'creative': 0.85,
    'balanced': 0.70,
    'precise': 0.55,
    'code': 0.35
}

LOCKS = {
    'write': Lock(),
    'global_cnt': Lock(),
    'api_delay_cnt': Lock()
}


class ConsoleColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


EXCLUDED_DIRS = ['_img', '_inc', '_test', 'about', 'author', 'contact', 'privacy', 'r', 'tr', 'terms']
