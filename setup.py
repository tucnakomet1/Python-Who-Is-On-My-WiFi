from setuptools import setup, find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='who-is-on-my-wifi',
	version='1.0.3',
	scripts=[
	"src/who_is_on_my_wifi.py",
	],
	description="Help you to find who is stealing your WiFI network, scan your WiFI and show you how many devices are currently connected!",
	url="https://github.com/tucnakomet1/Python-Who-Is-On-My-WiFi",
	author="Karel Velička",
	author_email="tucnakomet@gmail.com",
	py_modules=[
	"who_is_on_my_wifi",
	],
	package_dir={"": "src"},
	long_description=long_description,
	long_description_content_type="text/markdown",
	license="MIT",
	install_requires=[
	"getmac",
	"python-nmap",
	],
	classifiers=[
		"Environment :: Console",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX",
        "Operating System :: Unix",
	],
    entry_points={
        'console_scripts': [
            'whoisonmywifi=who_is_on_my_wifi:main',
            'who-is-on-my-wifi=who_is_on_my_wifi:main',
        ],
    },
)
