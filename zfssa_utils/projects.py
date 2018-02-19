"""Projects functions

Functions to create, list/show and delete projects.
"""
from __future__ import print_function, division
import json
from six.moves import input
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import (HEADER, response_size, read_yaml_file,
                                read_csv_file, createprogress, CreateLogger,
                                PROJECTLOGFILE, msgdeco)

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def list_projects(fileline, zfsurl, zauth, timeout, verify):
    """List/Show projects from line in csv format. (err, msg)"""
    pool = project = None
    if len(fileline) == 2:
        pool, project = fileline
    elif len(fileline) == 19:
        pool, project, _, _, _, _, _, _, _, _, \
            _, _, _, _, _, _, _, _, _ = fileline
    else:
        return True, msgdeco('FAIL', 'LIST', "Error in line {} It needs to be "
                             "2 or 19 columns long".format(fileline))
    fullurl = ("{}/storage/v1/pools/{}/projects/{}"
               .format(zfsurl, pool, project))
    try:
        req = requests.get(fullurl, auth=zauth, verify=verify, headers=HEADER,
                           timeout=timeout)
        j = json.loads(req.text)
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'LIST', "PRESENT - project '{}' pool "
                              "'{}' mountpoint '{}' quota '{}' reservation "
                              "'{}' compression '{}' dedup '{}' logbias '{}'"
                              " nodestroy '{}' recordsize '{}' readonly '{}' "
                              "atime '{}' def_sparse '{}' def_user '{}' "
                              "def_group '{}' def_perms '{}' def_volblocksize "
                              "'{}' def_volsize '{}' sharenfs '{}' sharesmb "
                              "'{}'"
                              .format(j["project"]["name"],
                                      j["project"]["pool"],
                                      j["project"]["mountpoint"],
                                      response_size(j["project"]["quota"]),
                                      response_size(j["project"]
                                                    ["reservation"]),
                                      j["project"]["compression"],
                                      j["project"]["dedup"],
                                      j["project"]["logbias"],
                                      j["project"]["nodestroy"],
                                      response_size(j["project"]
                                                    ["recordsize"]),
                                      j["project"]["readonly"],
                                      j["project"]["atime"],
                                      j["project"]["default_sparse"],
                                      j["project"]["default_user"],
                                      j["project"]["default_group"],
                                      j["project"]["default_permissions"],
                                      response_size(j["project"]
                                                    ["default_volblocksize"]),
                                      response_size(j["project"]
                                                    ["default_volsize"]),
                                      j["project"]["sharenfs"],
                                      j["project"]["sharesmb"]))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL', 'LIST', "project '{}', pool '{}' - "
                                 "Error \"{}\"".format(project, pool, error))
        return True, msgdeco('FAIL', 'list', "project '{}' pool '{}' - Error "
                             "\"{}\"".format(project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'LIST', "project '{}' pool '{}' - Error "
                             "\"{}\"".format(project, pool, error))


def create_project(fileline, zfsurl, zauth, timeout, verify):
    """Create Project from line in csv format. (err, msg)"""
    if len(fileline) != 19:
        return True, msgdeco('FAIL', 'CREATE', "Error in line {} It needs to "
                             "be 19 columns long".format(fileline))
    pool, project, mountpoint, quota, reservation, compression, \
        logbias, nodestroy, recordsize, readonly, atime, default_sparse, \
        default_user, default_group, default_permissions, \
        default_volblocksize, default_volsize, sharenfs, \
        sharesmb = fileline
    fullurl = "{}/storage/v1/pools/{}/projects".format(zfsurl, pool)
    try:
        data = {"name": project,
                "mountpoint": mountpoint,
                "quota": quota,
                "reservation": reservation,
                "compression": compression,
                "logbias": logbias,
                "nodestroy": nodestroy,
                "recordsize": recordsize,
                "readonly": readonly,
                "atime": atime,
                "default_sparse": default_sparse,
                "default_user": default_user,
                "default_group": default_group,
                "default_permissions": default_permissions,
                "default_volblocksize": default_volblocksize,
                "default_volsize": default_volsize,
                "sharenfs": sharenfs,
                "sharesmb": sharesmb}
        req = requests.post(fullurl, data=json.dumps(data),
                            auth=zauth, verify=verify, headers=HEADER,
                            timeout=timeout)
        j = json.loads(req.text)
        if 'fault' in j:
            if 'message' in j['fault']:
                return True, msgdeco('FAIL', 'CREATE', "project '{}' pool '{}'"
                                     " - Error \"{}\""
                                     .format(project, pool,
                                             j['fault']['message']))
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'CREATE', "project '{}' pool '{}'"
                              .format(project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL', 'CREATE', "project '{}' pool '{}' - "
                                 "Error \"{}\"".format(project, pool, error))
        return True, msgdeco('FAIL', 'CREATE', "project '{}' pool '{}' - Error"
                             " \"{}\"".format(project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'CREATE', "project '{}' pool '{}' - Error"
                             " \"{}\"".format(project, pool, error))


def delete_project(fileline, zfsurl, zauth, timeout, verify):
    """Delete project from line in csv format. (err, msg)"""
    if len(fileline) != 2:
        return True, msgdeco('FAIL', 'DELETE', "Error in line {} It needs to "
                             "be 2 columns long".format(fileline))
    pool, project = fileline
    fullurl = ("{}/storage/v1/pools/{}/projects/{}"
               .format(zfsurl, pool, project))
    try:
        req = requests.delete(fullurl, auth=zauth,
                              verify=verify, headers=HEADER,
                              timeout=timeout)
        req.close()
        req.raise_for_status()
        return False, msgdeco('SUCCESS', 'DELETE', "project '{}' pool '{}'"
                              .format(project, pool))
    except HTTPError as error:
        if error.response.status_code == 401:
            return True, msgdeco('FAIL', 'DELETE', "project '{}' pool '{}' - "
                                 "Error \"{}\"".format(project, pool, error))
        return True, msgdeco('FAIL', 'DELETE', "project '{}' pool '{}' - Error"
                             " \"{}\"".format(project, pool, error))
    except ConnectionError as error:
        return True, msgdeco('FAIL', 'DELETE', "DELETE - FAIL - project '{}' "
                             "pool '{}' - Error \"{}\""
                             .format(project, pool, error))


def run_projects(args):
    """Run all projects actions"""
    csvfile = args.file
    listprojects = args.list
    createproject = args.create
    deleteproject = args.delete
    timeout = args.timeout
    verify = args.cert
    projectlistfromfile = read_csv_file(csvfile)
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    initial = 0  # for progressbar
    if createproject:
        if args.progress:
            progbar = createprogress(len(projectlistfromfile))
            logger = CreateLogger(PROJECTLOGFILE)
            for entry in projectlistfromfile:
                err, msg = create_project(entry, zfsurl,
                                          zauth, timeout,
                                          verify)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Creating projects")
            print("#" * 79)
            for entry in projectlistfromfile:
                print(create_project(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
    elif deleteproject:
        if not args.noconfirm:
            print("You are about to destroy")
            print("=" * 30)
            print("{:15}{:15}".format("Pool", "Project"))
            print("-" * 30)
            for entry in projectlistfromfile:
                print("{:15}{:15}".format(entry[0], entry[1]))
            print("=" * 30)
            response = input("Do you want to destroy (y/N)")
            if response == "Y" or response == "y":
                pass
            else:
                exit("Not confirmed, Exiting program")
        if args.progress:
            progbar = createprogress(len(projectlistfromfile))
            logger = CreateLogger(PROJECTLOGFILE)
            for entry in projectlistfromfile:
                err, msg = delete_project(entry, zfsurl,
                                          zauth, timeout,
                                          verify)
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                initial += 1
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Deleting projects")
            print("#" * 79)
            for entry in projectlistfromfile:
                print(delete_project(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
    elif listprojects:
        if args.progress:
            progbar = createprogress(len(projectlistfromfile))
            logger = CreateLogger(PROJECTLOGFILE)
            for entry in projectlistfromfile:
                err, msg = list_projects(entry, zfsurl, zauth, timeout, verify)
                initial += 1
                if err:
                    logger.warning(msg)
                else:
                    logger.info(msg)
                progbar.update(initial)
            progbar.finish()
            logger.shutdown()
        else:
            print("#" * 79)
            print("Listing projects")
            print("#" * 79)
            for entry in projectlistfromfile:
                print(list_projects(entry, zfsurl, zauth, timeout, verify)[1])
                print("=" * 79)
