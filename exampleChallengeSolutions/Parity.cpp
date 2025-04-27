#include "ALL_H_FILES.h"
using namespace std;


class Parity {
public:
    int bitParity(vector<int> nums) {
        int res = 0;
        for (int x : nums) {
            bool parity = 0;
            while (x) {
                parity ^= x & 1;
                x >>= 1;
            }
            res += parity;
        }
        return res;
    }
};