import sys
import clang.cindex as cl
from clang.cindex import Index

cl.Config.set_library_file("/usr/local/lib/libclang.so")

filename = str(sys.argv[1])

index = cl.Index.create()
tu = index.parse(filename)
print(tu)
