"""LUNS functions

Functions to create, list/show and delete luns.
"""
from __future__ import print_function, division
import json
import ast
from six.moves import input
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import (HEADER, response_size, createprogress,
                                CreateLogger, read_yaml_file,
                                read_csv_file, LUNLOGFILE, msgdeco, COLORGREEN,
                                COLORRED, RESETCOLOR)

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def list_lun(fileline, zfsurl, zauth, timeout, verify):
    """List/Show lun from line in csv format. (err, msg)"""
    pool = project = lun = None
    if len(fileline) == 3:
        pool, project, lun = fileline
    elif len(fileline) == 11:
        pool, project, lun, _, _, _, _, _, _, _, _ = fileline
    else:
        return True, msgdeco('FAIL', 'LIST',
                             'Error in line {} It needs to be '
                             '3 or 11 columns long'.format(fileline))
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
               .format(zfsurl, pool, project, lun))
    try:
        req = requests.get(fullurl, auth=zauth, verify=verify, headers=HEADER,
                           timeout=timeout)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'LIST',
                              "lun '{}' project '{}' pool "
                              "'{}' assigned number '{}' initiatorgroup '{}'"
                              " volsize '{}' volblocksize '{}' status '{}' "
                              "space_total '{}' lunguid '{}' logbias '{}' "
                              "creation '{}' thin '{}' nodestroy '{}'"
                              .format(j["lun"]["name"], j["lun"]["project"],
                                      j["lun"]["pool"],
                                      j["lun"]["assignednumber"],
                                      j["lun"]["initiatorgroup"],
                                      response_size(j["lun"]["volsize"]),
                                      response_size(j["lun"]["volblocksize"]),
                                      j["lun"]["status"],
                                      response_size(j["lun"]["space_total"]),
                                      j["lun"]["lunguid"], j["lun"]["logbias"],
                                      j["lun"]["creation"], j["lun"]["sparse"],
                                      j["lun"]["nodestroy"]))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL ', 'LIST',
                                 "lun '{}' project '{}' pool '{}' - Error "
                                 "\"{}\"".format(lun, project, pool, error))
        return True, msgdeco('FAIL', 'LIST', "lun '{}' project '{}' pool '{}' "
                             "- Error \"{}\""
                             .format(lun, project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'LIST', "lun '{}' project '{}' pool '{}'"
                             " - Error \"{}\""
                             .format(lun, project, pool, error))


def create_lun(fileline, zfsurl, zauth, timeout, verify):
    """Create LUN from line in csv format. (err, msg)"""
    if len(fileline) != 11:
        return True, msgdeco('FAIL', 'CREATE', "Error in line {} It needs to "
                             "be 11 columns long".format(fileline))
    pool, project, lun, volsize, volblocksize, thin, targetgroup, \
        initiatorgroup, compression, latency, nodestroy = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns"
               .format(zfsurl, pool, project))
    try:
        data = {"name": lun,
                "volsize": volsize,
                "volblocksize": volblocksize,
                "sparse": ast.literal_eval(thin),
                "targetgroup": targetgroup,
                "initiatorgroup": initiatorgroup,
                "compression": compression,
                "logbias": latency,
                "nodestroy": ast.literal_eval(nodestroy)}
        req = requests.post(fullurl, data=json.dumps(data),
                            auth=zauth, verify=verify, headers=HEADER,
                            timeout=timeout)
        j = json.loads(req.text)
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, msgdeco('FAIL', 'CREATE', "lun '{}' project '{}' "
                                     "pool '{}' - Error \"{}\""
                                     .format(lun, project, pool,
                                             j['fault']['message']))
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'CREATE', "lun '{}' project '{}' pool"
                              " '{}'".format(lun, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL', 'CREATE', "lun '{}' project '{}' pool"
                                 " '{}' - Error \"{}\""
                                 .format(lun, project, pool, error))
        return True, msgdeco('FAIL', 'CREATE', "lun '{}' project '{}' pool "
                             "'{}' - Error \"{}\""
                             .format(lun, project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'CREATE', "lun '{}' project '{}' pool "
                             "'{}' - Error \"{}\""
                             .format(lun, project, pool, error))


def delete_lun(fileline, zfsurl, zauth, timeout, verify):
    """Delete lun from line in csv format. (err, msg)"""
    if len(fileline) != 3:
        return True, msgdeco('FAIL', 'DELETE', "Error in line {} It needs to "
                             "be 3 columns long".format(fileline))
    pool, project, lun = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
               .format(zfsurl, pool, project, lun))
    try:
        req = requests.delete(fullurl, auth=zauth,
                              verify=verify, headers=HEADER, timeout=timeout)
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'DELETE', "lun '{}' project '{}' pool"
                              " '{}'".format(lun, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL', 'DELETE', "lun '{}' project '{}' pool"
                                 " '{}' - Error \"{}\""
                                 .format(lun, project, pool, error))
        return True, msgdeco('FAIL', 'DELETE', "lun '{}' project '{}' pool "
                             "'{}' - Error \"{}\""
                             .format(lun, project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'DELETE', "lun '{}' project '{}' pool "
                             "'{}' - Error \"{}\""
                             .format(lun, project, pool, error))


def run_luns(args):
    """Run all luns actions"""
    csvfile = args.file
    listlun = args.list
    createlun = args.create
    deletelun = args.delete
    timeout = args.timeout
    verify = args.cert
    lunlistfromfile = read_csv_file(csvfile)
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    initial = 0
    if createlun:
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = CreateLogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = create_lun(entry, zfsurl, zauth, timeout, verify)
                if err:
                    logger.warning(msg.replace(COLORRED, "")
                                   .replace(RESETCOLOR, ""))
                else:
                    logger.info(msg.replace(COLORGREEN, "")
                                .replace(RESETCOLOR, ""))
                initial += 1
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Creating luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(create_lun(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
    elif deletelun:
        if not args.noconfirm:
            print("You are about to destroy")
            print("=" * 45)
            print("{:15}{:15}{:15}".format("Pool", "Project", "Lun"))
            print("-" * 45)
            for entry in lunlistfromfile:
                print("{:15}{:15}{:15}".format(entry[0], entry[1], entry[2]))
            print("=" * 45)
            response = input("Do you want to destroy (y/N)")
            if response == "Y" or response == "y":
                pass
            else:
                exit("Not confirmed, Exiting program")
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = CreateLogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = delete_lun(entry, zfsurl, zauth, timeout, verify)
                if err:
                    logger.warning(msg.replace(COLORRED, "")
                                   .replace(RESETCOLOR, ""))
                else:
                    logger.info(msg.replace(COLORGREEN, "")
                                .replace(RESETCOLOR, ""))
                initial += 1
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Deleting luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(delete_lun(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
    elif listlun:
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = CreateLogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = list_lun(entry, zfsurl, zauth, timeout, verify)
                if err:
                    logger.warning(msg.replace(COLORRED, "")
                                   .replace(RESETCOLOR, ""))
                else:
                    logger.info(msg.replace(COLORGREEN, "")
                                .replace(RESETCOLOR, ""))
                initial += 1
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Listing luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(list_lun(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
