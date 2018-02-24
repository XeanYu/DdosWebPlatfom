__author__ = 'XeanYu'
from user_agents import parse

def is_device(agent):
    device = parse(agent)
    return device.device.family

def user_msg(agent):
    msg = parse(agent)
    if msg.is_pc:
        return 'PC'

    if msg.is_tablet:
        return 'Pad'

    if msg.is_mobile:
        return 'MObile'

    else:
        return 'Unknow'


