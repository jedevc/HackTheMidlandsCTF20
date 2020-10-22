#include <stdio.h>
#include <string.h>

char FLAG[20] = "HTM{...............}";

// weeeeeelp. i should've commented this out.
char NOPE[20] = "HTM{7174niC_f4ilur3}";

int check_password1(char *target, size_t length) {
    int success = strncmp("hunter-root-4", target, length) == 0;
    if (success) {
        FLAG[7] = target[12];
        FLAG[13] = target[12];
        FLAG[16] = target[1];
        FLAG[17] = target[7];
    }
    return success;
}

int check_password2(char *target, size_t length) {
    int count = 0;
    for (size_t i = 0; i < length; i++) {
        if (target[i] < '0' || target[i] > '9') {
            return 0;
        }
        count *= 10;
        count += target[i] - '0';
    }

    if (count != 113575) {
        return 0;
    }

    FLAG[4] = target[4];
    FLAG[5] = target[1];
    FLAG[6] = target[4];
    FLAG[18] = target[2];
    return 1;
}

char goal3[] = { 34, 3, 13, 23, 28, 60, 20, 12, 24, 7, 0, 11 };

int check_password3(char *target, size_t length) {
    char *key = "abcsecretkey";
    for (size_t i = 0; i < length; i++) {
        char keych = key[i % strlen(key)];
        char goalch = goal3[i % strlen(key)];
        if ((target[i] ^ keych) != goalch) {
            return 0;
        }
    }

    FLAG[8] = target[2];
    FLAG[9] = target[7];
    FLAG[10] = target[0];
    FLAG[11] = target[5];
    FLAG[12] = target[6];
    FLAG[14] = target[7];
    FLAG[15] = target[8];
    return 1;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int (*ps[]) (char *target, size_t length) = {
        check_password1,  // hunter-root-4
        check_password2,  // 113575
        check_password3,  // Candy_filler
        NULL
    };

    char buffer[256];

    printf("---------------------------------------\n");
    printf(" ***  ENHANCED PROTECTION ENABLED  *** \n");
    printf("TRIPLE-PASSWORD AUTHENTICATION REQUIRED\n");
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
