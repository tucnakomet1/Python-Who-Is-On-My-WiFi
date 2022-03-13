from scapy.all import *
<<<<<<< HEAD
=======
from urllib import *
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

import urllib.request
import subprocess
import platform
<<<<<<< HEAD
import socket
import getmac
import re

if platform.system() == "Windows": import wmi


def check_ipv(out):
    ipv4 = "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ipv6 = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:" \
           "[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:" \
           "[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}" \
           "(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:" \
           ")|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}" \
           "[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]" \
           "|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"

    x = re.search(ipv4, out)
    y = re.search(ipv6, out)

    if x and y: out = out.replace(" ", ", ")
    return out


def get_output(command, url=False, i=0):
    ipv_warn = "hostname -I"
    check = False

    if command == ipv_warn: check = True

    try:
        if url:
            inp = urllib.request.urlopen(command)
            out = inp.read().decode("utf-8").split()
            return out[i]
        else:
            inp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = inp.stdout.readlines()
            out = out[i].decode("utf-8").replace("\n", "")

            if out == "" or out == []: return "unknown"
            if check: return check_ipv(out)

            return out
    except:
        return "unknown"


def get_new_wifi_name(wifi_nm):
    part1 = get_output("sudo nmcli -s -g 802-11-wireless-security.psk | grep 'to' | awk '{print $4}'")
    part2 = get_output("sudo nmcli -s -g 802-11-wireless-security.psk | grep 'to' | awk '{print $5}'")
    new_wifi = part1 + " " + part2

    return new_wifi


def get_pass(wifi_password, WifiName):
    if WifiName == "unknown":
        return "unknown"
    else:
        password = get_output(wifi_password + WifiName)

        if password == "unknown":
            return get_output(wifi_password + f"'{get_new_wifi_name(WifiName)}'")
        return password


def calculate_signal_strength():
    try:
        word_strength = "unknown"
        signal = int(get_output("iwconfig | grep level | awk '{print $4}'").replace("level=", ""))

        if -30 <= signal:
            word_strength = "super strong"
        elif (-30 > signal) and (-50 <= signal):
            word_strength = "excellent signal"
        elif (-50 > signal) and (-67 <= signal):
            word_strength = "good signal"
        elif (-67 > signal) and (-70 <= signal):
            word_strength = "reliable signal"
        elif (-70 > signal) and (-80 <= signal):
            word_strength = "not strong signal"
        elif (-80 > signal) and (-90 <= signal):
            word_strength = "unreliable signal"
        elif signal < -90:
            word_strength = "super weak signal"

        return f"{signal} DBm, {word_strength}"
    except:
        return "unknown"


def get_route(public_IP):
    try:
        response = urllib.request.urlopen(f"https://ip-api.io/json/{public_IP}")
        return response.read().decode("utf-8").replace(',', '":').split('":')
    except:
        return "unknown"


def get_route_arg(route, index):
    if route != "unknown":
        return route[index].replace('"', '')
    else:
        return "unknwon"


