import sys
import vk_api


def error_handler(func):

    def wrapper(*args, **kwargs):
        _exit = False

        try:
            func(*args, **kwargs)

        except vk_api.LoginRequired:
            print('Для авторизации необходим логин')
            _exit = True

        except vk_api.PasswordRequired:
            print('Для авторизации необходим пароль')
            _exit = True

        except vk_api.BadPassword:
            print('Неверный пароль')
            _exit = True

        except vk_api.AccessDenied:
            print('Доступ запрещён')
            _exit = True

        except vk_api.AccountBlocked:
            print('Аккаунт заблокирован')
            _exit = True

        except vk_api.TwoFactorError:
            print('Ошибка двухфакторной авторизации')
            _exit = True

        except vk_api.SecurityCheck:
            print('Необходима проверка безопасности')
            _exit = True

        except vk_api.exceptions.ApiError as e:
            print(f'Ошибка API, {e}')

        except Exception as e:
            print(e)

        finally:
            if _exit:
                input()
                sys.exit()

    return wrapper
