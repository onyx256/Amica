import time

import vk_api
from functions import Functions
from error_handler import error_handler
from captcha_handler import captcha_handler


class Account(object):
    def __init__(self, login=None, password=None):
        self.vk = None
        self.login = login
        self.password = password
        self.captcha_handler = captcha_handler

    @error_handler
    def auth(self):
        vk_session = vk_api.VkApi(login=self.login, password=self.password, captcha_handler=self.captcha_handler)
        vk_session.auth()

        self.vk = vk_session.get_api()

        return self.vk

    def print_info(self):
        profile_info = self.vk.account.getProfileInfo()

        print(f'Информация об аккаунте ({profile_info["id"]})\n'
              f'- {profile_info["first_name"]} {profile_info["last_name"]}\n\n')


def main():
    _max = 3  # Кол-во авторизаций
    _cancel_requests = 3  # Отменять исходящие заявки в друзья каждые N авторизаций
    _sleep = 3600  # КД между авторизациями

    for i in range(_max):
        print(f'[Авторизация №{i+1}/{_max}]\n')

        with open('account.txt', 'r', encoding='utf-8') as f:
            acc = f.readlines()[0].split(':')

        login = acc[0]
        password = acc[1]

        account = Account(login=login, password=password)

        account.auth()
        account.print_info()

        functions = Functions(account)

        if i+1 % _cancel_requests == 0:
            functions.close_friend_requests()

        functions.send_friend_requests(100)

        print('Ожидание...')

        time.sleep(_sleep)


if __name__ == '__main__':
    main()
