from dotenv import load_dotenv
import requests
import os
import wikipediaapi
import random
import sys
import time



load_dotenv()


def main():
    slow_print("Welcome To PySearchWeatherPlay")
    while True:
        try:
            slow_print("Enter ctrl + d to exit the program")
            slow_print("Enter 1 to use the calculator 2 to use the search tools and 3 to play a game")
            answer = input(">>>>>>>>>>: ")
            if answer == "1":
                slow_print("Welcome to the Calculator Section")
                slow_print("Enter 1 to Quit")
                while True:
                    try:
                       equation = input(">>>>>: ")
                       if equation == "1":
                           break 
                       else:
                          answer = calculator(equation)
                          print(answer)
                    except Exception:
                        slow_print("Wrong input")
                        continue
            elif answer == "2":
                slow_print("Enter 1 to get current weather information and 2 to search")
                args = input(">>>>>>>>>>>: ")
                if args == "1":
                    city = input("Enter Your City Name: ")
                    weather_data = Weather(city.lower())
                    if weather_data:
                        temperature = weather_data['main']['temp']
                        humidity = weather_data['main']['humidity']
                        description = weather_data['weather'][0]['description']
                        wind_speed = weather_data['wind']['speed']
                        wind_direction = weather_data['wind']['deg']
                        slow_print(description)
                        slow_print(f"Temperature: {temperature}")
                        slow_print(f"Humidity: {humidity}")
                        slow_print(f"Wind Speed: {wind_speed}")
                        slow_print(f"Wind Direction: {wind_direction}")
                    else:
                        slow_print("Invalid City Name")
                elif args == "2":
                    slow_print("Type in Your Search Queries")
                    search = input(">>>>>>>: ")
                    result = Search(search)
                    slow_print(result)
                else:
                    continue
            if answer == "3":
                slow_print("Enter 1 to play rock, paper, scissors and 2 to play the guessing game")
                play = input(">>>>>>>>>>: ")
                if play == "1":
                    play_rock_paper_scissor()
                elif play == "2":
                    play_guessing_game()
                else:
                    continue
            else:
                continue
        except EOFError:
            slow_print("Bye for now")
            break
                
                
                    
                
                
        
    
    
    

def Search(query):
    """
    connect and use the wikipedia api to search and return response to the user
    """
    wiki_wiki = wikipediaapi.Wikipedia('en',headers={"User-Agent":'PySearchWetherPlay/1.0 (samsonoluwafemi@gmail.com)'})
    reply = wiki_wiki.page(query)
    if reply.exists():
        return reply.text[:1000]
    else:
        return "No Info Found on your Query"
    
    


def Weather(city="lagos"):
    """
    request for weather condition using the openWeatherMap Api
    """
    
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=imperial'
    weather_data = requests.get(request_url).json()
    if not weather_data['cod'] == 200:
        return "City does not Exist"
    else:
        return weather_data
    
    
    



user_score = 0
computer_score = 0

def play_rock_paper_scissor():
    """
    Starts the rock paper and scissors game
    """
    choice = ["rock","paper","scissors"]
    slow_print("Welcome to Rock, Paper and scissors Game")
    slow_print("You can exit the game with ctrl + d")
    while True:
        try:
            while True:
                user_choice = input("Choose between rock paper and scissors: ")
                if user_choice not in choice:
                     continue
                else:
                    break
            computer_choice = random.choice(choice)
            slow_print(f"You choose {user_choice} and computer choose {computer_choice}")
            slow_print(check_winner(computer_choice,user_choice))
            continue
        except EOFError:
            return slow_print(f"You Scored {user_score} and the computer scored {computer_score}")
            
def check_winner(computer_choice,user_choice):
    if user_choice == computer_choice:
        return "It's a tie game"
    elif (user_choice == "rock" and computer_choice == "scissors") or (user_choice == "scissors" and computer_choice == "paper") or (user_choice == "paper" and computer_choice == "rock"):
        global user_score
        user_score += 1
        return "You Win"
    else:
        global computer_score
        computer_score += 1
        return "Computer Wins"
    
    
def play_guessing_game():
    """Number Guessing Game"""
    slow_print("Train Your Brain🧠 and make guesses like a genuies!! ")
    slow_print("Enter quit to exit th game")
    while True:
        number = random.randint(1,1000)
        try:
           guess = input("Am Thinking of a number between 1 and 1000 guess it: ")
           if guess.lower() == "quit":
               break
           else:
               slow_print(check(number,int(guess)))
               next_chance = input("Wanna Try Again, enter 1 for yes and any number for no: ")
               if next_chance == "1":
                   continue
               else:
                   break
        except:
            continue
        
def check(number,guess):
    if guess > number:
        return "Too large"
    elif guess < number:
        return "Too small, Try again"
    elif number == guess:
        return  "Yes you got it right"
        

    
def calculator(equ):
    return eval(equ)
         
         
        
        
def slow_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.04)
    sys.stdout.write('\n')
    
if __name__ == "__main__":
    main()