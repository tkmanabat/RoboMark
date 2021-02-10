from random import choice
import discord

def calculate(num1:int , operator , num2:int):
    if operator=="+":
        return num1 + num2
    if operator=="-":
        return num1 - num2
    if operator=="x" or operator=="*":
        return num1*num2
    if operator=="/":
        return num1/num2
    else:
        return False

def coinfliper():
    coin=['heads', 'tails']
    result=choice(coin)
    if result =='heads':
         result= '***Heads!!!*** :coin: :coin: :coin:'
         return result
    else:
        result= '***Tails!!!*** :coin: :coin: :coin:'
        return result

