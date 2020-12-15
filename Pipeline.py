# -*- coding: utf-8 -*-
"""

@author: Avramidis, Braun, Pasic, Schmatz
"""


from sys import stdout
from Operations import *
#from Utilities import *

def output(text,blanks=30):
    '''
    Helper Function to segment text by blanks.
    
    :param text: String with more than 30 words.
    :type text: String
    :return: String reduced to max. of 30 words
    '''
    output=''
    x=0
    blank=0
    while True:
        if text[x]==' ':
            blank+=1
        if blank==blanks or len(text)-2<x:
            break
        else:
            output+=text[x]
            x+=1
    return output

class Pipes():
    '''
    The class :class: Pipes provides the interface for the user to interact
    with different objects in module Operations
    '''
    
    def __init__(self,files=None):
        '''
        Create a new Pipeline object pointing to the directory.
        '''
        self.text=self.get_text(files=files)
        self.pipeline=self.clear()
        #self.lex=lexicon()
    
    
    def get_text(self,rand=True,files=None):
        '''
        :param rand: If true ,loads a random file from directory. IF false
                     loads first time from directory.
        :type rand: Boolean
        :param files: String pointing to the directory where the files are.
        :type files: If None subroutine is called that ask user to provide 
                     directory. Else String
        :returns: String from files provided in location files
        '''
        try:
            if not hasattr(self, 'text'):
                return self.file_obj.import_text(rand)
            else:
                self.text=self.file_obj.import_text(rand)
        except:
            self.file_obj=load_files(files)
            if not hasattr(self, 'text'):
                return self.file_obj.import_text(rand)
            else:
                self.text=self.file_obj.import_text(rand)
    
    def clear(self):
        '''
        Clears pipeline
        
        :return: Empty List
        '''
        if not hasattr(self, 'pipeline'):
            return []
        else:
            self.pipeline=[]
       
    
    
    def run(self):
        '''
        Executes all functions within the pipeline list
        '''
        text=self.text
        stdout.write(output(text)+'\n\n')
        #self.pipeline=[for op in self.pipeline]
        for x,operation in enumerate(self.pipeline):
            stdout.write(str(x)+': '+str(operation)+'\n')
            # if callable(operation)==True:
            #     print('x')
            text=operation.perform_operation(text)
            stdout.write(output(text)+'\n\n')
            text=self.text
            
    
    def random_operations(self):
        '''
        Adds an random entry from the Operation class to the pipeline list.

        :yields: random function within the Operation class

        '''
        try:
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)]())
        except:
            self.ops=[cls for cls in Operation.__subclasses__()]
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)]())
    
    
    def random_typo(self,p=0):
        '''
        Adds an random entry from the Operation class to the pipeline list

        :yields: random function within the Operation class

        '''
        if not 0 < p <= 1: 
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(RandomTypo(p))
            
    def syn_ant(self,ant=False):
        '''
        Returns a synonym or antonym for each word in the corpus if available.
        
        :param ant: Specifies if synonym or antonym.
        :type ant: Boolean
        :return: modified String representing synonym or antonym of word.
        '''
        self.pipeline.append(Syn_checker(ant))
         
    def stem(self):
        '''
        Adds stemmenizer Function from "Operations" into self.pipeline.
        '''
        self.pipeline.append(Stemmenizer())
    
    def vectorize(self):
        '''
        Adds vectorize Function from "Operations" into self.pipeline.
        '''
        self.pipeline.append(Vector())
        
    def keydist_typo(self,p=0):
        '''
        Typing errors resulting from the distances of the letters on the 
        keyboard. Adds KeyDistTypo Function from "Operations" into 
        self.pipeline.
        
        :param p: Probability of inserting typo
        :type p: Float
        '''
        if not 0 < p <= 1: 
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(KeyDistTypo(p))

    def letter_flip(self,p=0):
        '''
        Adds Letterflip Function to self.pipeline
        
        :param p: Probability of inserting a letter-flip
        :type p: Float
        '''
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(LetterFlip(p))


    def letter_skip(self,p=0):
        '''
        Adds LetterSkip Function to self.pipeline
        
        :param p: Probability of inserting a letter-skip.
        :type p: Float
        '''
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(LetterSkip(p))


    def double_letter(self,p=0):
        '''
        Adds DoubleLetter Function to self.pipeline
        
        :param p: Probability of inserting a double letter.
        :type p: Float
        '''
        
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(DoubleLetter(p))


    def space_inserter(self,p=0):
        '''
        Adds SpaceInserter Function to self.pipeline.
        
        :param p: Probability of inserting a space inserter.
        :type p: Float
        '''
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(SpaceInserter(p))
    
    def _auto(self):
        '''
        Performs all operations randomly until interrupted
        '''
        while True:
            self.get_text()
            for i in range(0,random.randint(1,5)):
                self.random_operations()
            self.run()
            self.clear()
