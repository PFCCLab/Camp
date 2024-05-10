#include <stdio.h>

extern const char* format;

void foo() {
  // print the address of the function foo
  printf(format, foo); 
}