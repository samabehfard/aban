from rest_framework import serializers

from purchase.logic.purchase_logic import CRYPTO_CURRENCIES
from purchase.models import Wallet


class PurchaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    currency_name = serializers.CharField(max_length=10)
    count = serializers.IntegerField(min_value=1)

    def validate_currency_name(self, value):
        if value not in CRYPTO_CURRENCIES:
            raise serializers.ValidationError("Unsupported cryptocurrency.")
        return value


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['currency_name', 'amount']
