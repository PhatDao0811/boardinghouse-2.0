from django.db import models

# Create your models here.
class Base(models.Model):
    class Meta:
        abstract = True
    phone = models.CharField(max_length=10, null=True)
    fullname = models.CharField(max_length=100)


class Personnel(Base):
    id_personnel = models.CharField(primary_key=True, max_length=100, null=False)

    def __str__(self):
        return self.id_personnel
    

class Area(models.Model):
    nameDistrict = models.CharField(max_length=100)

    def __str__(self):
        return self.nameDistrict

class House(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='house_area', null=True)
    personnel = models.ForeignKey(Personnel, on_delete=models.SET_NULL, related_name='house', null=True)
    nameHouse = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nameHouse

class Room(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True, related_name='room')
    roomsNumber = models.IntegerField()
    acreage = models.IntegerField()
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    interior = models.TextField()

class Guests(Base):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name='guest')
    date = models.DateField(null=True)

class Electricity(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='electricity', null=True)
    index_electricity = models.IntegerField()
    date = models.DateField(null=True)
    

