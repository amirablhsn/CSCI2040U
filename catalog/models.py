from django.db import models

class CatalogItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) :
        return self.name 