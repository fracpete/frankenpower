# frankenpower
Python library  for downloading and processing energy data from [Frank Energy (NZ)](frankenergy.co.nz).


## Installation

Using the latest github source code:

```bash
pip install git+https://github.com/fracpete/frankenpower.git
```


## Tools

### Download

```
usage: fp-download [-h] -u USER -p PASSWORD [-o OUTPUT_DIR] -f FROM_DATE -t
                   TO_DATE [--verbose] [--debug]

Downloads enervy consumption data as CSV files.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  The Frank Energy user to use, typically an email
                        address. (default: None)
  -p PASSWORD, --password PASSWORD
                        The password of the Frank Energy user. (default: None)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to download the CSV files to. (default:
                        None)
  -f FROM_DATE, --from_date FROM_DATE
                        The start date (format: YYYY-MM-DD). (default: None)
  -t TO_DATE, --to_date TO_DATE
                        The end date (format: YYYY-MM-DD). (default: None)
  --verbose             whether to output logging information (default: False)
  --debug               whether to output debugging information (default:
                        False)
```
