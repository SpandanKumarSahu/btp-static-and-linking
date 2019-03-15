import re
import sys
import pprint

# The compiler used by the project. In this example, it would `/usr/bin/cc `
# because it is a C-based project. Assuming default is C++. Can be changed by user
CXX_COMPILER = "/usr/bin/c++ "

#[TODO]: Implement support for other archivers (NOT A PRIORITY)
STATIC_ARCHIVER = "/usr/bin/ar "

CHANGE_DIRECTORY_CMD = "cd "

# filename: The make_log.txt file, which contains the verbose output of the build
# We try to extract various dependencies using this file
filename = sys.argv[1]

# for C++ projects, it would be "/usr/bin/c++ "
# for C projects, it would be "/usr/bin/cc "
#[TODO]: Support multiple number of compilers, for projects that are multi-lingual
if len(sys.argv) > 2:
    CXX_COMPILER = str(sys.argv[2]) + str(" ")


with open(filename, "r") as f:
    data = f.readlines()
'''
We open the make_log.txt file and try to find 3 types of essential commands:
1. CXX_COMMANDS: These commands including compiling and linking instructions
2. CD_COMMANDS: We use these commands to keep track of the directory of the files
                we are compiling/linking
3. AR_COMMANDS: Archiving commands. NOT RELEVANT NOW. But this command helps to
                code structure, and if there is a library (internal) being used.
                Might become useful in future

The algorithm is pretty simple. The way CMake generates the Makefile and the way
Makefile builds objects and binaries, is very standard, making the parsing
straightforward. We are just looking for the occurance of the three commands
mentioned above, and store relevant information in lists.
'''
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

for i in range(3):
    print("\t")

# For this small project, it is sufficient to print this
for line_num, path, data in cxx_cmds:
    print(data)

for i in range(3):
    print("\t")

# The tree representation of the very same information as printed above. It has
# relevance for big projects like symengine and if we want to parse external
# or standard libraries also
print("This is the TREE REPRESENTATION of the very same information.")

for i in range(3):
    print("\t")

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
        else:
            temp_dict = temp_dict[x]
    temp_dict['.'].append(data)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(tree)
