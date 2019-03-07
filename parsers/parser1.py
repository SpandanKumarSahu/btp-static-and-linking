import sys
import clang.cindex as cl
from clang.cindex import Index

cl.Config.set_library_file("/usr/local/lib/libclang.so")

include_string = "-I/home/spandan/KGP/BTP/testing/smallproj/lib"
filename = "/home/spandan/KGP/BTP/testing/smallproj/src/prog.c"

args = include_string

index = cl.Index.create()
tu = index.parse(filename)
print(tu)
