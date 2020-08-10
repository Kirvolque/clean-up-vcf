import csv
import argparse
from typing import List, Tuple, Dict

CHROM = "#CHROM"
INFO = "INFO"


def run():
    file_path = args.vcf
    info_fields = args.info_fields
    with open(file_path, "r") as input_file:
        fields, header = read_header(input_file)
        reader = csv.DictReader(input_file, delimiter='\t', fieldnames=fields)
        for header_line in header:
            print(header_line, end="")
        for row in reader:
            print(dict_to_line(filter_row(row, info_fields), fields))


def parse_info(pairs: str) -> Dict[str, str]:
    return dict(map(lambda field: split(field), pairs.split(";")))


def split(field: str) -> Tuple[str, str]:
    return (field, None) if "=" not in field else tuple(field.split("="))


def to_pair(key: str, value: str) -> str:
    return "{}={}".format(key, value) if key and value else key


def pairs_for_keys(info: Dict[str, str], keys: List[str]) -> map:
    return map(lambda key: to_pair(key if key in info else None, info.get(key)), keys)


def filter_row(row: Dict[str, str], keys: List[str]) -> dict:
    row.update({INFO: ";".join(filter(lambda pair: pair, (pairs_for_keys(parse_info(row[INFO]), keys))))})
    return row


def dict_to_line(row: Dict[str, str], fields: List[str]) -> str:
    return "\t".join(map(lambda field: row[field], fields))


def read_header(input_file) -> Tuple[List[str], List[str]]:
    line, header = "", []
    while not line.startswith(CHROM):
        line = input_file.readline()
        header.append(line)
    fields = list(map(lambda field: field.strip(), line.split("\t")))
    return fields, header


class StoreInfoFields(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreInfoFields, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vcf", help="VCF file", required=True)
    parser.add_argument('-i', "--info", action=StoreInfoFields, dest='info_fields', nargs="+",
                        help="List of INFO fields. ", required=True)
    args = parser.parse_args()
    run()
