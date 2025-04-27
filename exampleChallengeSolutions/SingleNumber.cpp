#include "ALL_H_FILES.h"
using namespace std;


class SingleNumber {
public:
    int singleNumber(vector<int> nums) {
        int ones = 0, twos = 0;
        for (int x : nums) {
            ones = (x ^ ones) & ~twos;
            twos = (x ^ twos) & ~ones;
        }
        return ones;
    }
};