def device():
    plat = platform.system()

    public_IP = get_output("https://icanhazip.com", True)
    if public_IP == "unknown": public_IP = get_output("ifconfig.me")

    route = get_route(public_IP)
    country = get_route_arg(route, 5)
    regionN = get_route_arg(route, 9)
    city = get_route_arg(route, 13)
    zipC = get_route_arg(route, 15)
    lat = get_route_arg(route, 19)
    lon = get_route_arg(route, 21)
    maps = f"https://www.google.com/maps/@{lat},{lon},14z"
    org = get_route_arg(route, 25)

    if plat == "Linux":
        nam = get_output("sudo dmidecode -s system-manufacturer")
        product_name = get_output("sudo dmidecode -s baseboard-product-name")
        MAC = getmac.get_mac_address()
        IP_host = get_output("hostname -i")
        IP_All = get_output("hostname -I")
        hostname = get_output("hostname")
        WifiName = get_output("iwgetid -r")
        Gateway = get_output("ip route | grep default | awk '{print $3}'")
        DNS1 = get_output("nmcli dev show | grep DNS | awk '{print $2}'")
        DNS2 = get_output("nmcli dev show | grep DNS | awk '{print $2}'", False, 1)
        password = get_pass("nmcli -s -g 802-11-wireless-security.psk connection show ", WifiName)
        security = get_output("sudo wpa_cli status | grep 'key_mgmt'").replace("key_mgmt=", "")
        interface = get_output("route | grep default | awk '{print $8}'")
        frequency = (get_output("iwgetid -f | awk '{print $2}'") + " GHz").replace("Frequency:", "")
        signal_strength = calculate_signal_strength()
        channel = get_output("iwgetid -c | awk '{print $2}'").replace("Channel:", "")

        if nam == "unknown": nam = get_output("cat /sys/devices/virtual/dmi/id/sys_vendor")
        if product_name == "unknown": product_name = get_output("cat /sys/devices/virtual/dmi/id/product_name")

        return [nam, product_name, MAC, IP_host, IP_All, public_IP, hostname, WifiName,
                      Gateway, DNS1, DNS2, password, security, interface, frequency, signal_strength,
                      channel, country, regionN, city, zipC, lat, lon, maps, org]

    # ========================= #
    #          WINDOWS          #
    # ========================= #
    # not tested
=======
import inspect
import socket
import getmac
import os

if platform.system()== "Windows":
    import wmi

