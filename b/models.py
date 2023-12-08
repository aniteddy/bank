from django.db import models

TRANSACTIONS_TYPE = (
    ('debit', 'debit'),
    ('credit', 'debit')
)


class BankAccount(models.Model):
    account_number = models.IntegerField('account_number', blank=False, null=False)
    balance = models.IntegerField('balance', blank=False, null=False)


class Clients(models.Model):
    client_id = models.IntegerField('client_id', blank=False, null=False)
    name = models.CharField('name', max_length=250, blank=False, null=False)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='clients', blank=False,
                                     null=False)


class Transactions(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TRANSACTIONS_TYPE, default="debit",
                            blank=False, null=False)
    amount = models.IntegerField('amount', blank=False, null=False)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='transactions',
                               blank=False, null=False)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                                     related_name='transactions', blank=False, null=False)
