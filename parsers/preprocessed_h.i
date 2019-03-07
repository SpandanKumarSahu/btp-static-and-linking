# 1 "lib/foo.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "lib/foo.c"
# 1 "lib/foo.h" 1



struct foo_str{
  int x;
  int y;
};

struct foo_str foo(struct foo_str x);
# 2 "lib/foo.c" 2

struct foo_str foo(struct foo_str x)
{
    x.x + 5;
    return x;
}
