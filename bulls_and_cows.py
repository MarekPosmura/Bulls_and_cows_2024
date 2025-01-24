# EDIT: 24.1.2025
# projekt_2.py: druhý projekt do Engeto Online Python Akademie

# author: Marek Pošmura
# email: m.posmura@seznam.cz

from random import sample, choice, seed
import time
import os
import csv

# DEFAULT VARIABLES
login = ""
difficulty = 4
secret_num = ""
scoreboard_name = f"scoreboard_{difficulty}.csv"

# TEXT FORMATTING
line = 79 * "-"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
reset = "\033[0m"

# START THE GAME
def game():
  """
  Starts the game by getting the user's name and displaying the main menu.
  """
  get_user_name()
  choose_from_main_menu()

# DISPLAY MAIN MENU
def show_menu():
  """
  Displays the main menu options to the user.
  """
  main_menu = [
  "1. Start game",
  "2. Rules of the Game",
  f"3. Change difficulty: {yellow}{difficulty} digits{reset}",
  f"4. Change player: {yellow}{show_10_char(login)}{reset}",
  "5. Scoreboard",
  "6. Exit game"
  ]
  print(f"Hello {show_10_char(login)}!", line, "Let's play Bulls and Cows!", line, sep="\n")
  print ("\n".join(main_menu), line, sep="\n")

# MAIN MENU SELECTION
def choose_from_main_menu():
  """
  User selection from the main menu.
  """
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
      set_difficulty()
    elif menu == "4":
      get_user_name()
    elif menu == "5":
      show_scoreboard_menu()
    elif menu == "6":
      exit_game()

# 1. MAIN MENU OPTION - START GAME
def start_game():
  """
  Initiates the game by generating a secret number and starting gameplay.
  """
  global secret_num
  secret_num = generate_random_number(difficulty)
  play_game()

# 2. MAIN MENU OPTION - SHOW GAME RULES
def show_rules_of_game():
  """
  Displays the game rules to the player.
  """
  bulls_and_cows = f"""
RULES OF THE GAME:
The goal of the game is to {yellow}guess a secret code{reset} (4-digit number in normal difficulty).

The code consists of digits (0–9) with{yellow} no repeated numbers{reset}, and the secret
code {yellow}cannot start with zero{reset}.

After your guess, the game will provide you with feedback:

    - {yellow}Number of Bulls:  Correct digit in the correct position.{reset}
    - {yellow}Number of Cows:   Correct digit in the wrong position.{reset}

If you correctly guess the entire secret code (all Bulls), you win the game!

The game can also be played with codes of different lengths.
You can set difficulty in the main menu.

Enjoy the challenge and beat the high score!
"""
  return print(bulls_and_cows), enter_to_continue()

# 3. MAIN MENU OPTION - CHANGE DIFFICULTY
def set_difficulty():
  """
  Allows the player to change the difficulty level.
  """
  show_difficulty_menu()
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

# 3.1 DISPLAY DIFFICULTY MENU
def show_difficulty_menu():
  """
  Shows available difficulty levels to the player.
  """
  difficulty_menu = [
  f"Easy difficulty:       {yellow}3 digits{reset}",
  f"Normal difficulty:     {yellow}4 digits{reset}",
  f"Hard difficulty:       {yellow}5 digits{reset}",
  f"Nightmare difficulty:  {yellow}6 digits{reset}"
  ]
  return print(f"Choose your difficulty level:", "\n".join(difficulty_menu), sep="\n")

# 4. MAIN MENU OPTION - CHANGE PLAYER NAME
def get_user_name():
  """
  Displays a request for the player to enter their name.
  """
  global login
  login = input("Type your name: ")
  return login

# 5. MAIN MENU OPTION - DISPLAY SCOREBOARD
def show_scoreboard_menu():
  """
  Displays the scoreboard and allows the user to choose difficulty.
  """
  scoreboard_menu = [
  f"Easy difficulty:       {yellow}3 digits{reset}",
  f"Normal difficulty:     {yellow}4 digits{reset}",
  f"Hard difficulty:       {yellow}5 digits{reset}",
  f"Nightmare difficulty:  {yellow}6 digits{reset}"
  ]
  print(f"Scoreboard:")
  for index, item in enumerate(scoreboard_menu, start=1):
    print(f"{index}. {item}")

  while True:
    try:
      chosen_scoreboard = int(input("Select the difficulty level to display the results table:"))
      if chosen_scoreboard in range (1, 5):
        clear_terminal()
        print(f"Scoreboard:\n{scoreboard_menu[chosen_scoreboard-1]}\n")
        sorted_results = load_and_sort_results(f"scoreboard_{chosen_scoreboard+2}.csv")
        display_results(sorted_results)
        break
      else:
        print(f"{red}You didn't chose number in the menu, try again.{reset}")
        continue
    except ValueError:
        print(f"{red}Invalid input. Please enter a number between 1 and 4:{reset}")

# 6. OPTION FROM MAIN MENU - EXIT GAME
def exit_game():
  """
  Ends the game and exits the program.
  """
  print("Game is over. See you nextime.")
  quit()

