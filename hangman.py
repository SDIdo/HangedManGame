#############################################################
# FILE: hangman.py
# WRITER: Ido Natan
# EXERCISE: EX4 intro2cs2
# DESCRIPTION: a program that runs the game hangman
##############################################################

import hangman_helper as hh
LETTER = hh.LETTER
HINT = hh.HINT
PLAY_AGAIN = hh.PLAY_AGAIN

NUMBER_OF_LETTERS = 26

CHAR_A = 97
#user_input = hh.get_input()  # a tuple containing the user input
#input_choice = user_input[0] # a string containing the user choice type
#letter = user_input[1]  # 

def letter_to_index(letter):
    """     
    :param letter: a string char from the alphabet
    Return the index of the given letter in an alphabet list.
    """
    return ord(letter.lower()) - CHAR_A

def index_to_letter(index):
    """     
    :param index: a numerical value indicating a place
    Return the letter corresponding to the given index.
    """
    return chr(index + CHAR_A) 

def update_word_pattern(word, pattern, letter):
    """
    :param word: the randomized chosen word from the text file.
    :param pattern: the visualy hidden state of the word to be guessed.
    :param letter: the letter input by the user.
    :return: an updated state of the pattern in relevance to the letter
    """
    for i in range(len(word)):
        if word[i] == letter:
            pattern = pattern[:i] + letter + pattern[i+1:]  # if the letter 
            # is present in the word, 
            # pattern changes to show it in it's place.
    return pattern

def filter_words_list(words,pattern,wrong_guess_lst):
    """
    :param words: all the words from the text file
    :param pattern: the visualy hidden state of the word to be guessed.
    :param wrong_guess_lst: list containing all the wrong guesses.
    :return: a list of filtered words, according to the requests.
    """
    filtered_list = []
    for word_from_words in words:
        is_word_ok = True  # a filter checkpoint flag
        if len(pattern) == len(word_from_words):  # filters words of unequal
        # to the hidden word, lenght.
            for j in range(len(pattern)):
                if word_from_words[j] in wrong_guess_lst:  # filters any word
                # which has letters that have proven wrong.
                    is_word_ok = False
                if pattern[j] != "_" and pattern[j] != word_from_words[j]:
                    #filters any word that has anything but rightly guessed 
                    # letters of the hidden word, and in their matching places 
                    is_word_ok = False
            if is_word_ok:
                filtered_list.append(word_from_words)  # creates the list
    return filtered_list
def choose_letter(words, pattern):
    """
    :param words: list of words after being filtered
    :param pattern: the visualy hidden state of the word to be guessed.
    :return: the most common letter within the words,
    will ignore letters which are already revealed in
    the pattern
    """
    letter_counter_list = [0] * NUMBER_OF_LETTERS  # a list of counters for 
    # each letter
    letter_matrix = ''.join(words)  # combines all the letters of the words
    # into one long string containing all letters side by side
    for letter in letter_matrix:
        if letter not in pattern:
            letter_counter_list[letter_to_index(letter)] += 1  # every letter
            #  gets it's own index via letter_to_index function.
            # It's value is the number of occurences in letter_matrix.
    mx_val = max(letter_counter_list)  # recieves the value of the most
    # occuring letter
    common_letter = index_to_letter(letter_counter_list.index(mx_val))
    # recieves the list index of the highest occuring letter
    # then turns it into the corresponding letter via index to letter function
    return common_letter                                      


def run_single_game(words_list):
    """
    :param words_list: all the words from the text.
    :return: one round of the game hangman.
    """
    error_count = 0  # Game_initializations
    wrong_guess_lst = []
    all_guesses_lst = []
    word = hh.get_random_word(words_list)  # brings a randomized word
    # from the list word_list
    pattern = '_'*len(word)  # # a mask for the word - 
    # underscores quantitized by the lenght of the word.
    
    msg = hh.DEFAULT_MSG  # msg assigning - a mandatory for each stage
    while error_count < hh.MAX_ERRORS and pattern != word:  
        # no six guesses yet, and hasn't guesses the hidden word
        # - game continues. 
        hh.display_state(pattern,error_count,wrong_guess_lst,msg,
                                     ask_play = False)  # a mandatory 
        # for the game at this stage
        user_input = hh.get_input()
        input_choice = user_input[0]
        letter = user_input[1]
        if input_choice == HINT:  # user asks for a hint
            f_w_l = filter_words_list(words_list, pattern, wrong_guess_lst)
            hint_letter = choose_letter(f_w_l, pattern)  # initiates the
            # function that finds the most common letter from the list
            msg = hh.HINT_MSG + hint_letter
            print(hint_letter)
        elif input_choice == LETTER:  # user guesses a letter
            print(letter)
            if len(letter) != 1 or not letter.isalpha():  
                # if letter is not within the alphabet
                # or is, but isn't one letter - then is invalid
                msg = hh.NON_VALID_MSG
            elif letter in all_guesses_lst:
                msg = hh.ALREADY_CHOSEN_MSG + letter
            elif letter in word and word not in all_guesses_lst:
                pattern = update_word_pattern(word, pattern, letter)
                all_guesses_lst.append(letter)
                msg = hh.DEFAULT_MSG
            else:
                wrong_guess_lst.append(letter)
                all_guesses_lst.append(letter)
                msg = hh.DEFAULT_MSG
                error_count += 1  # also changes the hangman pictures
    if error_count == hh.MAX_ERRORS:  # user fails to guess within the guess
    # limit of six guesses
        msg = hh.LOSS_MSG + word  # the lose message
        hh.display_state(pattern,error_count,wrong_guess_lst,msg,
                                 ask_play=True)  # the ending screen initiator
    else:
        msg = hh.WIN_MSG  # the win message
    hh.display_state(pattern,error_count,wrong_guess_lst,msg,
                                 ask_play=True)  # the ending screen initiator
def main():
    """
    function takes no parameters
    :return: a menu for the game 
    """
    words = hh.load_words()  # words assigning
    run_single_game(words)  # starts one round of the game
    user_input = hh.get_input()  # collecting user input
    while user_input[0] == PLAY_AGAIN:  # final screen decision to play again
    # or not.
            if user_input[1]:  #  for a positive answer
                run_single_game(words)  # starts over the game
                user_input = hh.get_input()
            else:  # for a negative answer
                break  # exits the game

if __name__ == "__main__":    # connects our code to the external
# module\plugin, thus runs the operations responsible for the game. 
    hh.start_gui_and_call_main(main)
    hh.close_gui()



    
                    
                
                
        
