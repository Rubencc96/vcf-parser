#!/usr/bin/env python3
# -- coding: utf-8 --

def LineFormatting (header, line):
    '''
    The VCF lines are process to obtain the information about the
    variants in the same order as it is in the header.
    This function allows the VCF to not be annotated (TODO: verify it works).

    Parameters:
        header: VCF header extracted with vcf-parser.
        line: VCF line containing the variant info
    Returns:
        formatted_line: list of info of the line, formatted to be the same
        length as the header.
    '''
    formatted_line = [""] * len(header)

    for index, var_info in enumerate(line.split(sep="\t")):
        if index < 7:
            # if we are before the info field, the index fields will
            # coincide with the info header
            formatted_line[index] = var_info
        elif index == 7:
            # In VCF file format the 8th field is intended for INFO
            # Since we already splitted INFO fields in the header
            # it will be necesary to do the same in the lines of the VCF variants
            ## TODO: i should do it w/o hardcoding

            for info_item in var_info.split(sep=";"):
                if info_item == 'NEGATIVE_TRAIN_SITE':
                    info_index = header.index('NEGATIVE_TRAIN_SITE')
                    formatted_line[info_index] = info_item
                elif info_item =='POSITIVE_TRAIN_SITE':
                    info_index = header.index('POSITIVE_TRAIN_SITE')
                    formatted_line[info_index] = info_item
                else:
                    
                    field, info = info_item.split(sep="=")
                    if field in header:
                        info_index = header.index(field)
                        formatted_line[info_index] = info
        else:
            # If we removed genotypes we should stop the processing
            if len(header)-1 == info_index:
                return [formatted_line]
            info_index += 1
            formatted_line[info_index] = var_info

    return [formatted_line]

def LineFormattingAnn (header, line, ann_option):
    '''
    The VCF lines are process to obtain the information about the
    variants in the same order as it is in the header.
    This function works for annotated VCFs.

    Parameters:
        header: VCF header extracted with vcf-parser.
        line: VCF line containing the variant info
        ann_option: Annotation string
    Returns:
        formatted_line: list of info of the line, formatted to be the same
        length as the header.
    '''
    formatted_line = [""] * len(header)

    for index, var_info in enumerate(line.split(sep="\t")):
        if index < 7:
            # if we are before the info field, the index fields will
            # coincide with the info header
            formatted_line[index] = var_info
        elif index == 7:
            # In VCF file format the 8th field is intended for INFO
            # Since we already splitted INFO fields in the header
            # it will be necesary to do the same in the lines of the VCF variants
            ## TODO: i should do it w/o hardcoding

            def_vcfinfo, ann_info = var_info.split(sep=";"+ann_option+"=")

            for info_item in def_vcfinfo.split(sep=";"):
                if info_item == 'NEGATIVE_TRAIN_SITE':
                    info_index = header.index('NEGATIVE_TRAIN_SITE')
                    formatted_line[info_index] = info_item
                elif info_item =='POSITIVE_TRAIN_SITE':
                    info_index = header.index('POSITIVE_TRAIN_SITE')
                    formatted_line[info_index] = info_item
                else:
                    
                    field, info = info_item.split(sep="=")
                    if field in header:
                        info_index = header.index(field)
                        formatted_line[info_index] = info

            dif_anns = ann_info.split(sep=",")
            n_anns = len(dif_anns)
            formatted_line = [formatted_line] * n_anns
            for i in range(n_anns):
                copy_index = info_index
                for info_item in dif_anns[i].split(sep="|"):
                    copy_index += 1
                    formatted_line[i][copy_index] = info_item
            info_index = copy_index
                
        else:
            # If we removed genotypes we should stop the processing
            if len(header)-1 == info_index:
                return formatted_line
            info_index += 1
            for i in range(n_anns):
                formatted_line[i][info_index] = var_info

    return formatted_line

def _MotiveProcessing(motive, header):
    motive_windex = list()
    for item in motive.split(sep="%"):
        if item == '':
            pass
        elif item in header:
            motive_windex.append(header.index(item))
        else:
            motive_windex.append(item)


    return motive_windex

def Parsing(motive, header, line):
    motive_windex = _MotiveProcessing(motive, header)

    out_line = list()
    for item in motive_windex:
        if type(item) == int:
            out_line.append(line[item])
        else:
            out_line.append(item)

    return out_line