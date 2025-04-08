from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Clear all existing data from the database
        User.objects.filter(pk__isnull=False).delete()
        Team.objects.filter(pk__isnull=False).delete()
        Activity.objects.filter(pk__isnull=False).delete()
        Leaderboard.objects.filter(pk__isnull=False).delete()
        Workout.objects.filter(pk__isnull=False).delete()

        # Remove duplicate User entries before creating new ones
        User.objects.all().delete()  # Clear all existing User entries to avoid duplicates

        # Create users
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', password='thundergodpassword'),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', password='metalgeekpassword'),
            User(email='zerocool@mhigh.edu', name='Elliot', password='zerocoolpassword'),
            User(email='crashoverride@hmhigh.edu', name='Dade', password='crashoverridepassword'),
            User(email='sleeptoken@mhigh.edu', name='Sleep Token', password='sleeptokenpassword'),
        ]
        
        # Clear existing User entries to avoid duplicates
        User.objects.filter(pk__isnull=False).delete()  # Ensure only valid primary key entries are deleted

        # Ensure all User objects are saved before referencing them
        saved_users = []
        for user_data in users:
            user = User.objects.create(email=user_data.email, name=user_data.name, password=user_data.password)
            saved_users.append(user)

        # Update the Team creation logic to use JSONField for members
        teams = [
            Team(name='Blue Team', members=[{'email': saved_users[0].email}, {'email': saved_users[1].email}]),
            Team(name='Gold Team', members=[{'email': saved_users[2].email}, {'email': saved_users[3].email}, {'email': saved_users[4].email}]),
        ]
        # Save teams individually to ensure they are persisted in the database
        for team in teams:
            team.save()

        # Fetch saved User objects explicitly before assigning to activities
        saved_users = list(User.objects.all())  # Ensure all User objects are fetched from the database

        # Update activities to reference fetched User objects
        activities = [
            Activity(user=saved_users[0], type='Cycling', duration=60),
            Activity(user=saved_users[1], type='Crossfit', duration=120),
            Activity(user=saved_users[2], type='Running', duration=90),
            Activity(user=saved_users[3], type='Strength', duration=30),
            Activity(user=saved_users[4], type='Swimming', duration=75),
        ]

        # Ensure all User objects are explicitly fetched and verified before assigning to activities
        for activity in activities:
            activity.user = User.objects.get(email=activity.user.email)  # Explicitly fetch the User object
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=teams[0], score=200),
            Leaderboard(team=teams[1], score=150),
        ]

        # Save leaderboard entries individually
        for entry in leaderboard_entries:
            entry.save()

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]

        # Save workouts individually
        for workout in workouts:
            workout.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
