# STATIC INSTRUMENTATION

## Project Dependency Parser
The first part of the project is to extract dependency of one file over other
header files and libraries. For this, we use cmake. To get started, first clone
the repo and then execute the following commands:
1. `mkdir build; cd build`
2. `cmake ..; make VERBOSE=1 > make_log.txt`
3. `cd ..`
4. `python parsers/cmake_extractor/project_parser.py build/make_log.txt`

The output has two segments. The second segment can be safely ignored for the
time being (detailed documentation has been mentioned in the `project_parser` file).
The first segment has 3 columns, out of which only the following are significant:
* first part, which is of the type `/usr/bin/cc` (or `/usr/bin/c++`). This specifies
the location of the compiler being used
* The second segment is of the type `-I/home/...`, this represents the dependencies
* The third and most important is the one ending with `.c` or `.cpp`, which tells
  the files being compiled, for which dependencies are being noted.

PS: Note that, the `make_log.txt` must contain all the compile/build/linking instructions
Hence, if there is any changes to the code, and the project is being build again,
first run `make clean`, and then repeat step 2, before proceeding further


## Sytax Parser
1. Use pycparser (For c based programs only):
  * First, get a precompiled program using `gcc -E`
  * Then use python python to run parser.py:
    `python parsers/parser.py src/prog.c -I/<path to lib>`
    (For me, it is: /home/spandan/KGP/BTP/testing/smallproj/lib)
  PS: The path to lib is extracted from the cmake extractor, code is in parsers/extractor
2. To run parser1.py:
  `python parsers/parser1.py`
3. To run parser2.py (Important):
  `python parsers/parser2.py src/prog.c -I/<path to lib>`
4. Run parserd_parser.py (Important features, plus conversion to xml):
  `python parsers/parsed_parser.py src/prog.c -I/<path to lib>`

### [TODO]:
- [X] Add .gitignore
- [ ] Include all features
- [ ] Provide flag for excluding standard libraries
- [X] Provide a cmake for building this file
