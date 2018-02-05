"""Filesystems functions

Functions to create, list/show and delete filesystems.
"""
from __future__ import print_function, division
import json
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import HEADER, response_size, read_yaml_file, \
     read_csv_file, createprogress, createlogger, FSLOGFILE

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def list_filesystems(fileline, zfsurl, zauth):
    """List/Show filesystems from line in csv format. (err, msg)"""
    # print(fileline)
    pool = project = fs = None
    if len(fileline) == 3:
        pool, project, fs = fileline
    elif len(fileline) == 18:
        pool, project, fs, _, _, _, _, _, _, _, \
            _, _, _, _, _, _, _, _, = fileline
    else:
        return True, ("LIST - FAIL - Error in line {} It needs to be 3 or 18 "
                      "columns long".format(fileline))
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}"
               .format(zfsurl, pool, project, fs))
    # print(fullurl)
    try:
        req = requests.get(fullurl, auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        # print(json.dumps(j))
        req.close()
        req.raise_for_status()
        return False, ("LIST - PRESENT - filesystem '{}' project '{}' pool "
                       "'{}' mountpoint '{}' quota '{}' reservation '{}' "
                       "compression '{}' dedup '{}' logbias '{}' nodestroy "
                       "'{}' recordsize '{}' readonly '{}' atime '{}' "
                       "root_user '{}' root_group '{}' root_permissions '{}' "
                       "sharenfs '{}' sharesmb '{}'"
                       .format(j['filesystem']['name'],
                               j['filesystem']['project'],
                               j['filesystem']['pool'],
                               j['filesystem']['mountpoint'],
                               response_size(j['filesystem']['quota']),
                               response_size(j['filesystem']['reservation']),
                               j['filesystem']['compression'],
                               j['filesystem']['dedup'],
                               j['filesystem']['logbias'],
                               j['filesystem']['nodestroy'],
                               response_size(j['filesystem']['recordsize']),
                               j['filesystem']['readonly'],
                               j['filesystem']['atime'],
                               j['filesystem']['root_user'],
                               j['filesystem']['root_group'],
                               j['filesystem']['root_permissions'],
                               j['filesystem']['sharenfs'],
                               j['filesystem']['sharesmb']))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("LIST - FAIL - filesystem '{}' project '{}', pool '{}' "
                 "- Error {}".format(fs, project, pool, error))
        else:
            return True, ("LIST - FAIL - filesystem '{}' project '{}' pool "
                          "'{}' - Error {}".format(fs, project, pool, error))
    except ConnectionError as error:
        return True, ("LIST - FAIL - fileystem '{}' project '{}' pool '{}' "
                      "- Error {}".format(fs, project, pool, error))


def create_filesystems(fileline, zfsurl, zauth):
    """Create Filesystems from line in csv format. (err, msg)"""
    if len(fileline) != 18:
        return True, ("CREATE - FAIL - Error in line {} It needs to be 18"
                      " columns long".format(fileline))
    pool, project, fs, mountpoint, quota, reservation, compression, dedup, \
        logbias, nodestroy, recordsize, readonly, atime, root_user, \
        root_group, root_permissions, sharenfs, sharesmb = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems"
               .format(zfsurl, pool, project))
    try:
        data = {"name": fs,
                "mountpoint": mountpoint,
                "quota": quota,
                "reservation": reservation,
                "compression": compression,
                "dedup": dedup,
                "logbias": logbias,
                "nodestroy": nodestroy,
                "recordsize": recordsize,
                "readonly": readonly,
                "atime": atime,
                "root_user": root_user,
                "root_group": root_group,
                "root_permissions": root_permissions,
                "sharenfs": sharenfs,
                "sharesmb": sharesmb}
        if quota == 'None' and reservation == 'None':
            del data["quota"]
            del data["reservation"]
        elif quota == 'None':
            del data["quota"]
        elif reservation == 'None':
            del data["reservation"]
        req = requests.post(fullurl, data=json.dumps(data),
                            auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, ("CREATE - FAIL - filesystem '{}' project '{}' "
                              "pool '{}' - Error {}"
                              .format(fs, project, pool,
                                      j['fault']['message']))
        req.close()
        req.raise_for_status()
        return False, ("CREATE - SUCCESS - filesystem '{}' project '{}' pool "
                       "'{}'".format(fs, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("CREATE - FAIL - filesystem '{}' project '{}' pool '{}' - "
                 "Error {}".format(fs, project, pool, error))
        else:
            return True, ("CREATE - FAIL - filesystem '{}' project '{}' pool "
                          "'{}' - Error {}".format(fs, project, pool, error))
    except ConnectionError as error:
        return True, ("CREATE - FAIL - filesystem '{}' project '{}' pool '{}' "
                      "- Error {}".format(fs, project, pool, error))


def delete_filesystems(fileline, zfsurl, zauth):
    """Delete filesystem from line in csv format. (err, msg)"""
    if len(fileline) != 3:
        return True, ("DELETE - FAIL - Error in line {} It needs to be 3 "
                      "columns long".format(fileline))
    pool, project, fs = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}"
               .format(zfsurl, pool, project, fs))
    try:
        req = requests.delete(fullurl, auth=zauth,
                              verify=False, headers=HEADER)
        req.close()
        req.raise_for_status()
        return False, ("DELETE - SUCCESS - filesystem '{}' project '{}' pool "
                       "'{}'".format(fs, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("DELETE - FAIL - filesystem '{}' project '{}' pool '{}' - "
                 "Error {}".format(fs, project, pool, error))
        else:
            return True, ("DELETE - FAIL - filesystem '{}' project '{}' pool "
                          "'{}' - Error {}".format(fs, project, pool, error))
    except ConnectionError as error:
        return True, ("DELETE - FAIL - filesystem '{}' project '{}' pool '{}' "
                      "- Error {}".format(fs, project, pool, error))


def run_filesystems(args):
    """Run all projects actions"""
    csvfile = args.file
    listfs = args.list
    createfs = args.create
    deletefs = args.delete
    fslistfromfile = read_csv_file(csvfile)
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    initial = 0  # for progressbar
    if createfs:
        if args.progress:
            progbar = createprogress(len(fslistfromfile))
            logger = createlogger(FSLOGFILE)
            for entry in fslistfromfile:
                err, msg = create_filesystems(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Creating filesystems")
            print("#" * 79)
            for entry in fslistfromfile:
                print(create_filesystems(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif deletefs:
        if args.progress:
            progbar = createprogress(len(fslistfromfile))
            logger = createlogger(FSLOGFILE)
            for entry in fslistfromfile:
                err, msg = delete_filesystems(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Deleting filesystems")
            print("#" * 79)
            for entry in fslistfromfile:
                print(delete_filesystems(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif listfs:
        if args.progress:
            progbar = createprogress(len(fslistfromfile))
            logger = createlogger(FSLOGFILE)
            for entry in fslistfromfile:
                err, msg = list_filesystems(entry, zfsurl, zauth)
                initial += 1
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Listing filesystems")
            print("#" * 79)
            for entry in fslistfromfile:
                print(list_filesystems(entry, zfsurl, zauth)[1])
                print("=" * 79)
