"""Update functions"""
import json
from six.moves import input
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
from zfssa_utils.common import (HEADER, read_csv_file, read_yaml_file,
                                createprogress, CreateLogger, UPDATELOGFILE,
                                msgdeco, COLORGREEN, COLORRED, RESETCOLOR)

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)


def update_component(component_type, fullurl, zauth, timeout, data, verify,
                     project=None, pool=None, filesystem=None, lun=None):
    """Update every component passed."""
    project, pool, filesystem, lun = project, pool, filesystem, lun
    stringdata = ""
    for k in data:
        stringdata += "{} '{}' ".format(k, data[k])
    if component_type == 'project':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=verify, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, msgdeco('FAIL', 'UPDATE', "project '{}' pool "
                                         "'{}' - Error \"{}\" - updates: {}"
                                         .format(project, pool,
                                                 j['fault']['message'],
                                                 stringdata))
            req.close()
            req.raise_for_status()
            return False, msgdeco('SUCCESS', 'UPDATE', "project '{}' pool '{}'"
                                  " - updates: {}"
                                  .format(project, pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, msgdeco('FAIL', 'UPDATE', "project '{}' pool '{}'"
                                     " - Error \"{}\" - updates: {}"
                                     .format(project, pool, error, stringdata))
            return True, msgdeco('FAIL', 'UPDATE', "project '{}' pool '{}' - "
                                 "Error \"{}\" - updates: {}"
                                 .format(project, pool, error, stringdata))
        except ConnectionError as error:
            return True, msgdeco('FAIL', 'UPDATE', "project '{}' pool '{}' - "
                                 "Error \"{}\" - updates: {}"
                                 .format(project, pool, error, stringdata))

    elif component_type == 'filesystem':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=verify, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, msgdeco('FAIL', 'UPDATE', "filesystem '{}' "
                                         "project '{}' pool '{}' - Error "
                                         "\"{}\" - updates: {}"
                                         .format(filesystem, project, pool,
                                                 j['fault']['message'],
                                                 stringdata))
            req.close()
            req.raise_for_status()
            return False, msgdeco('SUCCESS', 'UPDATE', "filesystem '{}' "
                                  "project '{}' pool '{}' - updates: {}"
                                  .format(filesystem, project,
                                          pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, msgdeco('FAIL', 'UPDATE', "filesystem '{}' "
                                     "project '{}' pool '{}' - Error \"{}\" "
                                     "- updates: {}"
                                     .format(filesystem, project, pool, error,
                                             stringdata))
            return True, msgdeco('FAIL', 'UPDATE', "filesystem '{}' project "
                                 "'{}' pool '{}' - Error \"{}\"  - updates: {}"
                                 .format(filesystem, project, pool, error,
                                         stringdata))
        except ConnectionError as error:
            return True, msgdeco('FAIL', 'UPDATE', "filesystem '{}' project "
                                 "'{}' pool '{}' - Error \"{}\" - updates: {}"
                                 .format(filesystem, project, pool, error,
                                         stringdata))

    elif component_type == 'lun':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=verify, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, msgdeco('FAIL', 'UPDATE', "lun '{}' project "
                                         "'{}' pool '{}' - Error \"{}\" - "
                                         "updates: {}"
                                         .format(lun, project, pool,
                                                 j['fault']['message'],
                                                 stringdata))
            req.close()
            req.raise_for_status()
            return False, msgdeco('SUCCESS', 'UPDATE', "lun '{}' project '{}' "
                                  "pool '{}' - updates: {}"
                                  .format(lun, project, pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, msgdeco('FAIL', 'UPDATE', "lun '{}' project '{}' "
                                     "pool '{}' - Error \"{}\" - updates: {}"
                                     .format(lun, project, pool,
                                             error, stringdata))
            return True, msgdeco('FAIL', 'UPDATE', "lun '{}' project '{}' pool"
                                 " '{}' - Error \"{}\" - updates: {}"
                                 .format(lun, project, pool,
                                         error, stringdata))
        except ConnectionError as error:
            return True, msgdeco('FAIL', 'UPDATE', "lun '{}' project '{}' pool"
                                 " '{}' - Error \"{}\" - updates: {}"
                                 .format(lun, project, pool,
                                         error, stringdata))
    else:
        return True, msgdeco('FAIL', 'UPDATE', "Wrong component type '{}'"
                             .format(component_type))


def noconfirm_update(noconfirm, update_list):
    """Ask for confirmation to continue or exit program."""
    if noconfirm:
        pass
    else:
        print("You are about to modify/update")
        print("=" * 79)
        print("{:15} {:30} {}"
              .format("TYPE", "NAME:PROJECT:POOL",
                      "keyx: valx , keyx+1: valx+1, ..."))
        print("=" * 79)
        for item in update_list:
            comp_type, comp = item[:2]
            changes = item[2:]
            print("{:15} {:30} {}"
                  .format(comp_type, comp.replace(';', ':'),
                          str(changes).replace(';', ': ')))
        print("=" * 79)
        response = input("Do you want to proceed (y/N)")
        if response == "Y" or response == "y":
            pass
        else:
            exit("Not confirmed, Exiting program")


def run_updates(args):
    """Update component based on a csv file with the following format.

    "component type", "name;project;pool", "key;value" ...

    Examples:
    project,-;projname;pool,key1;val1,key2;val2
    lun,lunname;projname;pool,key1;val1,key2;val2
    fs,fsname;projname;pool,key1;val1,key2;val2

    For projects the second col (name) is hyphen('-').
    """
    datafile = args.file
    timeout = args.timeout
    verify = args.cert
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    initial = 0  # for progressbar
    updates = read_csv_file(datafile)
    if args.progress:
        noconfirm_update(args.noconfirm, updates)
        progbar = createprogress(len(updates))
        logger = CreateLogger(UPDATELOGFILE)
        for item in updates:
            changes = item[2:]
            data = {}
            if item[0] == 'project':
                _, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}"
                           .format(zfsurl, pool, project))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                err, msg = update_component('project', fullurl, zauth, timeout,
                                            data, verify, project=project,
                                            pool=pool)
                if err:
                    logger.warning(msg.replace(COLORRED, "")
                                   .replace(RESETCOLOR, ""))
                else:
                    logger.info(msg.replace(COLORGREEN, "")
                                .replace(RESETCOLOR, ""))
                initial += 1
                progbar.update(initial)

            elif item[0] == 'filesystem':
                filesystem, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}"
                           .format(zfsurl, pool, project, filesystem))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                err, msg = update_component('project', fullurl, zauth, timeout,
                                            data, verify, project=project,
                                            pool=pool)
                if err:
                    logger.warning(msg.replace(COLORRED, "")
                                   .replace(RESETCOLOR, ""))
                else:
                    logger.info(msg.replace(COLORGREEN, "")
                                .replace(RESETCOLOR, ""))
                initial += 1
                progbar.update(initial)

            elif item[0] == 'lun':
                lun, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
                           .format(zfsurl, pool, project, lun))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                err, msg = update_component('lun', fullurl, zauth, timeout,
                                            data, verify, project=project,
                                            pool=pool, lun=lun)
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
        noconfirm_update(args.noconfirm, updates)
        for item in updates:
            changes = item[2:]
            data = {}
            if item[0] == 'project':
                _, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}"
                           .format(zfsurl, pool, project))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                print("#" * 79)
                print("Updating project")
                print("#" * 79)
                print(update_component('project', fullurl, zauth, timeout,
                                       data, verify, project=project,
                                       pool=pool)[1])
                print("=" * 79)

            elif item[0] == 'filesystem':
                filesystem, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}/filesystems/{}"
                           .format(zfsurl, pool, project, filesystem))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                print("#" * 79)
                print("Updating filesystem")
                print("#" * 79)
                print(update_component('filesystem', fullurl, zauth, timeout,
                                       data, verify, project=project,
                                       pool=pool, filesystem=filesystem)[1])
                print("=" * 79)

            elif item[0] == 'lun':
                lun, project, pool = item[1].split(';')
                fullurl = ("{}/storage/v1/pools/{}/projects/{}/luns/{}"
                           .format(zfsurl, pool, project, lun))
                for entry in changes:
                    key, value = entry.split(';')
                    data[key] = value
                print("#" * 79)
                print("Updating lun")
                print("#" * 79)
                print(update_component('lun', fullurl, zauth, timeout, data,
                                       verify, project=project, pool=pool,
                                       lun=lun)[1])
                print("=" * 79)

            else:
                print("Wrong type in file format.")
