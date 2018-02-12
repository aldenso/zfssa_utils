"""Common functions"""
import argparse
import logging
import csv
import json
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.exceptions import InsecureRequestWarning
import yaml
from progressbar import ProgressBar, AdaptiveETA, Bar, Percentage

# to disable warning
# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised. See:
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
requests.urllib3.disable_warnings(InsecureRequestWarning)

HEADER = {"Content-Type": "application/json"}
# TIMEOUT = 100  # seconds
PROJECTLOGFILE = "projects_output.log"
LUNLOGFILE = "luns_output.log"
SNAPLOGFILE = "snaps_output.log"
FSLOGFILE = "filesystems_output.log"


def read_yaml_file(configfile):
    """Read config file and return credentials in json."""
    config = {}
    with open(configfile, 'r') as configuration:
        try:
            config = yaml.load(configuration)
        except yaml.YAMLError as error:
            print("Error in configuration file: {}").format(error)
        return config


def read_csv_file(filename):
    """Read csv file and return the list"""
    csvlist = []
    with open(filename, 'r') as cvsfile:
        filereader = csv.reader(cvsfile, delimiter=',')
        for row in filereader:
            if not row[0].startswith('#'):
                csvlist.append(row)
    # del csvlist[0]
    return csvlist


def response_size(nbytes):
    """Return size in a human readable format."""
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('{:.2f}'.format(nbytes)).rstrip('0').rstrip('.')
    return '{} {}'.format(f, suffixes[i])


def exists(data, key):
    """Return a value if does exists or return a hyphen (-) if not."""
    try:
        return data[key]
    except KeyError:
        return "-"


def fetch(url, zauth, header, timeout, datatype):
    """Fetch data from zfs api, returning a tuple (data, datatype)"""
    req = requests.get(url, timeout=timeout, auth=zauth,
                       verify=False, headers=header)
    data = req.json()
    return data, datatype


def createprogress(count):
    """Return progress Bar"""
    widgets = [Percentage(),
               ' ', Bar(),
               ' ', AdaptiveETA()]
    pbar = ProgressBar(widgets=widgets, maxval=count)
    pbar.start()
    return pbar


