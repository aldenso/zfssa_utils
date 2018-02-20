# zfssa_utils

Command Line utility to handle most common tasks with ZFS Storage Appliance (OS86 and OS87).

This utility only works with the Rest Api service, so you must activate the service.

For convenience, clone the repo and setup a virtual environment to install the utility in it.

```sh
git clone https://github.com/aldenso/zfssa_utils
cd zfssa_utils
python -m venv .venv
source .venv/bin/activate
```

You'll see a prompt like this.

```txt
(.venv) $
```

At the moment you can install the utility building with setup.

```sh
python setup.py install
```

If you want to develop the program use the option.

```sh
python setup.py develop
```

Check the utility (remember to rehash if you are using zsh).

```sh
zfssa-utils -h
```

```txt
usage: zfssa-utils [-h] [-v] [-t TIMEOUT] [--cert CERT]
                   {EXPLORER,PROJECTS,FILESYSTEMS,LUNS,SNAPSHOTS,TEMPLATES,UPDATE}
                   ...

Utils for ZFS Storage Appliance. This program allow you to generate zfssa
general info csv files, manipulate or validate info for projects, luns and
snapshots.

positional arguments:
  {EXPLORER,PROJECTS,FILESYSTEMS,LUNS,SNAPSHOTS,TEMPLATES,UPDATE}
                        COMMANDS

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         program version
  -t TIMEOUT, --timeout TIMEOUT
                        connection timeout
  --cert CERT           use certificate
  --doc                 program documentation
```

**Note**: You can run operations without validating certificates, but you'll get a warning.

```txt
*******************************************************************************
Warning: not using certificate verification.
*******************************************************************************
```

If you download the certificate, you can use it with the --cert option before the COMMANDS options.

example:

```sh
zfssa-utils --cert myzfssa.cert [EXPLORER|PROJECTS|...]
```

For every operations you'll need a server configuration file, where you will indicate the ip of the system, a user with enough privileges and the password for the user.

```yaml
ip: 192.168.56.150
username: root
password: password
```

## EXPLORER COMMAND

Explorer generation will get the most common values you need about you zfssa system.

```sh
zfssa-utils EXPLORER -s test/serverOS86.yml -p
```

```txt
 23% |##############                                               | ETA:  0:01:19
 .
 .
 .
100% |#############################################################| Time: 0:01:57
```

```sh
ls data
```

```txt
zfssa_explorer_192.168.56.150_110218_144857.zip
```

```sh
unzip -l data/zfssa_explorer_192.168.56.150_110218_144857.zip
```

```txt
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

## TEMPLATES COMMAND

Create templates files to make several components operations in a serial way.

```sh
zfssa-utils TEMPLATES -h
```

```txt
usage: zfssa-utils TEMPLATES [-h] [--projects] [--filesystems] [--luns]
                             [--snapshots] [-t TIMEOUT] (--create | --delete)

optional arguments:
  -h, --help            show this help message and exit
  --projects            generate template for projects
  --filesystems         generate template for filesystems
  --luns                generate template for luns
  --snapshots           generate template for snapshots
  --updates             generate template for components(lun|fs|project)
                        updates/modification
  -t TIMEOUT, --timeout TIMEOUT
                        connection timeout
  --create              template for creation
  --delete              template for deletion
