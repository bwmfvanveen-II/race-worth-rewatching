import sqlite3
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view

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

@api_view(["POST"])
def add_user(request):
    get_token(request)

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor() # cursor

    insert_layout = "INSERT INTO ratings_user (Username, Password) " \
                     "VALUES (?, ?);"
    
    print(request.body)
    print(request.POST)


    name = request.POST['name']
    password = request.POST['password']


    inputs = (name, password)

    try:
        c.execute(insert_layout, inputs)
        conn.commit()
        return HttpResponse("Added user correctly")
    except:
        return HttpResponse("Error in adding user")
