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

if platform.system() == "Windows":
    import wmi

def contact():
	print("""
>>>> Contact <<<<
My Gmail: tucnakomet@gmail.com
My GitHub: https://github.com/tucnakomet1/
	""")


def license():
    pth = os.path.dirname(inspect.getfile(who_is_on_my_wifi))
    pth = pth+"/who_is_on_my_wifi-1.2.0.dist-info/"
    with open(pth+"LICENSE.txt", "r") as lic:
        SeeLicense = lic.read()
        os.system("clear")
        print(SeeLicense)

def who():
    plat = platform.system()
    if plat == "Linux":
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

    if plat == "Windows":
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
    
    if plat == "Darwin":
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
    plat = platform.system()
    if plat == "Linux":
        try:
            try:
                nam = subprocess.Popen("sudo dmidecode -s system-manufacturer", shell=True, stdout=subprocess.PIPE)
                nam = nam.stdout.readline()
                nam = nam.decode("utf-8").split()[0]
            except:
                nam = subprocess.Popen("cat /sys/devices/virtual/dmi/id/sys_vendor", shell=True, stdout=subprocess.PIPE)
                nam = nam.stdout.readline()
                nam = nam.decode("utf-8").split()[0]
        except:
            nam = "unknown"
        
        try:
            try:
                product_name = subprocess.Popen("sudo dmidecode -s baseboard-product-name", shell=True, stdout=subprocess.PIPE)
                product_name = product_name.stdout.readline()
                product_name = product_name.decode("utf-8").split()[0]
            except:
                product_name = subprocess.Popen("cat /sys/devices/virtual/dmi/id/product_name", shell=True, stdout=subprocess.PIPE)
                product_name = product_name.stdout.readline()
                product_name = product_name.decode("utf-8").split()[0]
        except:
            product_name = "unknown"
            

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

        try:
            WifiName = subprocess.Popen("iwgetid -r", shell=True, stdout=subprocess.PIPE)
            WifiName = WifiName.stdout.readline()
            WifiName = WifiName.decode("utf-8").split()
            if WifiName == []:
                os.system("sudo service network-manager restart")
                WifiName = subprocess.Popen("iwgetid -r", shell=True, stdout=subprocess.PIPE)
                WifiName = WifiName.stdout.readline()
                WifiName = WifiName.decode("utf-8").split()[0]
            else:
                WifiName = WifiName[0]
        except:
            WifiName = "unknown"
        
        try:
            DNS = subprocess.Popen("nmcli | grep servers", shell=True, stdout=subprocess.PIPE)
            DNS = DNS.stdout.readline()
            DNS = DNS.decode("utf-8")
            DNS = DNS.replace("\t", "")
            DNS = DNS.replace("\n", "")
            DNS = DNS.split()

            DNS1 = DNS[1]
            DNS2 = DNS[2]
        except:
            DNS1 = "unknown"
            DNS2 = "unknown"
        
        try:
            Gateway = subprocess.Popen("grep 0 /etc/resolv.conf", shell=True, stdout=subprocess.PIPE)
            Gateway = Gateway.stdout.readline()
            Gateway = Gateway.decode("utf-8").split()[1]
        except:
            Gateway = "unknown"

        try:
            SSID = WifiName
            if SSID == "unknown":
                password = "unknown"
            else:
                ShowProcess3 = subprocess.Popen(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", SSID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                password, erra = ShowProcess3.communicate()
                password = password.decode("utf-8").split()[0]
        except:
            password = "unknown"
    
        DeviceList = [nam, product_name, MAC, IP_host, IP_All, hostname, WifiName, Gateway, DNS1, DNS2, password]
    
    elif plat == "Windows":
        c = wmi.WMI()
        system = c.Win32_ComputerSystem()[0]
        sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
        out = c.query( sql )

        nam = system.Manufacturer
        product_name = system.Model
        MAC = getmac.get_mac_address()
        IP_host = socket.gethostbyname('localhost')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        IP_All = sock.getsockname()[0]

        hostname = socket.gethostname()

        try:
            resu = subprocess.check_output(["netsh", "wlan", "show", "network"])
            resu = resu.decode("ascii")
            resu = resu.replace("\r", "")
            ls = resu.split("\n")
            ls = ls[4:]
            ls = ls[0]
            ls = ls.split(": ")

            ssids = []

            if ls == [""]:
                ssids.append("unknown")

            else:
                if len(ls) >= 3:
                    ssid = ": ".join(ls[1:len(ls)])
                    ssids.append(ssid)
                else:
                    ssid = "".join(ls[1])
                    ssids.append(ssid)

            WifiName = "".join(ssids)
        except:
            WifiName = "unknown"
        
        
        try:
            SSID = WifiName
            if SSID == "unknown":
                password = "unknown"
            else:
                comm = f"netsh wlan show profile {SSID} key=clear | findstr Key"
                ShowProcess2 = subprocess.Popen(comm, stdout=subprocess.PIPE, stderr=None, shell=True)
                res2, erra2 = ShowProcess2.communicate()
                res2 = res2.decode()
                
                res2 = res2.replace("Key", "").replace("Content", "").replace(":", "").replace(" ", "")
                if res2 == "":
                    password = "unknown"
                else:
                    password = res2.replace("\r", "").replace("\n", "")
        except:
            password = "unknown"
        
        
        try:
            comma = 'nslookup localhost | findstr "Address:"'
            processx = subprocess.Popen(comma, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outx, err = processx.communicate()
            outx = outx.decode("utf-8").split()
            DNS1 = outx[1]
        except:
            DNS1 = "unknown"
            
            
        try:
            DNSbytes = DNS1.encode()
            process = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            out = out.split()
            indx = [g for g, rs in enumerate(out) if rs== DNSbytes]
            DNS2 = out[indx[0]+1]
            DNS2 = DNS2.decode()
        except:
            DNS2 = "unknown"
        
        try:
            scripton = 'ipconfig -all | findstr "DHCP" | findstr "Server"'
            process2 = subprocess.Popen(scripton, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out2, err2 = process2.communicate()

            out2 = out2.decode().replace("   DHCP Server", "").replace(" .", "").replace(" : ", "").replace("\r\n", "")
            Gateway = out2
        except:
            Gateway = "unknown"


        DeviceList = [nam, product_name, MAC, IP_host, IP_All, hostname, WifiName, Gateway, DNS1, DNS2, password]

    if plat == "Darwin":
        try:
            nam = subprocess.Popen("system_profiler SPHardwareDataType | grep 'Model Name:' | awk '{print $3}'", shell=True, stdout=subprocess.PIPE)
            nam = nam.stdout.readline()
            nam = nam.decode("utf-8").split()[0]
        except:
            nam = "unknown"

        try:
            product_name = subprocess.Popen("system_profiler SPHardwareDataType | grep 'Model Identifier:' | awk '{print $3}'", shell=True, stdout=subprocess.PIPE)
            product_name = product_name.stdout.readline()
            product_name = product_name.decode("utf-8").split()[0]
        except:
            product_name = "unknown"

        MAC = getmac.get_mac_address()

        try:
            IP_host = subprocess.Popen("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
            IP_host = IP_host.stdout.readline()
            IP_host = IP_host.decode("utf-8").split()[0]
        except:
            IP_host = "unknown"

        try:
            IP_All = subprocess.Popen("ipconfig getifaddr en0", shell=True, stdout=subprocess.PIPE)
            IP_All = IP_All.stdout.readline()
            IP_All = IP_All.decode("utf-8").split()[0]
        except:
                IP_All = "unknown"

        hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
        hostname = hostname.stdout.readline()
        hostname = hostname.decode("utf-8").split()[0]

        try:
            WifiName = subprocess.Popen("/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -I  | awk -F' SSID: '  '/ SSID: / {print $2}'", shell=True, stdout=subprocess.PIPE)
            WifiName = WifiName.stdout.readline()
            WifiName = WifiName.decode("utf-8").split()[0]
        except:
            WifiName = "unknown"
            
        try:
            DNS1 = subprocess.Popen("scutil --dns | grep nameserver | awk '{print $3}'", shell=True, stdout=subprocess.PIPE)
            DNS1 = DNS1.stdout.readline()
            DNS1 = DNS1.decode("utf-8").split()[0]
        except:
            DNS1 = "unknown"

        try:
            DNS2 = subprocess.Popen("nslookup google.com | grep 'Server:' | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
            DNS2 = DNS2.stdout.readline()
            DNS2 = DNS2.decode("utf-8").split()[0]
                
        except:
            DNS2 = "unknown"
            
        try:
            Gateway = subprocess.Popen("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
            Gateway = Gateway.stdout.readline()
            Gateway = Gateway.decode("utf-8").split()[0]
        except:
            Gateway = "unknown"

        try:
            SSID = WifiName
            if SSID == "unknown":
                password = "unknown"
            else:
                password = subprocess.Popen(f"security find-generic-password -ga {SSID} | grep 'password:'", shell=True, stdout=subprocess.PIPE)
                password = password.stdout.readline()
                password = password.decode("utf-8").split()[0]
        except:
            password = "unknown"
        
        if IP_host == DNS2 or Gateway == DNS2:
            DNS2 = "8.8.8.8"
        else:
            pass
    
        DeviceList = [nam, product_name, MAC, IP_host, IP_All, hostname, WifiName, Gateway, DNS1, DNS2, password]
    return DeviceList

    

def help():
    PURPLE, CYAN, DARKCYAN, BLUE, GREEN, YELLOW, RED, BOLD, UNDER, END = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[4m', '\033[0m'
    if platform.system() == "Linux":
        print(f"""
        
            {UNDER}>>>> Welcome to help page!  What's wrong? <<<<{END}
            
            
    --version | 1.2.0.

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
    
    else:
        print(f"""
        
            >>>> Welcome to help page!  What's wrong? <<<<
            

    --version | 1.2.0.
    
    
    About:
        Who-Is-On-My-WIFi module help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are currently connected.
    
    
    
    
    
    Usage:
        >>> import who_is_on_my_wifi
        
        #### show this help page ####
        >>> who_is_on_my_wifi.help()
        
        #### show contact ####
        >>> who_is_on_my_wifi.contact()
        
        #### show license ####
        >>> who_is_on_my_wifi.license()
        
        
        #### see who is on my wifi ####
        >>> who_is_on_my_wifi.who()
        
        #### see information about your device ####
        >>> who_is_on_my_wifi.device()
    
    
    
    
    
    CONTACT:
        My Gmail: tucnakomet@gmail.com
        My GitHub: https://github.com/tucnakomet1/
        who_is_on_my_wifi.contact()
        
        
        
        
        
    License:
        MIT License		
        You can see → who_is_on_my_wifi.license()
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
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.2.0', help='show current version')
    parser.add_argument('-c', '--contact', action='store_true', help='show contact')
    parser.add_argument('-d', '--device', action="store_true", help='show information about your device')
    parser.add_argument('-w', '--who', action="store_true", help='show who is on your WiFi?!')

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
Password:           {dev[10]}
""")



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
    main()
