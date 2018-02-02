"""Common functions"""
import argparse
import logging
import re
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
TIMEOUT = 100 # seconds
PROJECTLOGFILE = "projects_output.log"
LUNLOGFILE = "luns_output.log"
SNAPLOGFILE = "snaps_output.log"

def read_yaml_file(configfile):
    """Read config file and return credentials in json."""
    config = {}
    with open(configfile, 'r') as configuration:
        try:
            config = yaml.load(configuration)
        except yaml.YAMLError as error:
            print("Error in configuration file: {}").format(error)
        return config


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

    # Projects arguments
    proj_args = subparser.add_parser("PROJECTS")
    proj_args.add_argument("-f", "--file", type=str, required=True,
                           help="projects file (CSV)")
    proj_args.add_argument("-s", "--server", type=str, required=True,
                           help="Server config file (YAML)")
    proj_args.add_argument("-p", "--progress", action="store_true",
                           help="progress bar", required=False)
    proj_opers = proj_args.add_mutually_exclusive_group(required=True)
    proj_opers.add_argument("--create", action="store_true",
                            help="Create Snapshots specified in csv file")
    proj_opers.add_argument("--delete", action="store_true",
                            help="Delete Snapshots specified in csv file")
    proj_opers.add_argument("--list", action="store_true",
                            help="List/Check Snapshots specified in csv file")

    # LUNs arguments
    luns_args = subparser.add_parser('LUNS')
    luns_args.add_argument("-f", "--file", type=str, help="luns file (CSV)",
                           required=True)
    luns_args.add_argument("-s", "--server", type=str, required=True,
                           help="Server config file (YAML)")
    luns_args.add_argument("-p", "--progress", action="store_true",
                           help="progress bar", required=False)
    luns_opers = luns_args.add_mutually_exclusive_group(required=True)
    luns_opers.add_argument("--create", action="store_true",
                            help="Create Snapshots specified in csv file")
    luns_opers.add_argument("--delete", action="store_true",
                            help="Delete Snapshots specified in csv file")
    luns_opers.add_argument("--list", action="store_true",
                            help="List/Check Snapshots specified in csv file")

    # Snapshots arguments
    snaps_args = subparser.add_parser('SNAPSHOTS')
    snaps_args.add_argument("-f", "--file", type=str, help="luns file (CSV)",
                            required=True)
    snaps_args.add_argument("-s", "--server", type=str, required=True,
                            help="Server config file (YAML)")
    snaps_args.add_argument("-p", "--progress", action="store_true",
                            help="progress bar", required=False)
    snaps_opers = snaps_args.add_mutually_exclusive_group(required=True)
    snaps_opers.add_argument("--create", action="store_true",
                             help="Create Snapshots specified in csv file")
    snaps_opers.add_argument("--delete", action="store_true",
                             help="Delete Snapshots specified in csv file")
    snaps_opers.add_argument("--list", action="store_true",
                             help="List/Check Snapshots specified in csv file")
    snaps_type = snaps_args.add_mutually_exclusive_group(required=True)
    snaps_type.add_argument('--filesystems', action='store_true',
                            help="Apply to File Systems")
    snaps_type.add_argument('--projects', action='store_true',
                            help="Apply to Projects")
    snaps_type.add_argument('--luns', action='store_true',
                            help="Apply to LUNs")

    parsed_args = parser.parse_args()
    return parsed_args


def urls_contructor(zfsip):
    """Return full URL list (tuples: url, datatype) from defined IP or hostname"""
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
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handler to logger
    logger.addHandler(fh)
    return logger


def get_real_size(size, size_unit):
    """Get size in bytes for different unit sizes."""
    real_size = 0
    multiplier = {
        "KB": 1024,
        "MB": 1024 * 1024,
        "GB": 1024 * 1024 * 1024,
        "TB": 1024 * 1024 * 1024 * 1024
    }
    real_size = int(size) * (multiplier[size_unit.upper()])
    return real_size


def get_real_blocksize(blocksize):
    """Get integer blocksize from string"""
    if any(x in blocksize for x in ['k', 'K']):
        string = re.sub(r"\d+", "", blocksize)
        blocksize = int(blocksize.replace(string, "")) * 1024
        return blocksize
    elif any(x in blocksize for x in ['m', 'M']):
        string = re.sub(r"\d+", "", blocksize)
        blocksize = int(blocksize.replace(string, "")) * 1024 * 1024
        return blocksize
    else:
        return blocksize
