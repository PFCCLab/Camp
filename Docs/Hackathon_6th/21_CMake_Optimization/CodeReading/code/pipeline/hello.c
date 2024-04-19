#include <stdio.h>

void foo() { printf("Hello, World from address %p\n", foo); }

int main() {
  foo();
  return 0;
}
