from django.conf import settings
from django.db import models
from django.utils import timezone


class Chicken(models.Model):
    HEALTH_STATUS_CHOICES = (
        (0, 'Sihat'),
        (1, 'Sakit'),
    )

    PURPOSE_CHOICES = (
        (0, 'Petelur'),
        (1, 'Pedaging'),
    )


    date_added = models.DateField(default=timezone.now)
    age = models.IntegerField()
    health_status = models.PositiveIntegerField(choices=HEALTH_STATUS_CHOICES)
    purpose = models.PositiveIntegerField(choices=PURPOSE_CHOICES, default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.age} week old chicken, {self.get_health_status_display()}'\
                f' on {self.owner.username}\'s farm'
    
    def get_health_status_display(self):
        return self.HEALTH_STATUS_CHOICES[self.health_status][1]
    
    def get_purpose_display(self):
        return self.PURPOSE_CHOICES[self.purpose][1]
    
class Egg(models.Model):
    EGG_SIZE_CHOICES = (
        (0, 'Kecil'),
        (1, 'Sederhana'),
        (2, 'Besar'),
    )

    collection_date = models.DateField()
    quantity = models.PositiveIntegerField()
    size = models.PositiveIntegerField(choices=EGG_SIZE_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} {self.get_size_display()} eggs collected on {self.collection_date}'
    
    def get_size_display(self):
        return self.EGG_SIZE_CHOICES[self.size][1]



