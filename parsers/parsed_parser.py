import clang.cindex as cl
from clang.cindex import Index
from pprint import pprint
from optparse import OptionParser, OptionGroup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree as ET
from xml.dom import minidom

cl.Config.set_library_file("/usr/local/lib/libclang.so")

# def get_info(node):
#   children = [get_info(c) for c in node.get_children()]
#   return {  'usr' : node.get_usr(),
#             'spelling' : node.spelling,
#             'location' : node.location,
#             'extent.start' : node.extent.start,
#             'extent.end' : node.extent.end,
#             'is_definition' : node.is_definition(),
#             'children' : children }

def get_info(node, parent):
  try:
    sub = SubElement(parent, str(node.kind).split('.')[-1])
  except:
    sub = SubElement(parent, "Unknown")
  # print(dir(node.extent.start))
  sub.set('id', str(id(node)))
  sub.set('syntax_parent', str(id(parent)))
  sub.set('semantic_parent', str(0) if node.semantic_parent is None else str(id(node.semantic_parent)))
  sub.set('usr', "None" if node.get_usr() is None else str(node.get_usr()))
  sub.set('spelling', "None" if node.spelling is None else str(node.spelling))
  sub.set('location', "None" if (node.location is None or node.location.file is None) else str(node.location.file)+"["+str(node.location.line)+"]")
  sub.set('extent.start', "None" if (node.extent.start is None or node.extent.start.file is None) else str(node.extent.start.file)+"["+ str(node.extent.start.line) + "]")
  sub.set('extent.end', "None" if (node.extent.end is None or node.extent.end.file is None) else str(node.extent.end.file)+"["+ str(node.extent.end.line) + "]")
  sub.set('is_definition', str(node.is_definition()))
  children = [get_info(c, sub) for c in node.get_children()]
  return parent

parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")
parser.disable_interspersed_args()
(opts, args) = parser.parse_args()

index = Index.create()
tu = index.parse(None, args)

# print(dir(tu.cursor.get_children()[0].semantic_parent))
# print([dir(c.semantic_parent) for c in tu.cursor.get_children()])
# print(str(tu.cursor.kind).split('.')[-1], tu.cursor.type)

if not tu:
  parser.error("unable to load input")

root = Element("root")
root = get_info(tu.cursor, root)
root.set('id', str(0))
print(ET.tostring(root, encoding='utf8').decode('utf8'))
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open(str(args[0][:-1])+"xml", "w") as f:
    f.write(xmlstr)
