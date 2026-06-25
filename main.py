import time
import argparse

import getpak
from getpak.automation import Pipelines
from getpak.commons import Utils as U


"""
Authors: 
    David Guimaraes - dvdgmf (at) gmail (dot) com
    Matheus Tavares - tavaresmatheush (at) gmail (dot) com
    Jean-Michel Martinez - martinez (at) ird (dot) fr
"""

def build_parser():
    """
    Build parser for GET-Pak command line
    
    The command line interface is intentionally settings-first:
    processing folders, tile ID, and product options are read from settings.ini.
    """

    parser = argparse.ArgumentParser(prog='getpak',description='GET-Pak command line launcher.')

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='Display the installed GET-Pak version and exit.'
    )

    parser.add_argument(
        '-c',
        '--config',
        type=str,
        default=None,
        help='Optional path to a settings.ini file. Defaults to the repository settings.ini.'
    )

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'run',
        help='Run GET-Pak according to settings.ini.'
    )

    subparsers.add_parser(
        'l2b',
        help='Run only the L2B processing step.'
    )

    subparsers.add_parser(
        'report',
        help='Run only the report/time-series extraction step.'
    )

    return parser

def run_pipeline(command, config_path=None):
    """
    Execute a GET-Pak command using automation.Pipelines.
    """
    pipeline = Pipelines(config_path=config_path)
    print(f'GET-Pak instance run #{pipeline.INSTANCE_TIME_TAG}')
    if command == 'run':
        pipeline.run()
    elif command == 'l2b':
        pipeline.run(compute_l2b=True, make_report=False)
    elif command == 'report':
        pipeline.run(compute_l2b=False, make_report=True)
    else:
        raise ValueError(f'Unknown GET-Pak command: {command}')
    
    return pipeline

def main(argv=None):
    """
    Public entry point.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f'GET-Pak version: {getpak.__version__}')
        return 0

    command = args.command or 'run'

    U.print_logo()
    
    print(f'GET-Pak version: {getpak.__version__}')
    
    print(f'GET-Pak command: {command}')
    
    run_pipeline(command=command, config_path=args.config)

    return 0

if __name__ == '__main__':

    U.tic()
    t1 = time.perf_counter()
    
    exit_code = main()

    t_hour, t_min, t_sec, _ = U.tac()
    t2 = time.perf_counter()

    print(f'Finished in {round(t2 - t1, 2)} second(s).')
    print(f'Elapsed execution time: {t_hour}h : {t_min}m : {t_sec}s')
    raise SystemExit(exit_code)
