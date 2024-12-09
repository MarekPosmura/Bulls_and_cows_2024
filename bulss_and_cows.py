# projekt_2.py: druhý projekt do Engeto Online Python Akademie

# author: Marek Pošmura
# email: m.posmura@seznam.cz

from random import sample, choice, seed


seed(2) ########## ODSTRANIT SEED ##########
line = 47 * "-"
line2 = 47 * "="

difficulty = 5

def welcome_screen():
  print("Hello there!", line, sep="\n")
  print(f"I've generated a random {difficulty}-digit number for you.\n\
Let's play a bulls and cows game.\n\
If you don't want to play, type 'Q'\n\
If you want to see scoreboard, type 'S'", line, sep="\n")


def generate_random_number(number_of_digits):
  range_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  first_digit = choice(range(1, 10))
  rest_of_numbers = number_of_digits - 1
  range_list.remove(first_digit)
  other_digits = sample(range_list, rest_of_numbers)
  return list(map(str, ([first_digit] + other_digits)))

def check_bull_bulls(number):
  result = "bull" if number == 1 else "bulls"
  return result

def check_cow_cows(number):
  result = "cow" if number == 1 else "cows"
  return result

def check_unique_characters(string):
    return len(set(string)) == len(string)

def game_progres():
  var_cows = 0
  var_bulls = 0
  for index, number in enumerate(guess_num):
    if number == secret_num[index]:
      var_bulls += 1
    elif number in secret_num:
      var_cows += 1

  return print(f"{var_bulls} {check_bull_bulls(var_bulls)}, {var_cows} {check_cow_cows(var_cows)}")


# def play_again():
#   play_again = input("Do you want to play again? Y/N ")
#   if play_again.lower().strip() == "y":
#     runnig_game = True
#   elif play_again.lower().strip() == "n":
#     runnig_game = False
#   else:
#     print("You din't type Y or N, try again.")
#     pass

runnig_game = True



welcome_screen()
secret_num = "".join(generate_random_number(difficulty))

print(secret_num) ######## ODSTRANIT ########
attempts = 0

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

  # zobrazení SCOREBOARD (DODĚLAT)
  elif guess_num.lower().strip() == "s":
    print("SCOREBOARD")

  # NASTAVENÍ OBTÍŽNOSTI
  elif guess_num.lower().strip() == "D":
    difficulty = input(f"Typ")


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
      game_progres()

