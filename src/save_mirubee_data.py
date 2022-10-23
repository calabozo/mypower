
import logging
import argparse
import util.mirubox
from db.dao import Dao


if __name__=="__main__":

    parser = argparse.ArgumentParser(
        description='Downloads data from Mirubox.',
        epilog='''It stores the data in the table data and calculates its price.''')
    parser.add_argument('--log' ,metavar='LEVEL', help='Set log level. ERROR, WARNING, INFO, DEBUG', default='DEBUG')
    parser.add_argument('--logFile' ,metavar='LOG_FILE', help='Saves the log info in a file.',default=None)
    parser.add_argument('--file', metavar='FILE_NAME', help='CSV file to import data')

    args = parser.parse_args()

    loglevel =args.log
    log_file =args.logFile
    csv_file =args.file

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logging.basicConfig(filename=log_file ,format='%(asctime)s %(levelname)s:\t%(message)s' ,level=numeric_level)

    if csv_file is not None:
        util.mirubox.read_data_and_save_in_db(csv_file)
    else:
        exml = util.mirubox.launch_query_and_save_in_db('192.168.0.100')


