
.PHONY: build
build: clean
	mkdir -p build


.PHONY: clean
clean:
	rm -rf build


hello: hello.c build
	gcc -o build/hello hello.c

hello_verbose: hello.c build
	gcc -o build/hello -v hello.c

manual: hello.c build
	sh simulate_gcc.sh

dump: 
	objdump -d build/hello


.PHONY: run
run: hello
	./build/hello