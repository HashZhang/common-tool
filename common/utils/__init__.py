import logging

logger = logging.getLogger(__name__)
import time
import threading
import redis


class IdGenerator:
    def __init__(self, biz_name, redis_host, redis_port, redis_password, redis_db):
        self._biz_name = biz_name
        self._last_timestamp = time.time()
        self._instance_id = self.__get_current_instance_id(biz_name=biz_name, redis_host=redis_host,
                                                           redis_port=redis_port, redis_password=redis_password,
                                                           redis_db=redis_db)
        self._value_lock = threading.Lock()
        self._incr = 0

    def __get_current_instance_id(self, biz_name, redis_host, redis_port, redis_password, redis_db):
        client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
        key = 'IdGenerator:' + biz_name
        value = client.incr(key)
        client.expire(key, 3600)
        return value

    def uuid(self, name):
        if name is None or len(name) > 4 or len(name.strip()) < 1:
            raise Exception('name must be not empty and the length should be less than 4')
        with self._value_lock:
            timestamp = time.time()
            if timestamp < self._last_timestamp:
                logger.error("Time moved backforward. current: %d, last: %d", timestamp, self._last_timestamp)
                timestamp = self._last_timestamp
            self._incr += 1
            return "%s%s%d%08d" % (time.strftime("%Y%m%d%H%M%S", time.localtime(int(timestamp))), name, self._instance_id, self._incr % 100000000)

