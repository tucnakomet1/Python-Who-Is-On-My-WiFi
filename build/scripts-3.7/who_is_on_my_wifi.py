from scapy.all import *
from device import *
from who import *

import who_is_on_my_wifi
import urllib.request
import subprocess
import argparse
import textwrap
import platform
import inspect
import socket
import getmac
import os

if platform.system() == "Windows":
    import wmi

def contact():
	print("""
>>>> Contact <<<<
My Gmail: tucnakomet@gmail.com
My GitHub: https://github.com/tucnakomet1/
	""")

def license():
    lic_url = "https://raw.githubusercontent.com/tucnakomet1/Python-Who-Is-On-My-WiFi/master/LICENSE.txt"
    lic = urllib.request.urlopen(lic_url)
    lic = lic.read().decode("utf-8")
    print(lic)        

def help():
    PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDER, END = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[4m', '\033[0m'
    if platform.system() == "Linux":
        print(f"""
        
            {UNDER}>>>> Welcome to wiom help page!  What's wrong? <<<<{END}
                   
    --version | 1.3.0
    
    
    {UNDER}{BOLD}Usage:{END}
        {RED}>>> {YELLOW}import {CYAN}who_is_on_my_wifi{END}
        
        {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}help(){END} {BOLD}{RED}# show this help page{END}
        {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}contact(){END} {BOLD}{RED}# show contact{END}
        {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}license(){END} {BOLD}{RED}# show license{END}

        {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}who(n){END}  {BOLD}{RED}# see who is on my wifi (int('n') is scanning time - optional; default is 10){END}
        {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}device(){END} {BOLD}{RED}# see information about your device

        """)
    
    else:
        print(f"""
        
            >>>> Welcome to help page!  What's wrong? <<<<      

    --version | 1.3.0
      
    
    
    Usage:
        >>> import who_is_on_my_wifi
        
        >>> who_is_on_my_wifi.help() # show this help page
        >>> who_is_on_my_wifi.contact() # show contact
        >>> who_is_on_my_wifi.license() # show license
        
        >>> who_is_on_my_wifi.who(n) # see who is on my wifi (int('n') is scanning time - optional; default is 10)
        >>> who_is_on_my_wifi.device() # see information about your device
    
        """)



def main():
    wrapper = textwrap.TextWrapper(width=70)
    string = wrapper.fill(text = "Who-Is-On-My-WIFi")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=string, epilog=textwrap.dedent("""
                                        Thank you!
                                        ↓  ↓  ↓  ↓
                                        Visit my GitHub: https://github.com/tucnakomet1
                                        """))

    parser.add_argument(
        '-v', '--version',
        action='version', 
        version='%(prog)s 1.3.0', 
        help='show current version')

    parser.add_argument(
        '-l', '--license', 
        action='store_true', 
        help='show Open Source License')

    parser.add_argument(
        '-c', '--contact', 
        action='store_true', 
        help='show contact')

    parser.add_argument(
        '-d', '--device', 
        action="store_true", 
        help='show information about your device')

    parser.add_argument(
        '-w', '--who', 
        action="store_true",
        required=False,
        help='show who is on your WiFi!')
    
    parser.add_argument(
        "-t", "--time", 
        type=int,
        metavar="",
        required=False,
        default=10,
        help="int supplement for '-w' command (scanning '-t' seconds)")


    args = parser.parse_args()

    if args.device:
        dev = device()
        print(f"""
PC Name:            {dev[0]}
PC Product-Name:    {dev[1]}
MAC Address:        {dev[2]}
IP Address (host):  {dev[3]}
IP Address:         {dev[4]}
Public IP:          {dev[5]}
PC HostName:        {dev[6]}
WiFi Name:          {dev[7]}
Gateway:            {dev[8]}
DNS 1:              {dev[9]}
DNS 2:              {dev[10]}
Password:           {dev[11]}
Security:           {dev[12]}
Interface:          {dev[13]}
Frequency:          {dev[14]}
Signal:             {dev[15]}
Channel:            {dev[16]}


Country:            {dev[17]}
Region:             {dev[18]}
City:               {dev[19]}
Zip Code:           {dev[20]}
Latitude:           {dev[21]}
Longitude:          {dev[22]}
ISP:                {dev[23]}
""")

    if args.who:
        if args.time:
            WHO = who(args.time)
        else:
            WHO = who()
        
        for j in range(0, len(WHO)):
            comm = f"\n{WHO[j][0]} {WHO[j][1]}\n{WHO[j][2]} {WHO[j][3]}\n{WHO[j][4]} {WHO[j][5]}\n"
            print(comm)

    if args.contact:
        contact()

    if args.license:
        license()

if __name__ == "__main__":
    main()
