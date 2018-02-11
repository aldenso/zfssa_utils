"""Templates functions and default values."""

import os

TEMPL_FS_CREATE = """# Template create filesystems
# pool:             str
# project:          str
# filesystem:       str
# mountpoint:       str
# quota:            str or int   example: 10737418240 or 10g
# reservation:      str or int   example: 10737418240 or 10g
# compression:      str          example: gzip, lzjb, lz4, etc
# dedup:            bool
# logbias:          str          values: latency|throughput
# nodestroy:        bool
# recordsize:       str or int   example: 131072 or 128k
# readonly:         bool
# atime:            bool
# root_user:        str
# root_group:       str
# root_permissions: int          example: 750
# sharenfs:         str          example: on or rw=@192.168.56.101/24:@192.168.56.1/24
# sharesmb:         str
#
# Confirm the restful API accepted values in the Oracle Docs for your ZFSSA version.
#
# pool,project,filesystem,mountpoint,quota,reservation,compression,dedup,logbias,nodestroy,recordsize,readonly,atime,root_user,root_group,root_permissions,sharenfs,sharesmb
pool_0,unittest,fs10,/export/unittest/fs10,2g,1g,lzjb,False,latency,False,128k,False,False,root,other,750,rw=@192.168.56.101/24:@192.168.56.1/24,on
"""

TEMPL_FS_DESTROY = """# Template destroy filesystems
# pool:             str
# project:          str
# filesystem:       str
#
# pool,project,filesystem
pool_0,unittest,fs10
"""

TEMPL_LUN_CREATE = """# Template create luns
# pool:           str
# project:        str
# lun:            str
# size:           str or int   example: 10737418240 or 10g
# blocksize:      str or int   example: 131072 or 128k
# thin:           bool
# targetgrp:      str
# initiatorgrp:   str
# compression:    str          example: gzip, lzjb, lz4, etc
# logbias:        str          values: latency|throughput
# nodestroy:      bool
#
# Confirm the restful API accepted values in the Oracle Docs for your ZFSSA version.
#
# pool,project,lun,size,blocksize,thin,targetgrp,initiatorgrp,compression,logbias,nodestroy
pool_0,unittest,lun01,1g,128k,False,default,cluster-test,gzip,latency,False
"""

TEMPL_LUN_DESTROY = """# Template destroy luns
# pool:      str
# project:   str
# lun:       str
#
# pool,project,lun
pool_0,unittest,lun01
"""

TEMPL_PROJECT_CREATE = """# Template create projects
# pool:                 str
# project:              str
# mountpoint:           str
# quota:                str or int  example: 10737418240 or 10g
# reservation:          str or int  example: 10737418240 or 10g
# compression:          str
# dedup:                bool
# logbias:              str
# nodestroy:            bool
# recordsize:           str or int  example: example: 131072 or 128k
# readonly:             bool
# atime:                bool
# default_sparse:       bool
# default_user:         str
# default_group:        str
# default_permissions:  int         example: 750
# default_volblocksize: str or int  example: example: 131072 or 128k
# default_volsize:      str or int  example: 10737418240 or 10g
# sharenfs:             str
# sharesmb:             str
#
# Confirm the restful API accepted values in the Oracle Docs for your ZFSSA version.
#
# pool,project,mountpoint,quota,reservation,compression,dedup,logbias,nodestroy,recordsize,readonly,atime,default_sparse,default_user,default_group,default_permissions,default_volblocksize,default_volsize,sharenfs,sharesmb
pool_0,unittest01,/export/unittest01,10g,10g,gzip,True,latency,False,128k,False,True,True,nobody,other,750,128k,1g,on,off
"""

TEMPL_PROJECT_DESTROY = """# Template destroy projects
# pool:                 str
# project:              str
#
# pool,project
pool_0,unittest01
"""

TEMPL_SNAPSHOTS = """# Template projects snapshots
# pool:       str
# project:    str
# snaptarget: str
# snaptype:   str   for projects: '-', for luns: 'lun', for filesystems: 'filesystem'
# snapname:   str
#
# pool,project,snaptarget,snaptype,snapname
#
# Project Snap
pool_0,unittest,-,project,backup
#
# Filesystem snap
pool_0,unittest,fs01,filesystem,backup
#
# Lun snap
pool_0,unittest,lun10,lun,backup
"""


def write_file(name, data):
    """Write a file base on templates."""
    if os.path.exists(name):
        exit("File '{}' already exists, rename it or delete it.".format(name))
    try:
        with open(name, "w") as file:
            file.write(data)
            print("Created file '{}'".format(name))
    except Exception as err:
        print("Not able to create file: '{}'".format(err))


def create_template(args):
    """Create template based on the args given"""
    if args.projects:
        if args.create:
            write_file("create_projects.csv", TEMPL_PROJECT_CREATE)

        else:
            write_file("destroy_projects.csv", TEMPL_PROJECT_DESTROY)
    elif args.luns:
        if args.create:
            write_file("create_luns.csv", TEMPL_LUN_CREATE)
        else:
            write_file("destroy_luns.csv", TEMPL_LUN_DESTROY)
    elif args.filesystems:
        if args.create:
            write_file("create_filesystems.csv", TEMPL_FS_CREATE)
        else:
            write_file("destroy_filesystems.csv", TEMPL_FS_DESTROY)
    elif args.snapshots:
        if args.create:
            write_file("create_snapshots.csv", TEMPL_SNAPSHOTS)
        else:
            write_file("destroy_snapshots.csv", TEMPL_SNAPSHOTS)
    else:
        print("You need to choose an option:"
              "projects, --luns, --filesystems, --snapshots")
