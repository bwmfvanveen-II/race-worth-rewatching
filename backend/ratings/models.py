from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=255)

class Season(models.Model):
    year = models.IntegerField(primary_key=True)

# Name is just the name of the track. If there are two separate tracks with the same name then that would be weird anyway so we'll just have to deal with it if it ever comes
class Track(models.Model):
    name = models.CharField(max_length=255, primary_key=True) 

class Driver(models.Model):
    full_name = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)
    driver_number = models.IntegerField()

# This is made essentially to specify if it was a GP, sprint or maybe even qualifying could be included
class Type_of_race(models.Model):
    type = models.CharField(max_length=255)

# I would have liked to make the season+track be the composite primary key but we can't have a composite primary key be a foreign key in django
class Race(models.Model):
    id = models.BigAutoField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)
    track = models.ForeignKey(Track, on_delete=models.DO_NOTHING)
    date = models.DateField()
    race_number = models.IntegerField() # This is just like 'this is the 4th race in the season' 
    number_of_laps = models.IntegerField()
    drivers = models.ManyToManyField(Driver)
    race_type = models.ForeignKey(Type_of_race, on_delete=models.DO_NOTHING) 

# Bit annoying to make the starting grid separate like this but I guess we kind of have to for efficiency
class Starting_grid(models.Model):
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    driver = models.ForeignKey(Driver, on_delete=models.DO_NOTHING)
    starting_position = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['race', 'starting_position'], name='the_how-tf-do-two-drivers-start-on-the-same-position_constraint'),
        ]

class Rating(models.Model):
    # pk = models.CompositePrimaryKey("user", "race")
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    score = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'race'], name='rating-user_relation'),
        ]
    
