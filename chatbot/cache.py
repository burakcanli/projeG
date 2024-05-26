import time

class Cache:
    def __init__(self, expiration_time=3600):
        self.expiration_time = expiration_time
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['time'] < self.expiration_time:
                return entry['value']
            else:
                del self.cache[key]
        return None

    def set(self, key, value):
        self.cache[key] = {'value': value, 'time': time.time()}
