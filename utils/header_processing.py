#!/usr/bin/env python3
# -- coding: utf-8 --

def GetHeader(vcf_filename:str, 
                ann_option:str):
    '''
    Gets header from VCF metadata (##) and transforms it
    into a list.

    Parameters:
        vcf_filename: VCF to retrieve header
        ann_option: Annotation field, if any.
    Returns:
        header: List of all avaiable information in the
        VCF file
    '''
    header = list()
    default_info_fields = list()
    vcf_file = open(vcf_filename, "r")
    for vcf_line in vcf_file:
        if vcf_line.startswith("#"):
            if vcf_line.startswith("##INFO=<ID="):
                info_field = vcf_line[:-1].split(sep="##INFO=<ID=")[1].split(sep=",")[0]
                default_info_fields.append(info_field)
            elif vcf_line.startswith("#CHROM"):
                header = vcf_line[1:-1].split(sep="\t")
            else:
                pass
        else:
            # if # is not found we reached variants
            # not useful for obtaining the annotation
            break
    vcf_file.close()

    # Now it's time to replace the original "INFO" with the fields we encountered
    info_field_index = header.index("INFO")
    header.pop(info_field_index)
    for item in reversed(default_info_fields):
        header.insert(info_field_index, item)     

    if not ann_option:
        if "CSQ" in header:
            header.remove("CSQ")
        return header
    else:
        ann = "##INFO=<ID=" + ann_option
        vcf_file = open(vcf_filename, "r")
        for vcf_line in vcf_file:
            if vcf_line.startswith("#"):
                if vcf_line.startswith(ann):
                    header_ANN = vcf_line
                else:
                    pass
            else:
                break
        vcf_file.close()
        ann_field_index = header.index(ann_option)
        header_ANN = header_ANN.split(sep="Format: ")[1][:-3].split(sep="|")
        header.pop(ann_field_index)
        for item in reversed(header_ANN):
            header.insert(ann_field_index, item)      

        return header

def RemoveSamples(header:list):
    '''
    This function allows to remove samples from the
    output if it's not desired. Default is that the 
    samples are removed.

    Parameters:
        header: list of available information in the
        VCF file
    Returns:
        modified header: header without the samples
    '''
    samples_start = header.index("FORMAT")
    return header[:samples_start]

def PrintAvailableInfo(header:list):
    '''
    Print de list of available information extracted from the
    header.

    Parameters:
        header: list of available information in the VCF file
    Returns:
        None
    '''
    print("\n".join(header))
    return

