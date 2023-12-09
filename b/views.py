from datetime import datetime

from drf_yasg import openapi
from rest_framework.views import APIView
from b import utils
from b.models import Clients, BankAccount, Transactions
from b.serializers import ClientsSerializer, BankAccountSerializer, ClientsAccountsSerializer, TransactionsSerializer

from dicttoxml import dicttoxml
from drf_yasg.utils import swagger_auto_schema


from bs4 import BeautifulSoup


class ClientAPIView(APIView):

    @swagger_auto_schema(tags=['client'], operation_description='Получение клиента по id')
    def get(self, request, client_id):
        try:
            client: Clients = Clients.objects.get(client_id=client_id)
        except Clients.DoesNotExist:
            return utils.generic_404_response()
        serializer = ClientsSerializer(client)
        return utils.generic_successful_response(serializer.data)

    client_id = openapi.Parameter('client_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                  description='id клиента', required=True)
    name = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                             description='имя клиента', required=True)
    bank_account = openapi.Parameter('bank_account', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                     description='id банковского счета', required=True)

    @swagger_auto_schema(tags=['client'], manual_parameters=[client_id, name],
                         operation_description='Создание клиента по имени и уже созданному банковскому счёту')
    def post(self, request, **kwargs):
        serializer = ClientsSerializer(data=request.data)
        if serializer.is_valid():
            client_id = request.data['client_id']
            name = request.data['name']
            bank_account = BankAccount.objects.get(account_number=request.data['bank_account'])
            created_client: Clients = Clients.objects.create(client_id=client_id, name=name, bank_account=bank_account)
            return utils.generic_successful_response(serializer.data)
        else:
            first_error_key = next(iter(serializer.errors.keys()))
            return utils.generic_400_response(serializer.errors,
                                              client_message=f"<{first_error_key}> : <{str(serializer.errors[first_error_key][0])}>")

    @swagger_auto_schema(tags=['client'], operation_description='Удаление клиентов из БД по id ')
    def delete(self, client_id):
        try:
            client: Clients = Clients.objects.get(id=client_id)
        except Clients.DoesNotExist:
            return utils.generic_404_response()
        client.delete()
        return utils.generic_successful_response()


class ClientsAPIView(APIView):

    @swagger_auto_schema(tags=['clients'],
                         operation_description='Список клиентов')
    def get(self, request, **kwargs):
        clients: Clients = Clients.objects.all()
        serializer = ClientsSerializer(clients, many=True)
        return utils.generic_successful_response(serializer.data)


class BankAccountsAPIView(APIView):

    @swagger_auto_schema(tags=['bank_accounts'],
                         operation_description='Список банковских счетов')
    def get(self, request, **kwargs):
        bank_accounts: BankAccount = BankAccount.objects.all()
        serializer = BankAccountSerializer(bank_accounts, many=True)
        return utils.generic_successful_response(serializer.data)


class BankAccountAPIView(APIView):

    @swagger_auto_schema(tags=['bank_account'], operation_description='Получение банковского счёта по id')
    def get(self, request, bank_account_id):
        try:
            bank_account: BankAccount = BankAccount.objects.get(id=bank_account_id)
        except BankAccount.DoesNotExist:
            return utils.generic_404_response()
        serializer = BankAccountSerializer(bank_account)
        return utils.generic_successful_response(serializer.data)

    balance = openapi.Parameter('balance', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                description='баланс', required=True)

    @swagger_auto_schema(tags=['bank_account'], manual_parameters=[balance],
                         operation_description='Изменение баланса банковского счёта по id')
    def put(self, request, bank_account_id):
        try:
            bank_account: BankAccount = BankAccount.objects.get(id=bank_account_id)
        except BankAccount.DoesNotExist:
            return utils.generic_404_response()
        changed_values_message = list()
        if 'balance' in request.data:
            bank_account.balance = request.data['balance']
            changed_values_message.append(f"Name: {bank_account.balance}")
        if len(changed_values_message) > 0:
            bank_account.save()
            return utils.generic_200_response()
        else:
            return utils.generic_400_response("Cannot perform this request")


