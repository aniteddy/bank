from django.urls import path
from rest_framework import permissions

from b.views import ClientsAPIView, BankAccountAPIView, ClientAPIView, BankAccountsAPIView, ClientAccountsAPIView, \
    TransactionsHistoryAPIView, CreateTransactionAPIView, ClientAccountsXMLAPIView, CreateDebitCreditTransactionAPIView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Bank API",
      default_version='V1',
      description="Bank API",
      terms_of_service="https://www.google.com/",
      contact=openapi.Contact(email="aniteddy1999@gmail.com"),
      license=openapi.License(name="Awesome IP"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('client/<int:clients_id>/', ClientAPIView.as_view()),
    path('client/', ClientAPIView.as_view()),
    path('clients/', ClientsAPIView.as_view()),
    path('bank_account/<int:bank_accounts_id>/', BankAccountAPIView.as_view()),
    path('bank_accounts/', BankAccountsAPIView.as_view()),
    path('client_accounts/', ClientAccountsAPIView.as_view()),
    path('history/', TransactionsHistoryAPIView.as_view()),
    path('create_transaction/', CreateTransactionAPIView.as_view()),
    path('clients_create_transaction/', CreateDebitCreditTransactionAPIView.as_view()),
    path('create_xml/', ClientAccountsXMLAPIView.as_view())
]
