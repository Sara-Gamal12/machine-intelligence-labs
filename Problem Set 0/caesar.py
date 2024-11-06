from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    dictionary=set(dictionary)
    min_words:int=-1
    min_shift:int=0
    DechiperResult:str=""
    for i in range(26):
        count_invalid:int=0
        decipherd:list=[]
        for word in ciphered.split() :
            new_word=""
            for char in word:
              new_word += chr((ord(char)-ord('a') - i) % 26 + ord('a'))
            decipherd.append(new_word)
        
            if new_word not in dictionary:
                count_invalid+=1
        if min_words==-1 or count_invalid<min_words:
            min_words=count_invalid
            DechiperResult=" ".join(decipherd)
            min_shift=i
    return (DechiperResult,min_shift,min_words)