# -*- coding: utf-8 -*-
from Log import logs
import sys

logs = logs()

class Buffer:
    def __init__(self):
        self.buffer = {}

    def set_buffer(self, chat_id, object):
        self.buffer[chat_id] = object
        return True

    def get_buffer(self, chat_id):
        try:
            return self.buffer.get(chat_id)
        except:
            logs.error_logs("Ошибка в get_buffer")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))
            return False


    def del_buffer(self, chat_id):
        try:
            del self.buffer[chat_id]
        except:
            logs.error_logs("Ошибка в del_buffer")
            e = sys.exc_info()[1]
            logs.error_logs(str(e))


