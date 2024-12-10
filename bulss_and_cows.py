# projekt_2.py: druhý projekt do Engeto Online Python Akademie

# author: Marek Pošmura
# email: m.posmura@seznam.cz

from random import sample, choice, seed


seed(2) ########## ODSTRANIT SEED ##########
difficulty = 4
line = 79 * "-"
line_2 = 79 * "="



def welcome_screen():
  login = input("Type your name: ")
  print(f"Hello {login}!", "Let's play Bulls and Cows!", line, sep="\n")

def show_menu():
  main_menu = [
  "1. Start game",
  "2. Rules of the Game",
  "3. Difficulty",
  "4. Scoreboard",
  "5. Exit game"
  ]
  return "\n".join(main_menu)

def chose_from_main_menu():
  while True:
    print(show_menu(), line, sep="\n")
    menu = input("Choose number from main menu: ")

    if menu not in ("1", "2", "3", "4", "5"):
      print("You didn't chose number in the menu, try again.")
      continue
    elif menu == "1":
      start_game()
    elif menu == "2":
      show_rules_of_game()
    elif menu == "3":
      set_difficulty()
    elif menu == "4":
      print("Scoreboard") #### vložit funkci display_scoreboard()
    elif menu == "5":
      print("Game over")
      quit()

def start_game():
  generate_random_number(difficulty)
  play_game()

def show_rules_of_game():
  rules = """
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
  return print(rules)

def set_difficulty():
  while True:
    try:
      num_input = int(input("Set the length of the code between 1 and 10: "))
      if num_input in range (1, 11):
        difficulty = int(num_input)
        break
      else:
        print("You didn't enter a length of code between 1 and 10. Please try again.")
        continue
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 10: ")

  return difficulty

# def welcome_screen():
#   print("Hello there!", line, sep="\n")
#   print(f"I've generated a random {difficulty}-digit number for you.\n\
# Let's play a bulls and cows game.\n\
# If you don't want to play, type 'Q'\n\
# If you want to see scoreboard, type 'S'", line, sep="\n")

def generate_random_number(number_of_digits):
  range_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  first_digit = choice(range(1, 10))
  rest_of_numbers = number_of_digits - 1
  range_list.remove(first_digit)
  other_digits = sample(range_list, rest_of_numbers)
  return list(map(str, ([first_digit] + other_digits)))

secret_num = "".join(generate_random_number(difficulty))

def play_game():
  attempts = 0
  runnig_game = True
  print(f"I've generated a random {difficulty}-digit number for you.",
          "If you don't want to play, type 'Q'", sep="\n")
  while runnig_game:
    guess_num = input(f"Enter a {difficulty}-digit number: ")
    attempts += 1
    print(f">>> {guess_num}", line, sep="\n")
    # SPRÁVNĚ ZADÁNO HESLO
    if guess_num == secret_num:
      print(f"Correct, you've guessed the right number\nin {attempts} guesses!", line, sep="\n")
      runnig_game = False
    # UKONČENÍ PROGRAMU
    elif guess_num.lower().strip() == "q":
      print("Ukončuji hru!")
      runnig_game = False
    # ZKONTROLUJE NUMERICKE ZNAKY
    elif not guess_num.isnumeric():
      print("The number can contain only numeric characters, plese try again.")
    # ZAČÍNÁ NULOU
    elif guess_num.startswith("0"):
      print("The guessed number can't start with zero, please try again.")
    # ZADÁN ŠPATNÝ POČET ČÍSLIC
    elif len(guess_num) != difficulty:
      print("You have entered the wrong number of digits, please try again.")
    # VE VÝSTUPU JSOU DVĚ NEBO VÍCE STEJNÝCH ČÍSEL
    elif not check_unique_characters(guess_num):
      print("The number can't contain duplicate digits, please try again.")
    elif runnig_game:
        show_progres(guess_num)
  print(line)

def check_bull_bulls(number):
  result = "bull" if number == 1 else "bulls"
  return result

def check_cow_cows(number):
  result = "cow" if number == 1 else "cows"
  return result

def check_unique_characters(string):
    return len(set(string)) == len(string)

def show_progres(sec_num):
  var_cows = 0
  var_bulls = 0
  for index, number in enumerate(sec_num):
    if number == secret_num[index]:
      var_bulls += 1
    elif number in secret_num:
      var_cows += 1

  return print(f"{var_bulls} {check_bull_bulls(var_bulls)}, {var_cows} {check_cow_cows(var_cows)}")




welcome_screen()
show_menu()
chose_from_main_menu()
# přesměorvání do menu po nějaké době



# print(secret_num) ######## ODSTRANIT ########
