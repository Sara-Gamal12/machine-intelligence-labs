import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    for i in range(len(string)//2):
        if string[i] != string[len(string)-i-1]:
            return False
    return True