from __future__ import print_function
import os
from datetime import datetime
import argparse
import time
import threading
import schedule
import inotify.adapters
import zfssa_utils.explorer


def create_parser():
    """Get Arguments"""
    parser = argparse.ArgumentParser(
        description="Schedule zfssa explorers")
    parser.add_argument("-d", "--directory", type=str,
                        help="Directory to find Server config files (.yml)",
                        required=True)
    parser.add_argument("-c", "--cert", action="store_true",
                        help=("Use certificate (Certificates must be named "
                              "like the zfssa yml but with extension '.crt')"),
                        required=False)
    parser.add_argument("-p", "--progress", action="store_true",
                        help="progress bar", required=False)
    parser.add_argument("--timeout", type=int, help="connection timeout",
                        required=False, default=100)
    parser.add_argument("-t", "--time", nargs='+',
                        help=("24Hr time where the Job should be launched, "
                              "example: \"18:00\" \"21:00\""),
                        required=True)
    return parser


def get_zfssalist(directory):
    """Return list of yml files in current directory"""
    files = [file for file in os.listdir(directory) if file.endswith('.yml')]
    if not files:
        print('No yaml found in {}'.format(directory))
        exit(1)
    zfssalist = [os.path.join(directory, file) for file in files]
    return zfssalist


def launch_explorers(zfssalist, args):
    """Launch explorers from a zfsssa list"""
    for zfssa in zfssalist:
        if args.cert:
            certfile = zfssa.replace(".yml", ".crt")
            exists = os.path.exists(certfile)
            if exists:
                argsforexplorer = Namespace(server=zfssa,
                                            subparser_name='EXPLORER',
                                            progress=args.progress,
                                            timeout=args.timeout,
                                            cert=certfile)
            else:
                print("No certificate validation for: {}".format(zfssa))
                argsforexplorer = Namespace(server=zfssa,
                                            subparser_name='EXPLORER',
                                            progress=args.progress,
                                            timeout=args.timeout,
                                            cert=False)
        else:
            argsforexplorer = Namespace(server=zfssa,
                                        subparser_name='EXPLORER',
                                        progress=args.progress,
                                        timeout=args.timeout,
                                        cert=False)
        print("Explorer for '{}' launched".format(zfssa.split('.')[0]))
        zfssa_utils.explorer.run_explorer(argsforexplorer)


class Namespace:
    """Class to simulate args parsed"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ThreadingInotify(object):
    """ Threading inotify"""

    def __init__(self, iargs, interval=1):
        self.iargs = iargs
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            i = inotify.adapters.Inotify()

            i.add_watch(self.iargs.directory)

            for event in i.event_gen(yield_nones=False):
                (_, etype, _, _) = event

                if 'IN_DELETE' in etype or 'IN_MODIFY' in etype or \
                        'IN_MOVED_TO' in etype or 'IN_MOVED_FROM' in etype or \
                        'IN_CREATE' in etype:
                    schedule.clear()
                    print("---- Removed previous schedules ----")
                    zfssalist = get_zfssalist(self.iargs.directory)
                    for stime in self.iargs.time:
                        for zfs in zfssalist:
                            print("++++ Scheduled: {} {} ++++"
                                  .format(stime, zfs))
                        schedule.every().day.at(stime).do(launch_explorers,
                                                          zfssalist,
                                                          self.iargs)

            time.sleep(self.interval)


def main():
    parser = create_parser()
    args = parser.parse_args()
    print("Started at: {}".format(datetime.now()))
    zfssalist = get_zfssalist(args.directory)
    for schedtime in args.time:
        schedule.every().day.at(schedtime).do(launch_explorers, zfssalist,
                                              args)
        for zfssa in zfssalist:
            print("++++ Scheduled: {} {} ++++".format(schedtime, zfssa))
    ThreadingInotify(args)
    while True:
        schedule.run_pending()
        time.sleep(1)
