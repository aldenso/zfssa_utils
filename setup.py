from setuptools import setup

setup(name='zfssa_utils',
      version='0.1',
      description='Command Line utility to handle most common tasks with ZFS Storage Appliance.',
      url='http://github.com/aldenso/zfssa_utils',
      author='Aldo Sotolongo',
      author_email='aldenso@gmail.com',
      license='MIT',
      packages=['zfssa_utils'],
      install_requires=[
          'requests',
          'progressbar33',
          'pyyaml',
      ],
      scripts=['zfssa_utils/bin/zfssa-utils'],
      zip_safe=False)
