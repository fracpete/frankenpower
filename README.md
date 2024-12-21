# frankenpower
Python library for downloading and processing energy data from [Frank Energy (NZ)](frankenergy.co.nz).

Downloads are performed with [selenium](https://www.selenium.dev/).


## Installation

Using the latest github source code:

```bash
pip install git+https://github.com/fracpete/frankenpower.git
```


## Tools

### Download

```
usage: fp-download [-h] -u USER -p PASSWORD [-o OUTPUT_DIR]
                   [-a {daily,hourly}] -f FROM_DATE -t TO_DATE [-m] [-v] [-d]

Downloads energy consumption data as CSV files.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  The Frank Energy user to use, typically an email
                        address. (default: None)
  -p PASSWORD, --password PASSWORD
                        The password of the Frank Energy user. (default: None)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to download the CSV files to. (default:
                        None)
  -a {daily,hourly}, --aggregation {daily,hourly}
                        The type of aggrgated data to download. (default:
                        hourly)
  -f FROM_DATE, --from_date FROM_DATE
                        The start date (monthly: YYYY, daily: YYYY-MM, hourly:
                        YYYY-MM-DD). (default: None)
  -t TO_DATE, --to_date TO_DATE
                        The end date (monthly: YYYY, daily: YYYY-MM, hourly:
                        YYYY-MM-DD). (default: None)
  -m, --only_missing    whether to download only missing CSV files (default:
                        False)
  -v, --verbose         whether to output logging information (default: False)
  -d, --debug           whether to output debugging information (default:
                        False)
```

### Clean

```
usage: fp-clean [-h] [-i INPUT_DIR] [-o OUTPUT] [-v] [-d]

Cleans up the downloaded CSV files.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        The directory with the downloaded, raw CSV files.
                        (default: None)
  -o OUTPUT, --output OUTPUT
                        The directory or file to store the cleaned up CSV
                        files in; using an output file will combine all input
                        files into one. (default: None)
  -v, --verbose         whether to output logging information (default: False)
  -d, --debug           whether to output debugging information (default:
                        False)
```
