"""LUNS functions

Functions to create, list/show and delete luns.
"""
from __future__ import print_function, division
import json
import ast
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import HEADER, response_size, get_real_size,\
     get_real_blocksize, createprogress, createlogger, read_yaml_file,\
     read_csv_file, LUNLOGFILE

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def list_lun(fileline, zfsurl, zauth):
    """List/Show lun from line in csv format. (err, msg)"""
    pool = project = lun = None
    if len(fileline) == 3:
        pool, project, lun = fileline
    elif len(fileline) == 12:
        pool, project, lun, _, _, _, _, _, _, _, _, _ = fileline
    else:
        return True, ("LIST - FAIL - Error in line {} It needs to be 3 or 12"
                      " columns long".format(fileline))
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
               .format(zfsurl, pool, project, lun))
    try:
        req = requests.get(fullurl, auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        return False, ("LIST - PRESENT - name '{}' project '{}' pool '{}' "
                       "assigned number '{}' initiatorgroup '{}' volsize '{}' "
                       "volblocksize '{}' status '{}' space_total '{}' lunguid"
                       " '{}' logbias '{}' creation '{}' thin '{}' nodestroy "
                       "'{}'".format(j["lun"]["name"], j["lun"]["project"],
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
            exit("LIST - FAIL - lun '{}' project '{}' pool '{}' - Error {}"
                 .format(lun, project, pool, error))
        else:
            return True, ("LIST - FAIL - lun '{}' project '{}' pool '{}' - "
                          "Error {}".format(lun, project, pool, error))
    except ConnectionError as error:
        return True, ("LIST - FAIL - lun '{}' project '{}' pool '{}' - Error "
                      "{}".format(lun, project, pool, error))


def create_lun(fileline, zfsurl, zauth):
    """Create LUN from line in csv format. (err, msg)"""
    if len(fileline) != 12:
        return True, ("CREATE - FAIL - Error in line {} It needs to be 12 "
                      "columns long".format(fileline))
    pool, project, lun, size, size_unit, blocksize, thin, targetgroup, \
        initiatorgroup, compression, latency, nodestroy = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns"
               .format(zfsurl, pool, project))
    converted_size = get_real_size(size, size_unit)
    real_blocksize = get_real_blocksize(blocksize)
    try:
        data = {"name": lun,
                "volsize": converted_size,
                "volblocksize": real_blocksize,
                "sparse": ast.literal_eval(thin),
                "targetgroup": targetgroup,
                "initiatorgroup": initiatorgroup,
                "compression": compression,
                "logbias": latency,
                "nodestroy": ast.literal_eval(nodestroy)}
        req = requests.post(fullurl, data=json.dumps(data),
                            auth=zauth, verify=False, headers=HEADER)
        j = json.loads(req.text)
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, ("CREATE - FAIL - lun '{}' project '{}' pool '{}'"
                              " - Error {}".format(lun, project, pool,
                                                   j['fault']['message']))
        req.close()
        req.raise_for_status()
        return False, ("CREATE - SUCCESS - lun '{}' project '{}' pool '{}'"
                       .format(lun, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("CREATE - FAIL - lun '{}' project '{}' pool '{}' - Error {}"
                 .format(lun, project, pool, error))
        else:
            return True, ("CREATE - FAIL - lun '{}' project '{}' pool '{}' - "
                          "Error {}".format(lun, project, pool, error))
    except ConnectionError as error:
        return True, ("CREATE - FAIL - lun '{}' project '{}' pool '{}' - Error"
                      " {}".format(lun, project, pool, error))


def delete_lun(fileline, zfsurl, zauth):
    """Delete lun from line in csv format. (err, msg)"""
    if len(fileline) != 3:
        return True, ("DELETE - FAIL - Error in line {} It needs to be 3 "
                      "columns long".format(fileline))
    pool, project, lun = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
               .format(zfsurl, pool, project, lun))
    try:
        req = requests.delete(fullurl, auth=zauth,
                              verify=False, headers=HEADER)
        req.close()
        req.raise_for_status()
        return False, ("DELETE - SUCCESS - lun '{}' project '{}' pool '{}'"
                       .format(lun, project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            exit("DELETE - FAIL - lun '{}' project '{}' pool '{}' - Error {}"
                 .format(lun, project, pool, error))
        else:
            return True, ("DELETE - FAIL - lun '{}' project '{}' pool '{}' - "
                          "Error {}".format(lun, project, pool, error))
    except ConnectionError as error:
        return True, ("DELETE - FAIL - lun '{}' project '{}' pool '{}' - Error"
                      " {}".format(lun, project, pool, error))


def run_luns(args):
    """Run all luns actions"""
    csvfile = args.file
    listlun = args.list
    createlun = args.create
    deletelun = args.delete
    lunlistfromfile = read_csv_file(csvfile)
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    initial = 0
    if createlun:
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = createlogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = create_lun(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Creating luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(create_lun(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif deletelun:
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = createlogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = delete_lun(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Deleting luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(delete_lun(entry, zfsurl, zauth)[1])
                print("=" * 79)
    elif listlun:
        if args.progress:
            progbar = createprogress(len(lunlistfromfile))
            logger = createlogger(LUNLOGFILE)
            for entry in lunlistfromfile:
                err, msg = list_lun(entry, zfsurl, zauth)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
        else:
            print("#" * 79)
            print("Listing luns")
            print("#" * 79)
            for entry in lunlistfromfile:
                print(list_lun(entry, zfsurl, zauth)[1])
                print("=" * 79)
    else:
        print("#" * 79)
        print("You need to specify an option (--list, --create, --delete)")
        print("#" * 79)
    # delta = datetime.now() - START
    # print("Finished in {} seconds".format(delta.seconds))
