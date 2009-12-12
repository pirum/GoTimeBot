import re

VERSE_SPLIT_REGEX = re.compile(r'\d{1,2}:\d{1,2}')

f = open('data/king_james_bible_raw.txt')

for line in f.xreadlines():

    line = line.strip()
    
    if line == '':
        continue
    
    lines = VERSE_SPLIT_REGEX.split(line)
    assert len(lines) >= 1
    
    for line in lines:
        line = line.strip()
        if line == '':
            continue
            
        print line

