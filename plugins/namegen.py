import socrates

class NameGenPlugin(socrates.Plugin):
    
    def __init__(self, pluginRegistry):
        pluginRegistry.registerTrigger('NameGen:generate', '@namegen.*', self)
        self.nameGen = NameGen()
        
    def handleMessage(self, bot, triggerName, message):
        message = ', '.join(self.nameGen.generate_list(length=10))
        bot.say(message)
    
    

class NameGen(object):
    """
    Generates words that look like they could plausibly be English nouns.
    
    Add words to the blacklist to prevent certain words, e.g. curse words,
    from being generated.
    """
    
    # must be all lowercase
    blacklist = []
    
    beginning_freqs = [
        ('ch', 4495),
        ('ei', 126),
        ('ai', 656),
        ('ea', 482),
        ('ow', 132),
        ('kn', 403),
        ('eu', 188),
        ('au', 794),
        ('oa', 54),
        ('aw', 111),
        ('ay', 7),
        ('ew', 4),
        ('ie', 3),
        ('gh', 46),
        ('ng', 1),
        ('ee', 6),
        ('sh', 2209),
        ('th', 2304),
        ('ph', 832),
        ('rh', 194),
        ('oo', 3),
        ('wh', 498),
        ('sc', 2032),
        ('wr', 369),
        ('qu', 1038),
        ('a', 15029),
        ('c', 23206),
        ('b', 13420),
        ('e', 9685),
        ('d', 14140),
        ('g', 8037),
        ('f', 13043),
        ('i', 7657),
        ('h', 10465),
        ('k', 2183),
        ('j', 3849),
        ('m', 19442),
        ('l', 10265),
        ('o', 4810),
        ('n', 5653),
        ('q', 49),
        ('p', 23368),
        ('s', 25128),
        ('r', 13218),
        ('u', 2359),
        ('t', 12726),
        ('w', 10136),
        ('v', 3886),
        ('y', 2622),
        ('x', 66),
        ('ou', 302),
        ('z', 171),
        ('oe', 41),
    ]

    vowel_freqs = [
        ('a', 103528),
        ('oo', 3),
        ('ee', 7),
        ('e', 71346),
        ('ei', 126),
        ('ew', 4),
        ('i', 67633),
        ('eu', 188),
        ('ea', 483),
        ('o', 33902),
        ('ai', 656),
        ('ay', 7),
        ('au', 794),
        ('oa', 54),
        ('aw', 111),
        ('ow', 132),
        ('u', 29195),
        ('ou', 302),
        ('ie', 5),
        ('oe', 41),
    ]

    consonant_freqs = [
        ('ch', 5532),
        ('kn', 403),
        ('gh', 46),
        ('ng', 1),
        ('sh', 2209),
        ('th', 2304),
        ('ph', 832),
        ('rh', 194),
        ('wh', 498),
        ('sc', 2032),
        ('wr', 369),
        ('c', 171857),
        ('b', 77259),
        ('qu', 1038),
        ('d', 94965),
        ('g', 47695),
        ('f', 76287),
        ('h', 124331),
        ('k', 12094),
        ('j', 18714),
        ('m', 111874),
        ('l', 56004),
        ('n', 35338),
        ('q', 46),
        ('p', 160013),
        ('s', 157909),
        ('r', 92222),
        ('t', 73221),
        ('w', 52743),
        ('v', 24364),
        ('y', 12578),
        ('x', 149),
        ('z', 817),
    ]

    
    vowels = ['a', 'e', 'i', 'o', 'u']

    def __init__(self, seed=None):
        random.seed(seed)


    def _weighted_choice(self, lst):
        """
        Given a list of tuples, with each tuple consisting of 
        (choice, weight), returns a choice.
        
        For example, _weighted_choice([('one', 1), ('two', 5)])
        will usually return 'two'.
        """
        
        total_weight = reduce(lambda x,y:x+y, [tup[1] for tup in lst])
        n = random.uniform(0, total_weight)
        for item, weight in lst:
            if n < weight:
                break
            n = n - weight
        return item


    def generate_word(self, length=7, upper=True):
        """
        Generates a word of the given length consisting of alternating
        consonants and vowels. If upper is true, the first letter of the word 
        is uppercased. Will not return any of the words in self.blacklist
        """
        
        word = self._weighted_choice(self.beginning_freqs)

        if word[0] in self.vowels:
            offset = 0
        else:
            offset = 1
        
        for i in range(offset, length+offset):			
            if i%2 ==0:
                word += self._weighted_choice(self.consonant_freqs)
            else:
                word += self._weighted_choice(self.vowel_freqs)
            
        if upper:
            word = word[:1].upper() + word[1:]
        
        if word.lower() in self.blacklist:
            # recurse and find another word
            return self.generate_word(length, upper)
            
        return word
    
    
    def generate_list(self, length, mean=7, standard_dev=3, min=5, \
        max=12, upper=True, unique=True):
        """ 
        Returns a list of generated words. Their lengths are a normal
        distribution with the given mean and standard deviation. No words will
        be shorter than min or longer than max. If unique=True, the list will
        contain no duplicates.
        """
        
        words = []
        for i in range(0, length):
            len = int(random.gauss(mean, standard_dev))
            if len < min:
                len = min
            if len >= max:
                len = max-1
                
            if unique:
                word_ok = False
                while not word_ok:
                    word = self.generate_word(length=len, upper=upper)
                    if word not in words:
                        word_ok = True
            else:
                word = self.generate_word(length=len, upper=upper)
            
            words.append(word)
                
        return words
    
    
if __name__ == "__main__":
    
    gen = NameGen(seed=None)
    
    for word in gen.generate_list(1000, mean=5):
        print word

        
        

