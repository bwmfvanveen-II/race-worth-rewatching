from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import sqlite3

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

def user_data(request):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor() # cursor

    request_layout = "SELECT * FROM ratings_user;" 

    c.execute(request_layout)
    outputs = c.fetchall()
    return HttpResponse(outputs)

def add_user(request):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor() # cursor

    insert_layout = "INSERT INTO ratings_user (Username, Password) " \
                     "VALUES (?, ?);"

    name = "hardcoded example rn"
    pwd = "hardcoded example pwd"

    inputs = (name, pwd)

    try:
        c.execute(insert_layout, inputs)
        conn.commit()
        return HttpResponse("Added user correctly")
    except:
        return HttpResponse("Error in adding user")