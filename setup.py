import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# get version information
exec(open('arduinokeywords/version.py').read())

setup(name="ArduinoKeywords",
      version=__version__,
      description="A script for automatically generating a keywords.txt file for Arduino libraries",
      author="Richard Miles",
      author_email="pypi@fast-chat.co.uk",
      packages=['arduinokeywords'],
      url="https://github.com/r89m/arduino-keywords",
      install_requires=["CppHeaderParser==2.7.4"],
      scripts=[
            "bin/arduino-keywords"
      ],
      test_suite='nose.collector',
      tests_require=[
            'nose==1.3.7'
      ])