# GAMEPLAY FUNCTION FOR BULLS AND COWS
def play_game():
  """
  Main game loop for Bulls and Cows.
  Handles user input, checks for correctness, and tracks attempts and time.
  """
  attempts = 0 # ATTEMPT COUNTER
  running_game = True
  start_time = time.perf_counter() # START TIME COUNTER
  print(f"I've generated random {yellow}{difficulty}-digit{reset} number for you.",
        f"All {yellow}digits are unique{reset} and the number {yellow}can't start with zero{reset}.",
        "Can you crack the secret code?",
        f"If you want to give up, type {yellow}'Q'{reset}.", line, sep="\n")
  while running_game:
    guess_num = input(f"Enter a {difficulty}-digit number: ")
    attempts += 1
    print(f">>> {guess_num}")
    print(f"{red}{secret_num} SMAZAT{reset}") ############################################# pro testování

    # EXIT GAME
    if guess_num.lower().strip() == "q":
      give_up()
      running_game = False

    # CORRECT GUESS
    elif guess_num == secret_num:
      end_time = time.perf_counter()  # STOP TIME COUNTER
      elapsed_time = round(end_time - start_time, 1)  # CALCULATE TOTAL TIME
      save_result(scoreboard_name, show_10_char(login), attempts, elapsed_time) # SAVE RESULT TO SCOREBOARD
      print(f"{green}Well done! You found the correct number\nin {attempts} attempts and {elapsed_time} seconds!{reset}")
      enter_to_continue()
      running_game = False

    # INPUT VALIDATION55
    else:
      error_message = validate_guess(guess_num)
      if error_message:
        print(f"{red}{error_message}{reset}", line, sep="\n")
        continue

    # GAME CONTINUES IF INPUT IS VALID
    show_progres(guess_num)
    print(line)

# GENERATE RANDOM NUMBER BASED ON GAME RULES
def generate_random_number(number_of_digits):
  """
  Generates a random number of given length with unique digits.
  The number cannot start with zero.
  """
  range_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  first_digit = choice(range(1, 10))
  rest_of_numbers = number_of_digits - 1
  range_list.remove(first_digit)
  other_digits = sample(range_list, rest_of_numbers)
  return "".join(map(str, ([first_digit] + other_digits)))

# GIVE UP DURING THE GAME
def give_up():
  """
  Displays the correct number and ends the game session.
  """
  print(f"The number you were looking for was {yellow}{secret_num}{reset}. Better luck next time.")
  enter_to_continue()

# INPUT VALIDATION DURING THE GAME
def validate_guess(guess):
  """
  Validates the player's guess to ensure it meets game rules.
  """
  if not guess.isnumeric():
    return "The number can contain only numeric characters."
  if guess.startswith("0"):
    return "The number can't start with zero."
  if len(guess) != difficulty:
    return "You have entered the wrong number of digits."
  if not check_unique_characters(guess):
    return "The number can't contain duplicate digits."
  return None

# DISPLAY PROGRESS DURING THE GAME
def show_progres(sec_num):
  """
  Displays the current progress in terms of bulls and cows.
  """
  cows = 0
  bulls = 0
  for index, number in enumerate(sec_num):
    if number == secret_num[index]:
      bulls += 1
    elif number in secret_num:
      cows += 1
  return print(f"{bulls} {get_plural_bull(bulls,)}, {cows} {get_plural_cow(cows)}")



##### UTILITY FUNCTIONS #####

# PAUSE PROGRAM UNTIL PLAYER PRESSES "ENTER"
def enter_to_continue():
  """
  Waits for the player to press Enter to continue.
  """
  input("Press Enter to continue...")

# DISPLAY ONLY 10 CHARACTERS OF PLAYER NAME
def show_10_char(name):
  """
  Returns the first 10 characters of a name, adding ellipsis if longer.
  """
  if len(name) > 10:
    name_max_10 = f"{name[:10]}..."
    return name_max_10
  else:
    return name

# CLEAR TERMINAL BASED ON OPERATING SYSTEM
def clear_terminal():
  """
  Clears the terminal screen depending on the operating system.
  """
  os.system("cls" if os.name == "nt" else "clear")

# CHECK PLURAL FORM FOR BULL
def get_plural_bull(number):
  """
  Returns the correct plural form for 'bull'.
  """
  result = "bull" if number == 1 else "bulls"
  return result

# CHECK PLURAL FORM FOR COW
def get_plural_cow(number):
  """
  Returns the correct plural form for 'cow'.
  """
  result = "cow" if number == 1 else "cows"
  return result

# CHECK UNIQUE CHARACTERS IN SECRET CODE
def check_unique_characters(string):
  """
  Checks if all characters in the string are unique.
  """
  return len(string) == len(set(string))

############################ dodělat modul, např scoreboard a importovat vzorce z něj....alias sb

# SAVE RESULTS TO CSV FILE
def save_result(filename, name, attempts, time):
  """
  Saves player results to a CSV file. Adds a header if the file does not exist.
  """
  file_exists = os.path.exists(filename)
  with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
      writer.writerow(["Name", "Attempts", "Time"])
    writer.writerow([name, attempts, time])

# LOAD AND SORT SCOREBOARD RESULTS
def load_and_sort_results(filename):
  """
  Loads game results from a CSV file and sorts them by completion time.
  """
  results = []
  if not os.path.exists(filename):
    print(f"{red}There are no results saved in this table yet.{reset}")
    return results
  try:
    with open(filename, mode='r') as file:
      reader = csv.reader(file)
      header = next(reader)
      if header != ["Name", "Attempts", "Time"]:
        print(f"{red}Invalid file format. Expected header: Name, Attempts, Time{reset}")
        return results
      for row in reader:
        name, attempts, time = row
        results.append([name, int(attempts), time])
  except Exception as e:
    print(f"{red}Error loading results: {e}{reset}")

  return sorted(results, key=lambda x: x[2]) # SORTED BY TIME

# DISPLAY RESULTS TABLE IN TERMINAL
def display_results(results):
  """
  Displays the scoreboard results sorted by time.
  """
  print(f"{'Rank':<5}{'Name':<15}{'Attempts':<10}{'Time(sec)':<10}")
  print("-" * 40)
  for rank, (name, attempts, time) in enumerate(results, start=1):
    print(f"{rank:<5}{name:<15}{attempts:<10}{time:<10}")
  print()
  enter_to_continue()


if __name__ == "__main__":
  game()


