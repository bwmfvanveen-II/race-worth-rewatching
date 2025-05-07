import sqlite3
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view

from super_secret_hash_gen import verify_secret_hash

import random
# Create your views here.

def extract_col_names(query_cursor):
    column_names = []
    for col in query_cursor.description:
        column_names.append(col[0])
    return column_names

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

        # Request
        user_layout = "SELECT * from ratings_user WHERE username = (?);"
        inputs = [name]
    
        # Execute INSERT and commit
        query_cursor = c.execute(user_layout, inputs)

        # When fetching from the query we do not keep the names of each column, so we look for it here.
        column_names = extract_col_names(query_cursor)

        out = c.fetchall()

        # If we do not have a user or somehow have too many, we just reject
        if len(out) != 1:
            return HttpResponse("Rejected")
        else:
            # This gets the password from the index of "password". If there is no password block the excpet block is triggered and it fails.
            output_password = out[0][column_names.index("password")]

            if password == output_password:
                return HttpResponse("Authenticated")
            else:
                return HttpResponse("Rejected")
    except:
        error_code = HttpResponse("Error in authenticating user")
        error_code.status_code = 400
        return error_code
    
@api_view(["POST"])
def rate_race(request):
    try:
        incoming_user = request.headers['username']
        incoming_hash = request.headers['UserToken']

        # If the hash is false then we just go straight to the error stage because they were not authenticated properly
        assert verify_secret_hash(incoming_user, incoming_hash)

        # Connect to database
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor() # cursor

        # Get relevant data from the request
        name = request.POST['username']
        race_id = request.POST['race_id']
        rating = request.POST['rating']

        # Request
        user_layout = "SELECT * from ratings_rating WHERE user_id = (?) AND race_id = (?);"
        inputs = (name, race_id)
    
        # Execute INSERT and commit
        c.execute(user_layout, inputs)

        out = c.fetchall()

        # If we do not have a rating we add it. If we have one, we update. If we have more, we panic.
        if len(out) == 0:
            # Add rating
            insert_layout = "INSERT INTO ratings_rating (user_id, race_id, score) " \
                            "VALUES (?, ?, ?);"
            insert_inputs = (name, race_id, rating)
            c.execute(insert_layout, insert_inputs)
            conn.commit()

            return HttpResponse("Rating added correctly")
        elif len(out) == 1:
            # Request
            insert_layout = "UPDATE ratings_rating Set  score = (?) WHERE user_id = (?) AND race_id = (?);"
            insert_inputs = (rating, name, race_id)
            c.execute(insert_layout, insert_inputs)
            conn.commit()

            return HttpResponse("Rating updated correctly")
        else:
            return HttpResponse("how tf did we get multiple of the same rating")
        
    except:
        error_code = HttpResponse("Error in rating race")
        error_code.status_code = 400
        return error_code 

