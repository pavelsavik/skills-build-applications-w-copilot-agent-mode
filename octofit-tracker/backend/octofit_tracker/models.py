# models.py
# Define models for users, teams, activity, leaderboard, and workouts collections

from djongo import models
from bson import ObjectId
from djongo.models.fields import ObjectIdField

class User(models.Model):
    id = ObjectIdField(primary_key=True, default=ObjectId)  # Change ID type to ObjectId
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Team(models.Model):
    id = ObjectIdField(primary_key=True, default=ObjectId)  # Change ID type to ObjectId
    name = models.CharField(max_length=255)
    members = models.JSONField()

class Activity(models.Model):
    id = ObjectIdField(primary_key=True, default=ObjectId)  # Change ID type to ObjectId
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    duration = models.IntegerField()

class Leaderboard(models.Model):
    id = ObjectIdField(primary_key=True, default=ObjectId)  # Change ID type to ObjectId
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    score = models.IntegerField()

class Workout(models.Model):
    id = ObjectIdField(primary_key=True, default=ObjectId)  # Change ID type to ObjectId
    name = models.CharField(max_length=255)
    description = models.TextField()
