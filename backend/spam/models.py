from django.db import models

class Email(models.Model):
    """
    An email message, with a title, body, and date.
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField()
    rating = models.IntegerField()
    views = models.IntegerField()

class Lib(models.Model):
    """
    A lib represents a specific term in an email, the description of its part of
    speech, and its position in the original email.
    """
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    original = models.CharField(max_length=255)
    position = models.IntegerField()
    description = models.CharField(max_length=255)