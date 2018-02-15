"""Common functions"""
import os
import sys
import logging
import subprocess
import csv
import six
import requests
from urllib3.exceptions import InsecureRequestWarning
import yaml
from progressbar import ProgressBar, AdaptiveETA, Bar, Percentage
if six.PY2:
    import zfssa_utils.argparse_py2_modified as argparse
else:
    import argparse

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
UPDATELOGFILE = "updates_output.log"
EXPLORERLOGFILE = "explorer_output.log"


def read_yaml_file(configfile):
    """Read config file and return credentials in json."""
    config = {}
    try:
        with open(configfile, 'r') as configuration:
            try:
                config = yaml.load(configuration)
                if not isinstance(config, dict):
                    exit("Yaml file: Format looks wrong")
            except yaml.YAMLError as error:
                print("Error in configuration file: {}").format(error)
            return config
    except IOError as error:
        exit("Error: {}".format(error))


def read_csv_file(filename):
    """Read csv file and return the list"""
    csvlist = []
    try:
        with open(filename, 'r') as cvsfile:
            filereader = csv.reader(cvsfile, delimiter=',')
            for row in filereader:
                if not row[0].startswith('#'):
                    csvlist.append(row)
        # del csvlist[0]
    except IOError as error:
        exit("Error: {}".format(error))
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


def check_files_exists(filelist):
    """Return msg if files in list don't exists."""
    files = []
    for file in filelist:
        if not os.path.exists(file):
            files.append(file)
    if files:
        return "Files not found: {}".format(files)
    return None


def fetch(url, zauth, header, timeout, datatype, verify):
    """Fetch data from zfs api, returning a tuple (data, datatype)"""
    req = requests.get(url, timeout=timeout, auth=zauth,
                       verify=verify, headers=header)
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

    parser.add_argument("-v", "--version", action="store_true",
                        help="program version", required=False)
    parser.add_argument("-t", "--timeout", type=int, help="connection timeout",
                        required=False, default=100)
    parser.add_argument("--cert", type=str, help="use certificate",
                        required=False, default=False)
    parser.add_argument("--doc", action="store_true",
                        help="program documentation", required=False)

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
    proj_args.add_argument("--noconfirm", action="store_true",
                           help=("Don't ask for confirmation when deleting "
                                 "Projects"), required=False)

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
    template_args.add_argument("--updates", action="store_true",
                               required=False,
                               help=("generate template for components"
                                     "(lun|fs|project) updates/modification"))

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
    update_args.add_argument("-p", "--progress", action="store_true",
                             help="progress bar", required=False)
    update_args.add_argument("--noconfirm", action="store_true",
                             help=("Don't ask for confirmation when updating a"
                                   "component"), required=False)

    parsed_args = parser.parse_args()
    return parsed_args


def urls_constructor(zfsip):
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


class CreateLogger(object):

    def __init__(self, log_name):
        self.log_name = log_name
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                           '%(levelname)s - %(message)s')
        self.fh = logging.FileHandler(self.log_name)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def shutdown(self):
        self.logger.removeHandler(self.fh)
        logging.shutdown()


def pager(text):
    try:
        if os.name == 'nt':
            for line in text:
                if six.PY2:
                    sys.stdout.write(line)
                else:
                    sys.stdout.write(line)
        else:
            pager = subprocess.Popen(['less', '-F', '-R', '-S', '-X', '-K'],
                                     stdin=subprocess.PIPE, stdout=sys.stdout)
            for line in text:
                if six.PY2:
                    pager.stdin.write(line)
                else:
                    pager.stdin.write(line.encode())
            pager.stdin.close()
            pager.wait()
    except KeyboardInterrupt:
        pass
