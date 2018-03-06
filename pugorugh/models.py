from django.contrib.auth.models import User
from django.db import models


# All-purpose 'unknown' variable
UNKNOWN = 'u'

# Choices for sex of dog
MALE = 'm'
FEMALE = 'f'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNKNOWN, 'Unknown')
)


# Choices for size of dog
SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
EXTRA_LARGE = 'xl'
SIZE_CHOICES = (
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
    (EXTRA_LARGE, 'Extra Large'),
    (UNKNOWN, 'Unknown')
)

# Status choices
LIKED = 'l'
DISLIKED = 'd'
STATUS_CHOICES = (
    (LIKED, 'Like'),
    (DISLIKED, 'Dislike')
)

# Age choices
BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'
AGE_CHOICES = (
    (BABY, 'Baby'),
    (YOUNG, 'Young'),
    (ADULT, 'Adult'),
    (SENIOR, 'Senior'),
)


class Dog(models.Model):
    name = models.CharField(max_length=30)
    image_filename = models.CharField(max_length=200)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=UNKNOWN
    )
    size = models.CharField(
        max_length=2,
        choices=SIZE_CHOICES,
        default=UNKNOWN
    )

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES
    )

class UserPref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.CharField(
        max_length=10,
        choices=AGE_CHOICES
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='u'
    )
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)

    def __str__(self):
        return "User Preference " + str(self.pk)

