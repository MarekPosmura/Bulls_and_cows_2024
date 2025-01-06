# projekt_2.py: druhý projekt do Engeto Online Python Akademie

# author: Marek Pošmura
# email: m.posmura@seznam.cz

from random import sample, choice, seed
from os import system
import time
import os
import platform
import pandas as pd # pro ukládání výsledků do scoreboardu

# system("cls") - vymazání teminálu

seed(2) ########## ODSTRANIT SEED ##########
difficulty = 4
line = 79 * "-"
login = ""

secret_num = ""

red = "\033[31m"
green = "\033[32m"
reset = "\033[0m"

def welcome_screen():
  global login
  login = input("Type your name: ")
  return login


def show_menu():
  main_menu = [
  "1. Start game",
  "2. Rules of the Game",
  "3. Change difficulty",
  "4. Change player",
  "5. Scoreboard",
  "6. Exit game"
  ]
  print(f"Hello {login}!", line, "Let's play Bulls and Cows!", line, sep="\n")
  print ("\n".join(main_menu), line, sep="\n")

def chose_from_main_menu():
  while True:
    clear_terminal()
    show_menu()
    menu = input("Choose number from main menu: ")
    clear_terminal()
    if menu not in ("1", "2",  "3", "4", "5", "6"):
      print(f"{red}You didn't chose number in the menu, try again.{reset}")
      continue
    elif menu == "1":
      start_game()
    elif menu == "2":
      show_rules_of_game()
    elif menu == "3":
      show_difficulty_menu()
      set_difficulty()
    elif menu == "4":
      global login
      login = input("Type your name: ")
    elif menu == "5":
      show_scoreboard_menu()


    elif menu == "6":
      # clear_terminal()
      print("Game is over. See you nextime.")
      quit()

def enter_to_continue():
    input("Press Enter for continue...")


def start_game():
  global secret_num
  secret_num = generate_random_number(difficulty)
  play_game()

def show_rules_of_game():
  rules = """
  RULES OF THE GAME:
  The goal of the game is to guess a secret code (usually a 4-digit number).

  The code consists of digits (0–9) with no repeated numbers, and the secret
  code cannot start with zero.

  After your guess, the game will provide you with feedback:

    - Number of Bulls: Correct digit in the correct position.
    - Number of Cows: Correct digit in the wrong position.

  If you correctly guess the entire secret code (all Bulls), you win the game!

  The game can also be played with codes of different lengths.
  You can set difficulty in the main menu.

  Enjoy the challenge and beat the high score!
  """
  print(rules)
  enter_to_continue()

def show_difficulty_menu():
  difficulty_menu = [
  "3 digits - Easy difficulty",
  "4 digits - Normal difficulty",
  "5 digits - Hard difficulty",
  "6 digits - Nightmare difficulty"
  ]
  print(f"Choose your difficulty level:")
  print("\n".join(difficulty_menu))


def set_difficulty():
  while True:
    try:
      num_input = int(input("Set the length of the code between 3 and 6: "))
      if num_input in range (3, 7):
        global difficulty
        difficulty = int(num_input)
        break
      else:
        print(f"{red}You didn't enter a length of code between 3 and 6. Please try again.{reset}")
        continue
    except ValueError:
        print(f"{red}Invalid input. Please enter a number between 3 and 6:{reset}")

  return difficulty

def show_scoreboard_menu():
  scoreboard_menu = [
  "Easy difficulty",
  "Normal difficulty",
  "Hard difficulty",
  "Nightmare difficulty"
  ]
  print(f"Scoreboard:")
  for index, item in enumerate(scoreboard_menu, start=1):
    print(f"{index}. {item}")

  while True:
    try:
      chosen_scoreboard = int(input("Select the difficulty level to display the results table:"))
      if chosen_scoreboard in range (1, 5):
        print(f"You selected {scoreboard_menu[chosen_scoreboard-1]} from the menu.")
        enter_to_continue()
        break
      else:
        print(f"{red}You didn't chose number in the menu, try again.{reset}")
        continue
    except ValueError:
        print(f"{red}Invalid input. Please enter a number between 1 and 4:{reset}")






  #   else:
  #       print(f"Chosen scoreboard{red}You didn't enter a length of code between 1 and 4. Please try again.{reset}")
  #       continue
  #   except ValueError:
  #       print(f"{red}Invalid input. Please enter a number between 1 and 4:{reset}")

  # return difficulty


