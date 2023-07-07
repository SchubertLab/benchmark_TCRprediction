import os


col_cdr3a = 'CDR3_alpha'
col_va = 'V_alpha'
col_ja = 'J_alpha'

col_cdr3b = 'CDR3_beta'
col_vb = 'V_beta'
col_jb = 'J_beta'

col_mhc = 'MHC'
col_epitope = 'epitope'

required_cols = [col_cdr3a, col_va, col_ja, col_cdr3b, col_vb, col_jb, col_epitope, col_mhc]


path_file = os.path.dirname(__file__)
path_data = f'{path_file}/../data'
path_results = f'{path_file}/../results'