```

```sh
zfssa-utils TEMPLATES --projects --create
zfssa-utils TEMPLATES --projects --delete
zfssa-utils TEMPLATES --filesystems --create
zfssa-utils TEMPLATES --filesystems --delete
zfssa-utils TEMPLATES --luns --create
zfssa-utils TEMPLATES --luns --delete
zfssa-utils TEMPLATES --snapshots --create
zfssa-utils TEMPLATES --snapshots --delete
zfssa-utils TEMPLATES --updates --create
```

```txt
Created file 'create_projects.csv'
Created file 'destroy_projects.csv'
Created file 'create_filesystems.csv'
Created file 'destroy_filesystems.csv'
Created file 'create_luns.csv'
Created file 'destroy_luns.csv'
Created file 'create_snapshots.csv'
Created file 'destroy_snapshots.csv'
Created file 'update_components.csv'
```

Every template comes with comment lines (lines starting with '#') indicating some values allowed for the fields, but check your restful API zfssa version to be sure (**Only lines without comments will be processed**).

Example lun creation file.

```csv
# pool,project,lun,volsize,volblocksize,sparse,targetgroup,initiatorgroup,compression,logbias,nodestroy
pool_0,unittest,lun01,1g,128k,False,default,cluster-test,gzip,latency,False
```

Example delete lun file.

```csv
# pool,project,lun
pool_0,unittest,lun01
```

Make changes in the templates you want and create, delete or show the components you need.

## PROJECTS COMMAND

Projects operations, create, delete or show projects.

```sh
zfssa-utils PROJECTS -s serverOS86.yml -f create_projects.csv --create
zfssa-utils PROJECTS -s serverOS86.yml -f create_projects.csv --list
zfssa-utils PROJECTS -s serverOS86.yml -f destroy_projects.csv --delete
```

```txt
###############################################################################
Creating projects
###############################################################################
CREATE - SUCCESS - project 'unittest01' pool 'pool_0'
===============================================================================

###############################################################################
Listing projects
###############################################################################
LIST - PRESENT - project 'unittest01' pool 'pool_0' mountpoint '/export/unittest01' quota '10 GB' reservation '10 GB' compression 'gzip' dedup 'True' logbias 'latency' nodestroy 'False' recordsize '128 KB' readonly 'False' atime 'True' def_sparse 'True' def_user 'nobody' def_group 'other' def_perms '750' def_volblocksize '128 KB' def_volsize '1 GB' sharenfs 'on' sharesmb 'off'
===============================================================================

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

**Note**: Every delete operation for projects has a --noconfirm flag if you are completely sure about the file accuracy.

## FILESYSTEMS COMMAND

Filesystems operations, create, delete or show filesystems.

```sh
zfssa-utils FILESYSTEMS -s serverOS86.yml -f create_filesystems.csv --create
zfssa-utils FILESYSTEMS -s serverOS86.yml -f create_filesystems.csv --list
zfssa-utils FILESYSTEMS -s serverOS86.yml -f create_filesystems.csv --delete
```

```txt
###############################################################################
Creating filesystems
###############################################################################
CREATE - SUCCESS - filesystem 'fs10' project 'unittest' pool 'pool_0'
===============================================================================

###############################################################################
Listing filesystems
###############################################################################
LIST - SUCCESS - filesystem 'fs10' project 'unittest' pool 'pool_0' mountpoint '/export/unittest/fs10' quota '2 GB' reservation '1 GB' compression 'lzjb' dedup 'False' logbias 'latency' nodestroy 'False' recordsize '128 KB' readonly 'False' atime 'False' root_user 'root' root_group 'other' root_permissions '750' sharenfs rw=@192.168.56.101/24:@192.168.56.1/24' sharesmb 'on'
===============================================================================

You are about to destroy
=============================================
Pool           Project        Filesystem
---------------------------------------------
pool_0         unittest       fs10
=============================================
Do you want to destroy (y/N)y
###############################################################################
Deleting filesystems
###############################################################################
DELETE - SUCCESS - filesystem 'fs10' project 'unittest' pool 'pool_0'
===============================================================================
```

**Note**: Every delete operation for filesystems has a --noconfirm flag if you are completely sure about the file accuracy.

## LUNS COMMAND

Luns operations, create, delete or show luns.

```sh
zfssa-utils LUNS -s serverOS86.yml -f create_luns.csv --create
zfssa-utils LUNS -s serverOS86.yml -f create_luns.csv --list
zfssa-utils LUNS -s serverOS86.yml -f destroy_luns.csv --delete
```

