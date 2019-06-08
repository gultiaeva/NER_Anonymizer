from gensim.models import Word2Vec, KeyedVectors
import json
from processing.postprocessing import Predictor
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from joblib import load
import pickle


with open('processing/binaries/LGBMClassifier.pkl', 'rb') as f:
        classifier = pickle.load(f)

pred = Predictor(classifier)

def get_random_id():
    return random.getrandbits(31) * random.choice([-1, 1])


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id':get_random_id()})


# API-ключ созданный ранее
token = "5d1d08c4b4b739b6718b5a9a09aa71332ba4f687aa58321344f706b4351c2a470d3a9011ad64e312dad30"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print('Server started')
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            pred.provide_data(event.text)
            # Сообщение от пользователя
            response = pred.form_answer()

            write_msg(event.user_id, response)
                                       