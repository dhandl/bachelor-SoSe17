from analyses import analyses, Analysis
from collections import namedtuple

#####################
# ANALYSIS
#####################

def get_opt_id(opt):
  opt_id = opt.replace("!", "") # remove intital !
  if "=" in opt_id:
    opt_id = opt_id.split("=")[0] # take everything in front of =

  return opt_id


def get_opt_index(settings, k):
  for i, opt in enumerate(settings):
    if k == get_opt_id(opt):
      return i

  return -1


def remove_opts(haystack, needles):
  needle_keys = map(get_opt_id, needles)
  return [hay for hay in haystack if not get_opt_id(hay) in needle_keys]


def get_mva(name, extra_opts=[], rm_opts=[]):
  for (mva_type, mva_name, opts) in analyses:
    # look for mva config with matching mva_name
    if name == mva_name:
      opts = remove_opts(opts, extra_opts)
      opts += extra_opts
      opts = remove_opts(opts, rm_opts)
      print Analysis(mva_type, mva_name, ":".join(opts))
      return Analysis(mva_type, mva_name, ":".join(opts))

  raise Exception("No such analysis '{}'".format(mva_name))

#####################
# VARIABLES
#####################

Var = namedtuple("Var", "name type")

def parse_var(var):
  if "$" in var: 
    parts = var.split("$", 1)
    name = parts[0].strip()
    vtype = parts[1].strip()
  else:
    name = var
    vtype = 'F'

  return Var(name, vtype)

def load_var_list(file_name, add_vars=[], rm_vars=[]):
  with open("config/{}.txt".format(file_name)) as f:
    all_variables = [parse_var(l.strip()) for l in f.read().split("\n") if l.strip() != "" and not l.strip().startswith("#")]

  if add_vars:
    for entry in add_vars:
      var = parse_var(entry)

      if var.name not in [v.name for v in all_variables]:
        all_variables.append(var)

  rm_vars = [parse_var(var).name for var in rm_vars]

  return [var for var in all_variables if not var.name in rm_vars]

