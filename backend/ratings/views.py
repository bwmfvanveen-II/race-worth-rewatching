from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import json

import random
# Create your views here.

def home(request):
    rand = random.randint(0, 2)
    jsonObj = {}
    if rand == 0 :
        jsonObj['evaluation'] = "Race was pretty bad"
    elif rand == 1:
        jsonObj['evaluation'] = "Race was ok"
    else:
        jsonObj['evaluation'] = "Literally the greatest instance of going around the funny circle ever"
    return JsonResponse(jsonObj)
