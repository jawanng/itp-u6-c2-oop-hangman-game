from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if (hit != None and hit == miss) or (hit == None and miss == None):
          raise InvalidGuessAttempt()

        self.hit = hit
        self.miss = miss

    def is_hit(self):
        if self.hit == True or self.miss == False:
            return True
        else:
            return False

    def is_miss(self):
        return not self.is_hit()


class GuessWord(object):
    def __init__(self, word):
        if word == '':
            raise InvalidWordException()

        self.answer = word.lower()
        self.masked = '*' * len(word)

    def perform_attempt(self, letter):
        if len(letter) != 1:
            raise InvalidGuessedLetterException()

        letter = letter.lower()
        if letter in self.answer:
            change = self.answer.find(letter)

            while change != -1:
                self.answer = self.answer.replace(letter, '*', 1)
                self.masked = self.masked[:change] + letter + self.masked[change+1:]
                change = self.answer.find(letter)

            obj = GuessAttempt(letter, hit=True)
        else:
            obj = GuessAttempt(letter, miss=True)

        return obj


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    @classmethod
    def select_random_word(cls, list_of_words):
        if list_of_words == None or list_of_words == []:
          raise InvalidListOfWordsException()
        return random.choice(list_of_words)

    def __init__(self, word_list=None, number_of_guesses=5):
        if word_list == None:
            self.word_list = HangmanGame.WORD_LIST
        else:
            self.word_list = word_list

        self.remaining_misses = number_of_guesses
        rand_word = HangmanGame.select_random_word(self.word_list)
        self.word = GuessWord(rand_word)
        self.previous_guesses = []

    def guess(self, letter):
        if self.is_finished():
          raise GameFinishedException()

        letter = letter.lower()
        holder = self.word.perform_attempt(letter)
        self.previous_guesses.append(letter)
        if holder.is_miss():
          self.remaining_misses -= 1
          if self.remaining_misses <= 0:
              raise GameLostException()
        elif '*' not in self.word.masked:
            raise GameWonException()

        return holder

    def is_finished(self):
        return self.is_lost() or self.is_won()

    def is_lost(self):
        if self.remaining_misses <= 0:
            return True
        else:
            return False

    def is_won(self):
        if '*' not in self.word.masked:
            return True
        else:
            return False
