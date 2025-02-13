import redis
import ujson


class BaseStorage:
    """
    Абстрактный класс хранилища.
    Чтобы создать своё хранилище (использующее например бд или файл) нужно имплементировать все методы
    """
    def get_user_data(self, user_id):
        pass

    def set_user_data(self, user_id, data):
        pass

    def update_user_data(self, user_id, key, value):
        pass

    def get_user_state(self, user_id):
        pass

    def set_user_state(self, user_id, state):
        pass


class RedisStorage(BaseStorage):
    def __init__(self, redis_url, redis_port, db):
        self.redis_instance = redis.Redis(redis_url, redis_port, db=db)

    def get_user_data(self, user_id):
        if data := self.redis_instance.get(f'{user_id}_data'):
            return ujson.loads(data)
        else:
            self.redis_instance.set(str(user_id), '{}')
            return {}

    def set_user_data(self, user_id, data):
        return self.redis_instance.set(f'{user_id}_data', ujson.dumps(data))

    def update_user_data(self, user_id, key, value):
        data = self.get_user_data(user_id)
        data[key] = value
        return self.set_user_data(user_id, data)

    def set_user_state(self, user_id, state=''):
        return self.redis_instance.set(f'{user_id}_state', state)

    def get_user_state(self, user_id):
        res = self.redis_instance.get(f'{user_id}_state')
        if res:
            return res.decode('utf-8')
