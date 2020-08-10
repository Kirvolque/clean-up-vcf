# clean-up-vcf

The script that removes unnecessary INFO fields from VCF file.

Launch command example:
`python3 clean-up-vcf.py --vcf input.vcf --info AC AN_nfe_est faf95 > output.vcf`

Where `--info` argument accepts list of INFO fields that will remain in the output file.
