from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address
import re

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0) 

contract = w3.eth.contract(address=contract_address, abi=abi) 

def login():    
    try:
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

def is_strong_password(password):
    if len(password) < 12:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*()-+=]', password):
        return False
    
    return True

def register(): 
    while True:
        print("Условия для пароля: \n 1 - Минимум 12 символов\n 2 - Минимум 1 Заглавная буква\n 3 - Минимум 1 Строчная буква\n 4 - Минимум 1 цифра\n 5 - Минимум 1 спец.символ\n")
        password = input("Новый пароль: ")
        if is_strong_password(password):
            break
        else:
            print("Пароль слишком плохой. Убедитесь, что он содержит минимум 12 символов, включая заглавные и строчные буквы, цифры и специальные символы.")
    account = w3.geth.personal.new_account(password)
    print(f"Публичный ключ: {account}")

def send_eth(account):
    try:
        value = int(input("Введите количество эфира для отправки: "))
        tx_hash = contract.functions.toPay(account).transact({
            "from": account,
            "value": value,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка отправки эфира: {e}")

def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({
            'from': account
        })
        print(f"Ваш баланс на смарт-контракта: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса: {e}")

def withdraw(account):
    try:
        amount = int(input("Введите количество эфира для вывода: "))
        tx_hash = contract.functions.withdraw(amount).transact({
            'from': account,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка снятия средств: {e}")

def create_estate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        address = input("Введите адрес недвижимости: ")
        es_type = int(input("Выберите тип недвижимости (0 - Дом, 1 - Квартира, 2 - Комната): "))
        tx_hash = contract.functions.createEstate(size, address, es_type).transact({
            'from': account
        })
        print(f"Транзакция {tx_hash.hex()} отправлена для создания недвижимости")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_ad(account):
    try:
        id_estate = int(input("Введите ID недвижимости, для которой создается объявление: "))
        price = int(input("Введите цену продажи: "))
        tx_hash = contract.functions.createAd(id_estate, price).transact({
            'from': account
        })
        print(f"Транзакция {tx_hash.hex()} отправлена для создания объявления")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")

def update_estate_status(account):
    try:
        id_estate = int(input("Введите ID недвижимости, для которой нужно изменить статус: "))
        new_status = int(input("Выберите новый статус (0 - Неактивен, 1 - Активен): "))
        tx_hash = contract.functions.updateEstateStatus(id_estate, bool(new_status)).transact({
            'from': account
        })
        print(f"Транзакция {tx_hash.hex()} отправлена для изменения статуса недвижимости")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка изменения статуса недвижимости: {e}")

def update_ad_status(account):
    try:
        id_ad = int(input("Введите ID объявления, для которого нужно изменить статус: "))
        new_status = int(input("Выберите новый статус (0 - Закрыто, 1 - Открыто): "))
        tx_hash = contract.functions.updateAdStatus(id_ad, new_status).transact({
            'from': account
        })
        print(f"Транзакция {tx_hash.hex()} отправлена для изменения статуса объявления")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка изменения статуса объявления: {e}")

def get_estates_info():
    try:
        estates = contract.functions.getEstates().call()
        print("Информация о недвижимости:")
        for estate in estates:
            print(f"ID: {estate[5]}, Размер: {estate[0]}, Адрес: {estate[1]}, Владелец: {estate[2]}, Тип: {estate[3]}, Статус: {'Активен' if estate[4] else 'Неактивен'}")
    except Exception as e:
        print(f"Ошибка получения информации о недвижимостях: {e}")

def get_ads_info():
    try:
        ads = contract.functions.getAds().call()
        print("Текущие объявления о продаже недвижимости:")
        for ad in ads:
            print(f"ID: {ad[6]}, Владелец: {ad[0]}, Цена: {ad[2]}, Недвижимость: {ad[3]}, Дата/время: {ad[4]}, Статус: {'Открыто' if ad[5] else 'Закрыто'}")
    except Exception as e:
        print(f"Ошибка получения информации о текущих объявлениях: {e}")

def buy_estate(account):
    try:
        id_ad = int(input("Введите ID объявления, чтобы купить недвижимость: "))
        tx_hash = contract.functions.buyEstate(id_ad).transact({
            'from': account,
            'value': 0 
        })
        print(f"Транзакция {tx_hash.hex()} отправлена для покупки недвижимости")
    except ValueError:
        print("Ошибка: неверное значение")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")

def main():
    account = ""
    while True:
        if account == "" or account is None: 
            choice = int(input("Выберите: \n1 - Авторизация \n2 - Регистрация \n3 - Выход\nНомер операции: "))
            match choice:
                case 1:
                    account = login()
                case 2: 
                    register()
                case 3:
                    print("Успешный выход!")
                    exit()
                case _:
                    print("Выберите от 1 до 3")
        else:
            choice = int(input("Выберите: \n1 - Отправить wei \n2 - Баланс смарт-контракта \n3 - Баланс аккаунта \n4 - Снять средства \n5 - Создание недвижимости \n6 - Создание объявления \n7 - Изменения статуса недвижимости \n8 - Изменения статуса объявления \n9 - Покупка недвижимости \n10 - Информация о недвижимостях \n11 - Информация о объявлениях \n12 - Выход\nНомер операции: "))
            match choice:
                case 1:
                    send_eth(account)
                case 2:
                    get_balance(account)
                case 3:
                    print(f"Баланс аккауната: {w3.eth.get_balance(account)}")
                case 4:
                    withdraw(account)
                case 5:
                    create_estate(account)
                case 6:
                    create_ad(account)
                case 7:
                    update_estate_status(account)
                case 8:
                    update_ad_status(account)
                case 9:
                    buy_estate(account)
                case 10:
                    get_estates_info()
                case 11:
                    get_ads_info()
                case 12: 
                    print("Успешный выход из аккаунта!")
                    account = ""
                case _:
                    print("Выберите от 1 до 12")

if __name__ == "__main__":
    main()
