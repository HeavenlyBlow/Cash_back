# -*- coding: utf-8 -*-

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
            print("Error in get_buffer")
            return False


    def del_buffer(self, chat_id):
        try:
            del self.buffer[chat_id]
        except:
            print("Error in del_buffer")


