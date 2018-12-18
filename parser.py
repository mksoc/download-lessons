import argparse
import os


class readable_dir(argparse.Action):
    """ Custom action for argparse to check if the supplied directory
    actually exists and is writable """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{} is not a valid path".format(prospective_dir))
        if not os.access(prospective_dir, os.W_OK):
            raise argparse.ArgumentTypeError("readable_dir:{} is not a writable dir".format(prospective_dir))


def setup_parser():
    """ Function to setup command line arguments in a single place """

    parser = argparse.ArgumentParser('Pippi', description='Automatically download lessons from Portale della Didattica')
    parser.add_argument('-u', dest='username', help='Polito username', required=True)
    parser.add_argument('-p', dest='password', help='Polito password', required=True)
    parser.add_argument('-t', '--max-wait', dest='max_wait', type=int, default=10, help='number of seconds to wait for page loading (default 10)')
    parser.add_argument('course', help='exact name of the course in the Portale')
    parser.add_argument('output_dir', action=readable_dir, help='output directory')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all', action='store_true', help='download all lessons (default)')
    group.add_argument('-n', '--newer', action='store_true', help='download only lessons newer than the last present in the output folder')
    group.add_argument('-l', '--latest', action='store_true', help='download only latest lesson (useful when receiving upload notification)')

    return parser.parse_args()
