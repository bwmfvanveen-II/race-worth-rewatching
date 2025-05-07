import sqlite3
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

import random
# Create your views here.

@api_view(["GET"])
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

@api_view(["GET"])
def user_data(request):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor() # cursor

    request_layout = "SELECT * FROM ratings_user;" 

    c.execute(request_layout)
    outputs = c.fetchall()
    return HttpResponse(outputs)

@api_view(["POST"])
def add_user(request):
    try:
        # Connect to database
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor() # cursor

        # Get relevant data from the request
        name = request.POST['name']
        password = request.POST['password']

        # Request
        insert_layout = "INSERT INTO ratings_user (Username, Password) " \
                        "VALUES (?, ?);"
        inputs = (name, password)
    
        # Execute INSERT and commit
        c.execute(insert_layout, inputs)
        conn.commit()
        return HttpResponse("Added user correctly")
    except:
        return HttpResponse("Error in adding user")
    
# Method to authenticate users and send over a unique hash to ensure users only make requests under their own name.
@api_view(["POST"])
def authenticate_user(request):
    try:
        # Connect to database
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor() # cursor

        # Get relevant data from the request
        name = request.POST['name']
        password = request.POST['password']

        print(name)

        # Request
        insert_layout = "SELECT * from ratings_user WHERE username = (?);"
        inputs = [name]

        print("seems to get to this point at least")
    
        # Execute INSERT and commit
        query_cursor = c.execute(insert_layout, inputs)

        # When fetching from the query we do not keep the names of each column, so we look for it here.
        headerpos = []
        for col in query_cursor.description:
            headerpos.append(col[0])

        out = c.fetchall()

        # If we do not have a user or somehow have too many, we just reject
        if len(out) != 1:
            return HttpResponse("Rejected")
        else:
            # This gets the password from the index of "password". If there is no password block the excpet block is triggered and it fails.
            output_password = out[0][headerpos.index("password")]

            if password == output_password:
                return HttpResponse("Authenticated")
            else:
                return HttpResponse("Rejected")
    except:
        error_code = HttpResponse("Error in authenticating user")
        error_code.status_code = 400
        return error_code
    
@api_view(["POST"])
def add_rating(request):
    try:
        # Connect to database
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor() # cursor

        # Get relevant data from the request

        name = request.POST['name']
        password = request.POST['password']

        # Request
        insert_layout = "INSERT INTO ratings_user (Username, Password) " \
                        "VALUES (?, ?);"
        inputs = (name, password)
    
        # Execute INSERT and commit
        c.execute(insert_layout, inputs)
        conn.commit()
        return HttpResponse("Added user correctly")
    except:
        return HttpResponse("Error in adding user")        

