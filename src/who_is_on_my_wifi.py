import who_is_on_my_wifi
import subprocess
import argparse
import textwrap
import platform
import inspect
import socket
import getmac
import nmap
import os

def contact():
	print("""
>>>> Contact <<<<
My Gmail: tucnakomet@gmail.com
My GitHub: https://github.com/tucnakomet1/
	""")


def license():
    pth = os.path.dirname(inspect.getfile(who_is_on_my_wifi))
    pth = pth+"/who_is_on_my_wifi-1.0.3.dist-info/"
    with open(pth+"LICENSE.txt", "r") as lic:
        SeeLicense = lic.read()
        os.system("clear")
        print(SeeLicense)

def SeeConnect(num):
    num = int(num)+1
    dev = device()
    BASIC_IP = list(dev[4])
    BASIC_IP.pop()
    BASIC_IP = "".join(BASIC_IP)
    listOFip = []
    Conn = 0
    NotConn = 0

    for i in range(1, num):
        ADDRESS = BASIC_IP + str(i)
        CountProcess = subprocess.call(["ping", "-c", "1", ADDRESS], stdout=subprocess.PIPE)

        ShowProcess = subprocess.Popen(["ping", "-c", "1", ADDRESS], stdout=subprocess.PIPE)
        line = ShowProcess.stdout.readline()
        con = line.decode("utf-8").split()[1]

        if CountProcess == 0 or CountProcess == 2:
            Conn += 1
            listOFip.append(["IP Address:", f"{con}", "is currently", "connected"])
        elif CountProcess == 1:
            NotConn += 1
            subprocess.Popen.kill(ShowProcess)
            listOFip.append(["IP Address:", f"{con}", "is currently", "not connected"])
        else:
            listOFip.append("Something went wrong! Please try it again.")
    listOFip.insert(0, [f"Not connected devices: {NotConn}"])
    listOFip.insert(0, [f"Connected devices: {Conn}"])

    return listOFip


def who():
    if os.getuid() == 1000:
        print("Please run this command as sudo! (for better result)")
    else:
        pass

    WhoList = []
    dev = device()
    MyIP = dev[4]
    MyMac = dev[2]
    name = dev[0]
    product_name = dev[1]

    nm = nmap.PortScanner()
    host = MyIP + "/24"
    dictList = nm.scan(hosts=host, arguments='-sn')
    scan = dictList.get("scan")

    YourDeviceList = ["IP Address:", MyIP, "Mac Address:", MyMac, "Device:", f"{name} {product_name} (Your device)"]
    
    for IP in scan:
        vendor = scan[IP]
        vendor = vendor.get("vendor")
        for MAC in vendor:
            WhoList.append(["IP Address:", IP, "Mac Address:", MAC, "Device:", vendor[MAC]])

    WhoList.append(YourDeviceList)

    return WhoList
        

