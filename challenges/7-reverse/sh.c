#include <stdio.h>
#include <string.h>

char FLAG[20] = "HTM{...-....-..-..}";

int check_password1(char *target, size_t length) {
    int success = strncmp("hunter-root-4", target, length) == 0;
    if (success) {
        FLAG[9] = target[length - 1];
    }
    return success;
}

int check_password2(char *target, size_t length) {
    int count = 0;
    for (size_t i = 0; i < length; i++) {
        if (target[i] < '1' || target[i] > '9') {
            return 0;
        }
        count *= 10;
        count += target[i] - '0';
    }

    if (count != 113575) {
        return 0;
    }

    FLAG[4] = target[4];
    FLAG[6] = target[2];
    FLAG[11] = target[2];
    FLAG[13] = target[1];
    FLAG[14] = target[5];
    return 1;
}

char goal3[] = {41, 11, 46, 6, 53, 19, 55, 17, 51, 4, 33};

int check_password3(char *target, size_t length) {
    char *key = "abcsecretkey";
    if (length != 11) {
        return 0;
    }
    for (size_t i = 0; i < length; i++) {
        char keych = key[i % strlen(key)];
        char goalch = goal3[i % strlen(key)];
        if ((target[i] ^ keych) != goalch) {
            return 0;
        }
    }

    FLAG[5] = target[0];
    FLAG[8] = target[8];
    FLAG[10] = target[2];
    FLAG[16] = target[3];
    FLAG[17] = target[4];
    return 1;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    int (*ps[]) (char *target, size_t length) = {
        check_password1,  // hunter-root-4
        check_password2,  // 113575
        check_password3,  // HiMuPpEtGoD
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
