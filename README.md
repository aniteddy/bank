Тестовое задание:

- Таблица клиентов (ID + наименование)
- Таблица со счетами клиентов (номер счета + остаток)
- Реализовать просмотр списка клиентов и его счетов.
- Реализовать простую проводку между счетами клиентов - просто дебет-кредит суммы с изменением остатка на счете.
- Реализовать выгрузку импорт-экспорт списка клиентов со счетами в XML. 
- Реализовать историю операций проводок по счетам клиентов язык Рython, БД MySQL.

Swagger 

http://localhost:8000/b/swagger/


API

Экспорт списка клиентов со счетами в XML

http://localhost:8000/b/export_xml/

Импорт списка клиентов со счетами в XML (добавляет или изменяет данные в БД)

http://localhost:8000/b/import_xml/

Пример проверки через postman:

![image](https://github.com/aniteddy/bank/assets/77286116/d09fe893-bcf4-4e32-9f1f-213df0f36c00)


Просмотр списка клиентов и его счетов

http://localhost:8000/b/client_accounts/

Список клиентов

http://localhost:8000/b/clients/

Проводка между счетами клиентов, дебет-кредит суммы с изменением остатка на счете

http://localhost:8000/b/clients_create_transaction/

Пример запроса через postman

{
    
    "debit_bank_account" : 1,
    
    "debit_client" : 2,
    
    "amount" : 333,
    
    "credit_bank_account" :  5,
    
    "credit_client" : 4
}

Проводка со счётом клиента

http://localhost:8000/b/create_transaction/

Пример запроса через postman

{

    "bank_account" : 3,
    
    "type" : "credit",
    
    "amount" : 20,
    
    "client" :  3
    
}

История операций проводок по счетам

http://localhost:8000/b/history/

Пример xml файла есть в проекте "09 December 2023 00 37 12.xml"

![image](https://github.com/aniteddy/bank/assets/77286116/64166361-b0dc-49f0-8a29-d75ff6a2c5bb)
