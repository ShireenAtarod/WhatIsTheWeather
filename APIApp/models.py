from django.db import models

class City(models.Model):
    name = models.TextField(max_length=150)
    temperature = models.FloatField(max_length=200, default=0)

    def __str__(self) -> str:
        return self.name