def generate_random_number(number_of_digits):
  range_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  first_digit = choice(range(1, 10))
  rest_of_numbers = number_of_digits - 1
  range_list.remove(first_digit)
  other_digits = sample(range_list, rest_of_numbers)
  return "".join(map(str, ([first_digit] + other_digits)))

# secret_num = "".join(generate_random_number(difficulty))


def play_game():
  attempts = 0
  runnig_game = True
  start_time = time.perf_counter()
  print(f"I've generated random {difficulty}-digit number for you.",
        "All digits are unique and the number can't start with zero.",
        "Can you crack the secret code?",
        "If you want to give up, type 'Q'.", line, sep="\n")
  while runnig_game:
    guess_num = input(f"Enter a {difficulty}-digit number: ")
    attempts += 1
    print(f">>> {guess_num}")

    # SPRÁVNĚ ZADÁNO HESLO
    if guess_num == secret_num:
      end_time = time.perf_counter()
      elapsed_time = end_time - start_time
      print(f"{green}Correct, you've guessed the right number\nin {attempts} guesses and {elapsed_time:.2f} seconds!{reset}")
      # vlož funkci na uložení výsledku to scoreboard
      enter_to_continue()
      runnig_game = False

    # UKONČENÍ PROGRAMU
    elif guess_num.lower().strip() == "q":
      print(f"The number you were looking for was {secret_num}. Better luck next time.")
      enter_to_continue()
      runnig_game = False

    # ZKONTROLUJE NUMERICKE ZNAKY
    elif not guess_num.isnumeric():
      print(f"{red}The number can contain only numeric characters, plese try again.{reset}", line, sep="\n")

    # ZAČÍNÁ NULOU
    elif guess_num.startswith("0"):
      print(f"{red}The guessed number can't start with zero, please try again.{reset}", line, sep="\n")

    # ZADÁN ŠPATNÝ POČET ČÍSLIC
    elif len(guess_num) != difficulty:
      print(f"{red}You have entered the wrong number of digits, please try again.{reset}", line, sep="\n")

    # VE VÝSTUPU JSOU DVĚ NEBO VÍCE STEJNÝCH ČÍSEL
    elif not check_unique_characters(guess_num):
      print(f"{red}The number can't contain duplicate digits, please try again.{reset}", line, sep="\n")

    elif runnig_game:
        show_progres(guess_num)
        print(line)


def plural_bull(number):
  result = "bull" if number == 1 else "bulls"
  return result

def plural_cow(number):
  result = "cow" if number == 1 else "cows"
  return result

def check_unique_characters(string):
    return len(set(string)) == len(string) # počet znaků v množině musí odpovídat počtu znaků v zadaném stringu (v množině nejsou duplicity)

def show_progres(sec_num):
  print(f"Smazat:{secret_num}"
  )
  cows = 0
  bulls = 0
  for index, number in enumerate(sec_num):
    if number == secret_num[index]:
      bulls += 1
    elif number in secret_num:
      cows += 1
  return print(f"{bulls} {plural_bull(bulls)}, {cows} {plural_cow(cows)}")

def clear_terminal():
    # Zjistí operační systém
    system = platform.system()

    # Použije správný příkaz pro vymazání
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def game():
  welcome_screen()
  chose_from_main_menu()
# přesměorvání do menu po nějaké době


if __name__ == "__main__":
  game()


