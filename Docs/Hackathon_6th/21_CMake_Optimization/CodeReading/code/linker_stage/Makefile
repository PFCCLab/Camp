
all: link

.PHONY: build
build:
	@mkdir -p build

.PHONY: clean
clean:
	rm -rf build

compile: build
	gcc -g -c ill.c -o build/ill.o

# https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html#index-mcmodel_003dlarge-3
compile_large: build
	gcc -g -mcmodel=large -c ill.c -o build/ill_large.o

build/ill.o: compile
link: build/ill.o
	ld -T ill.lds build/ill.o -o build/ill

build/ill_large.o: compile_large
link_large: build/ill_large.o
	ld -T ill.lds build/ill_large.o -o build/ill_large

list_program_headers: link
	readelf -lW build/ill

list_sections: link
	readelf -SW build/ill

dump_raw: build/ill.o
	objdump -d build/ill.o

dump_raw_large: build/ill_large.o
	objdump -d build/ill_large.o

dump_ill: build/ill
	objdump -d build/ill

dump_ill_large: build/ill_large
	objdump -d build/ill_large

.PHONY: default_lds
default_lds:
	ld --verbose > default.lds