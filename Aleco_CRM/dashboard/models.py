from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

class Projects(models.Model):
    name = models.SlugField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=500)
    stage1 = models.BooleanField(default=False)
    stage1_date = models.DateField(null=True, blank=True)
    stage2 = models.BooleanField(default=False)
    stage2_date = models.DateField(null=True, blank=True)
    stage3 = models.BooleanField(default=False)
    stage3_date = models.DateField(null=True, blank=True)
    stage4 = models.BooleanField(default=False)
    stage4_date = models.DateField(null=True, blank=True)
    stage5 = models.BooleanField(default=False)
    stage5_date = models.DateField(null=True, blank=True)
    stage6 = models.BooleanField(default=False)
    stage6_date = models.DateField(null=True, blank=True)
    stage7 = models.BooleanField(default=False)
    stage7_date = models.DateField(null=True, blank=True)
    stage8 = models.BooleanField(default=False)
    stage8_date = models.DateField(null=True, blank=True)
    stage9 = models.BooleanField(default=False)
    stage9_date = models.DateField(null=True, blank=True)
    windows = models.IntegerField()
    address = models.CharField(max_length=200)
    order_date = models.DateField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate slug if this is a new object
            original_slug = slugify(self.name)
            slug = original_slug
            counter = 1

            while Projects.objects.filter(name=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.name = slug  # Assign the unique slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name
    

class Inventory(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name
    

class InventoryHistory(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    given_to = models.ForeignKey(Projects, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    date = models.DateField(auto_now_add=True)

    

class Progress(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    stage1_window = models.IntegerField(default=0)
    stage2_window = models.IntegerField(default=0)
    stage3_window = models.IntegerField(default=0)
    stage4_window = models.IntegerField(default=0)
    stage5_window = models.IntegerField(default=0)
    stage6_window = models.IntegerField(default=0)
    stage7_window = models.IntegerField(default=0)
    stage8_window = models.IntegerField(default=0)
    stage9_window = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.project.name}"
    

class MaintenanceMode(models.Model):
    maintenace_mode = models.BooleanField(default=False)


    
