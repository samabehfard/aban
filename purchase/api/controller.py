from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from purchase.api.serializers import PurchaseSerializer, WalletSerializer
from purchase.errors import UserNotFoundError, InsufficientBalanceError, CryptoNotFoundError
from purchase.logic import PurchaseLogic
from purchase.models import Wallet
from users.models import User


class PurchaseCryptoView(APIView):
    def post(self, request):
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            currency_name = serializer.validated_data['currency_name']
            count = serializer.validated_data['count']

            purchase_logic = PurchaseLogic()

            try:
                purchase_logic.purchase(username=username, currency_name=currency_name, count=count)
                return Response({"message": "Purchase successful"}, status=status.HTTP_200_OK)
            except UserNotFoundError:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except InsufficientBalanceError:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            except CryptoNotFoundError:
                return Response({"error": "Cryptocurrency not found"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserWalletsView(APIView):
    def get(self, request, username):
        # Check if the user exists
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all wallets for the user
        wallets = Wallet.objects.filter(user=user)

        # Serialize the wallet data
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
