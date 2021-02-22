from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Customer(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 14 digits "
                                         "allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.phone) + '  ' + str(self.name)


class Order(models.Model):
    trans_id = models.CharField(null=False, max_length=40)
    item = models.CharField(null=False, max_length=40)
    quantity = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_transaction = models.DateTimeField(auto_now_add=True, blank=False,null=True)

    def __str__(self):
        return str(self.trans_id)
