from scapy.all import *
from device import *
from who import *

import subprocess
import argparse
import textwrap
import platform
import inspect
import socket
import sys
import os

if platform.system() == "Windows": import wmi

# contact links

def contact():
    print("\n-- Gmail: <tucnakomet@gmail.com> \n-- GitHub: <https://github.com/tucnakomet1/>\n")


# license link

def license():
    print("""\nWho-Is-On-My-WiFi is under MIT open-source license...
    -- See: <https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi/blob/master/LICENSE.txt>\n""")


# run device
def device_():
    dev = device()
	
    dvc = f"""
PC Name:            {dev[0]} \nPC Product-Name:    {dev[1]}
MAC Address:        {dev[2]} \nIP Address (host):  {dev[3]}
IP Address:         {dev[4]} \nPublic IP:          {dev[5]}
PC HostName:        {dev[6]} \nWiFi Name:          {dev[7]}
Gateway:            {dev[8]} \nDNS 1:              {dev[9]}
DNS 2:              {dev[10]} \nPassword:           {dev[11]}
Security:           {dev[12]} \nInterface:          {dev[13]}
Frequency:          {dev[14]} \nSignal:             {dev[15]}
Channel:            {dev[16]} \n\n
Country:            {dev[17]} \nRegion:             {dev[18]}
City:               {dev[19]} \nZip Code:           {dev[20]}
Latitude:           {dev[21]} \nLongitude:          {dev[22]}
Map:                {dev[23]} \nISP:                {dev[24]}
	"""
    print(dvc)

########
# help #
########

def help():
    if platform.system() == "Linux":
        PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDER, END = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[4m', '\033[0m'
    else:
        PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDER, END = '', '', '', '', '', '', '', '', '', ''

    print(f""" 
who-is-on-my-wifi 1.3.4
    
{UNDER}{BOLD}Usage:{END}
    {RED}>>> {YELLOW}import {CYAN}who_is_on_my_wifi{END} as wiom
        
    {RED}>>> {CYAN}wiom{END}.{GREEN}help(){END} {BOLD}{RED}    # show this help page{END}
    {RED}>>> {CYAN}wiom{END}.{GREEN}contact(){END} {BOLD}{RED} # show contact{END}
    {RED}>>> {CYAN}wiom{END}.{GREEN}license(){END} {BOLD}{RED} # show license{END}

    {RED}>>> {CYAN}wiom{END}.{GREEN}who(n){END}  {BOLD}{RED}   # scan wifi (n : optional integer, means scanning time in seconds; default 10){END}
    {RED}>>> {CYAN}wiom{END}.{GREEN}device(){END} {BOLD}{RED}  # see information about your device{END}
    """)


# main function --> argparse

def main():
    wrapper = textwrap.TextWrapper(width=70)
    string = wrapper.fill(text="Who-Is-On-My-WIFi")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=string,
                                     epilog=textwrap.dedent("""GitHub: <https://github.com/tucnakomet1>\n"""))

    parser.add_argument('-v', '--version', action='version',
                        version='who_is_on_my_wifi 1.3.5', help='show current version')

    parser.add_argument('-l', '--license', action='store_true',
                        help='show Open Source License')

    parser.add_argument('-c', '--contact', action='store_true',
                        help='show contact')

    parser.add_argument('-d', '--device', action="store_true",
                        help='show information about your device')

    parser.add_argument('-w', '--who', action="store_true",
                        required=False, help='show who is on your WiFi!')

    parser.add_argument("-t", "--time", type=int,
                        metavar="", required=False,
                        default=10, help="int supplement for '-w' command (scanning '-t' seconds)")

    args = parser.parse_args()

    if args.contact: contact()
    elif args.license: license()
    elif args.device: device_()
    elif args.who:
        WHO = who(args.time)
        for j in range(0, len(WHO)):
            print(f"\n{WHO[j][0]} {WHO[j][1]}\n{WHO[j][2]} {WHO[j][3]}\n{WHO[j][4]} {WHO[j][5]}\n")


    elif len(sys.argv) == 1:
        parser.print_help()
    else: parser.print_help()

if __name__ == "__main__":
    main()
