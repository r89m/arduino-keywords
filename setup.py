from setuptools import setup

setup(name="ArduinoKeywords",
      version="1.0.3",
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
