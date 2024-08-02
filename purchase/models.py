from django.db import models

# Create your models here.

from django.db import models

from users.models import User


class Wallet(models.Model):
    currency_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.currency_name}: {self.amount}"


class Transaction(models.Model):
    amount = models.IntegerField()
    source = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='outgoing_transactions')
    destination = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='incoming_transactions')

    def __str__(self):
        return f"Transaction: {self.amount} from {self.source} to {self.destination}"
