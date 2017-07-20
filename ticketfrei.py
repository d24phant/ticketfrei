#!/usr/bin/env python

import pytoml as toml
import time
import traceback
import os
import datetime

from retootbot import RetootBot
from retweetbot import RetweetBot
from trigger import Trigger


if __name__ == '__main__':
    # read config in TOML format (https://github.com/toml-lang/toml#toml)
    with open('ticketfrei.cfg') as configfile:
        config = toml.load(configfile)

    trigger = Trigger(config)

    logpath = os.path.join("logs", "{%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now()))

    mbot = RetootBot(config, trigger, logpath=logpath)
    tbot = RetweetBot(trigger, config, logpath=logpath)

    try:
        statuses = []
        while True:
            statuses = mbot.retoot(statuses)
            statuses = tbot.flow(statuses)
            time.sleep(10)
    except:
        traceback.print_exc()
        tbot.shutdown()
