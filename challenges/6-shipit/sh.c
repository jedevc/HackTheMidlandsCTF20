#include <stdio.h>
#include <string.h>

char FLAG[20] = "HTM{7174niC_f4ilur3}";

int check_password(char *target, size_t length) {
    int success = strcmp(FLAG, target) == 0;
    return success;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int (*ps[]) (char *target, size_t length) = {
        check_password,
        NULL
    };

    char buffer[256];

    printf("---------------------------------------\n");
    printf(" ***  ENHANCED PROTECTION ENABLED  *** \n");
    printf("   PASSWORD AUTHENTICATION REQUIRED    \n");
    printf("---------------------------------------\n");

    int (**p) (char *target, size_t length) = 0;
    for (p = &ps[0]; *p != NULL; p++) {
        printf("password: ");
        if (fgets(buffer, 256, stdin) == NULL) {
            return 1;
        }
        buffer[strlen(buffer) - 1] = '\0';
        if (!(*p)(buffer, strlen(buffer))) {
            printf("shell access has been rejected!\n");
            return 1;
        }
        printf("UNLOCKED\n");
    }

    printf("---------------------------------------\n");
    printf(" ***     AUTHENTICATION SUCCESS    *** \n");
    printf("---------------------------------------\n\n");

    printf("FLAG: %s\n", FLAG);

    return 0;
}
