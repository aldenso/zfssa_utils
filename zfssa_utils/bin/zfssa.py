import os
import sys
from zfssa_utils import __version__
from zfssa_utils import __file__ as zfssa_utils_file
from zfssa_utils.common import create_parser, check_files_exists, pager
from zfssa_utils.explorer import run_explorer
from zfssa_utils.projects import run_projects
from zfssa_utils.luns import run_luns
from zfssa_utils.snapshots import run_snaps
from zfssa_utils.filesystems import run_filesystems
from zfssa_utils.templates import create_template
from zfssa_utils.updates import run_updates

module_path = os.path.abspath(os.path.dirname(zfssa_utils_file))

def main():
    args = create_parser()
    if args.version:
        exit(__version__)
    if args.doc:
        with open(os.path.join(module_path, "doc.txt"), 'r') as file:
            text = file.read()
            pager(text)
            exit("Closing documentation")
    if args.subparser_name == 'TEMPLATES':
        create_template(args)
        exit("Remember to adjust the content to your needs.")
    if not args.cert:
        print("*" * 79)
        print("Warning: not using certificate verification.")
        print("*" * 79)
    arglist = []
    try:
        if args.cert:
            arglist.append(args.cert)
        if args.server:
            arglist.append(args.server)
        if args.file:
            arglist.append(args.file)
    except Exception:
        pass
    msg = check_files_exists(arglist)
    if msg:
        exit(msg)
    if args.subparser_name == 'EXPLORER':
        run_explorer(args)
    elif args.subparser_name == 'PROJECTS':
        run_projects(args)
    elif args.subparser_name == 'LUNS':
        run_luns(args)
    elif args.subparser_name == 'SNAPSHOTS':
        run_snaps(args)
    elif args.subparser_name == 'FILESYSTEMS':
        run_filesystems(args)
    elif args.subparser_name == 'UPDATE':
        run_updates(args)
    else:
        pass
    # print(args)
