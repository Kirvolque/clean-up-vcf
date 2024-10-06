# clean-up-vcf
The clean-up-vcf script is designed to remove unnecessary INFO fields from a VCF file. This script can be used to simplify and reduce the size of a VCF file, making it more manageable.

# Usage
To use clean-up-vcf, simply execute the following command:

```
python3 clean_up_vcf.py --vcf <input_file> --info <info_fields> > <output_file>
```
The --vcf argument specifies the path to the input VCF file, while the --info argument accepts a list of INFO fields that will remain in the output file. Multiple fields can be specified by separating them with spaces. The resulting VCF file will be written to the specified output_file.

Here's an example:

```
python3 clean_up_vcf.py --vcf input.vcf --info AC AN_nfe_est faf95 > output.vcf
```
This command will remove all INFO fields from input.vcf except for AC, AN_nfe_est, and faf95, and will write the result to output.vcf.

# Requirements
To use clean-up-vcf, you need Python 3.9 or higher installed on your system.

# License
This script is licensed under the MIT License. See LICENSE for more information.