# ========================= #
#          LINUX            #
# ========================= #

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
                product_name = product_name.decode("utf-8").split()
                product_name = " ".join(product_name)
            except:
                product_name = subprocess.Popen("cat /sys/devices/virtual/dmi/id/product_name", shell=True, stdout=subprocess.PIPE)
                product_name = product_name.stdout.readline()
                product_name = product_name.decode("utf-8").split()[0]
        except:
            product_name = "unknown"
            
        try:
            MAC = getmac.get_mac_address()
        except:
            MAC = "unknown"

        try:
            IP_host = subprocess.Popen("hostname -i", shell=True, stdout=subprocess.PIPE)
            IP_host = IP_host.stdout.readline()
            IP_host = IP_host.decode("utf-8").split()[0]
        except:
            IP_host = "unknown"
        try:
            IP_All = subprocess.Popen("hostname -I", shell=True, stdout=subprocess.PIPE)
            IP_All = IP_All.stdout.readline()
            IP_All = IP_All.decode("utf-8").split()[0]
        except:
            IP_All = "unknown"

        try:
            public_IP = urllib.request.urlopen("https://icanhazip.com")
            public_IP = public_IP.read().decode("utf-8").split()
            public_IP = public_IP[len(public_IP)-1]
        except:
            try:
                public_IP = os.popen('curl -s ifconfig.me')
                public_IP = public_IP.read()
            except:
                public_IP = "unknown"
        
        try:
            hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
            hostname = hostname.stdout.readline()
            hostname = hostname.decode("utf-8").split()[0]
        except:
            hostname = "unknown"

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
            Gateway = subprocess.Popen("ip route | grep default | awk '{print $3}'", shell=True, stdout=subprocess.PIPE)
            Gateway = Gateway.stdout.readline()
            Gateway = Gateway.decode("utf-8").split()[0]
        except:
            Gateway = "unknown"

        try:
            DNSs = os.popen("nmcli dev show | grep DNS | awk '{print $2}'")
            DNSs = DNSs.read().split("\n")
            num = 0
            for res in DNSs:
                if res == "":
                    pass
                else:
                    num += 1
                    if num == 1:
                        DNS1 = res
                    elif num == 2:
                        DNS2 = res
        except:
            DNS1 = "unknown"
            DNS2 = "unknown"

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
        
        try:
            secur_stat = subprocess.Popen("sudo wpa_cli status | grep 'key_mgmt'", shell=True, stdout=subprocess.PIPE)
            secur_stat = secur_stat.stdout.readline()
            secur_stat = secur_stat.decode("utf-8").split()

            security = secur_stat[len(secur_stat)-1].replace("key_mgmt=", "")
        except:
            security = "unknown"

        try:
            route = os.popen("route")
            inter = route.read().split()
            default_index = inter.index("default") + 7
            interface = inter[default_index]

        except:
            interface = "unknown"

        try:
            chan_procc = subprocess.check_output(["iwlist", interface, "channel"])
            chan_procc = chan_procc.decode("utf-8").split()
            wholeList = []

            for xyz in range(len(chan_procc)):
                res_chan = xyz
                res_chan = chan_procc[res_chan]
                wholeList.append(res_chan)

            channel = wholeList[len(wholeList)-1].replace(")", "")
        except:
            channel = "unknown"

        try:
            iwconfig = subprocess.check_output("iwconfig", stderr=subprocess.STDOUT)
            iwconfig = iwconfig.decode("utf-8").split()

            for po in range(len(iwconfig)):
                if ("Frequency" in iwconfig[po]) :
                    freq_res = po
                    freq_res = iwconfig[freq_res].replace("Frequency:", "")
                    GHz = po + 1
                    GHz = iwconfig[GHz]

                else:
                    pass
            frequency =  freq_res + " " + GHz
        except:
            frequency = "unknown"

        try:
            config2 = subprocess.check_output("iwconfig", stderr=subprocess.STDOUT)
            config2 = config2.decode("utf-8").split()

            maximum = 0
            result_now = 0
            dbm = 0

            for mom in range(len(config2)):
                if ("level" in config2[mom]) :
                    result_now = mom
                    result_now = config2[result_now].replace("level=", "")
                    dbm = mom + 1
                    dbm = config2[dbm]

                else:
                    pass

            proc = 100+(int(maximum) + int(result_now))

            if proc >= 75:
                word_strengh = "super strong"
            if proc < 75 and proc >= 50:
                word_strengh = "strong"
            if proc < 50 and proc >= 25:
                word_strengh = "weak"
            if proc < 25:
                word_strengh = "super weak"


            signal = result_now + " " + dbm
            procenta = str(proc) + " %"

            signal_strenght = signal + " (" +  procenta + ") - " + word_strengh
        except:
            signal_strenght = "unknown"

        try:
            response = urllib.request.urlopen(f"https://ip-api.io/json/{public_IP}")
            route = response.read().decode("utf-8").replace(',', '":').split('":')
        except:
            route = "unknown"
        try: 
            country = route[5].replace('"', '')
        except:
            country = "unknown"
        try:
            regionN =route[9].replace('"', '')
        except:
            regionN = "unknown"
        try:
            city = route[13].replace('"', '')
        except:
            city = "unknown"
        try:  
            zipC = route[15].replace('"', '')
        except:
            zipC = "unknown"
        try:    
            lat = route[19]
        except:
            lat = "unknown"
        try:    
            lon = route[21]
        except:
            lon = "unknown"
        try:    
            org = route[25].replace('"', '')
        except:
            org = "unknown"

        DeviceList = [nam, product_name, MAC, IP_host, IP_All, public_IP, hostname, WifiName, Gateway, DNS1, DNS2, password, security, interface, frequency, signal_strenght, channel, country, regionN, city, zipC , lat, lon, org]


# ========================= #
#          WINDOWS          #
# ========================= #

>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

    elif plat == "Windows":
        c = wmi.WMI()
        system = c.Win32_ComputerSystem()[0]
        sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
<<<<<<< HEAD
        c.query(sql)

        def get_ip_all():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]

        def get_wifi_name():
            try:
                resu = subprocess.check_output(["netsh", "wlan", "show", "network"])
                resu = (resu.decode("ascii")).replace("\r", "").split("\n")
                ls = resu[4:]
                ls = ls[0].split(": ")

                ssids = []

                if ls == [""]:
                    ssids.append("unknown")
                else:
                    if len(ls) >= 3:
                        ssids.append(": ".join(ls[1:len(ls)]))
                    else:
                        ssids.append("".join(ls[1]))

                return "".join(ssids)
            except:
                return "unknown"
=======
        out = c.query( sql )
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

        nam = system.Manufacturer
        product_name = system.Model
        MAC = getmac.get_mac_address()
        IP_host = socket.gethostbyname('localhost')
<<<<<<< HEAD
        IP_All = get_ip_all()
        hostname = socket.gethostname()
        WifiName = get_wifi_name()
