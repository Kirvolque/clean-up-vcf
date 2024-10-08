import csv
import argparse
from typing import Generator

VCF_HEADER_CHROM = "#CHROM"
VCF_INFO_FIELD = "INFO"

def parse_info(info_content: str) -> dict[str, str]:
    """Parses the INFO field from VCF into a dictionary of key-value pairs."""
    return {
        k: v
        for k, v in (
            split(field) for field in info_content.split(";")
        )
    }

def split(field: str) -> tuple[str, str | None]:
    """Splits a field by '=' if present, otherwise returns the field as a key with None value."""
    return (field, None) if "=" not in field else tuple(field.split("="))

def to_pair(key: str, value: str | None) -> str:
    """Formats a key-value pair into 'key=value', or just 'key' if value is None."""
    return f"{key}={value}" if key and value else key

def get_info_pair_for_key(info: dict[str, str], key: str) -> str | None:
    """Retrieves a formatted pair for a given key if it exists in the info dictionary."""
    return to_pair(key, info.get(key)) if key in info else None

def filter_info(info: dict[str, str], keys: list[str]) -> Generator[str, None, None]:
    """Yields filtered info pairs for the given list of keys."""
    for key in keys:
        pair = get_info_pair_for_key(info, key)
        if pair:
            yield pair

def dict_to_line(row: dict[str, str], fields: list[str]) -> str:
    """Converts a dictionary row into a VCF-formatted line."""
    return "\t".join(row[field] for field in fields)

def read_header(input_file) -> tuple[list[str], list[str]]:
    """Reads the VCF header and extracts the fields."""
    line, header = "", []
    while not line.startswith(VCF_HEADER_CHROM):
        line = input_file.readline()
        header.append(line)
    fields = [field.strip() for field in line.split("\t")]
    return fields, header

def run(file_path: str, info_fields: list[str]) -> None:
    """Main function to run the VCF processing pipeline."""
    with open(file_path, "r") as input_file:
        fields, header = read_header(input_file)
        reader = csv.DictReader(input_file, delimiter='\t', fieldnames=fields)
        for header_line in header:
            print(header_line, end="")
        for row in reader:
            info = parse_info(row[VCF_INFO_FIELD])
            filtered_info = filter_info(info, info_fields)
            row[VCF_INFO_FIELD] = ";".join(filtered_info)
            print(dict_to_line(row, fields))


class StoreInfoFields(argparse.Action):
    """Custom argparse action to store INFO fields."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super().__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VCF Filter Script")
    parser.add_argument("--vcf", help="VCF file", required=True)
    parser.add_argument('-i', "--info", action=StoreInfoFields, dest='info_fields', nargs="+",
                        help="List of INFO fields to retain.", required=True)
    args = parser.parse_args()
    run(args.vcf, args.info_fields)
