from django.db import models


class City(models.Model):

    name = models.CharField(max_length=30, unique=True)
    html_href = models.CharField(max_length=100)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name


class Age(models.Model):

    age = models.IntegerField(unique=True)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.age == other.age
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.age)


class Images(models.Model):

    name = models.CharField(max_length=15)
    time = models.DateTimeField(auto_now=False, auto_now_add=False,)

    def __str__(self):
        return str(self.name)


class Number(models.Model):

    number = models.BigIntegerField(unique=True)

    cities = models.ManyToManyField(City)
    ages = models.ManyToManyField(Age)
    images = models.ManyToManyField(Images)





    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.number == other.number
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.number)


class TimeDate(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    number = models.ForeignKey(Number, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.time == other.time
        return False

    def __ne__(self, other):
        return not self.__eq__(other)





