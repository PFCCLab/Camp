int foovar = 2;

int main() {
  int *bar = &foovar;
  return sizeof(bar);
}