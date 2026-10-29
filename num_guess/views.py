from django.http import JsonResponse, request, response
import secrets
import string
from .models import Game
import random


# requests
def num_guess(request):
    uid=request.COOKIES.get('uid') 
    guess = request.GET.get('guess')
    max_guess = convert_max_attempts(request.GET.get('max_guess'))
    new_uid = generate_random_uid()
 
    game, created = Game.objects.get_or_create(uid=uid, defaults={'number': random.randint(1, 100), 'max_attempts': max_guess, 'uid': new_uid})

    
    response = JsonResponse(data_is_guess_correct(guess, game))
    if created:
        response.set_cookie(
            key='uid',
            value=new_uid,
        )

    return response

def restart_game(request):
    uid=request.COOKIES.get('uid') 
    max_guess = convert_max_attempts(request.GET.get('max_guess'))
    new_uid = generate_random_uid()

    game, created = Game.objects.get_or_create(uid=uid, defaults={'number': random.randint(1, 100), 'max_attempts': max_guess, 'uid': new_uid})
    
    response = JsonResponse({'message': 'Game restarted. A new number has been generated.'})
    if not created:
        game.number = random.randint(1, 100)
        game.attempts_count = 0
        game.save()
    else:
        response.set_cookie(
            key='uid',
            value=new_uid,
        )
    return response
# helper functions
def generate_random_uid(length: int = 32) -> str:
  alphabet = string.ascii_letters + string.digits
  return "".join(secrets.choice(alphabet) for _ in range(length))

def convert_max_attempts(max_attempts:str):
    if max_attempts is None or not max_attempts.isdigit():
        return 10
    return int(max_attempts)

def check_if_guess_in_range(number):
    if number is None or not number.isdigit():
        return False
    return 1 <= int(number) <= 100

def data_is_guess_correct(guess, game):
    answer = game.number
    if not check_if_guess_in_range(guess):
        data = {
            'message': 'Your guess is out of range. Please enter a number between 1 and 100.',
        }
        return data
    if game.attempts_count >= game.max_attempts:
        data = {
            'message': 'You have exceeded the maximum number of attempts. Please start a new game.',
        }
        return data
    
    guess = int(guess)
   
    if guess>answer:
        data = {
            'message': 'Your guess is too high',
        }
    elif guess<answer:
        data = {
            'message': 'Your guess is too low',
        }
    else:
        data = {
            'message': 'Congratulations! You guessed the number.',
        }
    game.attempts_count += 1
    game.save()
    return data
