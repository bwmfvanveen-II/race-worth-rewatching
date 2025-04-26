from django.shortcuts import render
from django.http import HttpResponse

import random
# Create your views here.

def home(request):
    rand = random.randint(0, 2)
    if rand == 0 :
        return HttpResponse("Race was pretty bad")
    elif rand == 1:
        return HttpResponse("Race was ok")
    else:
        return HttpResponse("Literally the greatest instance of going around the funny circle ever")
