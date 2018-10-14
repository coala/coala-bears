#define f(c) { \
    char s[10]; \
    s[c] = 42; \
}
int main() {
    f(100);
    return 0;
}
