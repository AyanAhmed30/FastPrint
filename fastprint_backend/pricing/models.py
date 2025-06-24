from django.db import models

class TrimSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BindingType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class SpineType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class ExteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class FoilStamping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class ScreenStamping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class CornerProtector(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class InteriorColor(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=6, decimal_places=4)

    def __str__(self):
        return self.name

class PaperType(models.Model):
    name = models.CharField(max_length=100)
    price_per_page = models.DecimalField(max_digits=6, decimal_places=4)

    def __str__(self):
        return self.name
    
class Spine(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name    
