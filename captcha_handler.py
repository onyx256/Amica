import base64
import requests
from capmonster_python import ImageToTextTask


def captcha_handler(captcha):
    print('[AntiCaptcha] Разгадываю капчу...')

    resp = requests.get(captcha.get_url())

    img = resp.content

    img_encoded = base64.b64encode(img).decode('utf-8')

    with open('clientkey.txt', 'r', encoding='utf-8') as f:
        clientkey = f.read()

    capmonster = ImageToTextTask(client_key=clientkey)
    task_id = capmonster.create_task(base64_encoded_image=img_encoded)
    result = capmonster.join_task_result(task_id=task_id)

    return captcha.try_again(result)
