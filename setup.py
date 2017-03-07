from distutils.core import setup
setup(
  name = 'stationdiy',
  packages = ['stationdiy'], # this must be the same as the name above
<<<<<<< HEAD
  version = '0.6',
  description = 'Custom Controller for StationDiY IoT platform',
=======
  version = '0.1',
  description = 'Module controller for StationDiY IoT platform',
>>>>>>> e76685e73cbc9019bc3f61d70fcb63d157b61df2
  author = 'Baurin Leza',
  author_email = 'baurin.lg@gmail.com',
  url = 'https://github.com/trpill/stationdiy', # use the URL to the github repo
  download_url = 'https://github.com/trpill/stationdiy/archive/master.zip', # I'll explain this in a second
  keywords = ['stationdiy', 'iot', 'internet'], #  keywords
  classifiers = [],
  install_requires=[
        'paho-mqtt'
    ]
)
