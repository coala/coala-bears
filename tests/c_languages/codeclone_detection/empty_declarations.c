#include <stdio.h>
#include "not_existant.c"

int wihtout_params(void);

void* with_one_param(int x);

char with_two_params(char*, double);

int with_body(int *argc) {
    if (argc) {
        return 0;
    } else {
        return 1;
    }
    return 2;
}
