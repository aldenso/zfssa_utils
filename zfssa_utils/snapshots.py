"""Snapshots functions

Functions to create, list/show and delete snapshots.

Every snap line should look like this:
#pool(str),project(str),snaptarget(str),snaptype(str),snapname(str)

Available values:

pool: string
project: string
snaptarget: [string|-] # it may be a filesystem or lun name,
            the hyphen is for projects.
snaptype: [filesystem|lun|project]
snapname: string
"""
from __future__ import print_function, division
import json
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import HEADER, response_size, read_yaml_file, \
     read_csv_file, createprogress, createlogger, SNAPLOGFILE

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def list_snap(snap, zfsurl, zauth):
    """List Snapshots from line in csv format. (err, msg)"""
    pool, project, snaptarget, snaptype, snapname = snap
    fullurl = ""
    if snaptype == 'filesystem':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
                   "snapshots".format(zfsurl, pool, project, snaptarget))
    elif snaptype == 'lun':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}/"
                   "snapshots".format(zfsurl, pool, project, snaptarget))
    elif snaptype == 'project':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/snapshots"
                   .format(zfsurl, pool, project))
    else:
        return False, "snaptype '{}' unknown".format(snaptype)
    try:
        req = requests.get(fullurl, auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        if len(j['snapshots']) == 0:
            return False, ("LIST - NOTPRESENT - snapshot '{}' {} '{}' "
                           "project '{}' and pool '{}' - Message Snapshot not "
                           "present".format(snapname, snaptype, snaptarget,
                                            project, pool))
        else:
            for i in j['snapshots']:
                if i['name'] == snapname:
                    return False, ("LIST - PRESENT - snapshot '{}' {} "
                                   "'{}' project '{}' pool '{}' created_at "
                                   "'{}' space_data '{}' space_unique '{}'"
                                   .format(i['name'], snaptype, snaptarget,
                                           project, pool, i['creation'],
                                           response_size(i['space_data']),
                                           response_size(i['space_unique'])))
        return False, ("LIST - NOTPRESENT - snapshot '{}' {} '{}' "
                       "project '{}' pool '{}' - Message Snapshot not present"
                       .format(snapname, snaptype, snaptarget, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("LIST - FAIL - snapshot '{}' {} '{}' project '{}' "
                 "pool '{}' - Error {}".format(snapname, snaptype, snaptarget,
                                               project, pool, error))
        else:
            return True, ("LIST - FAIL - snapshot '{}' {} '{}' project "
                          "'{}' pool '{}' - Error {}"
                          .format(snapname, snaptype, snaptarget, project,
                                  pool, error))
    except ConnectionError as error:
        return True, ("LIST - FAIL - snapshot '{}' {} '{}' project "
                      "'{}' pool '{}' - Error {}".format(snapname, snaptype,
                                                         snaptarget, project,
                                                         pool, error))


def create_snap(snap, zfsurl, zauth):
    """Create Snapshots from line in csv format. (err, msg)"""
    pool, project, snaptarget, snaptype, snapname = snap
    fullurl = ""
    if snaptype == 'filesystem':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
                   "snapshots".format(zfsurl, pool, project, snaptarget))
    elif snaptype == 'lun':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}/"
                   "snapshots".format(zfsurl, pool, project, snaptarget))
    elif snaptype == 'project':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/snapshots"
                   .format(zfsurl, pool, project))
    else:
        return False, "snaptype '{}' unknown".format(snaptype)
    try:
        req = requests.post(fullurl, data=json.dumps({'name': snapname}),
                            auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, ("CREATE - FAIL - snapshot '{}' {} '{}' "
                              "project '{}' pool {}' - Error {}"
                              .format(snapname, snaptype, snaptarget, project,
                                      pool, j['fault']['message']))
        else:
            return False, ("CREATE - SUCCESS - snapshot '{}' {} '{}' "
                           "project '{}' pool '{}'"
                           .format(snapname, snaptype, snaptarget,
                                   project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("CREATE - FAIL - snapshot '{}' {} '{}' project '{}' "
                 "pool '{}' - Error {}".format(snapname, snaptype, snaptarget,
                                               project, pool, error))
        else:
            return True, ("CREATE - FAIL - snapshot '{}' {} '{}' "
                          "project '{}' pool '{}' - Error {}"
                          .format(snapname, snaptype, snaptarget, project,
                                  pool, error))
    except ConnectionError as error:
        return True, ("CREATE - FAIL - snapshot '{}' {} '{}' project "
                      "'{}' pool '{}' - Error {}"
                      .format(snapname, snaptype, snaptarget, project, pool,
                              error))


def delete_snap(snap, zfsurl, zauth):
    """Delete Snapshots from line in csv format. (err, msg)"""
    pool, project, snaptarget, snaptype, snapname = snap
    fullurl = ""
    if snaptype == 'filesystem':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
                   "snapshots/{}".format(zfsurl, pool, project, snaptarget,
                                         snapname))
    elif snaptype == 'lun':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}/"
                   "snapshots/{}".format(zfsurl, pool, project, snaptarget,
                                         snapname))
    elif snaptype == 'project':
        fullurl = ("{}/storage/v1/pools/{}/projects/{}/snapshots/{}"
                   .format(zfsurl, pool, project, snapname))
    else:
        return False, "snaptype ''{}' unknown".format(snaptype)
    try:
        req = requests.delete(fullurl, auth=zauth, verify=False,
                              headers=HEADER)
        req.close()
        req.raise_for_status()
        return False, ("DELETE - SUCCESS - snapshot '{}' {} '{}' "
                       "project '{}' pool '{}'"
                       .format(snapname, snaptype, snaptarget, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("DELETE - FAIL - snapshot '{}' {} '{}' project '{}'"
                 "pool '{}' - Error {}".format(snapname, snaptype, snaptarget,
                                               project, pool, error))
        else:
            return True, ("DELETE - FAIL - snapshot '{}' {} '{}' "
                          "project '{}' pool '{}' - Error {}"
                          .format(snapname, snaptype, snaptarget, project,
                                  pool, error))
    except ConnectionError as error:
        return True, ("DELETE - FAIL - snapshot '{}' {} '{}' project "
                      "'{}' pool '{}' - Error {}"
                      .format(snapname, snaptype, snaptarget, project, pool,
                              error))


def run_snaps(args):
    """Run all filesystems snapshots actions"""
    csvfile = args.file
    listsnaps = args.list
    createsnaps = args.create
    deletesnaps = args.delete
    snaplist = read_csv_file(csvfile)
    configfile = args.server
    config = read_yaml_file(configfile)
    zfsurl = "https://{}:215/api".format(config['ip'])
    zauth = (config['username'], config['password'])
    initial = 0 # for progressbar
    if createsnaps:
        if args.progress:
            progbar = createprogress(len(snaplist))
            logger = createlogger(SNAPLOGFILE)
            for entry in snaplist:
                err, msg = create_snap(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Creating snapshots")
            print("#" * 79)
            for entry in snaplist:
                print(create_snap(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif deletesnaps:
        if args.progress:
            progbar = createprogress(len(snaplist))
            logger = createlogger(SNAPLOGFILE)
            for entry in snaplist:
                err, msg = delete_snap(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Deleting snapshots")
            print("#" * 79)
            for entry in snaplist:
                print(delete_snap(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif listsnaps:
        if args.progress:
            progbar = createprogress(len(snaplist))
            logger = createlogger(SNAPLOGFILE)
            for entry in snaplist:
                err, msg = list_snap(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Listing snapshots")
            print("#" * 79)
            for entry in snaplist:
                print(list_snap(entry, zfsurl, zauth)[1])
                print("=" * 79)
    else:
        print("#" * 79)
        print("You need to specify a snap option (--list, --create, --delete)")
        print("#" * 79)
    # delta = datetime.now() - START
    # print("Finished in {} seconds".format(delta.seconds))
