from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user model representing registered users in the database.
    Can be extended in the future with additional profile fields.
    """
    pass
