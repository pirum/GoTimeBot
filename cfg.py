import random
import sys

class ContextFreeGrammar:
    
    def __init__(self, grammar, seed=None):
        self._grammar = grammar
        random.seed(seed)
            

    def generate(self, phrase='S', probabilistic=True):
        """
        generate a phrase from the grammar, joining elements together with a
        separator
        """
        self.probabilistic = probabilistic
        #return separator.join(self._generate_recursive(phrase))
        
        def tostring(item):
            if callable(item):
                return item()
            else:
                return str(item)
        
        return ''.join([tostring(e) for e in self._generate_recursive(phrase)])
    



    def _generate_recursive(self, phrase):
        """recursively resolve the given phrase"""
    
        if isinstance(phrase, list): 
            # call _generate_recursive on each item in the list
            phrase = map(self._generate_recursive, phrase)
            
            # reduce to unnest list
            # e.g.  [['0'], ['0']]  =>  ['0', '0']
            return reduce(lambda x,y: x+y, phrase)
        
        elif phrase in self._grammar:
            # choose and generate one of the elements in this phrase
            return self._generate_recursive(self._choose_phrase(phrase))
        
        else:
            # atom, just return 
            return [phrase]
            
            
    def _choose_phrase(self, phrase):
        
        choices = self._grammar[phrase]
        
        if len(choices) == 0:
            raise ValueError("Each element of the grammer must have at least \
                one choice.")
        
        if self.probabilistic: 
            choice = self._weighted_choice(choices)
        else:
            choice = random.choice(choices)
        
        # strip the choice's weight, if any
        if isinstance(choice, tuple):
            choice = choice[0]
            
        return choice
        
        
    def _weighted_choice(self, lst):
        """
        Each item in the list can be
            * A tuple of (choice, weight)
            * Just a choice. It is assumed to have weight 1
        
        e.g. weighted_choice([('one', 10), 'two', ('three', 0.1)])
        will usually return 'one'
        """
    
        def get_weight(item):
            if isinstance(item, tuple):
                return item[1]
            return 1

        total_weight = reduce(lambda x,y:x+y, [get_weight(tup) for tup in lst])
        n = random.uniform(0, total_weight)
    
        try:
            for item in lst:
                weight = get_weight(item)
                if n < weight:
                    break
                n = n - weight
            return item
        except ValueError:
            print lst
        


if __name__ == '__main__':

    from namegen import NameGen
    planet_name_gen = NameGen()

    insults = {
    
        'S' : [
            (['Your ', '#relative', ' was a ', '#thing', ' and your ',
            '#relative', ' smelt of ', '#smelly_thing', '.'],
            1.1),
                
            ["You're so ", '#insulting_adj', ' you ', '#dumb_action', '.'],
            
            ["I wouldn't expect any better from someone coming from ",
            '#location', '.'],
                
            ["You're so ", '#insulting_adj', ' you use ', '#insulting_adj',
            ' insults like "', 'S', '"'],
        ],
        
        '#relative' : [
            ('mother', 5), 
            'father', 
            'sister', 
            'brother',
        ],
        
        '#thing' : [
            ('hampster', 5), 
            'Java programmer',
        ],
        
        '#smelly_thing' : [
            ('eldeberries', 3), 
            'garbage',
            'trash',
        ],
        
        '#insulting_adj' : [
            'stupid',
            'dumb',
            'retarded',
            'absent minded',
            'clueless',
        ],
        
        '#dumb_action' : [
            'modified an array while iterating over it',
            'sorted a list using bubble sort',
            'tripped over your own foot',
        ],
        
        '#location' : [
            planet_name_gen.generate_word,
            ['#region_prefix', ' ', planet_name_gen.generate_word],
            'where you come from',
        ],
        
        '#region_prefix' : [
            'North',
            'South',
            'East',
            'West',
            'upper',
            'lower',
        ],
        
        
    }
    
    cfg = ContextFreeGrammar(insults)
    
    for i in range(0, 100):
        print cfg.generate()