```txt
###############################################################################
Creating luns
###############################################################################
CREATE - SUCCESS - lun 'lun01' project 'unittest' pool 'pool_0'
===============================================================================

###############################################################################
Listing luns
###############################################################################
LIST - SUCCESS - lun 'lun01' project 'unittest' pool 'pool_0' assigned number '4' initiatorgroup '['cluster-test']' volsize '1 GB' volblocksize '128 KB' status 'online' space_total '1 GB' lunguid '600144F0EF0D2BCE00005A8C05890001' logbias ' latency' creation '20180220T11:24:42' thin 'False' nodestroy 'False'
===============================================================================

You are about to destroy
=============================================
Pool           Project        Lun
---------------------------------------------
pool_0         unittest       lun01
=============================================
Do you want to destroy (y/N)y
###############################################################################
Deleting luns
###############################################################################
DELETE - SUCCESS - lun 'lun01' project 'unittest' pool 'pool_0'
===============================================================================
```

**Note**: Every delete operation for luns has a --noconfirm flag if you are completely sure about the file accuracy.

## UPDATE COMMAND

Update/Modify operations, modify mutable values in projects, filesystems and luns.

```sh
zfssa-utils.exe UPDATE -s serverOS86.yml -f update_components.csv
```

```txt
You are about to modify/update
===============================================================================
TYPE            NAME:PROJECT:POOL              keyx: valx , keyx+1: valx+1, ...
===============================================================================
project         -:unittest:pool_0              ['logbias: latency']
lun             lun10:unittest:pool_0          ['compression: lzjb', 'sparse: True']
filesystem      fs01:unittest:pool_0           ['reservation: 512m', 'atime: False']
===============================================================================
Do you want to proceed (y/N)y
###############################################################################
Updating project
###############################################################################
UPDATE - SUCCESS - project 'unittest' pool 'pool_0' - updates: logbias 'latency'
===============================================================================
###############################################################################
Updating lun
###############################################################################
UPDATE - SUCCESS - lun 'lun10' project 'unittest' pool 'pool_0' - updates: compression 'lzjb' sparse 'True'
===============================================================================
###############################################################################
Updating filesystem
###############################################################################
UPDATE - SUCCESS - filesystem 'fs01' project 'unittest' pool 'pool_0' - updates: reservation '512m' atime 'False'
===============================================================================
```

**Note**: Every update/modify operation for projects, filesystems and luns has a --noconfirm flag if you are completely sure about the file accuracy.

## SNAPSHOTS COMMAND

Snapshots operations, create, delete or show snaps.

```sh
zfssa-utils SNAPSHOTS -s serverOS86.yml -f create_snapshots.csv --create
zfssa-utils SNAPSHOTS -s serverOS86.yml -f create_snapshots.csv --list
zfssa-utils SNAPSHOTS -s serverOS86.yml -f create_snapshots.csv --delete
```

```txt
###############################################################################
Creating snapshots
###############################################################################
CREATE - SUCCESS - snapshot 'backup' project '-' project 'unittest' pool 'pool_0'
===============================================================================

###############################################################################
Listing snapshots
###############################################################################
LIST - SUCCESS - snapshot 'backup' project '-' project 'unittest' pool 'pool_0' created_at '20180220T11:41:15' space_data '112 KB' space_unique '0 B'
===============================================================================

You are about to destroy
===========================================================================
Pool           Project        fs|lun         SnapType       Snapshot
---------------------------------------------------------------------------
pool_0         unittest       -              project        backup
===========================================================================
Do you want to destroy (y/N)y
###############################################################################
Deleting snapshots
###############################################################################
DELETE - SUCCESS - snapshot 'backup' project '-' project 'unittest' pool 'pool_0'
===============================================================================
```

**Note**: Every delete operation for snapshots has a --noconfirm flag if you are completely sure about the file accuracy.
