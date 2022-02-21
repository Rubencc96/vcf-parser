# vcf-parser
**Author**: Rubén Cañas Cañas  


Tool for parsing VCF files.

This tool allows the convertion of the information in a VCF file as a tab delimited file, allowing a more simple processing of the variant information in different programs (such as R). The tool also allows to pass a string as an argument to output a file with only the desired information. See examples and usage for more info.

vcf-parser also permits to output the genotypes for the different samples, if desired, and even subset the samples.

This tool could be useful for obtaining different Summary outputs of final VCF or SetIDs, required for other Software.  

*Recommended*  
Use the program for filtered VCF files, either from annotation or variant calling info.
The tool allows to change the annotation field, but is recommended to use VEP for the annotation when using vcf-parser. The annotation field for VEP is 'CSQ' and it has to be introduced via options in annotation field.  
When using annotated VCF files, some variants can hit various annotations for a single variant. This will generate duplicates on the output, so it's a good step to take some filtering for the canonical transcript when using annotation software.  

 
## Usage
**Options for vcf-parser:**  

- Input (-i, --input): Input file.
- Output (-o, --output): Output file.
- Annotation field (-a, --annotation): Annotation field used in the VCF (CSQ for VEP).
- Parsing (-p, --parsing): Parsing string. It will allow to select only the desired fields on our output.  
- Genotypes (-g, --genotypes): If present, this option will mantain the genotypes in the output file, or it will allow to subset the samples we want if using the parsing option. Doesn't require any argument.
- List (-l, --list): Print all the available info present in the VCF file. Option used alone, since the program exits after printing the available fields.

**To be considered**
The input option is the only one that is mandatory. The file format is VCF v4.2.  
When parsing, the fields we want to extract from the VCF file **MUST** be between '%' symbols for the program to recognize them. Example string: '%CHROM%:%POS%\_%REF%\_%ALT%\t%ID%\n'.
Remember to use delimiters when using the parser (\n is crucial if we want the variants to be in different lines).  
If we are not using a parsing string, the output will contain all the fields separated by tabs (\t). The advantage of this is that the program will divide the different INFO fields for us to access it easily.  
When adding the Genotypes flag, it will allow to include the samples genotypes in the output file, but if we are using a parsing string, it will only include the selected samples, as if it were a field.  
When using an annotated VCF file remember to check the annotation field. It usually is 'CSQ' for VEP annotated files and 'ANN' for SnpEff annotated files. It is recommended to use VEP, since the testing was performed using VEP annotated VCFs.  

### Future ideas  
- Retrieve ID option: the ID field usually remains empty ('.') when performing Variant Calling protocols. It should be a nice idea to make the program to retrieve a desired field (via parsing option) to introduce it on the ID field, outputting a better annotated VCF file. This could be useful since many other tools remove annotion and info fields.
- Variant case-control counter: it would be useful for having a preliminary idea of the cohort we are managing. Moreover, it could have a simple association test (Fisher or chisq). Also interesting, it could have the prior parsing string to add some annotation fields, in order to process this data more easily.
