
<h1 id="who-is-on-my-wifi">Who is on my WiFi - Python</h1>

Who-is-on-my-wifi is python module for Linux, Windows and Mac users. It shows you IP Addresses of all cannected devices and much more!

* <a href="#install">INSTALLATION</a><br/>
  * <a href="#upgrade">UPGRADE</a><br/>
* <a href = "#usage">USAGE</a><br/>
  * <a href="#module">Command</a><br/>
  * <a href="#python">Python</a><br/>
* <a href = "#update">UPDATES AND VERSION</a><br/>
  * <a href="#zerozero">Version 1.0</a><br/>
  * <a href="#zeroone">Version 1.1</a><br/>
  * <a href="#zerotwo">Version 1.2</a><br/> 
* <a href = "#about">ABOUT</a><br/>
* <a href = "#screen">SCREENSHOTS</a><br/>
* <a href = "#help">HELP</a><br/>
  * <a href = "#app">Application</a><br/>
    * <a href = "#who">How to see who is on my wifi?</a><br/>
    * <a href = "#info">How to get information about my device?</a><br/>
  * <a href = "#error">Error</a><br/>
    * <a href = "#attribute">AttributeError:</a><br/>
    * <a href = "#nmap">NmapError:</a><br/>
* <a href = "#license">LICENSE</a><br/>
* <a href = "#contact">CONTACT</a><br/>
<br/>

<h2 id="install">INSTALLATION</h2>

See the <a href="https://pypi.org/project/who-is-on-my-wifi/">PyPi</a> page for more information.<br/><br/>

***Python3***<br/>
`pip3 install who-is-on-my-wifi` <br/>

***Python***<br/>
`pip install who-is-on-my-wifi` <br/>
<br/>


If you want to download source code (zip file) you can download it <a href="https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi/archive/master.zip">here</a>.<br/><br/>
Or via GitHub:<br/> `git clone https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi.git`
<br/><br/>


<h3 id="upgrade">UPGRADE</h3>

***Python3***<br/>
`pip3 install who-is-on-my-wifi --upgrade`<br/>

***Python***<br/>
`pip install who-is-on-my-wifi --upgrade`<br/>
<br/><br/><br/><br/><br/><br/><br/><br/><br/>



<h2 id="usage">USAGE</h2>

<h3 id="module"> Command </h3>

```
usage: who-is-on-my-wifi [-h] [-v] [-c] [-d] [-w]
usage: wiom[-h] [-v] [-c] [-d] [-w]

Who-Is-On-My-WIFi module help you to find who is stealing your WiFI
network, scan your WiFI and show you how many devices are currently
connected.

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show current version
  -c, --contact    show contact
  -d, --device     show information about your device
  -w, --who        show who is on your WiFI?!

Thank you!
↓  ↓  ↓  ↓
Visit my GitHub: https://github.com/tucnakomet1
```
<br/><br/>

<h3 id="python"> Python </h3>

```python
>>> import who_is_on_my_wifi

#### show help page ####
>>> who_is_on_my_wifi.help()

#### show license ####
>>> who_is_on_my_wifi.license()

#### show contact page ####
>>> who_is_on_my_wifi.contact()


#### see who is on my wifi ####
>>> who_is_on_my_wifi.who()

#### see information about your device ####
>>> who_is_on_my_wifi.device()

```
<br/><br/><br/><br/><br/><br/><br/><br/>

<h2 id="update">UPDATES AND VERSION </h2>

<h3 id="zerozero"> Version 1.0 </h3> 

<em>Old version</em><br/>
- Supported only Linux
- Show you connected devices, IP and MAC Addresses
- Scan your WiFi and show you connected and not connected devices

<h3 id="zeroone"> Version 1.1 </h3> 

<em> Old version </em><br/>
- Supported Linux and Windows<br/>
- More functions (see wifi password)<br/>

<h3 id="zerotwo"> Version 1.2 </h3> 

<em> Current version </em><br/>
- Supported Linux, Windows and Mac OS <br/>
- bug fixes<br/>

<br/><br/><br/><br/><br/><br/><br/><br/><br/>



<h2 id="about">ABOUT</h2>

This script is created with the help of language Pyhon3. Who-is-on-my-wifi help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are connected.<br/> I tried to do my best so I hope everything is working. If you have some problem, please let me <a href = "#error">know</a>.<br/>
<br/><br/><br/><br/><br/><br/><br/><br/>


<h2 id="screen">SCREENSHOTS</h2>

