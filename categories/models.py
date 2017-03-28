from django.db import models


class Category(models.Model):
    tipo_categoria = models.CharField(max_length=20)

    def __str__(self):
        return self.tipo_categoria