def device():
    nam = subprocess.Popen("cat /sys/devices/virtual/dmi/id/sys_vendor", shell=True, stdout=subprocess.PIPE)
    nam = nam.stdout.readline()
    nam = nam.decode("utf-8").split()[0]

    product_name = subprocess.Popen("cat /sys/devices/virtual/dmi/id/product_name", shell=True, stdout=subprocess.PIPE)
    product_name = product_name.stdout.readline()
    product_name = product_name.decode("utf-8").split()[0]

    MAC = getmac.get_mac_address()

    IP_host = subprocess.Popen("hostname -i", shell=True, stdout=subprocess.PIPE)
    IP_host = IP_host.stdout.readline()
    IP_host = IP_host.decode("utf-8").split()[0]

    IP_All = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE)
    IP_All = IP_All.stdout.readline()
    IP_All = IP_All.decode("utf-8").split()[0]

    hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
    hostname = hostname.stdout.readline()
    hostname = hostname.decode("utf-8").split()[0]

    WifiName = subprocess.Popen("sudo iw dev wlan0 info | grep ssid | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
    WifiName = WifiName.stdout.readline()
    WifiName = WifiName.decode("utf-8").split()[0]

    DNS1 = subprocess.Popen("grep 'nameserver' /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
    DNS1 = DNS1.stdout.readline()
    DNS1 = DNS1.decode("utf-8").split()[1]

    DNS2 = subprocess.Popen("nmcli device show eth0 | grep IP4.DNS | grep -v 1", shell=True, stdout=subprocess.PIPE)
    DNSTRY = DNS2.stdout.readline()
    DNSTRY = DNSTRY.decode("utf-8").split()
    if DNSTRY == []:
        DNS2 = subprocess.Popen("nmcli device show wlan0 | grep IP4.DNS | grep -v 1", shell=True, stdout=subprocess.PIPE)
    else:
        DNS2 = DNSTRY
    DNS2 = DNS2.stdout.readline()
    DNS2 = DNS2.decode("utf-8").split()[1]

    Gateway = subprocess.Popen("grep 0 /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
    Gateway = Gateway.stdout.readline()
    Gateway = Gateway.decode("utf-8").split()[1]
 
    DeviceList = [nam, product_name, MAC, IP_host, IP_All, hostname, WifiName, Gateway, DNS1, DNS2]
    return DeviceList

def help():
    PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDER, END = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[4m', '\033[0m'
    print(f"""
    

		{UNDER}>>>> Welcome to help page!  What's wrong? <<<<{END}

--version | 1.0.3.


{UNDER}{BOLD}About:{END}

    Who-Is-On-My-WIFi module help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are currently connected.




{UNDER}{BOLD}Usage:{END}

    {RED}>>> {YELLOW}import {CYAN}who_is_on_my_wifi{END}

    {BOLD}{RED}#### show this help page ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}help(){END}


    {BOLD}{RED}#### show contact ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}contact(){END}


    {BOLD}{RED}#### show license ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}license(){END}


    {BOLD}{RED}#### see connected devices ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}SeeConnect({END}number{GREEN}){END} {YELLOW}#int number (0 - 255) of searching devices (smaller = faster searching){END}

    {BOLD}{RED}#### see who is on my wifi ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}who(){END}

    {BOLD}{RED}#### see information about your device ####{END}
    {RED}>>> {CYAN}who_is_on_my_wifi{END}.{GREEN}device(){END}





{UNDER}{BOLD}CONTACT:{END}

    {UNDER}My Gmail:{END} tucnakomet@gmail.com
    {UNDER}My GitHub:{END} https://github.com/tucnakomet1/

    {CYAN}who_is_on_my_wifi{END}.{GREEN}contact(){END}





{UNDER}{BOLD}License:{END}


    MIT License		
    {UNDER}You can see{END} → {CYAN}who_is_on_my_wifi{END}.{GREEN}license(){RED}{END}
                → https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi/blob/master/LICENSE.txt









    """)

def main():
    wrapper = textwrap.TextWrapper(width=70)
    string = wrapper.fill(text = "Who-Is-On-My-WIFi module help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are currently connected.")
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=string, epilog=textwrap.dedent("""

                                        Thank you!
                                        ↓  ↓  ↓  ↓
                                        Visit my GitHub: https://github.com/tucnakomet1
                                        """))
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.3', help='show current version')
    parser.add_argument('-C', '--contact', action='store_true', help='show contact')
    parser.add_argument('-d', '--device', action="store_true", help='show information about your device')
    parser.add_argument('-w', '--who', action="store_true", help='show who is on your WiFI?!')
    parser.add_argument('-c', '--connect', metavar="", help='show how many devices are currently connected')

    args = parser.parse_args()

    if args.device:
        dev = device()
        print(f"""
PC Name:            {dev[0]}
PC Product-Name:    {dev[1]}
MAC Address:        {dev[2]}
IP Address (host):  {dev[3]}
IP Address:         {dev[4]}
PC HostName:        {dev[5]}
WiFi Name:          {dev[6]}
Gateway:            {dev[7]}
DNS 1:              {dev[8]}
DNS 2:              {dev[9]}
""")

    if args.connect:
        conn = SeeConnect(args.connect)
        print(f"\n{''.join(conn[0])}\n{''.join(conn[1])}\n")
        for k in range(2,len(conn)):
            commandConn = f"{' '.join(conn[k])}"
            
            print(commandConn)

    if args.who:
        WHO = who()
        for j in range(0, len(WHO)):
            comm = f"\n{WHO[j][0:2]}\n{WHO[j][2:4]}\n{WHO[j][4:6]}\n"
            comm = comm.replace("[", "")
            comm = comm.replace("]", "")
            comm = comm.replace("'", "")
            comm = comm.replace(",", " ")
            print(comm)
    

    if args.contact:
        contact()

if __name__ == "__main__":
    plat = platform.system()
    if plat == "Linux":
        pass
    else:
        print(f"Your Operating System ({plat}) is not supported!\nThis module may not work properly for you!\nPlease wait for Version 1.1.0.\nFor more information: https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi#update")
    main()
    

