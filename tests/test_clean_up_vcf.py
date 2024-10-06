import unittest
from io import StringIO
from clean_up_vcf import parse_info, split, to_pair, get_info_pair_for_key, filter_info, dict_to_line, read_header

class TestCleanUpVCF(unittest.TestCase):

    def test_parse_info(self):
        info_content = "AC=10;AF=0.5;DB"
        expected_output = {'AC': '10', 'AF': '0.5', 'DB': None}
        self.assertEqual(parse_info(info_content), expected_output)

    def test_split_with_equals(self):
        field = "AC=10"
        expected_output = ("AC", "10")
        self.assertEqual(split(field), expected_output)

    def test_split_without_equals(self):
        field = "DB"
        expected_output = ("DB", None)
        self.assertEqual(split(field), expected_output)

    def test_to_pair_with_value(self):
        key = "AC"
        value = "10"
        expected_output = "AC=10"
        self.assertEqual(to_pair(key, value), expected_output)

    def test_to_pair_without_value(self):
        key = "DB"
        value = None
        expected_output = "DB"
        self.assertEqual(to_pair(key, value), expected_output)

    def test_get_info_pair_for_key_present(self):
        info = {"AC": "10", "AF": "0.5", "DB": None}
        key = "AC"
        expected_output = "AC=10"
        self.assertEqual(get_info_pair_for_key(info, key), expected_output)

    def test_get_info_pair_for_key_absent(self):
        info = {"AC": "10", "AF": "0.5", "DB": None}
        key = "XYZ"
        expected_output = None
        self.assertEqual(get_info_pair_for_key(info, key), expected_output)

    def test_filter_info(self):
        info = {"AC": "10", "AF": "0.5", "DB": None}
        keys = ["AC", "DB"]
        expected_output = ["AC=10", "DB"]
        self.assertEqual(list(filter_info(info, keys)), expected_output)

    def test_dict_to_line(self):
        row = {"#CHROM": "chr1", "POS": "12345", "ID": ".", "REF": "A", "ALT": "G", "QUAL": ".", "FILTER": "PASS", "INFO": "AC=10"}
        fields = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        expected_output = "chr1\t12345\t.\tA\tG\t.\tPASS\tAC=10"
        self.assertEqual(dict_to_line(row, fields), expected_output)

    def test_read_header(self):
        vcf_content = StringIO("##fileformat=VCFv4.2\n##source=myvcf\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
        expected_fields = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]
        expected_header = ['##fileformat=VCFv4.2\n', '##source=myvcf\n', '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n']
        fields, header = read_header(vcf_content)
        self.assertEqual(fields, expected_fields)
        self.assertEqual(header, expected_header)

if __name__ == "__main__":
    unittest.main()
