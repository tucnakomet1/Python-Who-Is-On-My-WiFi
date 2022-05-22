from scapy.all import *

import urllib.request
import subprocess
import platform
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
        return response.read().decode("utf-8").replace(',', '":').replace("}", "").split('":')
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
    country = get_route_arg(route, 9)
    regionN = get_route_arg(route, 33)
    city = get_route_arg(route, 3)
    zipC = get_route_arg(route, len(route)-1)
    lat = get_route_arg(route, 23)
    lon = get_route_arg(route, 25)
    maps = f"https://www.google.com/maps/@{lat},{lon},14z"
    org = get_route_arg(route, 29)

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

    elif plat == "Windows":
        c = wmi.WMI()
        system = c.Win32_ComputerSystem()[0]
        sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
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

        nam = system.Manufacturer
        product_name = system.Model
        MAC = getmac.get_mac_address()
        IP_host = socket.gethostbyname('localhost')
        IP_All = get_ip_all()
        hostname = socket.gethostname()
        WifiName = get_wifi_name()

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
            indx = [g for g, rs in enumerate(out) if rs == DNSbytes]
            DNS2 = out[indx[0] + 1]
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
            secur_stat = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            secur_stat = secur_stat.decode("utf-8").split()
            secur_index = secur_stat.index("Authentication")

            security = secur_stat[secur_index + 2]
        except:
            security = "unknown"

        try:
            chan_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            chan_procc = chan_procc.decode("utf-8").split()
            chan_index = chan_procc.index("Channel")

            channel = chan_procc[chan_index + 2]
        except:
            channel = "unknown"

        try:
            freq_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            freq_procc = freq_procc.decode("utf-8").split()
            freq_index = freq_procc.index("Radio")
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
            sign_index = sign_procc.index("Signal")

            procenta = sign_procc[sign_index + 2]

            proc = list(procenta)
            proc.pop()
            proc = int("".join(proc))

            if proc >= 75:
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

        try:
            inter_procc = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            inter_procc = inter_procc.decode("utf-8").split()
            inter_index = inter_procc.index("Name")

            interface = inter_procc[inter_index + 2]
        except:
            interface = "unknown"

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
                    result_now = mom
                    result_now = config2[result_now].replace("level=", "")
                    dbm = mom + 1
                    dbm = config2[dbm]

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