![info](https://user-images.githubusercontent.com/55558124/88484780-6fabb700-cf71-11ea-8088-f6795c048d20.png)<br/>
![who](https://user-images.githubusercontent.com/55558124/88484844-18f2ad00-cf72-11ea-94fd-e00acfc46047.png)<br/>

<h2 id="help">HELP</h2>

* <a href = "#app">Application</a><br/>
  * <a href = "#who">How to see who is on my wifi?</a><br/>
  * <a href = "#info">How to get information about my device?</a><br/>
* <a href = "#error">Error</a><br/>
  * <a href = "#attribute">AttributeError:</a><br/>
  * <a href = "#nmap">NmapError</a><br/>
<br/><br/>

 <h2 id = "app"> Application </h2>


<h3 id="who"> How to see who is on my wifi? </h3>

!!! You have to run this command as `sudo` or as `Administrator` !!!

<strong>Command</strong>

```shell
linux@name:~$ sudo who-is-on-my-wifi -w
```
or
```shell
linux@name:~$ sudo wiom -w
```

<br/>
<strong>Python (sudo/ admin)</strong>

```python
from who_is_on_my_wifi import *


WHO = who()
for i in range(0, len(WHO)):
    print(WHO[i])

# >>> OUTPUT <<<

# ['IP Address:', '192.168.0.1', 'Mac Address:', 'FF:FF:FF:FF:FF:FF', 'Device:', 'Netcore Technology']
# ['IP Address:', '192.168.0.2', 'Mac Address:', 'FF:FF:FF:FF:FF:FF', 'Device:', 'Samsung Electronics']
# ['IP Address:', '192.168.0.4', 'Mac Address:', 'FF:FF:FF:FF:FF:FF', 'Device:', 'Acer TravelMate (Your device)']

```
<br/><br/>

<h3 id="info"> How to get information about my device? </h3>

<strong>Command</strong>

```shell
linux@name:~$ sudo who-is-on-my-wifi -d
```
or
```shell
linux@name:~$ sudo wiom -d
```

<br/>
<strong>Python</strong>

```python
from who_is_on_my_wifi import *

info = device()

print(f"PC: {info[0]}")
print(f"PC Product-Name: {info[1]}")
print(f"MAC Address: {info[2]}")
print(f"IP Address (host): {info[3]}")
print(f"IP Address: {info[4]}")
print(f"PC HostName: {info[5]}")
print(f"WiFI Name: {info[6]}")
print(f"Gateway: {info[7]}")
print(f"DNS 1: {info[8]}")
print(f"DNS 2: {info[9]}")
print(f"Password: {info[10]}")


# >>> OUTPUT <<<


# PC: Acer
# PC Product-Name: TravelMate
# MAC Address: FF:FF:FF:FF:FF:FF
# IP Address (host): 127.0.0.1
# IP Address: 192.168.0.4
# PC Name: tucna
# WiFI Name: WifiHome
# Gateway: 192.168.0.1
# DNS 1: 85.119.89.2
# DNS 2: 8.8.8.8
# Password: FFFFFFFFF


```
<br/>

 <h2 id = "error"> Error </h2>

<h3 id="attribute"> AttributeError: 'NoneType' object has no attribute '...' </h3>

This error means that you used / entered an object that doesn't exist. It is probably typing error.<br/>
Make sure you wrote everything <a href="#usage">correctly</a>.
<br/><br/>

<h3 id = "nmap"> nmap.nmap.PortScannerError: 'nmap program was not found in path. PATH is : ...' </h3>

This error means that you don't have Nmap installed. <br/>
To fix this type into the terminal `sudo apt-get install nmap` or [download](https://nmap.org/download.html) it from their web page.
<br/><br/>

<h3 id="c"> Different Error: </h3>

If you have different error make sure you are running command as `sudo` or as `Administrator` and make sure you have [Nmap](https://nmap.org/download.html) installed.

<br/><br/><br/><br/><br/><br/><br/><br/>

<h2 id = "license"> LICENSE </h2>

[MIT](https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi/blob/master/LICENSE.txt)
<br/><br/><br/><br/><br/><br/><br/><br/>

<h2 id="contact">CONTACT</h2>
You can contact me via my gmail address <a href="mailto:tucnakomet@gmail.com">tucnakomet@gmail.com</a>.<br/>
 <br/><br/>
 
 
 <a href = "#who-is-on-my-wifi"><span title="Go UP!"><img alt="up" src="https://ps.w.org/wpfront-scroll-top/assets/icon.svg?rev=1534312" width="40" height="40" style="border:0px solid;" /></a></span>
  <a href = "https://github.com/tucnakomet1"><span title="GitHub"><img alt="github" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/1200px-Octicons-mark-github.svg.png" width="40" height="40" style="border:0px solid;" /></a></span>
   <a href = "https://pypi.org/user/Tucnakomet/"><span title="PyPi"><img alt="pypi" src="https://miro.medium.com/max/660/1*2FrV8q6rPdz6w2ShV6y7bw.png" width="40" height="40" style="border:0px solid;" /></a></span>

 
