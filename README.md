# zfssa_utils

Command Line utility to handle most common tasks with ZFS Storage Appliance **Work In progress**

For convenience setup a virtual environment and install the utility in it.

```sh
python -m venv .venv
source .venv/bin/activate
(.venv) $
```

At the moment you can install the utility cloning the repo and building with setup.

```sh
(.venv) $ python setup.py install
```

Check the utility (remember to rehash if you are using zsh).

```sh
(.venv) $ zfssa-utils -h
usage: zfssa-utils [-h]
                   {EXPLORER,PROJECTS,FILESYSTEMS,LUNS,SNAPSHOTS,TEMPLATES}
                   ...

Utils for ZFS Storage Appliance. This program allow you to generate zfssa
general info csv files, manipulate or validate info for projects, luns and
snapshots.

positional arguments:
  {EXPLORER,PROJECTS,FILESYSTEMS,LUNS,SNAPSHOTS,TEMPLATES}
                        COMMANDS

optional arguments:
  -h, --help            show this help message and exit
```

Explorer generation will get the most common values you need about you zfssa system.

```sh
(.venv) $ zfssa-utils EXPLORER -s test/serverOS86.yml -p
 23% |##############                                               | ETA:  0:01:19
 .
 .
 .
 (.venv) $ zfssa-utils EXPLORER -s test/serverOS86.yml -p
100% |#############################################################| Time: 0:01:57

(.venv) $ ls data
zfssa_explorer_192.168.56.150_110218_144857.zip

(.venv) $ unzip -l data/zfssa_explorer_192.168.56.150_110218_144857.zip
Archive:  data/zfssa_explorer_192.168.56.150_110218_144857.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
      178  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/devices.csv
     5489  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/projects.csv
     2829  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/luns.csv
      326  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/cluster.csv
      190  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/datalinks.csv
      407  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/users.csv
      249  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/fc_initiator-groups.csv
     5951  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/filesystems.csv
      601  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/pools.csv
       62  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/routing.csv
      247  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/iscsi_targets.csv
      290  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/routes.csv
      551  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/iscsi_initiators.csv
      100  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/problems.csv
      222  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/iscsi_initiator-groups.csv
       28  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/iscsi_target-groups.csv
       28  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/fc_target-groups.csv
      687  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/version.csv
      287  2018-02-11 14:49   zfssa_explorer_192.168.56.150_110218_144857/interfaces.csv
      172  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/fc_targets.csv
      339  2018-02-11 14:50   zfssa_explorer_192.168.56.150_110218_144857/fc_initiators.csv
---------                     -------
    19233                     21 files
```

Create templates files to create several components in a serial way.

```sh
(.venv) $ zfssa-utils TEMPLATES -h
usage: zfssa-utils TEMPLATES [-h] [--projects] [--filesystems] [--luns]
                             [--snapshots] [-t TIMEOUT] (--create | --delete)

optional arguments:
  -h, --help            show this help message and exit
  --projects            generate template for projects
  --filesystems         generate template for filesystems
  --luns                generate template for luns
  --snapshots           generate template for snapshots
  -t TIMEOUT, --timeout TIMEOUT
                        connection timeout
  --create              template for creation
  --delete              template for deletion
```

```sh
(.venv) $ zfssa-utils TEMPLATES --projects --create
Created file 'create_projects.csv'
(.venv) $ zfssa-utils TEMPLATES --projects --delete
Created file 'destroy_projects.csv'
(.venv) $ zfssa-utils TEMPLATES --filesystems --create
Created file 'create_filesystems.csv'
(.venv) $ zfssa-utils TEMPLATES --filesystems --delete
Created file 'destroy_filesystems.csv'
(.venv) $ zfssa-utils TEMPLATES --luns --create
Created file 'create_luns.csv'
(.venv) $ zfssa-utils TEMPLATES --luns --delete
Created file 'destroy_luns.csv'
(.venv) $ zfssa-utils TEMPLATES --snapshots --create
Created file 'create_snapshots.csv'
(.venv) $ zfssa-utils TEMPLATES --snapshots --delete
Created file 'destroy_snapshots.csv'
```

Every template comes with a comment line (lines starting with '#') indicating some values allowed for the fields, but check your restful API zfssa version to be sure.

Make changes in the templates you want and create, delete or show the components you need.

Projects operations.

```sh
(.venv) $ zfssa-utils PROJECTS -s test/serverOS86.yml -f create_projects.csv --create
###############################################################################
Creating projects
###############################################################################
CREATE - SUCCESS - project 'unittest01' pool 'pool_0'
===============================================================================

(.venv) $ zfssa-utils PROJECTS -s test/serverOS86.yml -f create_projects.csv --list
###############################################################################
Listing projects
###############################################################################
LIST - PRESENT - project 'unittest01' pool 'pool_0' mountpoint '/export/unittest01' quota '10 GB' reservation '10 GB' compression 'gzip' dedup 'True' logbias 'latency' nodestroy 'False' recordsize '128 KB' readonly 'False' atime 'True' def_sparse 'True' def_user 'nobody' def_group 'other' def_perms '750' def_volblocksize '128 KB' def_volsize '1 GB' sharenfs 'on' sharesmb 'off'
===============================================================================

(.venv) $ zfssa-utils PROJECTS -s test/serverOS86.yml -f destroy_projects.csv --delete
You are about to destroy
==============================
Pool           Project
------------------------------
pool_0         unittest01
==============================
Do you want to destroy (y/N)y
###############################################################################
Deleting projects
###############################################################################
DELETE - SUCCESS - project 'unittest01' pool 'pool_0'
===============================================================================
```

**Note**: Every delete operation for projects, filesystems, luns and snapshots has a --noconfirm flag if you are completely sure about the file accuracy.
