# -*- coding: utf-8 -*-
"""
Avramidis, Braun, Pasic, Schmatz
"""

import random
import string
import re
from nltk.tokenize import word_tokenize, sent_tokenize 
from Utilities import *

class Operation(object):
    '''
    The class :class:`Operation` represents the base class for all operations
    that can be performed. Inherit from :class:`Operation`, overload
    its methods, and instantiate super to create a new operation. 
    '''
    
    def __init__(self,p=0.01,lex=lexicon()):
        '''
        All operations must at least have a :attr:'probability' which is 
        initialised when creating the operations's object.
        
        :param p: Controls the probability that the opertation is performed 
        when it is invoked in the pipeline.
        
        :type p:  Float
        '''
        self.p = p
        self.lex=lex
    
        
    def __str__(self):
        '''
        Used to display a string representation of the operation, which is used 
        by the :func: 'Pipeling.status' to display the currend pipeline's 
        operations in a human readable way.
        
        :return: A string representation of the operation. Can be overridden 
                 if required.
        '''
        return self.__class__.__name__
    
    def perform_operation(self,text):
        '''
        Perform the operation on the passed text. Each operation must at least
        have this function, which accepts a list containing objects, perform 
        its operation, and returns a new list containing objects.
        
        :param text: The text(s) to transform.
        :type text: modified String.
        :return: The transformed text.
        '''
        raise RuntimeError('You cannot call base class.')
        

def nltk_split_text(text, to_words = True):
    '''
    Basic NLTK tokenizer for words and sentences.
        
    :param text: Whole document which is going to be tokenized
    :type text: String
    :return: Returns String in Lists in List that were seperated by 
             individual words and sentences.
    '''
    if to_words == True:
        sep = word_tokenize(text)
    else:
        sep = sent_tokenize(text)
    return sep


def back_to_text(tokens):
    '''
    Untokenizes the modified text
    
    :param tokens: List of tokens 
    :type tokens: List
    :returns: Untokenized modified text as a String
    '''
    befor=['[','{','(']
    after=['.',',',':',';',')',']','}']
    neither_nor=['\'','\"',' ']
    res = "".join(i if tokens[pos+1 if pos<len(tokens)-1 else pos] in after or i in befor else i+' ' for pos,i in enumerate(tokens))
    return res
    

        
class RandomTypo(Operation):
    '''
    The class :class:`RandomTypo` generates a random typo.
    '''
    
    def __init__(self, p=None):
        '''
        As there are no further user definable paramters, the class is
        instantiated using only the :attr:`p` argument.
        
        :param p: Controls the probability that the operation is performed when
                  it is invoked in the pipeline.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        '''
        Inserts random typos with a certain probability.
        
        :param p: This represents the probability a letter gets exchanged by 
                  random letter. The default is 0.01.
        :type p: Float
        :return: Returns String with the modified tokens in altered_text.

        '''
        letters = string.ascii_lowercase
        token_list = nltk_split_text(text, to_words = True)
        final_list = []
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    if letter.isupper():  #optional: with all_chars
                        letter = letters[random.randint(0,len(letters)-1)].upper()
                    else:
                        letter = letters[random.randint(0,len(letters)-1)]         
                word_list.append(letter)
                new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    

class LetterSkip(Operation):
    '''
    The class :class:`LetterSkip` skips random characters with a certain 
    probability.
    '''
    
    def __init__(self, p=None):
        '''
        As there are no further user definable paramters, the class is
        instantiated using only the :attr:`p` argument.
        
        :param p: Controls the probability that the operation is performed when
                  it is invoked in the pipeline.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        """
        Skips random characters with a certain probability.
        
        :param p: Probabilty of exchanging a letter with an empty string 
                 (i.e to skip it). The default is 0.01.
        :make htmltype p: Float
        :return: Returns String with the modified tokens in altered_text.
        """
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = ''
                word_list.append(letter)
                new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
        
    
