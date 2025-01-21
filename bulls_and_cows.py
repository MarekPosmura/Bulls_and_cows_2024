# projekt_2.py: druhý projekt do Engeto Online Python Akademie

# author: Marek Pošmura
# email: m.posmura@seznam.cz

from random import sample, choice, seed
import time
import os
import csv
import rules


# seed(2) ########## ODSTRANIT SEED ##########


difficulty = 4
line = 79 * "-"
login = ""
scoreboard_name = f"scoreboard_{difficulty}.csv"

secret_num = ""


red = "\033[31m"
green = "\033[32m"
reset = "\033[0m"



def get_user_name():
  global login
  login = input("Type your name: ")
  # show_10_char(login)


def enter_to_continue():
    input("Press Enter to continue...")

def give_up():
  print(f"The number you were looking for was {secret_num}. Better luck next time.")
  enter_to_continue()

def exit_game():
  print("Game is over. See you nextime.")
  quit()

# def max_length_of_login(name):
#    if len(name) > 10:
#        print(f"{red}Your name is too long, max 10 characters. Try again.{reset}")
#        return False
#    else:
#       return True

def show_10_char(name):
    if len(name) > 10:
      name_max_10 = f"{name[:10]}..."
      return name_max_10
    else:
      return name

def show_menu():
  main_menu = [
  "1. Start game",
  "2. Rules of the Game",
  f"3. Change difficulty: {difficulty} digits",
  f"4. Change player: {show_10_char(login)}", 
  "5. Scoreboard",
  "6. Exit game"
  ]
  print(f"Hello {show_10_char(login)}!", line, "Let's play Bulls and Cows!", line, sep="\n")
  print ("\n".join(main_menu), line, sep="\n")

def show_rules_of_game():
  print(rules.bulls_and_cows)
  enter_to_continue()

def choose_from_main_menu():
  while True:
    clear_terminal()
    show_menu()
    menu = input("Select an option from the menu: ")
    clear_terminal()
    if menu not in map(str, range(1, 7)):
      print(f"{red}You didn't choose a number from the menu, try again.{reset}")
      enter_to_continue()
      continue
    elif menu == "1":
      start_game()
    elif menu == "2":
      show_rules_of_game()
    elif menu == "3":
      show_difficulty_menu()
      set_difficulty()
    elif menu == "4":
      get_user_name()
    elif menu == "5":
      show_scoreboard_menu()
    elif menu == "6":
      exit_game()


def start_game():
  global secret_num
  secret_num = generate_random_number(difficulty)
  play_game()

def show_difficulty_menu():
  difficulty_menu = [
  "3 digits - Easy difficulty",
  "4 digits - Normal difficulty:",
  "5 digits - Hard difficulty",
  "6 digits - Nightmare difficulty"
  ]
  print(f"Choose your difficulty level:")
  print("\n".join(difficulty_menu))
  print()

def set_difficulty():
  global scoreboard_name
  while True:
    try:
      num_input = int(input("Set the length of the code between 3 and 6: "))
      if num_input in range(3, 7):
        global difficulty
        difficulty = int(num_input)
        scoreboard_name = f"scoreboard_{difficulty}.csv"
        break
      else:
        print(f"{red}You didn't enter a length of code between 3 and 6. Please try again.{reset}")
        continue
    except ValueError:
        print(f"{red}Invalid input. Please enter a number between 3 and 6:{reset}")

  return difficulty

def show_scoreboard_menu():
  scoreboard_menu = [
  "3 digits - Easy difficulty",
  "4 digits - Normal difficulty",
  "5 digits - Hard difficulty",
  "6 digits - Nightmare difficulty"
  ]
  print(f"Scoreboard:")
  for index, item in enumerate(scoreboard_menu, start=3):
    print(f"{index}. {item}")

  while True:
    try:
      chosen_scoreboard = int(input("Select the difficulty level to display the results table:"))
      if chosen_scoreboard in range (1, 7):
        clear_terminal()
        print(f"You selected {scoreboard_menu[chosen_scoreboard-1]} from the menu.")
        sorted_results = load_and_sort_results(f"scoreboard_{chosen_scoreboard}.csv")
        display_results(sorted_results)
        break
      else:
        print(f"{red}You didn't chose number in the menu, try again.{reset}")
        continue
    except ValueError:
        print(f"{red}Invalid input. Please enter a number between 3 and 6:{reset}")




# Funkce pro uložení výsledku do CSV souboru
def save_result(filename, name, attempts, time):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, attempts, time])

# Funkce pro načtení a seřazení tabulky
def load_and_sort_results(filename):
    results = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                name, attempts, time = row
                results.append([name, int(attempts), float(time)])
    except FileNotFoundError:
        print(f"{red}There are no results saved in this table yet.{reset}")
        
    return sorted(results, key=lambda x: x[2])  # Seřadí podle času (třetí sloupec)


# Funkce pro zobrazení výsledků jako tabulky
def display_results(results):
    print(f"{'Rank':<5}{'Name':<15}{'Attempts':<10}{'Time':<10}")
    print("-" * 40)
    for rank, (name, attempts, time) in enumerate(results, start=1):
        print(f"{rank:<5}{name:<15}{attempts:<10}{time:<10.2f}")
    enter_to_continue()

# Funkce pro generování náhodného čísla
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
  running_game = True
  start_time = time.perf_counter()
  print(f"I've generated random {difficulty}-digit number for you.",
        "All digits are unique and the number can't start with zero.",
        "Can you crack the secret code?",
        "If you want to give up, type 'Q'.", line, sep="\n")
  while running_game:
    guess_num = input(f"Enter a {difficulty}-digit number: ")
    attempts += 1
    print(f">>> {guess_num}")
    print(f"{red}{secret_num} SMAZAT{reset}") # pro testování

    # UKONČENÍ PROGRAMU
    if guess_num.lower().strip() == "q":
      give_up()
      running_game = False

    # SPRÁVNĚ ZADÁNO HESLO
    elif guess_num == secret_num:
      end_time = time.perf_counter()
      elapsed_time = end_time - start_time
      save_result(scoreboard_name, show_10_char(login), attempts, elapsed_time)
      print(f"{green}Well done! You found the correct number\nin {attempts} attempts and {elapsed_time:.2f} seconds!{reset}")
      enter_to_continue()
      running_game = False

    # Kontrola platnosti vstupu
    else:
      error_message = validate_guess(guess_num)
      if error_message:
          print(f"{red}{error_message}{reset}", line, sep="\n")
          continue
      
      # Pokud je vstup platný, pokračujeme s hodnocením
      show_progres(guess_num)
      print(line)

def validate_guess(guess):
    if not guess.isnumeric():
        return "The number can contain only numeric characters."
    if guess.startswith("0"):
        return "The number can't start with zero."
    if len(guess) != difficulty:
        return "You have entered the wrong number of digits."
    if not check_unique_characters(guess):
        return "The number can't contain duplicate digits."
    return None

def get_plural_bull(number):
  result = "bull" if number == 1 else "bulls"
  return result

def get_plural_cow(number):
  result = "cow" if number == 1 else "cows"
  return result

def check_unique_characters(string):
    return len(string) == len(set(string))

def show_progres(sec_num):
  cows = 0
  bulls = 0
  for index, number in enumerate(sec_num):
    if number == secret_num[index]:
      bulls += 1
    elif number in secret_num:
      cows += 1
  return print(f"{bulls} {get_plural_bull(bulls,)}, {cows} {get_plural_cow(cows)}")

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def game():
  get_user_name()
  choose_from_main_menu()



if __name__ == "__main__":
  game()


