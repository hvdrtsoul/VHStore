import enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()
    image = models.ImageField(upload_to='movie_images/', default="media/no-image.png")

    def __str__(self):
        return self.title


class Cassette(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    condition = models.CharField(max_length=10,
                                 choices=[('MINT', 'Mint'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('POOR', 'Poor')])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.condition}"


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=50)
    image = models.ImageField(upload_to='equipment_images/', default="media/no-image.png")

    def __str__(self):
        return self.name

@enum.unique
class StatusType(str, enum.Enum):
    SIMPLE = 'simple',
    BRONZE = 'bronze',
    SILVER = 'silver',
    GOLD = 'gold'

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

class MembershipStatus(models.Model):
    name = models.CharField(max_length=20, choices=StatusType.choices())
    milestone = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True, default="none")
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    role = models.CharField(max_length=20,
                            choices=[('buyer', 'Buyer'), ('seller', 'Seller')], default="buyer")
    plan = models.ForeignKey(MembershipStatus, on_delete=models.CASCADE, default=1)
    total_purchases = models.IntegerField(default=0)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')


class CartItem(models.Model):
    cassette = models.ForeignKey(Cassette, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
