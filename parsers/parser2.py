import clang.cindex as cl
from clang.cindex import Index
from pprint import pprint
from optparse import OptionParser, OptionGroup

cl.Config.set_library_file("/usr/local/lib/libclang.so")

def get_info(node):
  children = [get_info(c) for c in node.get_children()]
  return {  'usr' : node.get_usr(),
            'spelling' : node.spelling,
            'location' : node.location,
            'extent.start' : node.extent.start,
            'extent.end' : node.extent.end,
            'is_definition' : node.is_definition(),
            'children' : children }

# def get_loc(nodes):
#     loc = [get_loc(c) for c in nodes['children']]
#     if loc is None:
#         return
#     return loc.extend(nodes['location'])

parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
parser.disable_interspersed_args()
(opts, args) = parser.parse_args()

index = Index.create()
tu = index.parse(None, args)
# print(dir(tu.cursor))
if not tu:
  parser.error("unable to load input")

# nodes = get_info(tu.cursor)
# print(nodes)
# print(get_loc(nodes))
pprint(('nodes', get_info(tu.cursor)))
