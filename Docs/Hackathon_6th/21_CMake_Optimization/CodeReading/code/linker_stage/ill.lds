
SECTIONS
{
  . = 0x10000;
  .text : { *(.text) }            /* PC will be at 0x1000b */
                        
  . = 0x1000b + 0x7fffffff - 0x2; /* 0x80010008 */
                                  /* -0x02 caused by section alignment, .data section 
                                    can't be at 0x8001000a but 0x8001000c */
  .data : { *(.data) }
}