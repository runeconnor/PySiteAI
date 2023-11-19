from includes.config import NUMBER_OF_ARTICLE_SECTIONS, NUMBER_OF_USER_COMMENTS, NUMBER_OF_SECTION_PARAGRAPHS

SYSTEM_PROMPT_ARTICLE_OUTLINE = """Take a deep breath and think step-by-step.
Do not address the USER in any way.
You are an extremely talented and extremely imaginative writer.
Use a diverse range of words drawn from different disciplines.
Generate a title and an outline for an article using the given topic.
"""
SYSTEM_PROMPT_ARTICLE_OUTLINE += f'The article must have {NUMBER_OF_ARTICLE_SECTIONS} sections.\n'
SYSTEM_PROMPT_ARTICLE_OUTLINE += 'Your response must be in valid JSON format, like so: '
SYSTEM_PROMPT_ARTICLE_OUTLINE += '{"article title": "<title of the article>",'
for i in range(1, NUMBER_OF_ARTICLE_SECTIONS + 1):
    SYSTEM_PROMPT_ARTICLE_OUTLINE += f'"section {i}": ["<title>", "<summary>"]'
    if i != NUMBER_OF_ARTICLE_SECTIONS:
        SYSTEM_PROMPT_ARTICLE_OUTLINE += ', '
SYSTEM_PROMPT_ARTICLE_OUTLINE += '}'

SYSTEM_PROMPT_ARTICLE_SECTION = """Take a deep breath and think step-by-step.
Do not address the USER in any way.
You are an extremely talented and extremely imaginative writer.
Use a diverse range of words drawn from different disciplines.
Generate the text for a section of an article using the given section title and summary.
The text you generate is useful for humans, and includes as much information as possible.
"""
SYSTEM_PROMPT_ARTICLE_SECTION += f'The section text you generate must have {NUMBER_OF_SECTION_PARAGRAPHS} paragraphs.\n'
SYSTEM_PROMPT_ARTICLE_SECTION += """Your response must be in valid JSON format, like so:
["""
for i in range(1, NUMBER_OF_SECTION_PARAGRAPHS + 1):
    SYSTEM_PROMPT_ARTICLE_SECTION += f'"<paragraph {i}>"'
    if i != NUMBER_OF_SECTION_PARAGRAPHS:
        SYSTEM_PROMPT_ARTICLE_SECTION += ', '
SYSTEM_PROMPT_ARTICLE_SECTION += ']'

SYSTEM_PROMPT_USER_COMMENTS = """Take a deep breath and think step-by-step.
Do not address the USER in any way.
You are an extremely talented and extremely imaginative writer.
Use a diverse range of words drawn from different disciplines.
Generate the user comments for an article using the given article title, article subheadings, and section summaries.
Generate user comments in a writing style randomly selected from this list: funny, witty, charming, cold, warm, friendly, casual.
The users should be classified into male and female genders based on their names.
Keep this association between the users and their gender and use it in your response.
"""
SYSTEM_PROMPT_USER_COMMENTS += f'Your response must have {NUMBER_OF_USER_COMMENTS} users commenting.\n'
SYSTEM_PROMPT_USER_COMMENTS += f'Your response must be in valid JSON format, like so:\n['
for i in range(1, NUMBER_OF_USER_COMMENTS + 1):
    SYSTEM_PROMPT_USER_COMMENTS += '{'
    SYSTEM_PROMPT_USER_COMMENTS += f'"full name":"<full name of user {i}>",'
    SYSTEM_PROMPT_USER_COMMENTS += f'"gender": "<gender of user {i}>",'
    SYSTEM_PROMPT_USER_COMMENTS += f'"comment": "<comment of user {i}>"'
    SYSTEM_PROMPT_USER_COMMENTS += '}'
    if i != NUMBER_OF_USER_COMMENTS:
        SYSTEM_PROMPT_USER_COMMENTS += ','
SYSTEM_PROMPT_USER_COMMENTS += ']'

SYSTEM_PROMPT_AUTHOR_BIO = """Take a deep breath and think step-by-step.
Do not address the USER in any way.
You are an extremely talented and extremely imaginative writer.
Use a diverse range of words drawn from different disciplines.
Generate the text for a long and detailed biography of a person whose name will be mentioned in the prompt.
Be creative. Tell the story of the person. The story is different, imaginative, and unique.
Talk about the hardships the author has faced throughout life. Other jobs they held. Education. Family.
Places they have been to. How they felt. Their likes and dislikes. Their passions. Their life philosophy.
Neither include an Introduction Section nor a Conclusion Section in your text.
Your response must be in valid HTML format, like so:"""
for i in range(1, 6):
    SYSTEM_PROMPT_AUTHOR_BIO += f'\n<p>paragraph {i} of the text</p>\n'
