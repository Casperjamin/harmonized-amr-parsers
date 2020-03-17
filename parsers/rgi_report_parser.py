#!/usr/bin/env python

import argparse
import csv
import json


def parse_rgi_report_txt(path_to_rgi_result):
    """
    Args:
        path_to_rgi_report (str): Path to the tabular rgi report file (SAMPLE-ID.rgi.txt).
    Returns:
        list of dict: Parsed rgi report.
        For example:
        [
            {
                'orf_id': 'contig00007_44 # 46711 # 49833 # -1 # ID=7_44;partial=00;start_type=ATG;rbs_motif=AGGAG;rbs_spacer=5-10bp;gc_cont=0.547',
                'contig': 'contig00007_44',
                'start': 46711,
                'stop': 49833,
                'orientation': '-',
                'cut_off': 'Strict',
                'pass_bitscore': 1800,
                'best_hit_bitscore': 1894.78,
                'best_hit_aro': 'mdtB',
                'best_identities': 92.7,
                'aro': '3000793',
                'model_type': 'protein homolog model',
                'snps_in_best_hit_aro': [
                    'S357N',
                    'D350N'
                ],
                'other_snps': None,
                'drug_class': 'aminocoumarin antibiotic',
                'resistance mechanism': 'antibiotic efflux',
                'amr_gene_family': 'resistance-nodulation-cell division (RND) antibiotic efflux pump',
                'predicted_dna': 'ATGCAGGTGTTACCTCCTGACAACACAGGCGGACCATCGC...',
                'predicted_protein': 'MQVLPPDNTGGPSRLFILRPVATTLLMVAILLAGII...',
                'card_protein_sequence': 'MQVLPPSSTGGPSRLFIMRPVATTLLMVAILL...',
                'percentage_length_of_reference_sequence': 100.00,
                'id': 'gnl|BL_ORD_ID|776|hsp_num:0',
                'model_id': '820'
            },
            ...
        ]
    """
    rgi_report_fieldnames = [
        'orf_id',
        'contig',
        'start',
        'stop',
        'orientation',
        'cut_off',
        'pass_bitscore',
        'best_hit_bitscore',
        'best_hit_aro',
        'best_identities',
        'aro',
        'model_type',
        'snps_in_best_hit_aro',
        'other_snps',
        'drug_class',
        'resistance mechanism',
        'amr_gene_family',
        'predicted_dna',
        'predicted_protein',
        'card_protein_sequence',
        'percentage_length_of_reference_sequence',
        'id',
        'model_id'
    ]
    rgi_report_results = []
    
    def parse_value_maybe(value):
        if value == "n/a":
            return None
        else:
            return value
        
    with open(path_to_rgi_result) as rgi_report_file:
        reader = csv.DictReader(rgi_report_file, fieldnames=rgi_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = [
            'start',
            'stop',
        ]
        float_fields = [
            'pass_bitscore',
            'best_hit_bitscore',
            'best_identities',
            'percentage_length_of_reference_sequence'
        ]
        array_fields = [
            'snps_in_best_hit_aro',
            'other_snps'
        ]
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            for key in array_fields:
                # 'n/a' => None
                # 'S80I' => ['S80I']
                # 'S357N, D350N' => ['S357N', 'D350N']
                row[key] = row[key].split(', ') if parse_value_maybe(row[key]) else None
            rgi_report_results.append(row)

    return rgi_report_results


def main(args):
    parsed_rgi_report = parse_rgi_report_txt(args.rgi_report)
    print(json.dumps(parsed_rgi_report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("rgi_report", help="Input rgi report (txt)")
    args = parser.parse_args()
    main(args)
