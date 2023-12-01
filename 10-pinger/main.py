import os
import threading
from datetime import datetime
import time

from colorama import Fore, Back, Style

INTERVAL = 1
PING_COUNT = 4


def ping_thread(ip):
    response = os.popen(f"ping -c {PING_COUNT} {ip} ").read()
    outcome_percent, outcome_time = parse_result(response)
    if outcome_percent == 0:
        print(Fore.GREEN + f'{datetime.now().strftime("%H:%M:%S")} - {ip} => {outcome_percent}', end="")
    elif outcome_percent == 100:
        print(Fore.RED + f'{datetime.now().strftime("%H:%M:%S")} - {ip} => {outcome_percent}', end="")
    else:
        print(Fore.YELLOW + f'{datetime.now().strftime("%H:%M:%S")} - {ip} => {outcome_percent}', end="")
    print(Style.RESET_ALL)

def parse_result(result_string):
    '''
    Parses outcome of one "ping" command.
    Returns percentage value near "packet loss" or 100 if fails
    Returns time of response or 10000 if fails
    '''
    retval_percent = 100
    retval_time = 10000
    lines = result_string.splitlines()
    ### PERCENT ###
    for line in lines:
        if "packet loss" in line:
            parts = line.split(',')
            for part in parts:
                if 'packet loss' in part:
                    words = part.split(' ')
                    for word in words:
                        if '%' in word:
                            retval_percent = int(word[:-1])
    ### TIME ###
    for line in lines:
        if "ttl" in line:
            parts = line.split(' ')
            for part in parts:
                if 'time' in part:
                    retval_time = part[5:]

    return retval_percent, retval_time

class PingerClass(object):
    def __init__(self):
        pass
    def collect(self):
        with open("ip_list.txt") as file:
            self.park = file.read()
            self.park = self.park.splitlines()
        self.packet_loss = 0
        self.packet_loss_final = 0
        self.thread_list = []
        result = []
        for ip in self.park:
            ping_thread(ip)
            time.sleep(INTERVAL)


if __name__ == '__main__':
    print("All right, let's go!")
    pingu = PingerClass()
    while True: 
        pingu.collect()