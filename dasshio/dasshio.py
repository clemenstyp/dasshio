#!/usr/bin/env python3

import json
import logging
import os
import requests
from scapy.all import sniff
from scapy.all import ARP
import sys
import time


def arp_display(pkt):
    mac = pkt[ARP].hwsrc.lower()
    if mac in [button['address'].lower() for button in config['buttons']]:
        idx = [button['address'].lower() for button in config['buttons']].index(mac)
        button = config['buttons'][idx]

        logging.info(button['name'] + " button pressed!")
        logging.info("Request: " + button['url'])
        
        try:
            if 'body' in button.keys():
                request = requests.post(button['url'], json=json.loads(button['body']), headers=json.loads(button['headers']))
            else:
                request = requests.get(button['url'], headers=json.loads(button['headers']))
            logging.info('Status Code: {}'.format(request.status_code))
            
            if request.status_code == requests.codes.ok:
                logging.info("Successful request")
                time.sleep(5) # Wait 5 seconds to let dash button disconnect from wifi before scanning again
            else:
                logging.error("Bad request")
        except:
            logging.exception("Unable to perform  request: Check url, body and headers format. Check API password")


# Create basepath
path = os.path.dirname(os.path.realpath(__file__))

# Log events to stdout
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stdoutHandler.setFormatter(formater)

logger.addHandler(stdoutHandler)


# Read config file
logging.info("Reading config file: /data/options.json")

with open(path + '/data/options.json', mode='r') as data_file:
    config = json.load(data_file)

# Start sniffing
logging.info("Starting sniffing...")
sniff(prn=arp_display, filter='arp', store=0, count=0)
