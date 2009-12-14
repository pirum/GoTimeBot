#!/usr/bin/env python

# Copyright (C) 2009 Go-time team
# For license information, see LICENSE.TXT

import pdb
import random
import copy

import nltk

class MarkovGenerator(object):

    SENTENCE_BEGINNER = 'CtK7mc2tpx'
    SENTENCE_TERMINATOR = 'ODTphNBJSp'
    DONT_PREPEND_SPACE = (',', '.', ';', '?', '!', ':')

    sentence_segmenter = nltk.data.load('tokenizers/punkt/english.pickle')

    def __init__(self, ngram_size=3):
    
        self.ngram_size = ngram_size
        
        self.training_ngram_dict_forward = {}
        self.training_ngram_dict_backward = {}
    
        self.topical_ngram_dict_forward = {}
        self.topical_ngram_dict_backward = {}
        
        
    def load_training_text(self, text):
    
        for sentence in self.sentence_segmenter.tokenize(text):
        
            for ngram in self._sentence_to_ngrams(sentence):
            
                forward_key = ngram[:-1]
                forward_value = ngram[-1]
                
                if forward_key in self.training_ngram_dict_forward.iterkeys():
                    self.training_ngram_dict_forward[forward_key].append(forward_value)
                else:
                    self.training_ngram_dict_forward[forward_key] = [forward_value]
        
                backward_key = ngram[1:]
                backward_value = ngram[0]
                
                if backward_key in self.training_ngram_dict_backward.iterkeys():
                    self.training_ngram_dict_backward[backward_key].append(backward_value)
                else:
                    self.training_ngram_dict_backward[backward_key] = [backward_value]

    def load_topical_text(self, text):
        
        for line in text.split('\n'):
        
            for sentence in self.sentence_segmenter.tokenize(line):
            
                for ngram in self._sentence_to_ngrams(sentence):
                
                    # TODO: filter ugly ngrams, like those containing urls
                
                    forward_key = ngram[:-1]
                    forward_value = ngram[-1]
                    
                    if forward_key in self.topical_ngram_dict_forward.iterkeys():
                        self.topical_ngram_dict_forward[forward_key].append(forward_value)
                    else:
                        self.topical_ngram_dict_forward[forward_key] = [forward_value]
                
                
                    backward_key = ngram[1:]
                    backward_value = ngram[0]
                
                    if backward_key in self.topical_ngram_dict_backward.iterkeys():
                        self.topical_ngram_dict_backward[backward_key].append(backward_value)
                    else:
                        self.topical_ngram_dict_backward[backward_key] = [backward_value]
                        
                

    def _sentence_to_ngrams(self, sentence):
        
        #words = nltk.word_tokenize(sentence)
        words = sentence.split()
        
        words.insert(0, self.SENTENCE_BEGINNER)
        words.append(self.SENTENCE_TERMINATOR)
        
        if len(words) < self.ngram_size:
            return
            
        for i in range(len(words) - (self.ngram_size-1)):
            yield tuple(words[i:i+self.ngram_size])


    def _collapse_sentence(self, list_of_words):
    
        sentence = ''
        
        for word in list_of_words:
            if word in self.DONT_PREPEND_SPACE:
                sentence += word
            else:
                sentence += ' ' + word
                
        return sentence.strip()
     

    def generate_sentence(self, seed):
        
        assert len(seed) == self.ngram_size
        
        gen_words = copy.copy(seed)
        current_ngram = copy.copy(seed)
        
        # TODO: with a small probability, attempt to find the next word in the topical text first
        
        # generate in forward direction
        
        while True:
            
            try:
                next_word = random.choice(self.training_ngram_dict_forward[tuple(current_ngram[1:])])
            except KeyError:
                next_word = random.choice(self.topical_ngram_dict_forward[tuple(current_ngram[1:])])
            
            if next_word == self.SENTENCE_TERMINATOR:
                break
            
            gen_words.append(next_word)
            
            current_ngram = current_ngram[1:]
            current_ngram.append(next_word)
            

        # generate in backward direction
        
        current_ngram = gen_words[:self.ngram_size]
        
        while True:
        
            try:
                next_word = random.choice(self.training_ngram_dict_backward[tuple(current_ngram[:-1])])
            except KeyError:
                next_word = random.choice(self.topical_ngram_dict_backward[tuple(current_ngram[:-1])])
            
            if next_word == self.SENTENCE_BEGINNER:
                break
            
            gen_words.insert(0, next_word)
            
            current_ngram = current_ngram[:-1]
            current_ngram.insert(0, next_word)
                
                
        return self._collapse_sentence(gen_words)



markov = MarkovGenerator(ngram_size=3)

markov.load_training_text(open('data/king_james_bible_cleaned_short.txt').read())
markov.load_training_text(open('data/plato-apology.txt').read())
markov.load_topical_text(open('data/irc_text.txt').read())


while True:
    print markov.generate_sentence(['weave', 'the', 'corpora'])
    pdb.set_trace()
    
    
    


