from django.db import models

from users.models import User


class Wallet(models.Model):
    currency_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallets')

    @property
    def amount(self):
        return Transaction.objects.filter(source=self).aggregate(s=models.Sum("amount")).get("s") or 0

    def __str__(self):
        return f"{self.user.username} - {self.currency_name}: {self.amount}"

    @classmethod
    def get_for(cls, user, currency_name):
        return cls.objects.get_or_create(user=user, currency_name=currency_name)[0]


class Transaction(models.Model):
    amount = models.IntegerField()
    source = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='outgoing_transactions')

    def __str__(self):
        return f"Transaction: {self.amount} from {self.source}"
