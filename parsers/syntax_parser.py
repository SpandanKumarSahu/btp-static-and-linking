import clang.cindex as cl
from clang.cindex import Index
from pprint import pprint
from optparse import OptionParser, OptionGroup
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree as ET
from xml.dom import minidom

cl.Config.set_library_file("/usr/local/lib/libclang.so")

'''
Please refer to the classic SyntaxTree.cpp used in clang examples
'''
def get_info(node, parent):
    global root
    if node.kind.is_declaration():
        if node.kind.name == "USING_DIRECTIVE":
            sub = SubElement(root, str(node.kind.name))
            sub.set("symbol", node.spelling)
            sub.set("type", node.type.spelling)
            sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
            sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
            sub.set("id", str(node.hash))
            sub.set("parent_id", str(node.semantic_parent.hash))
        elif node.kind.name == "NAMESPACE":
            # For global namespace
            if node.semantic_parent.kind.name == "TRANSLATION_UNIT":
                sub = SubElement(root, str(node.kind.name))
                sub.set("symbol", str(node.spelling))
                sub.set("type", str(node.type.spelling))
                sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                sub.set("id", str(node.hash))
                sub.set("parent_id", str(node.semantic_parent.hash))
            # For nested namespace
            elif node.semantic_parent.kind.name == "NAMESPACE":
                for c in root.findall(".//NAMESPACE"):
                    if c.attrib['symbol'] == node.semantic_parent.spelling and c.attrib['id'] == str(node.semantic_parent.hash):
                        sub = SubElement(c, str(node.kind.name))
                        sub.set("symbol", str(node.spelling))
                        sub.set("type", str(node.type.spelling))
                        sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                        sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                        sub.set("id", str(node.hash))
                        sub.set("parent_id", str(node.semantic_parent.hash))
        elif node.kind.name == "PARM_DECL":
            # The parameter information is updates in the function declaration, so we do nothing here
            pass
        elif node.kind.name == "VAR_DECL":
            # For global variable
            if node.semantic_parent.kind.name == "TRANSLATION_UNIT":
                sub = SubElement(root, str(node.kind.name))
                sub.set("symbol", str(node.spelling))
                sub.set("type", str(node.type.spelling))
                sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                sub.set("use_case", "declaration")
                sub.set("id", str(node.hash))
                sub.set("parent_id", str(node.semantic_parent.hash))
            # Else if parent is a namespace
            elif node.semantic_parent.kind.name == "NAMESPACE":
                for c in root.findall(".//NAMESPACE"):
                    if c.attrib['symbol'] == node.semantic_parent.spelling and c.attrib['id'] == str(node.semantic_parent.hash):
                        sub = SubElement(c, str(node.kind.name))
                        sub.set("symbol", str(node.spelling))
                        sub.set("type", str(node.type.spelling))
                        sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                        sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                        # [TODO]: Complete function for inline methods (SyntaxTree.cpp: 205)
                        # this is for extern/static
                        sub.set("storage_class_type", str(node.storage_class.name))
                        # this is for constant
                        sub.set("is_const", str(node.type.is_const_qualified()))
                        sub.set("is_volatile", str(node.type.is_volatile_qualified()))
                        # this is for inline
                        sub.set("id", str(node.hash))
                        sub.set("parent_id", str(node.semantic_parent.hash))
        elif node.kind.name in ["CLASS_DECL", "UNION_DECL", "STRUCT_DECL"]:
            if node.semantic_parent.kind.name == "TRANSLATION_UNIT":
                semantic_parent = root
            elif node.semantic_parent.kind.name in ["CLASS_DECL", "UNION_DECL", "STRUCT_DECL"]:
                #[TODO]: put them in an if-else format
                for c in root.findall(".//CLASS_DECL"):
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        semantic_parent = c
                for c in root.findall(".//UNION_DECL"):
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        semantic_parent = c
                for c in root.findall(".//STRUCT_DECL"):
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        semantic_parent = c
            elif node.semantic_parent.kind.name == "NAMESPACE":
                for c in root.findall(".//NAMESPACE"):
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        semantic_parent = c
            sub = SubElement(semantic_parent, str(node.kind.name))
            sub.set("symbol", str(node.spelling))
            sub.set("type", str(node.type.spelling))
            sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
            sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
            sub.set("id", str(node.hash))
            sub.set("parent_id", str(node.semantic_parent.hash))
            # As of C++11, Unions can't inherit. For C++ structs and class are identical (except for default access specifier)
            # [TODO]: Check for C/C++ compatibility
            inheritance = SubElement(sub, "INHERITANCES")
            for c in node.get_children():
                if c.kind.name == "CXX_BASE_SPECIFIER":
                    inherit = SubElement(inheritance, "BASE")
                    inherit.set("symbol", str(c.spelling))
                    inherit.set("type", str(c.referenced.kind.name))
                    inherit.set("access", str(c.access_specifier.name))
                    inherit.set("ref_id", str(c.referenced.hash))
                    inherit.set("name", str(c.referenced.spelling))
        elif node.kind.name == "TYPEDEF_DECL":
            sub = SubElement(root, str(node.kind.name))
            sub.set("symbol", str(node.spelling))
            sub.set("type", str(node.type.spelling))
            sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
            sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
            sub.set("id", str(node.hash))
            sub.set("parent_id", str(node.semantic_parent.hash))
        elif node.kind.name == "CXX_ACCESS_SPEC_DECL":
            pass
        elif node.kind.name == "FIELD_DECL":
            for c in root.iter():
                try:
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        sub = SubElement(c, str(node.kind.name))
                        sub.set("symbol", str(node.spelling))
                        sub.set("type", str(node.type.spelling))
                        sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                        sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                        sub.set("id", str(node.hash))
                        sub.set("parent_id", str(node.semantic_parent.hash))
                except:
                    continue
        elif node.kind.name == "FRIEND_DECL":
            #[TODO]: See and implement from SyntaxTree.cpp
            pass
        elif node.kind.name == "FUNCTION_TEMPLATE":
            #[TODO]: Not even implemented in SyntaxTree. Less priority, but needs to be done
            pass
        elif node.kind.name == "FUNCTION_DECL":
            pass
    elif node.kind.is_statement():
        if node.kind.name in ["COMPOUND_STMT", "IF_STMT", "FOR_STMT", "WHILE_STMT",
        "DO_STMT", "SWITCH_STMT", "CASE_STMT", "CONDITIONAL_OPERATOR", "PAREN_EXPR", "BINARY_OPERATOR"] :
            for c in root.iter():
                try:
                    if c.attrib['id'] == str(node.semantic_parent.hash):
                        sub = SubElement(c, str(node.kind.name))
                        sub.set("symbol", str(node.spelling))
                        sub.set("type", str(node.type.spelling))
                        sub.set("begin", str(node.extent.start.file) + "[" + str(node.extent.start.line) + ":" + str(node.extent.start.column) + "]")
                        sub.set("end", str(node.extent.end.file) + "[" + str(node.extent.end.line) + ":" + str(node.extent.end.column) + "]")
                        sub.set("id", str(node.hash))
                        sub.set("parent_id", str(node.semantic_parent.hash))
                except:
                    continue
        elif node.kind.name == "DECL_STMT":
            pass
    # if node.kind.name == "CXX_BASE_SPECIFIER":
    #     print(node.spelling)
    print(node.kind.name)
    # print(node.kind.name, node.kind.is_declaration())
    for c in node.get_children():
        get_info(c, node)
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

root = Element("GLOBAL")
root = get_info(tu.cursor, root)
# root.set('id', str(0))
# print(ET.tostring(root, encoding='utf8').decode('utf8'))
xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
with open(str(args[0].split('.')[0])+".xml", "w") as f:
    f.write(xmlstr)
