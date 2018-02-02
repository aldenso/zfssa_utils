"""Snapshots functions"""
from __future__ import print_function, division
import json
import csv
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import HEADER, response_size, read_yaml_file, \
     createprogress, createlogger, SNAPLOGFILE

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def read_snap_file(filename):
    """Read snap csv file and return the list"""
    snaplist = []
    with open(filename, 'r') as cvsfile:
        filereader = csv.reader(cvsfile, delimiter=',')
        for row in filereader:
            snaplist.append(row)
    del snaplist[0]
    return snaplist


def list_snap(snap, zfsurl, zauth):
    """List Snapshots specified in csv file (fail, message)"""
    pool, project, filesystem, snapname = snap
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
               "snapshots".format(zfsurl, pool, project, filesystem))
    try:
        req = requests.get(fullurl, auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        if len(j['snapshots']) == 0:
            return False, ("LIST - NOTPRESENT - snapshot '{}' filesystem '{}' "
                           "project '{}' and pool '{}' - Message Snapshot not "
                           "present".format(snapname, filesystem,
                                            project, pool))
        else:
            for i in j['snapshots']:
                if i['name'] == snapname:
                    return False, ("LIST - PRESENT - snapshot '{}' filesystem "
                                   "'{}' project '{}' pool '{}' created_at "
                                   "'{}' space_data '{}' space_unique '{}'"
                                   .format(i['name'], filesystem, project,
                                           pool, i['creation'],
                                           response_size(i['space_data']),
                                           response_size(i['space_unique'])))
        return False, ("LIST - NOTPRESENT - snapshot '{}' filesystem '{}' "
                       "project '{}' pool '{}' - Message Snapshot not present"
                       .format(snapname, filesystem, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("LIST - FAIL - snapshot '{}' filesystem '{}' project '{}' "
                 "pool '{}' - Error {}".format(snapname, filesystem, project,
                                               pool, error))
        else:
            return True, ("LIST - FAIL - snapshot '{}' filesystem '{}' project"
                          "'{}' pool '{}' - Error {}"
                          .format(snapname, filesystem, project, pool, error))
    except ConnectionError as error:
        return True, ("LIST - FAIL - snapshot '{}' filesystem '{}' project "
                      "'{}' pool '{}' - Error {}".format(snapname, filesystem,
                                                         project, pool, error))


def create_snap(snap, zfsurl, zauth):
    """Create Snapshots from csv file"""
    pool, project, filesystem, snapname = snap
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
               "snapshots".format(zfsurl, pool, project, filesystem))
    try:
        req = requests.post(fullurl, data=json.dumps({'name': snapname}),
                            auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, ("CREATE - FAIL - snapshot '{}' filesystem '{}' "
                              "project '{}' pool {}' - Error {}"
                              .format(snapname, filesystem, project, pool,
                                      j['fault']['message']))
        else:
            return False, ("CREATE - SUCCESS - snapshot '{}' filesystem '{}' "
                           "project '{}' pool '{}'"
                           .format(snapname, filesystem, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("CREATE - FAIL - snapshot '{}' filesystem '{}' project '{}' "
                 "pool '{}' - Error {}".format(snapname, filesystem, project,
                                               pool, error))
        else:
            return True, ("CREATE - FAIL - snapshot '{}' filesystem '{}' "
                          "project '{}' pool '{}' - Error {}"
                          .format(snapname, filesystem, project, pool,
                                  error))
    except ConnectionError as error:
        return True, ("CREATE - FAIL - snapshot '{}' filesystem '{}' project "
                      "'{}' pool '{}' - Error {}"
                      .format(snapname, filesystem, project, pool, error))


def delete_snap(snap, zfsurl, zauth):
    """Delete Snapshots specified in csv file"""
    pool, project, filesystem, snapname = snap
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}/"
               "snapshots/{}".format(zfsurl, pool, project, filesystem,
                                     snapname))
    try:
        req = requests.delete(fullurl, auth=zauth, verify=False,
                              headers=HEADER)
        req.close()
        req.raise_for_status()
        return False, ("DELETE - SUCCESS - snapshot '{}' filesystem '{}' "
                       "project '{}' pool '{}'"
                       .format(snapname, filesystem, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("DELETE - FAIL - snapshot '{}' filesystem '{}' project '{}'"
                 "pool '{}' - Error {}".format(snapname, filesystem, project,
                                               pool, error))
        else:
            return True, ("DELETE - FAIL - snapshot '{}' filesystem '{}' "
                          "project '{}' pool '{}' - Error {}"
                          .format(snapname, filesystem, project, pool, error))
    except ConnectionError as error:
        return True, ("DELETE - FAIL - snapshot '{}' filesystem '{}' project "
                      "'{}' pool '{}' - Error {}"
                      .format(snapname, filesystem, project, pool, error))


def run_fs_snaps(args):
    """Run all filesystems snapshots actions"""
    csvfile = args.file
    listsnaps = args.list
    createsnaps = args.create
    deletesnaps = args.delete
    snaplist = read_snap_file(csvfile)
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
