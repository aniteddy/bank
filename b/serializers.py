from b.models import Clients, BankAccount, Transactions
from rest_framework import serializers


class ClientsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'


class BankAccountSerializer (serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class ClientBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'balance']


class ClientsAccountsSerializer(serializers.ModelSerializer):
    bank_accounts = serializers.SerializerMethodField()

    class Meta:
        model = Clients
        fields = ['client_id', 'name', 'bank_accounts']

    def get_bank_accounts(self, client: Clients):
        try:
            client_bank_account_query = Clients.objects.filter(client_id=client.client_id).values('bank_account')\
                .values_list('bank_account', flat=True).distinct()
            bank_account = BankAccount.objects.filter(id__in=client_bank_account_query).all()
            serializer = ClientBankAccountSerializer(bank_account, many=True)
            return serializer.data
        except BankAccount.DoesNotExist:
            return None


class TransactionsSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()

    class Meta:
        model = Transactions
        fields = ['created', 'type', 'amount', 'client', 'bank_account']

    def get_client(self, transaction: Transactions):
        client_id = transaction.client.client_id
        return client_id
