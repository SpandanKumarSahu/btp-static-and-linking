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

#[TODO]:
1. Include all features
2. Provide flag for excluding standard libraries
3. Provide a cmake for building this file
