import re
import sys

CXX_COMPILER = "/usr/bin/c++ "
STATIC_ARCHIVER = "/usr/bin/ar "
CHANGE_DIRECTORY_CMD = "cd "

filename = sys.argv[1]
with open(filename, "r") as f:
    data = f.readlines()

cxx_cmds = []
cd_cmds = []
static_link_cmds = []

for line_num, x in enumerate(data):
    if CHANGE_DIRECTORY_CMD in x:
        if CXX_COMPILER in x:
            temp_ls = x.split()
            cd_cmds.append((line_num, ' '.join(temp_ls[temp_ls.index(CHANGE_DIRECTORY_CMD.strip()):temp_ls.index(CHANGE_DIRECTORY_CMD.strip())+2])))
            cxx_cmds.append((line_num, cd_cmds[-1][1], ' '.join(temp_ls[temp_ls.index(CXX_COMPILER.strip()):])))
        else:
            temp_ls = x.split()
            cd_cmds.append((line_num, ' '.join(temp_ls[temp_ls.index(CHANGE_DIRECTORY_CMD.strip()):temp_ls.index(CHANGE_DIRECTORY_CMD.strip())+2])))
    elif CXX_COMPILER.strip() in x:
        cxx_cmds.append((line_num, cd_cmds[-1][1], ' '.join(x[x.index(CXX_COMPILER.strip()):].strip().split(';'))))
    elif STATIC_ARCHIVER in x:
        static_link_cmds.append((line_num, x))

tree = {}
tree['.'] = []

for line_num, path, data in cxx_cmds:
    # print(data)
    temp_ls = path[path.index(CHANGE_DIRECTORY_CMD) + len(CHANGE_DIRECTORY_CMD):].split('/')
    temp_ls = [x for x in temp_ls if len(x) > 0]
    temp_dict = tree
    for x in temp_ls:
        if x not in temp_dict:
            temp_dict[x] = {}
            temp_dict = temp_dict[x]
            temp_dict['.'] = []
    temp_dict['.'].append(data)
print(tree)
