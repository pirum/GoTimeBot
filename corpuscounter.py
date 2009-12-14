import string

from nltk.corpus import brown


def process_brown(func, tag):
    for word in brown.tagged_words():
        if word[1].startswith(tag):
            func(word[0])

def print_word(word):
    print word
    
    
beginning_freqs = {}
vowel_freqs = {}
consonant_freqs = {}
vowels = ['a', 'e', 'i', 'o', 'u']
digraphs = ['ai', 'au', 'aw', 'ay', 'ch', 'ck', 'ea', 'ee', 'ei', 'ei', 'eu', 
    'ew', 'gh', 'ie', 'kn', 'ng', 'oa', 'oe', 'oo', 'ou', 'ow', 'ow', 'ph', 
    'qu', 'rh', 'sc', 'sh', 'th', 'wh', 'wr']
letters = [a for a in string.ascii_lowercase]
    
def do_counts(word):
    word = word.lower() + "x"
    
    if word[0] not in letters:
        return
        
    beginning = word[:2]
    if beginning not in digraphs:
        beginning = beginning[0]
    
    if beginning_freqs.has_key(beginning):
        beginning_freqs[beginning] += 1
    else:
        beginning_freqs[beginning] = 1
        
    queue = []    
    
    for letter in word:
        
        if letter not in letters:
            return
            
        queue.append(letter)
        if len(queue) == 1:
            continue
            
        is_vowel = queue[0] in vowels
        if is_vowel:
            using_list = vowel_freqs
        else:
            using_list = consonant_freqs
            
        digraph = ''.join(queue)
        if digraph in digraphs:
            if using_list.has_key(digraph):
                using_list[digraph] += 1
            else:
                using_list[digraph] = 1
            queue = queue[1:]
            continue
            
            
        if using_list.has_key(queue[0]):
            using_list[queue[0]] += 1
        else:
            using_list[queue[0]] = 1

    


process_brown(do_counts, tag="N")

print "beginning_freqs = ["
beginning_freqs.items().sort()
for k in beginning_freqs.keys():
    print "    ('%s', %s)," % (k, beginning_freqs[k])
print "]\n"

print "vowel_freqs = ["
vowel_freqs.items().sort()
for k in vowel_freqs.keys():
    print "    ('%s', %s)," % (k, vowel_freqs[k])
print "]\n"

print "consonant_freqs = ["
consonant_freqs.items().sort()
for k in consonant_freqs.keys():
    print "    ('%s', %s)," % (k, consonant_freqs[k])
print "]\n"