class LetterFlip(Operation):
    '''
    The class :class:`LetterFlip` flips two neighbouring characters with a 
    certain probability.
    '''
    
    def __init__(self, p=None):
        '''
        As there are no further user definable paramters, the class is
        instantiated using only the :attr:`p` argument.
        
        :param p: Controls the probability that the operation is performed when
                  it is invoked in the pipeline.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        """
        Flips two neighbouring characters with a certain probability.
        
        :param text: Text which is going to be modified.
        :type text: String
        :return: Returns String with the modified tokens in altered_text
        """
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = list(token)
            if len(word_list) > 2:
                if random.uniform(0,1) < self.p:
                    idx = random.randint(1,len(word_list)-1)
                    word_list[idx], word_list[idx-1] = word_list[idx-1], word_list[idx]
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    
    
class SpaceInserter(Operation):
    '''
    The class :class:`SpaceInserter` inserts random spaces in a word with a 
    certain probability.
    '''
    
    def __init__(self, p=None):
        '''
        As there are no further user definable paramters, the class is
        instantiated using only the :attr:`p` argument.
        
        :param p: Controls the probability that the operation is performed when
                  it is invoked in the pipeline.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        """
        Inserts random spaces in a word with a certain probability.  
        
        :param p: Probability of inserting a random space between two letters. 
                  The default is 0.01.
        :type p: Float
        :return: Returns String with the modified tokens in altered_text
        """
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = letter + ' '
                word_list.append(letter)
                string_word = ''.join(word_list)
            final_list.append(string_word)
        altered_text = back_to_text(final_list)
        return altered_text
    