=======

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        IP_All = sock.getsockname()[0]

        try:
            public_IP = urllib.request.urlopen("https://icanhazip.com")
            public_IP = public_IP.read().decode("utf-8").split()
            public_IP = public_IP[len(public_IP)-1]
        except:
            public_IP = "unknown"

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
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

        try:
            comma = 'nslookup localhost | findstr "Address:"'
            processx = subprocess.Popen(comma, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outx, err = processx.communicate()
            outx = outx.decode("utf-8").split()
            DNS1 = outx[1]
        except:
            DNS1 = "unknown"
<<<<<<< HEAD

=======
        
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
        try:
            DNSbytes = DNS1.encode()
            process = subprocess.Popen(['ipconfig', '/all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            out = out.split()
<<<<<<< HEAD
            indx = [g for g, rs in enumerate(out) if rs == DNSbytes]
            DNS2 = out[indx[0] + 1]
=======
            indx = [g for g, rs in enumerate(out) if rs== DNSbytes]
            DNS2 = out[indx[0]+1]
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
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
<<<<<<< HEAD

=======
        
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
        try:
            SSID = WifiName
            if SSID == "unknown":
                password = "unknown"
            else:
                comm = f"netsh wlan show profile {SSID} key=clear | findstr Key"
                ShowProcess2 = subprocess.Popen(comm, stdout=subprocess.PIPE, stderr=None, shell=True)
                res2, erra2 = ShowProcess2.communicate()
                res2 = res2.decode()
<<<<<<< HEAD

=======
                
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
                res2 = res2.replace("Key", "").replace("Content", "").replace(":", "").replace(" ", "")
                if res2 == "":
                    password = "unknown"
                else:
                    password = res2.replace("\r", "").replace("\n", "")
        except:
            password = "unknown"
<<<<<<< HEAD

        try:
            secur_stat = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            secur_stat = secur_stat.decode("utf-8").split()
            secur_index = secur_stat.index("Authentication")

=======
        
        try:
            secur_stat = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            secur_stat = secur_stat.decode("utf-8").split()
            
            secur_index = secur_stat.index("Authentication")
            
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
            security = secur_stat[secur_index + 2]
        except:
            security = "unknown"

        try:
            chan_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            chan_procc = chan_procc.decode("utf-8").split()
<<<<<<< HEAD
            chan_index = chan_procc.index("Channel")

            channel = chan_procc[chan_index + 2]
=======
            
            chan_index = chan_procc.index("Channel")
            
            channel = secur_stat[chan_index + 2]
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
        except:
            channel = "unknown"

        try:
            freq_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            freq_procc = freq_procc.decode("utf-8").split()
<<<<<<< HEAD
            freq_index = freq_procc.index("Radio")
=======

            freq_index = freq_procc.index("Radio")
            
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
            freq = freq_procc[freq_index + 3]

            if freq == "802.11a":
                frequency = "5 GHz"
            elif freq == "802.11b":
                frequency = "2.4 GHz"
            elif freq == "802.11g":
                frequency = "2.4 GHz"
            elif freq == "802.11n":
                frequency = "2.4 GHz / 5 GHz"
            elif freq == "802.11c":
                frequency = "5 GHz"
            else:
                frequency = "unknown"
        except:
            frequency = "unknown"

        try:
            sign_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            sign_procc = sign_procc.decode("utf-8").split()
<<<<<<< HEAD
            sign_index = sign_procc.index("Signal")

=======

            sign_index = sign_procc.index("Signal")
            
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
            procenta = sign_procc[sign_index + 2]

            proc = list(procenta)
            proc.pop()
            proc = int("".join(proc))

            if proc >= 75:
<<<<<<< HEAD
                word_strength = "super strong"
            elif proc < 75 and proc >= 50:
                word_strength = "strong"
            elif proc < 50 and proc >= 25:
                word_strength = "weak"
            else:
                word_strength = "super weak"

            signal_strength = f"{proc} % - {word_strength}"
        except:
            signal_strength = "unknown"
=======
                word_strengh = "super strong"
            if proc < 75 and proc >= 50:
                word_strengh = "strong"
            if proc < 50 and proc >= 25:
                word_strengh = "weak"
            if proc < 25:
                word_strengh = "super weak"

            signal_strenght = procenta + " - " + word_strengh
        except:
            signal_strenght = "unknown"
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac

        try:
            inter_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            inter_procc = inter_procc.decode("utf-8").split()
<<<<<<< HEAD
=======

>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
            inter_index = inter_procc.index("Name")

            interface = inter_procc[inter_index + 2]
        except:
            interface = "unknown"

<<<<<<< HEAD
        return [nam, product_name, MAC, IP_host, IP_All, public_IP, hostname,
                      WifiName, Gateway, DNS1, DNS2, password, security, interface,
                      frequency, signal_strength, channel, country, regionN, city,
                      zipC, lat, lon, maps, org]

    # ========================= #
    #          DARWIN           #
    # ========================= #
    # not tested

    if plat == "Darwin":
        nam = get_output("system_profiler SPHardwareDataType | grep 'Model Name:' | awk '{print $3}'")
        product_name = get_output("system_profiler SPHardwareDataType | grep 'Model Identifier:' | awk '{print $3}'")
        MAC = getmac.get_mac_address()
        IP_host = get_output("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'")
        IP_All = get_output("ipconfig getifaddr en0")
        hostname = get_output("hostname")
        WifiName = get_output("/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -I  | awk -F' SSID: '  '/ SSID: / {print $2}'")
        Gateway = get_output("netstat -rn | grep 'default' | awk '{print $2}'")
        DNS1 = get_output("scutil --dns | grep nameserver | awk '{print $3}'")
        DNS2 = get_output("nslookup google.com | grep 'Server:' | awk '{print $2}'")

        try:
            if WifiName == "unknown": password = "unknown"
            else: password = get_output(f"security find-generic-password -ga {WifiName} | grep 'password:'")
        except: password = "unknown"

        security = get_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
        security = security[security.index("link auth") + 1]
        interface = get_output("ifconfig")
        channel = get_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -c", False, 1)
        frequency = get_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -c", False, 2)

        try:
            config2 = subprocess.check_output("", stderr=subprocess.STDOUT)
            config2 = config2.decode("utf-8").split()
            maximum, result_now, dbm = 0, 0, 0

            for mom in range(len(config2)):
                if ("level" in config2[mom]):
=======
        try:
            response = urllib.request.urlopen(f"https://ip-api.io/json/{public_IP}")
            route = response.read().decode("utf-8").replace(',', '":').split('":')
        except:
            route = "unknown"
        try: 
            country = route[5].replace('"', '')
        except:
            country = "unknown"
        try:
            regionN =route[9].replace('"', '')
        except:
            regionN = "unknown"
        try:
            city = route[13].replace('"', '')
        except:
            city = "unknown"
        try:  
            zipC = route[15].replace('"', '')
        except:
            zipC = "unknown"
        try:    
            lat = route[19]
        except:
            lat = "unknown"
        try:    
            lon = route[21]
        except:
            lon = "unknown"
        try:    
            org = route[25].replace('"', '')
        except:
            org = "unknown"

        DeviceList = [nam, product_name, MAC, IP_host, IP_All, public_IP, hostname, WifiName, Gateway, DNS1, DNS2, password, security, interface, frequency, signal_strenght, channel, country, regionN, city, zipC , lat, lon, org]

# ========================= #
#          DARWIN           #
# ========================= #
    
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

        try:
            public_IP = urllib.request.urlopen("https://icanhazip.com")
            public_IP = public_IP.read().decode("utf-8").split()
            public_IP = public_IP[len(public_IP)-1]
        except:
            public_IP = "unknown"

        try:
            hostname = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
            hostname = hostname.stdout.readline()
            hostname = hostname.decode("utf-8").split()[0]
        except:
            hostname = "unknown"

        try:
            WifiName = subprocess.Popen("/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -I  | awk -F' SSID: '  '/ SSID: / {print $2}'", shell=True, stdout=subprocess.PIPE)
            WifiName = WifiName.stdout.readline()
            WifiName = WifiName.decode("utf-8").split()[0]
        except:
            WifiName = "unknown"

        try:
            Gateway = subprocess.Popen("netstat -rn | grep 'default' | awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
            Gateway = Gateway.stdout.readline()
            Gateway = Gateway.decode("utf-8").split()[0]
        except:
            Gateway = "unknown"
            
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
            SSID = WifiName
            if SSID == "unknown":
                password = "unknown"
            else:
                password = subprocess.Popen(f"security find-generic-password -ga {SSID} | grep 'password:'", shell=True, stdout=subprocess.PIPE)
                password = password.stdout.readline()
                password = password.decode("utf-8").split()[0]
        except:
            password = "unknown"

        try:
            security = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
            security = security.read().split()
            sec_index = security.index("link auth") + 1
            security = security[sec_index]
        except:
            security = "unknown"

        try:
            interface = os.popen("ifconfig")
            interface = interface.read().split()
            interface = interface[0]
        except:
            interface = "unknown"

        try:
            channel = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -c")
            channel = channel.read().split()
            channel = channel[1]
        except:
            channel = "unknown"

        try:
            frequency = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -c")
            frequency = frequency.read().split()
            frequency = frequency[2]
        except:
            frequency = "unknown"

        try:

            config2 = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I")
            config2 = config2.read().split()
            str_ind = config2.index("agrCtlRSSI") + 1
            config2 = config2[str_ind]

            maximum = 0
            result_now = 0
            dbm = 0

            for mom in range(len(config2)):
                if ("level" in config2[mom]) :
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
                    result_now = mom
                    result_now = config2[result_now].replace("level=", "")
                    dbm = mom + 1
                    dbm = config2[dbm]

<<<<<<< HEAD
            proc = 100 + (int(maximum) + int(result_now))
            word_strength = ""

            if proc >= 75: word_strength = "super strong"
            if 75 > proc >= 50: word_strength = "strong"
            if 50 > proc >= 25: word_strength = "weak"
            if proc < 25: word_strength = "super weak"

            signal = result_now + " " + dbm
            signal_strength = f"{signal} ({proc} %) - {word_strength}"
        except:
            signal_strength = "unknown"

        return [nam, product_name, MAC, IP_host, IP_All, public_IP,
                      hostname, WifiName, Gateway, DNS1, DNS2, password,
                      security, interface, frequency, signal_strength,
                      channel, country, regionN, city, zipC, lat, lon, maps, org]
=======
                else:
                    pass

            proc = 100+(int(maximum) + int(result_now))

            if proc >= 75:
                word_strengh = "super strong"
            if proc < 75 and proc >= 50:
                word_strengh = "strong"
            if proc < 50 and proc >= 25:
                word_strengh = "weak"
            if proc < 25:
                word_strengh = "super weak"


            signal = result_now + " " + dbm
            procenta = str(proc) + " %"

            signal_strenght = signal + " (" +  procenta + ") - " + word_strengh
        except:
            signal_strenght = "unknown"
        
        try:
            response = urllib.request.urlopen(f"https://ip-api.io/json/{public_IP}")
            route = response.read().decode("utf-8").replace(',', '":').split('":')
        except:
            route = "unknown"
        try: 
            country = route[5].replace('"', '')
        except:
            country = "unknown"
        try:
            regionN =route[9].replace('"', '')
        except:
            regionN = "unknown"
        try:
            city = route[13].replace('"', '')
        except:
            city = "unknown"
        try:  
            zipC = route[15].replace('"', '')
        except:
            zipC = "unknown"
        try:    
            lat = route[19]
        except:
            lat = "unknown"
        try:    
            lon = route[21]
        except:
            lon = "unknown"
        try:    
            org = route[25].replace('"', '')
        except:
            org = "unknown"
    
        DeviceList = [nam, product_name, MAC, IP_host, IP_All, public_IP, hostname, WifiName, Gateway, DNS1, DNS2, password, security, interface, frequency, signal_strenght, channel, country, regionN, city, zipC , lat, lon, org]
    return DeviceList
>>>>>>> bbecd3217d7e7fe82a2e4882674367939ef297ac
