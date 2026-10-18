from django.db import models

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}, {self.location}"

class employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(department, on_delete=models.CASCADE,blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subordinates')
    image=models.ImageField(upload_to='emp_images',default='default.png')
   

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def full_name(self):
        return f"{self.first_name} {self.last_name}"