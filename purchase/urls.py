from django.urls import path

from purchase.api.controller import PurchaseCryptoView, UserWalletsView

urlpatterns = [
    path('purchase/', PurchaseCryptoView.as_view(), name='purchase-crypto'),
    path('wallets/<str:username>/', UserWalletsView.as_view(), name='user-wallets'),
]
