from setuptools import setup, find_packages
import platform

with open(('README.md'), encoding='utf-8') as f:
    long_description = f.read()

try:
	inst = "getmac", "scapy"#, "wmi"
except:
	inst = "getmac", "scapy"

setup(
	name='who-is-on-my-wifi',
	version='1.3.3',
	scripts=["src/who_is_on_my_wifi.py", "src/who.py", "src/device.py"],
	description="Help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are currently connected!",
	url="https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi",
	author="Karel Velička",
	author_email="tucnakomet@gmail.com",
	py_modules=["who_is_on_my_wifi", "who", "device"],
	package_dir={"": "src"},
	long_description=long_description,
	long_description_content_type='text/markdown',
	platforms=['any'],
	license="MIT",
	install_requires=[inst],
	classifiers=[
		"Environment :: Console",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		#"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX",
		"Operating System :: Unix",
		'Operating System :: Microsoft :: Windows',
		"Operating System :: OS Independent",
	],
	entry_points={
        'console_scripts': [
            'wiom=who_is_on_my_wifi:main',
            'who-is-on-my-wifi=who_is_on_my_wifi:main',
        ],
    },
)
