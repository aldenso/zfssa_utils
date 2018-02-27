from setuptools import setup
from zfssa_utils import __version__

setup(name='zfssa_utils',
      version=__version__,
      description='Command Line utility to handle common tasks on ZFSSA.',
      url='http://github.com/aldenso/zfssa_utils',
      author='Aldo Sotolongo',
      author_email='aldenso@gmail.com',
      license='MIT',
      packages=['zfssa_utils', 'zfssa_utils.bin'],
      install_requires=[
          'requests',
          'progressbar33',
          'pyyaml',
          'six',
          'colorama',
          'schedule',
          'inotify',
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
      entry_points={'console_scripts':
                    ['zfssa-utils=zfssa_utils.bin.zfssa:main',
                     'zfssa-sched-explorer=zfssa_utils.bin.scheduler:main']},
      zip_safe=False,
      include_package_data=True)