class DoubleLetter(Operation):
    '''
    The class :class:`DoubleLetter` doubles characters with a certain probability.
    '''
    
    def __init__(self, p=None):
        '''
        As there are no further user definable paramters, the class is
        instantiated using only the :attr:`p` argument.
        
        :param p: Controls the probability that the operation is performed when
                  it is invoked in the pipeline.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        '''
        Doubles characters with a certain probability.
        
        :param p: Probabilty that a certain letter occures twice in a row. 
                  The default is 0.01 
        :type p: Float
        :return: Returns String with the modified tokens in altered_text.
        '''
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = 2*letter
                word_list.append(letter)
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text


class Syn_checker(Operation):
    '''
    The class :class:`Syn_checker` checks if synonyms are available. 
    '''
    
    def __init__(self,ant=False, lex=None):
        '''
        Calls lexicon class from Utilities. Replaces word with synonym or 
        antonym.
        
        :param ant: If true antonyms are chosen, if false synonyms are chosen.
        :type ant: Boolean
        :param lex: If None it autocalls lexicon from Utilities.
        :type lex: String or class
        '''
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex
        self.ant=ant
            
    def perform_operation(self,text):
        '''
        Checks if synonyms are available in lexicon.
        
        :param text: String which shall be tokenized and altered.
        :type text: String
        :return: Returns modified String in altered_text
        '''
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            try:
                if list in [type(x) for x in self.lex[token]]:
                    for num,i in enumerate(self.lex[token]):
                        if type(i)==list:
                            if i[self.ant]==[]:
                                final_list.append(token)
                                break
                            per=100
                            pos_per=random.randint(1,per)
                            base=len(i[self.ant])
                            which_one=int(round((base**(1/per))**pos_per,0))-1
                            final_list.append(self.lex[i[self.ant][which_one]][0])
                            break
                else:
                    final_list.append(token)
            except:
                final_list.append(token)
        altered_text = back_to_text(final_list)
        return altered_text


class Stemmenizer(Operation):
    '''
    The class :class:`Stemmenizer` stemmenizes text.
    '''
    
    def __init__(self, lex=None):
        '''
        Calls lexicon from Utilities and looks from stemmed words in the lexica.
        
        :param lex: If None it autocalls lexicon from Utilities.
        :type lex: String or Class
        '''
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex
                
    def perform_operation(self, text):
        '''
        Stemmenizes Text
        
        :param text: String which shall be stemmenized and altered
        :type text: String
        :return: Text with stemmed words in altered_text
        '''
        final_list=[]
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            x=1
            if len(token)<4:
                final_list.append(token)
                continue
            while True:
                pos=int(-1*x)                
                if None==self.lex[token[:pos]]:
                    x+=1
                    if len(token)-1==x:
                        break
                else:
                    final_list.append(self.lex[token[:pos]][0])
                    break
        altered_text = back_to_text(final_list)
        return altered_text  


class Vector(Operation):
    '''
    The class :class:`Vector` transform alphabetic representation of text into
    numerical representation of text.
    '''
    
    def __init__(self, lex=None):
        '''
        Calls lexicon from Utilities to either store or restore numerical representation.
        
        :param lex: If None it autocalls lexicon From Utilities.
        :type lex: String or Class
        '''
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex

    def perform_operation(self, text):
        '''
        Transform alphabetic representation of text into numerical
        numerical representation of text.
        
        :param text: String which shall be vectorized and altered.
        :type text: String
        :return: Text with vectorized words in altered_text.
        '''
        final_list=[]
        token_list = nltk_split_text(text, to_words = True)
        if not hasattr(self, 'vec_pos'):
            self.vec_pos=0
        output=[]
        for word in token_list:
            tf,pos=self.lex.is_it_in_yet(word)
            if tf == True:
               if True==any([True for i in self.lex[pos] if type(i)==int]):
                   pos_return=[i for i in self.lex[pos] if type(i)==int][0]
                   output.append((pos_return,word))
               else:
                   self.lex[pos].append(self.vec_pos)
                   pos_return=self.vec_pos
                   self.vec_pos+=1
                   output.append((pos_return,word))
               
        return str(output)
    

class KeyDistTypo(Operation):
    '''
    The class :class:`KeyDistTypo` Typing errors resulting from the distances 
    of the letters on the keyboard.
    '''
   
    def __init__(self, p=None):
        '''
        The class is instantiated using the :attr:`p` argument and keyboard
        positions are specified.
        
        :param p: Determins probability that is used to apply functions.
        :type p: Float
        '''
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        self.keyboard_positions_lower = {
            '`' : (-1,0),
            '1' : (0, 0),
            '2' : (1, 0),
            '3' : (2, 0),
            '4' : (3, 0),
            '5' : (4, 0),
            '6' : (5, 0),
            '7' : (6, 0),
            '8' : (7, 0),
            '9' : (8, 0),
            '0' : (9, 0),
            '-' : (10,0),
            '=' : (11,0),
          
            'q' : (0, 1),
            'w' : (1, 1),
            'e' : (2, 1),
            'r' : (3, 1),
            't' : (4, 1),
            'y' : (5, 1),
            'u' : (6, 1),
            'i' : (7, 1),
            'o' : (8, 1),
            'p' : (9, 1),
            '[' : (10,1),
            ']' : (11,1),
            '\\': (12,1),
          
            'a' : (0, 2),
            's' : (1, 2),
            'd' : (2, 2),
            'f' : (3, 2),
            'g' : (4, 2),
            'h' : (5, 2),
            'j' : (6, 2),
            'k' : (7, 2),
            'l' : (8, 2),
            ';' : (9, 2),
            "'" : (10,2),
           
           
            'z' : (0, 3),
            'x' : (1, 3),
            'c' : (2, 3),
            'v' : (3, 3),
            'b' : (4, 3),
            'n' : (5, 3),
            'm' : (6, 3),
            ',' : (7, 3),
            '.' : (8, 3),
            '/' : (9, 3),
          
            ' ' : (5, 4)
            }
          
        self.keyboard_positions_upper = {
            '~' : (-1,0),
            '!' : (0, 0),
            '@' : (1, 0),
            '#' : (2, 0),
            '$' : (3, 0),
            '%' : (4, 0),
            '^' : (5, 0),
            '&' : (6, 0),
            '*' : (7, 0),
            '(' : (8, 0),
            ')' : (9, 0),
            '_' : (10,0),
            '+' : (11,0),
           
            'Q' : (0, 1),
            'W' : (1, 1),
            'E' : (2, 1),
            'R' : (3, 1),
            'T' : (4, 1),
            'Y' : (5, 1),
            'U' : (6, 1),
            'I' : (7, 1),
            'O' : (8, 1),
            'P' : (9, 1),
            '{' : (10,1),
            '}' : (11,1),
            '|' : (12,1),
           
            'A' : (0, 2),
            'S' : (1, 2),
            'D' : (2, 2),
            'F' : (3, 2),
            'G' : (4, 2),
            'H' : (5, 2),
            'J' : (6, 2),
            'K' : (7, 2),
            'L' : (8, 2),
            ':' : (9, 2),
            '"' : (10,2),
           
            'Z' : (0, 3),
            'X' : (1, 3),
            'C' : (2, 3),
            'V' : (3, 3),
            'B' : (4, 3),
            'N' : (5, 3),
            'M' : (6, 3),
            '<' : (7, 3),
            '>' : (8, 3),
            '?' : (9, 3),
           
            ' ' : (5, 4)
            }
       
    def calculate_distance(self,x1, y1, x2, y2):
        '''
        Calculates distance between two two-dimensional points.
        
        :param x1: X-Coordinate of point 1.
        :type x1: Integer
        :param y1: Y-Coordinate of point 1.
        :type y1: Integer
        :param x2: X-Coordinate of point 2.
        :type x2: Integer
        :param y2: Y-Coordinate of pont 2.
        :type y2: Y-Coordinate of point 2.
        :return: Returns euclidean distance between two points.
        '''
        xdist = x2-x1
        ydist = y2-y1
        return (xdist**2 + ydist**2)**0.5
   
    def calculating_probs(self,key):
        '''
        Calculates probability between keys.
        
        :param key: Single letter
        :type key: String
        :return: Dictionary of the probabilities.
        '''
        sum_inverse_dists = 0
        inverse_dists = {}
        if key in self.keyboard_positions_lower:
            keyboard_positions = self.keyboard_positions_lower
        else:
            keyboard_positions = self.keyboard_positions_upper
        posx, posy = keyboard_positions[key]
        for letter in keyboard_positions: 
            if letter != key:
                posx1, posy1 = keyboard_positions[letter]
                dist = self.calculate_distance(posx, posy, posx1, posy1)
                inverse_dist = 1/(dist**6)
                inverse_dists[letter] = inverse_dist
                sum_inverse_dists += inverse_dist
        probs = {}
        for key, value in inverse_dists.items():
            probs[key] = value/sum_inverse_dists
        return probs
   
    def pick_random_letter(self,prob_dist):
        '''
        Picks a random letter according to the calculated probabilties by 
        calculated_probs.
        
        :param prob_dist: Dictionary in which the probabilities for each key
                          are.
        :type prob_dist: Dictionary
        :return: Picked letter from the dictionary.
        '''
        letters = []
        probs = []
        for key, value in prob_dist.items():
            letters.append(key)
            probs.append(value)
        picked_letter = random.choices(letters, probs)
        return picked_letter[0]
       
    def perform_operation(self, text):
        '''
        Typing errors resulting from the distances 
        of the letters on the keyboard.
        
        :param text: Text which is going to be modified.
        :type text: String
        :return: modified Text.
        '''
        key_list=list(self.keyboard_positions_lower.keys())+list(self.keyboard_positions_upper.keys())
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if letter not in key_list:
                    continue
                if random.uniform(0,1) < self.p:
                    neighbour_probs = self.calculating_probs(letter)
                    letter = self.pick_random_letter(neighbour_probs)
                word_list.append(letter)
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    
# debug the back to text function (brackets)
# Check if the letter is in the "correct" signs (no @ for example)
# clear_pipe    
    



    