#!/usr/bin/env python

import pdb
import random
import copy

import nltk

class MarkovGenerator(object):

    sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_terminator = 'SENTENCE_TERMINATOR'
    dont_prepend_spaces = (',', '.', ';', '?', '!', ':')

    def __init__(self, ngram_size=3):
    
        self.ngram_size = ngram_size
        self.ngram_dict_forward = {}
        self.ngram_dict_backward = {}
    
        
    def add_text(self, text):
    
        for sentence in self.sentence_segmenter.tokenize(text):
        
            for ngram in self._sentence_to_ngrams(sentence):
            
                forward_key = ngram[:-1]
                forward_value = ngram[-1]
                
                if forward_key in self.ngram_dict_forward.iterkeys():
                    self.ngram_dict_forward[forward_key].append(forward_value)
                else:
                    self.ngram_dict_forward[forward_key] = [forward_value]
        
                """
                backward_key = ngram[1:]
                backward_value = ngram[0]
                
                if backward_key in self.ngram_dict_backward.iterkeys():
                    self.ngram_dict_backward[backward_key].append(backward_value)
                else:
                    self.ngram_dict_backward[backward_key] = [backward_value]
                """


    def _sentence_to_ngrams(self, sentence):
        
        words = nltk.word_tokenize(sentence)
        words.append(self.sentence_terminator)
        
        if len(words) < self.ngram_size:
            return
            
        for i in range(len(words) - (self.ngram_size-1)):
            yield tuple(words[i:i+self.ngram_size])


    def _collapse_sentence(self, list_of_words):
    
        sentence = ''
        
        for word in list_of_words:
            if word in self.dont_prepend_spaces:
                sentence += word
            else:
                sentence += ' ' + word
                
        return sentence[1:]
            


    def generate_sentence(self):
    
        # length ngram size - 1
        
        #seed = ['I', 'think']
        seed = ['I', 'think', 'that']
        #seed = ['I', 'think', 'that', 'I']
        
        gen_words = copy.copy(seed)
        current_ngram = copy.copy(seed)
        
        while True:
            
            next_word = random.choice(self.ngram_dict_forward[tuple(current_ngram[1:])])
            
            if next_word == self.sentence_terminator:
                return self._collapse_sentence(gen_words)
            
            gen_words.append(next_word)
            
            current_ngram = current_ngram[1:]
            current_ngram.append(next_word)
            



markov = MarkovGenerator(ngram_size=3)
markov.add_text(open('data/plato-apology.txt').read())

while True:
    print markov.generate_sentence()
    pdb.set_trace()
    
    
    
    


