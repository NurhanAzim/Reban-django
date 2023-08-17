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
    age = models.IntegerField(null=True, blank=True)
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
    
    def get_age(self, subtracted_date=False):
        days_passed = (timezone.now().date() - self.date_added).days
        weeks_passed = days_passed // 7
        calculated_age = self.age + weeks_passed
        return calculated_age

    
class Egg(models.Model):
    EGG_SIZE_CHOICES = (
        (0, 'Kecil'),
        (1, 'Sederhana'),
        (2, 'Besar'),
    )

    collection_date = models.DateField()
    size = models.PositiveIntegerField(choices=EGG_SIZE_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    egg_shipment = models.ForeignKey('EggShipment', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Telur saiz {self.get_size_display()} dikutip pada {self.collection_date}'
    
    def get_size_display(self):
        return self.EGG_SIZE_CHOICES[self.size][1]

class EggShipment(models.Model):
    
    date_shipped = models.DateField()
    customer = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer} - {self.date_shipped} - {self.get_total_dozens()} dozens'
    
    def get_total_dozens(self):
         return Egg.objects.filter(egg_shipment=self).count() // 12
    
    def get_eggs_counts_by_size(self):
        egg_counts = {
            'small': self.egg_set.filter(size=0).count(),
            'medium': self.egg_set.filter(size=1).count(),
            'large': self.egg_set.filter(size=2).count(),
        }

        egg_descriptions = {
            'small': 'telur kecil',
            'medium': 'telur sederhana',
            'large': 'telur besar',
        }

        result = {}
        for size, count in egg_counts.items():
            if count > 0:
                result[size] = f"{count} {egg_descriptions[size]}"

        return result
    
    # get total sales for a shipment
    def get_total_sales(self):
        return self.egg_set.count() * 0.5
    
    

    
    
    
    


