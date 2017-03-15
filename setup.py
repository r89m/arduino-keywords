from setuptools import setup

setup(name="Arduino Keywords Generator",
      version="1.0",
      description="A script for automatically generating a keywords.txt file for Arduino libraries",
      author="Richard Miles",
      packages=['arduinokeywords'],
      url="https://github.com/r89m/arduino-keywords-generator",
      install_requires=["CppHeaderParser==2.7.4"],
      scripts=[
            "bin/arduino-keywords-generator"
      ],
      test_suite='nose.collector',
      tests_require=[
            'nose==1.3.7'
      ])
