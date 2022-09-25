import time
import vk_api
from error_handler import error_handler


class Functions(object):
    def __init__(self, account):
        self.vk = account.vk

    def send_friend_requests(self, count=100):
        if count > 1000:
            count = 1000

        users = self.vk.users.search(count=count, can_access_closed=True, fields=['is_friend', 'blacklisted'])['items']

        print(f'Загружен список из {count} пользователей\n\n')

        for i in range(len(users)):
            print(f'[{i + 1} ({users[i]["id"]})]\n'
                  f'{users[i]["first_name"]} {users[i]["last_name"]}')

            if users[i]['is_friend']:
                print('- Пользователь находится в списке друзей\n\n')
                continue

            if users[i]['blacklisted']:
                print('- Пользователь находится в чёрном списке\n\n')
                continue

            self._send_friend_request(self.vk, users[i]['id'])

            print('- Заявка отправлена\n\n')

            time.sleep(0)

        return True

    def close_friend_requests(self):
        requests = self.vk.friends.getRequests(count=1000, out=1)['items']

        print(f'Кол-во исходящих заявок: {len(requests)}\n\n')

        for i in range(len(requests)):
            print(f'[{i + 1}]')

            self._close_friend_request(self.vk, user_id=requests[i])

            time.sleep(0)

    @staticmethod
    @error_handler
    def _send_friend_request(vk, user_id: int) -> bool:
        vk.friends.add(user_id=user_id)

        return True

    @staticmethod
    @error_handler
    def _close_friend_request(vk, user_id: int) -> bool:
        vk.friends.delete(user_id=user_id)

        return True
