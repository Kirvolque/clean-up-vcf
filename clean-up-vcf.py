import csv
import argparse
from typing import List, Tuple, Dict, Optional

CHROM = "#CHROM"
INFO = "INFO"

def run(file_path: str, info_fields: List[str]) -> None:
    with open(file_path, "r") as input_file:
        fields, header = read_header(input_file)
        reader = csv.DictReader(input_file, delimiter='\t', fieldnames=fields)
        for header_line in header:
            print(header_line, end="")
        for row in reader:
            print(dict_to_line(filter_row(row, info_fields), fields))

def parse_info(info_content: str) -> Dict[str, str]:
    return {
        k: v
        for k, v in (
            split(field) for field in info_content.split(";")
        )
    }

def split(field: str) -> Tuple[str, Optional[str]]:
    return (field, None) if "=" not in field else tuple(field.split("="))

def to_pair(key: str, value: str) -> str:
    return f"{key}={value}" if key and value else key

def pairs_for_keys(info: Dict[str, str], keys: List[str]) -> List[str]:
    return [to_pair(key if key in info else None, info.get(key)) for key in keys]

def filter_row(row: Dict[str, str], keys: List[str]) -> Dict[str, str]:
    row[INFO] = ";".join(pair for pair in pairs_for_keys(parse_info(row[INFO]), keys) if pair)
    return row

def dict_to_line(row: Dict[str, str], fields: List[str]) -> str:
    # Using a list comprehension to replace map and lambda
    return "\t".join(row[field] for field in fields)

def read_header(input_file) -> Tuple[List[str], List[str]]:
    line, header = "", []
    while not line.startswith(CHROM):
        line = input_file.readline()
        header.append(line)
    fields = [field.strip() for field in line.split("\t")]
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
    run(args.vcf, args.info_fields)
