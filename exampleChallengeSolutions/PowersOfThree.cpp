#include "ALL_H_FILES.h"
using namespace std;


class PowersOfThree {
public:
    bool powersOfThree(int n) {
        while (n > 0) {
            if (n % 3 == 2) {
                return false;
            }
            n /= 3;
        }
        return true;
    }
};

