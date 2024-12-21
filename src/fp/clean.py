import argparse
import csv
import logging
import os
import traceback
from datetime import datetime

# logging setup
logger = logging.getLogger("fp.clean")


def clean(input_dir: str, output: str):
    """
    Cleans up the usage data.

    :param input_dir: the dir with the raw data
    :type input_dir: str
    :param output: the dir or file to store the clean data in
    :type output: str
    """
    separate_outputs = os.path.isdir(output)
    if not separate_outputs and os.path.exists(output):
        logger.info("Removing output file: %s" % output)
        os.remove(output)
    first_file = True
    for f in os.listdir(input_dir):
        if not f.lower().endswith(".csv"):
            continue
        path_in = os.path.join(input_dir, f)
        if separate_outputs:
            flags_out = "w"
            path_out = os.path.join(output, f)
        else:
            flags_out = "a"
            path_out = output
        logger.info("Loading from: %s" % path_in)
        logger.info("Saving to: %s" % path_out)
        with open(path_in, "r") as fp_in:
            reader = csv.reader(fp_in)
            first_row = True

            # skip header when merging
            skip_header = False
            if not separate_outputs and not first_file:
                skip_header = True

            # clean data and write to output
            with open(path_out, flags_out) as fp_out:
                writer = csv.writer(fp_out)
                for row in reader:
                    # header
                    if first_row:
                        first_row = False
                        if skip_header:
                            continue
                        row[1] = row[1] + "_kwh"
                        row[2] = "cost"
                    # data
                    else:
                        if ("AM " in row[0]) or ("PM" in row[0]):
                            d_str = row[0].replace("1st ", "1 ").replace("2nd ", "2 ").replace("3rd ", "3 ").replace("th ", " ")
                            d = datetime.strptime(d_str, "%I:%M%p %d %B %Y")
                            row[0] = d.strftime("%Y-%m-%d %H:%M")
                        elif "/" in row[0]:
                            d = datetime.strptime(row[0], "%d/%m/%Y")
                            row[0] = d.strftime("%Y-%m-%d")
                        else:
                            d = datetime.strptime(row[0], "%B %Y")
                            row[0] = d.strftime("%Y-%m")
                        row[1] = row[1].replace(" kWh", "")
                        row[2] = row[2].replace("$", "")
                    writer.writerow(row)

            first_file = False


def main(args=None):
    """
    Runs the .nfo generation.
    Use -h/--help to see all options.

    :param args: the command-line arguments to use, uses sys.argv if None
    :type args: list
    """

    parser = argparse.ArgumentParser(
        description='Cleans up the downloaded CSV files.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="fp-clean")
    parser.add_argument("-i", "--input_dir", required=False, help="The directory with the downloaded, raw CSV files.")
    parser.add_argument("-o", "--output", required=False, help="The directory or file to store the cleaned up CSV files in; using an output file will combine all input files into one.")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", required=False, help="whether to output logging information")
    parser.add_argument("-d", "--debug", action="store_true", dest="debug", required=False, help="whether to output debugging information")
    parsed = parser.parse_args(args=args)
    # configure loggin
    if parsed.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed.verbose:
        logging.basicConfig(level=logging.INFO)
    logger.debug(parsed)
    clean(parsed.input_dir, parsed.output)


def sys_main():
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    :rtype: int
    """

    try:
        main()
        return 0
    except Exception:
        logger.info(traceback.format_exc())
        return 1


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
