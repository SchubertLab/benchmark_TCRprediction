import os
import re
import yaml


col_cdr3a = "CDR3_alpha"
col_va = "V_alpha"
col_ja = "J_alpha"

col_cdr3b = "CDR3_beta"
col_vb = "V_beta"
col_jb = "J_beta"

col_mhc = "MHC"
col_epitope = "Epitope"

required_cols = [col_cdr3a, col_va, col_ja, col_cdr3b, col_vb, col_jb, col_epitope, col_mhc]


path_file = os.path.dirname(__file__)
path_data = f"{path_file}/../data"
path_results = f"{path_file}/../results"


def read_config_yaml(path_yaml):
    _var_matcher = re.compile(r"\${([^}^{]+)}")
    _tag_matcher = re.compile(r"[^$]*\${([^}^{]+)}.*")

    def _path_constructor(_loader, node):
        def replace_fn(match):
            envparts = f"{match.group(1)}:".split(":")
            return os.environ.get(envparts[0], envparts[1])

        return _var_matcher.sub(replace_fn, node.value)

    yaml.add_implicit_resolver("!envvar", _tag_matcher, None, yaml.SafeLoader)
    yaml.add_constructor("!envvar", _path_constructor, yaml.SafeLoader)
    with open(path_yaml, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

