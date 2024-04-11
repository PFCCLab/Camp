
# .PHONY: build
build:
	@mkdir -p build

.PHONY: clean
clean:
	@rm -rf build

.PHONY: determistic_va_space
determistic_va_space:
	echo 0 > /proc/sys/kernel/randomize_va_space

.PHONY: determistic_va_space
randomize_va_space:
	echo 2 > /proc/sys/kernel/randomize_va_space

compile: build
	@gcc -c a.c -g -o build/a.o
	@gcc -c b.c -g -o build/b.o
	@gcc build/a.o build/b.o -o build/ab

list_a_symbols: compile
	readelf --symbols build/a.o

list_b_symbols: compile
	readelf --symbols build/b.o

list_ab_symbols: compile
	readelf --symbols build/ab

dump_a: compile
	objdump -d build/a.o
	
dump_b: compile
	objdump -d build/b.o

dump_ab: compile
	objdump -d build/ab
