# -*- coding: utf-8 -*-

import logging
import datetime

class logs:
    def __init__(self):
        self.loggs = logging
        self.loggs.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                            filename=u'logs.log')



    def info_logs(self, message):
        self.loggs.info(message)

    def error_logs(self, message):
        self.loggs.error(message)