class ClientAccountsAPIView(APIView):

    @swagger_auto_schema(tags=['client_accounts'],
                         operation_description='Список клиентов и его счетов')
    def get(self, request):
        client = []
        value_list = Clients.objects.values_list('client_id', flat=True).distinct()
        for v in value_list:
            client.append(Clients.objects.filter(client_id=v).first())
        serializer = ClientsAccountsSerializer(client, many=True)
        return utils.generic_successful_response(serializer.data)


class TransactionsHistoryAPIView(APIView):

    @swagger_auto_schema(tags=['transactions'],
                         operation_description='История операций проводок по счетам')
    def get(self, request):
        transactions: Transactions = Transactions.objects.all()
        serializer = TransactionsSerializer(transactions, many=True)
        return utils.generic_successful_response(serializer.data)


class CreateTransactionAPIView(APIView):
    bank_account = openapi.Parameter('bank_account', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                     description='id банковского счёта', required=True)
    type = openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                             description='debit or credit', required=True)
    amount = openapi.Parameter('amount', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                               description='остаток', required=True)
    client = openapi.Parameter('client', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                     description='id клиента, корому принадлежит счёт', required=True)

    @swagger_auto_schema(tags=['transactions'],
                         operation_description='Create transaction, проводка со счётом клиента',
                         manual_parameters=[bank_account, type, amount, client])
    def post(self, request, **kwargs):
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            bank_account = BankAccount.objects.get(account_number=request.data['bank_account'])
            type = request.data['type']
            amount = request.data['amount']
            try:
                client = Clients.objects.get(bank_account_id=bank_account.id, client_id=request.data['client'])
            except Clients.DoesNotExist:
                return utils.generic_404_response("Client does not exist")
            created_transactions: Transactions = Transactions.objects.create(bank_account=bank_account,
                                                                             client=client, type=type, amount=amount)
            serializer = TransactionsSerializer(created_transactions)
            # изменение баланса счёта
            if type == 'debit':
                bank_account.balance = bank_account.balance + amount
                bank_account.save()
            elif type == 'credit':
                bank_account.balance = bank_account.balance - amount
                bank_account.save()
            return utils.generic_successful_response(serializer.data)
        else:
            first_error_key = next(iter(serializer.errors.keys()))
            return utils.generic_400_response(serializer.errors,
                                              client_message=f"<{first_error_key}> : <{str(serializer.errors[first_error_key][0])}>")


# Прибавляет остаток к первому дебет счёту, и вычитает из второго кредит счёта
class CreateDebitCreditTransactionAPIView(APIView):
    debit_bank_account = openapi.Parameter('debit_bank_account', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                           description="id банковского счёта пополнения", required=True)
    debit_client = openapi.Parameter('debit_client', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                     description='id клиента, корому принадлежит счёт для пополнения', required=True)
    amount = openapi.Parameter('amount', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                               description='остаток', required=True)
    credit_bank_account = openapi.Parameter('credit_bank_account', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                            description='id банковского счёта списания', required=True)
    credit_client = openapi.Parameter('credit_client', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                                      description='id клиента, корому принадлежит счёт для списания', required=True)

    @swagger_auto_schema(tags=['transactions'], description='Create transaction, проводка со счётами клиента',
                         manual_parameters=[debit_bank_account, debit_client, amount, credit_bank_account,
                                            credit_client])
    def post(self, request, **kwargs):
        debit_bank_account = BankAccount.objects.get(account_number=request.data['debit_bank_account'])
        credit_bank_account = BankAccount.objects.get(account_number=request.data['credit_bank_account'])
        amount = request.data['amount']
        try:
            debit_client = Clients.objects.get(bank_account_id=debit_bank_account.id,
                                               client_id=request.data['debit_client'])
            credit_client = Clients.objects.get(bank_account_id=credit_bank_account.id,
                                                client_id=request.data['credit_client'])
        except Clients.DoesNotExist:
            return utils.generic_404_response("Client does not exist")
        debit_created_transactions: Transactions = Transactions.objects.create(bank_account=debit_bank_account,
                                                                               client=debit_client, type='debit',
                                                                               amount=amount)
        credit_created_transactions: Transactions = Transactions.objects.create(bank_account=credit_bank_account,
                                                                                client=credit_client, type='credit',
                                                                                amount=amount)
        # изменение баланса счёта
        debit_bank_account.balance = debit_bank_account.balance + amount
        debit_bank_account.save()

        credit_bank_account.balance = credit_bank_account.balance - amount
        credit_bank_account.save()
        return utils.generic_successful_response("OK")


