# PySearchWeatherPlay

#### Video Demo: <https://youtu.be/IPDT6bnu4VY>

#### Description:

 The pysearchweatherplay is an command-line app written in python that allows users to calculate, request the current weather condition, make searches and play games like rock paper and scissors or number guessing game.

 This is a Python implementation of the Search Weather Play game, which can be played in the terminal or integrated into other applications.

 To integreate the search functionality i used the python Wikipedia-API package so when the user typs their query in it is passed to the function that makes the request and the return value will be printed out to the user.

 The Weather search is powered by the openweathermap's API which espects a city to search and return the value if the city is valid, and an error message if it's not a valid city. To achieve this i used the requests library to make request to the api and then print out some values to the user.

The calculator is just the python eeval function calculating the users inputs and returns the answer or though the eval do raise a lots of exceptions which is why i handled the Exception object it self.

The logic for the games is really straight forward that is the rock, paper and scissors game all revolves around the random module. Using the random.choice() method i was able to help the computer player pick randomly between rock paper and scissors and then in a loop the user can continue to play for as long as they want and as soon as they enter ctrl + d the game will stop and the scores will be displayed.

The number guessing game too does almost the same as the rock paper and scissors game but this one is pretty hard cause you will have to guess a number between 1 and 1000 which is a very long list but was made easy with the random.randint() method.

And the last function in the script is the slow_print fuction that when passed a string it iterates over it and uses the sys.stdout.write() to write out the string one by one and uses the time module to slow down the writing and create a slow printing effect