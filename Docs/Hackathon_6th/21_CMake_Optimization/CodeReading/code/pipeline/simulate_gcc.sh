
/usr/lib/gcc/x86_64-linux-gnu/12/cc1 -quiet -v -imultiarch x86_64-linux-gnu hello.c -quiet -dumpbase hello.c -dumpbase-ext .c -mtune=generic -march=x86-64 -g -version -fasynchronous-unwind-tables -o build/hello.s

as -v --gdwarf-5 --64 -o build/hello.o build/hello.s

/usr/lib/gcc/x86_64-linux-gnu/12/collect2 \
  -plugin /usr/lib/gcc/x86_64-linux-gnu/12/liblto_plugin.so \
  -plugin-opt=/usr/lib/gcc/x86_64-linux-gnu/12/lto-wrapper \
  -plugin-opt=-fresolution=/tmp/ccqJldw3.res \
  -plugin-opt=-pass-through=-lgcc \
  -plugin-opt=-pass-through=-lgcc_s \
  -plugin-opt=-pass-through=-lc \
  -plugin-opt=-pass-through=-lgcc \
  -plugin-opt=-pass-through=-lgcc_s \
  --build-id --eh-frame-hdr \
  -m elf_x86_64 \
  --hash-style=gnu --as-needed \
  -dynamic-linker /lib64/ld-linux-x86-64.so.2 \
  -pie \
  -o build/hello \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/Scrt1.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/crti.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/crtbeginS.o \
  -L/usr/lib/gcc/x86_64-linux-gnu/12 \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../../../lib \
  -L/lib/x86_64-linux-gnu \
  -L/lib/../lib \
  -L/usr/lib/x86_64-linux-gnu \
  -L/usr/lib/../lib \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../.. \
  build/hello.o \
  -lgcc \
  --push-state --as-needed \
  -lgcc_s \
  --pop-state \
  -lc \
  -lgcc \
  --push-state --as-needed \
  -lgcc_s \
  --pop-state \
  /usr/lib/gcc/x86_64-linux-gnu/12/crtendS.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/crtn.o


exit 0

/usr/bin/ld \
  -plugin /usr/lib/gcc/x86_64-linux-gnu/12/liblto_plugin.so \
  -plugin-opt=/usr/lib/gcc/x86_64-linux-gnu/12/lto-wrapper \
  -plugin-opt=-fresolution=/tmp/ccVOmAPn.res \
  -plugin-opt=-pass-through=-lgcc \
  -plugin-opt=-pass-through=-lgcc_s \
  -plugin-opt=-pass-through=-lc \
  -plugin-opt=-pass-through=-lgcc \
  -plugin-opt=-pass-through=-lgcc_s \
  --build-id --eh-frame-hdr \
  -m elf_x86_64 \
  --hash-style=gnu --as-needed \
  -dynamic-linker /lib64/ld-linux-x86-64.so.2 \
  -pie \
  -o build/hello \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/Scrt1.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/crti.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/crtbeginS.o \
  -L/usr/lib/gcc/x86_64-linux-gnu/12 \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../../../lib \
  -L/lib/x86_64-linux-gnu \
  -L/lib/../lib \
  -L/usr/lib/x86_64-linux-gnu \
  -L/usr/lib/../lib \
  -L/usr/lib/gcc/x86_64-linux-gnu/12/../../.. \
  build/hello.o \
  -v \
  -lgcc --push-state --as-needed \
  -lgcc_s --pop-state -lc \
  -lgcc --push-state --as-needed \
  -lgcc_s --pop-state \
  /usr/lib/gcc/x86_64-linux-gnu/12/crtendS.o \
  /usr/lib/gcc/x86_64-linux-gnu/12/../../../x86_64-linux-gnu/crtn.o