class ExportClientAccountsXMLAPIView(APIView):

    @swagger_auto_schema(tags=['xml'],
                         operation_description='Экспорт в xml файл информации о клиентах и их счетах')
    def get(self, request):
        client = []
        value_list = Clients.objects.values_list('client_id', flat=True).distinct()
        for v in value_list:
            client.append(Clients.objects.filter(client_id=v).first())
        serializer = ClientsAccountsSerializer(client, many=True)

        result = []
        for c in serializer.data:
            bank_accounts = []
            for ba in c['bank_accounts']:
                bank_accounts.append({'account_number': ba['account_number'], 'balance': ba['balance']})
            result.append({'client': {'client_id': c['client_id'], 'name': c['name'], 'bank_accounts': bank_accounts}})

        xml_string = dicttoxml(result, attr_type=False).decode()
        # xml_string = dicttoxml(serializer.data, attr_type=False).decode()
        xml_file = open(datetime.now().strftime("%d %B %Y %H %M %S") + '.xml', 'w')
        xml_file.write(str(xml_string))
        xml_file.close()

        return utils.generic_successful_response(serializer.data)


class ImportClientAccountsXMLAPIView(APIView):
    file = openapi.Parameter('file', openapi.IN_QUERY, type=openapi.TYPE_FILE,
                             description="xml файл", required=True)

    @swagger_auto_schema(tags=['xml'],
                         operation_description='Импорт xml файла с информацией о клиентах и их счетах')
    def post(self, request):
        selected_file = request.FILES['file']
        xml_file = open(selected_file.name, 'r')
        text_from_xml_file = xml_file.read()

        bs_data = BeautifulSoup(text_from_xml_file, 'xml')
        bs_data_clients = bs_data.find_all('client')

        client = []
        for c in bs_data_clients:
            bank_accounts = []
            client_bank_accounts = c.find_all('item')
            for cba in client_bank_accounts:
                bank_accounts.append({'account_number': cba.find('account_number').text,
                                      'balance': cba.find('balance').text})
            client.append({'client_id': c.find('client_id').text, 'name': c.find('name').text,
                           'bank_accounts': bank_accounts})

        for cl in client:
            if cl['client_id'] is not None and cl['name'] is not None:
                for ba in cl['bank_accounts']:
                    if ba['account_number'] is not None and ba['balance'] is not None:
                        find_bank_account, find_client = None, None
                        try:
                            # проверка существует ли такой банковский аккаунт
                            find_bank_account: BankAccount = BankAccount.objects.get(account_number=int(ba['account_number']))
                            if int(ba['balance']) != find_bank_account.balance:
                                find_bank_account.balance = int(ba['balance'])
                                find_bank_account.save(())
                        except BankAccount.DoesNotExist:
                            find_bank_account: BankAccount = BankAccount.objects.create(balance=int(ba['balance']),
                                                                                        account_number=int(ba['account_number']))
                        try:
                            # есть клиент с таким id  и банковским аккаунтом
                            find_client: Clients = Clients.objects.get(client_id=int(cl['client_id']),
                                                                       bank_account__account_number=find_bank_account.account_number)
                            # если имя не совпадает, поменять
                            if cl['name'] != find_client.name:
                                find_client.name = cl['name']
                                find_client.save()
                        except Clients.DoesNotExist:
                            # клиента с таким id и банковским номером не существует
                            find_client: Clients = Clients.objects.create(client_id=int(cl['client_id']),
                                                                          bank_account=find_bank_account, name=cl['name'])

        return utils.generic_successful_response('OK')