def create_parser():
    """
    Create program arguments parser.
    """

    desc = """Utils for ZFS Storage Appliance.
    This program allow you to generate zfssa general info csv files, manipulate
    or validate info for projects, luns and snapshots.
    """
    parser = argparse.ArgumentParser(description=desc)

    subparser = parser.add_subparsers(help='COMMANDS', dest='subparser_name')

    # Explorer arguments
    explorer_args = subparser.add_parser("EXPLORER")
    explorer_args.add_argument("-s", "--server", type=str, required=True,
                               help="Server config file (YAML)")
    explorer_args.add_argument("-p", "--progress", action="store_true",
                               help="progress bar", required=False)
    explorer_args.add_argument("-t", "--timeout", type=int,
                               help="connection timeout", required=False,
                               default=100)
    # Projects arguments
    proj_args = subparser.add_parser("PROJECTS")
    proj_args.add_argument("-f", "--file", type=str, required=True,
                           help="projects file (CSV)")
    proj_args.add_argument("-s", "--server", type=str, required=True,
                           help="Server config file (YAML)")
    proj_args.add_argument("-p", "--progress", action="store_true",
                           help="progress bar", required=False)
    proj_args.add_argument("--noconfirm", action="store_true",
                           help=("Don't ask for confirmation when deleting "
                                 "Projects"), required=False)
    proj_args.add_argument("-t", "--timeout", type=int,
                           help="connection timeout", required=False,
                           default=100)
    proj_opers = proj_args.add_mutually_exclusive_group(required=True)
    proj_opers.add_argument("--create", action="store_true",
                            help="Create Projects specified in csv file")
    proj_opers.add_argument("--delete", action="store_true",
                            help="Delete Projects specified in csv file")
    proj_opers.add_argument("--list", action="store_true",
                            help="List/Check Projects specified in csv file")

    # Filesystems arguments
    fs_args = subparser.add_parser("FILESYSTEMS")
    fs_args.add_argument("-f", "--file", type=str, required=True,
                         help="filesystems file (CSV)")
    fs_args.add_argument("-s", "--server", type=str, required=True,
                         help="Server config file (YAML)")
    fs_args.add_argument("-p", "--progress", action="store_true",
                         help="progress bar", required=False)
    fs_args.add_argument("--noconfirm", action="store_true",
                         help=("Don't ask for confirmation when deleting "
                               "Filesystems"), required=False)
    fs_args.add_argument("-t", "--timeout", type=int,
                         help="connection timeout", required=False,
                         default=100)
    fs_opers = fs_args.add_mutually_exclusive_group(required=True)
    fs_opers.add_argument("--create", action="store_true",
                          help="Create Filesystems specified in csv file")
    fs_opers.add_argument("--delete", action="store_true",
                          help="Delete Filesystems specified in csv file")
    fs_opers.add_argument("--list", action="store_true",
                          help="List/Check Filesystems specified in csv file")

    # LUNs arguments
    luns_args = subparser.add_parser('LUNS')
    luns_args.add_argument("-f", "--file", type=str, help="luns file (CSV)",
                           required=True)
    luns_args.add_argument("-s", "--server", type=str, required=True,
                           help="Server config file (YAML)")
    luns_args.add_argument("-p", "--progress", action="store_true",
                           help="progress bar", required=False)
    luns_args.add_argument("--noconfirm", action="store_true",
                           help=("Don't ask for confirmation when deleting "
                                 "Luns"), required=False)
    luns_args.add_argument("-t", "--timeout", type=int,
                           help="connection timeout", required=False,
                           default=100)
    luns_opers = luns_args.add_mutually_exclusive_group(required=True)
    luns_opers.add_argument("--create", action="store_true",
                            help="Create Luns specified in csv file")
    luns_opers.add_argument("--delete", action="store_true",
                            help="Delete Luns specified in csv file")
    luns_opers.add_argument("--list", action="store_true",
                            help="List/Check Luns specified in csv file")

    # Snapshots arguments
    snaps_args = subparser.add_parser('SNAPSHOTS')
    snaps_args.add_argument("-f", "--file", type=str, help="snaps file (CSV)",
                            required=True)
    snaps_args.add_argument("-s", "--server", type=str, required=True,
                            help="Server config file (YAML)")
    snaps_args.add_argument("-p", "--progress", action="store_true",
                            help="progress bar", required=False)
    snaps_args.add_argument("--noconfirm", action="store_true",
                            help=("Don't ask for confirmation when deleting "
                                  "Snapshots"), required=False)
    snaps_opers = snaps_args.add_mutually_exclusive_group(required=True)
    snaps_opers.add_argument("--create", action="store_true",
                             help="Create Snapshots specified in csv file")
    snaps_opers.add_argument("--delete", action="store_true",
                             help="Delete Snapshots specified in csv file")
    snaps_opers.add_argument("--list", action="store_true",
                             help="List/Check Snapshots specified in csv file")

    # Templates arguments
    template_args = subparser.add_parser("TEMPLATES")
    template_args.add_argument("--projects", action="store_true",
                               required=False,
                               help="generate template for projects")
    template_args.add_argument("--filesystems", action="store_true",
                               required=False,
                               help="generate template for filesystems")
    template_args.add_argument("--luns", action="store_true",
                               required=False,
                               help="generate template for luns")
    template_args.add_argument("--snapshots", action="store_true",
                               required=False,
                               help="generate template for snapshots")
    template_args.add_argument("-t", "--timeout", type=int,
                               help="connection timeout", required=False,
                               default=100)
    templ_opers = template_args.add_mutually_exclusive_group(required=True)
    templ_opers.add_argument("--create", action="store_true",
                             help="template for creation")
    templ_opers.add_argument("--delete", action="store_true",
                             help="template for deletion")

    # Update components arguments
    update_args = subparser.add_parser("UPDATE")
    update_args.add_argument("-f", "--file", type=str, required=True,
                             help="filesystems file (CSV)")
    update_args.add_argument("-s", "--server", type=str, required=True,
                             help="Server config file (YAML)")
    update_args.add_argument("-t", "--timeout", type=int,
                             help="connection timeout", required=False,
                             default=100)

    parsed_args = parser.parse_args()
    return parsed_args


def urls_contructor(zfsip):
    """Return full URL list (tuples: url, datatype) from defined IP or
    hostname"""
    urls_group = [("{}/system/v1/version".format(zfsip), "version"),
                  ("{}/hardware/v1/cluster".format(zfsip), "cluster"),
                  ("{}/problem/v1/problems".format(zfsip), "problems"),
                  ("{}/network/v1/datalinks".format(zfsip), "datalinks"),
                  ("{}/network/v1/devices".format(zfsip), "devices"),
                  ("{}/network/v1/interfaces".format(zfsip), "interfaces"),
                  ("{}/network/v1/routes".format(zfsip), "routes"),
                  ("{}/network/v1/routing".format(zfsip), "routing"),
                  ("{}/storage/v1/pools".format(zfsip), "pools"),
                  ("{}/storage/v1/projects".format(zfsip), "projects"),
                  ("{}/storage/v1/luns".format(zfsip), "luns"),
                  ("{}/storage/v1/filesystems".format(zfsip), "filesystems"),
                  ("{}/san/v1/fc/initiators".format(zfsip), "fc_initiators"),
                  ("{}/san/v1/fc/initiator-groups".format(zfsip),
                   "fc_initiator-groups"),
                  ("{}/san/v1/fc/targets".format(zfsip), "fc_targets"),
                  ("{}/san/v1/fc/target-groups".format(zfsip),
                   "fc_target-groups"),
                  ("{}/san/v1/iscsi/initiators".format(zfsip),
                   "iscsi_initiators"),
                  ("{}/san/v1/iscsi/initiator-groups".format(zfsip),
                   "iscsi_initiator-groups"),
                  ("{}/san/v1/iscsi/targets".format(zfsip), "iscsi_targets"),
                  ("{}/san/v1/iscsi/target-groups".format(zfsip),
                   "iscsi_target-groups"),
                  ("{}/user/v1/users".format(zfsip), "users")]
    return urls_group


