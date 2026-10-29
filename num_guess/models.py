from django.db import models



class Game(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    number = models.IntegerField()
    game_status = models.CharField(max_length=16, default='active')
    attempts_count = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=5)
