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

# I would have liked to make the season+track be the composite primary key but we can't have a composite primary key be a foreign key in django
class Race(models.Model):
    id = models.BigAutoField(primary_key=True)
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)
    track = models.ForeignKey(Track, on_delete=models.DO_NOTHING)
    date = models.DateField()
    race_number = models.IntegerField() # This is just like 'this is the 4th race in the season' 

class Rating(models.Model):
    # pk = models.CompositePrimaryKey("user", "race")
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    score = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'race'], name='rating-user_relation'),
        ]
    