def createlogger(log_name):
    """Return logger"""
    # create logger with 'progress bar'
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_name)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handler to logger
    logger.addHandler(fh)
    return logger


def update_component(component_type, fullurl, zauth, timeout, data,
                     project=None, pool=None, filesystem=None, lun=None):
    project, pool, filesystem, lun = project, pool, filesystem, lun
    stringdata = ""
    for k in data:
        stringdata += "{} '{}' ".format(k, data[k])
    if component_type == 'project':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=False, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, ("UPDATE - FAIL - project '{}' pool '{}' "
                                  "- Error {} - updates: {}"
                                  .format(project, pool,
                                          j['fault']['message'], stringdata))
            req.close()
            req.raise_for_status()
            return False, ("UPDATE - SUCCESS - project '{}' pool '{}' - "
                           "updates: {}".format(project, pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, ("UPDATE - FAIL - project '{}' pool '{}' - "
                              "Error '{}' - updates: {}"
                              .format(project, pool, error, stringdata))
            else:
                return True, ("UPDATE - FAIL - project '{}' pool '{}' - "
                              "Error '{}' - updates: {}"
                              .format(project, pool, error, stringdata))
        except ConnectionError as error:
            return True, ("UPDATE - FAIL - project '{}' pool '{}' - Error "
                          "'{}' - updates: {}"
                          .format(project, pool, error, stringdata))

    elif component_type == 'filesystem':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=False, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, ("UPDATE - FAIL - filesystem '{}' project"
                                  " '{}' pool '{}' - Error '{}' - updates: {}"
                                  .format(filesystem, project, pool,
                                          j['fault']['message'], stringdata))
            req.close()
            req.raise_for_status()
            return False, ("UPDATE - SUCCESS - filesystem '{}' project "
                           "'{}' pool '{}' - updates: {}"
                           .format(filesystem, project, pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, ("UPDATE - FAIL - filesystem '{}' project "
                              "'{}' pool '{}' - Error '{}' - updates: {}"
                              .format(filesystem, project, pool, error,
                                      stringdata))
            else:
                return True, ("UPDATE - FAIL - filesystem '{}' project "
                              "'{}' pool '{}' - Error '{}'  - updates: {}"
                              .format(filesystem, project, pool, error,
                                      stringdata))
        except ConnectionError as error:
            return True, ("UPDATE - FAIL - filesystem '{}' project '{}' "
                          "pool '{}' - Error '{}' - updates: {}"
                          .format(filesystem, project, pool, error,
                                  stringdata))

    elif component_type == 'lun':
        try:
            req = requests.put(fullurl, data=json.dumps(data),
                               auth=zauth, verify=False, headers=HEADER,
                               timeout=timeout)
            j = json.loads(req.text)
            if 'fault' in j:
                if 'message' in j['fault']:
                    return True, ("UPDATE - FAIL - lun '{}' project '{}' "
                                  "pool '{}' - Error '{}' - updates: {}"
                                  .format(lun, project, pool,
                                          j['fault']['message'], stringdata))
            req.close()
            req.raise_for_status()
            return False, ("UPDATE - SUCCESS - lun '{}' project '{}' pool "
                           "'{}' - updates: {}"
                           .format(lun, project, pool, stringdata))
        except HTTPError as error:
            if error.response.status_code == 401:
                return True, ("UPDATE - FAIL - lun '{}' project '{}' pool "
                              "'{}' - Error '{}' - updates: {}"
                              .format(lun, project, pool, error, stringdata))
            else:
                return True, ("UPDATE - FAIL - lun '{}' project '{}' pool "
                              "'{}' - Error '{}' - updates: {}"
                              .format(lun, project, pool, error, stringdata))
        except ConnectionError as error:
            return True, ("UPDATE - FAIL - lun '{}' project '{}' pool '{}'"
                          " - Error '{}' - updates: {}"
                          .format(lun, project, pool, error, stringdata))
    else:
        return True, ("Wrong component type '{}'".format(component_type))


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
    configfile = args.server
    config = read_yaml_file(configfile)
    zauth = (config['username'], config['password'])
    zfsurl = "https://{}:215/api".format(config['ip'])
    # initial = 0  # for progressbar
    updates = read_csv_file(datafile)
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
            print(update_component('project', fullurl, zauth, timeout, data,
                                   project=project, pool=pool)[1])
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
            print(update_component('filesystem', fullurl, zauth, timeout, data,
                                   project=project, pool=pool,
                                   filesystem=filesystem)[1])
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
                                   project=project, pool=pool, lun=lun)[1])
            print("=" * 79)

        else:
            print("Wrong type in file format.")
