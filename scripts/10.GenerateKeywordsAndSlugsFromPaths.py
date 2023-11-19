paths_file = '../input/_paths.txt'
keywords_file = '../input/_keywords.txt'
slugs_file = '../input/_slugs.txt'
keywords = []
slugs = []

with open(paths_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        dirs = line.split('/')
        if len(dirs) > 1 and '' in dirs:
            del dirs[dirs.index('')]
        slug = dirs[-1]
        dirs.reverse()
        keyword = ''
        cnt = 1
        for d in dirs:
            keyword += d.replace('-', ' ') + ' category'
            if cnt < len(dirs):
                keyword += ' under '
            cnt += 1

        keywords.append(keyword)
        slugs.append(slug)

with open(keywords_file, 'w', encoding='utf-8') as f:
    for keyword in keywords:
        f.write(keyword + '\n')

with open(slugs_file, 'w', encoding='utf-8') as f:
    for slug in slugs:
        f.write(slug + '\n')
