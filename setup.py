from setuptools import setup

setup(name='zfssa_utils',
      version='0.1',
      description='Command Line utility to handle common tasks on ZFSSA.',
      url='http://github.com/aldenso/zfssa_utils',
      author='Aldo Sotolongo',
      author_email='aldenso@gmail.com',
      license='MIT',
      packages=['zfssa_utils'],
      install_requires=[
          'requests',
          'progressbar33',
          'pyyaml',
          'six',
      ],
      extras_require={
          ':python_version < "3.2"': [
              'futures',
          ],
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'License :: Freely Distributable',
          'Operating System :: POSIX :: Linux',
          'Topic :: System :: Systems Administration',
          ],
      scripts=['zfssa_utils/bin/zfssa-utils'],
      zip_safe=False)
