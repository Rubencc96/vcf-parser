#!/usr/bin/env python3
# -- coding: utf-8 --
'''
#################################################################
#                                                               #
#                           VCF parser                          #
#                                                               #
#       Tool for parsing VCF files.                             #
#       This tool lets convert de information in the            #
#       VCF file as a tab delimited file, or extract            #
#       the desired information passed as an argument           #
#                                                               #
#                                                               #
#################################################################

@author Rubén Cañas Cañas
@version 1.0

For more information and usage examples visit my Github:
https://github.com/Rubencc96
'''

import argparse
from utils import header_processing
from utils import line_processing

# Options input and collection
parser = argparse.ArgumentParser(usage=__doc__)
parser.add_argument("-i", "--input",
                    type=str, 
                    help="VCF file to parse.",
                    action="store",
                    default=None)
parser.add_argument("-o", "--output",
                    type=str, 
                    help="output file name.",
                    action="store",
                    default="output.txt")
parser.add_argument("-a", "--annotation",
                    type=str, 
                    help="Annotation Field, if any. VEP is recommended which uses \
                    CSQ info field.",
                    action="store",
                    default=False)
parser.add_argument("-l", "--list",
                    help="List all possible information fields that could be parsed.",
                    action="store_true")
parser.add_argument("-g", "--genotypes",
                    help="Allows adding the samples genotypes to the parsed file.",
                    action="store_true")
parser.add_argument("-p", "--parsing",
                    type=str, 
                    help="String to parse. Desired INFO must be between 'percentage' symbols",
                    action="store",
                    default=False)


args=parser.parse_args()
# GLBAL VARS (OPTIONS)
INPUT = args.input
OUTPUT = args.output
ANNOTATION = args.annotation
LIST = args.list
GENOTYPES = args.genotypes
PARSING_STR = args.parsing
if PARSING_STR:
    PARSING_STR = PARSING_STR.replace("\\t", "\t").replace("\\n","\n")


def OutputFile(vcf_header, input_file, output_file, ann_opt, parsing_motive):
    '''
    Output function
    '''
    f = open(input_file, "r")
    out = open(output_file, "w")
    if parsing_motive:
        new_header = parsing_motive.replace("%", "")
        out.write(new_header)
    else:
        out.write('\t'.join(vcf_header)+'\n')

    for vcf_line in f:
        if not vcf_line.startswith("#"):
            if ann_opt:
                output_lines = line_processing.LineFormattingAnn(vcf_header,
                                                                vcf_line[:-1],
                                                                ann_opt)
            else:
                output_lines = line_processing.LineFormatting(vcf_header,
                                                            vcf_line[:-1])

            while len(output_lines) > 0:
                out_line = output_lines[0]
                if parsing_motive:
                    out_line = line_processing.Parsing(parsing_motive,
                                                            vcf_header,
                                                            out_line)
                    out.write(''.join(out_line))
                else:
                    out.write('\t'.join(out_line)+'\n')
                output_lines.pop(0)
    f.close()
    out.close()
    
    return


def main():

    try:
        
        header = header_processing.GetHeader(INPUT, ANNOTATION)
        if not GENOTYPES:
            header = header_processing.RemoveSamples(header)
        if LIST:
            header_processing.PrintAvailableInfo(header)
            return
        
        OutputFile(header, INPUT, OUTPUT, ANNOTATION, PARSING_STR)

    except Exception as exc:
        print(exc)
        print("Did you input any VCF file?")

    return

if __name__ == '__main__':
    main()
