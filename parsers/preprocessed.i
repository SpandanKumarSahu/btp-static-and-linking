# 1 "src/prog.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "src/prog.c"

# 1 "/home/spandan/KGP/BTP/testing/smallproj/lib/foo.h" 1



struct foo_str{
  int x;
  int y;
};

struct foo_str foo(struct foo_str x);
# 3 "src/prog.c" 2

int main(void)
{
    struct foo_str x;
    x.x = 3;
    struct foo_str y;
    y = foo(x);

    return 0;
}
