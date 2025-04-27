#include "ALL_H_FILES.h"
using namespace std;


class Password {
private:
    const int secretNum = 030525;
    const int minASCII = 33;
    const int maxASCII = 126;

    int inRange(int c) {
        c = (c - minASCII) % (maxASCII - minASCII);
        if (c < 0) c += maxASCII - minASCII;
        c += minASCII;
        return c;
    }
public:
    string passwordDecode(string encoded) {
        const int n = encoded.size();
        int l = 0, r = n - 1;
        
        string word = "";
        
        while (l <= r) {
            int sum = encoded[l++] + encoded[r--];
            int avg  = sum / 2;
            int shift = inRange(sum);           
            word = (char)avg + word + (char)shift;

        }
        
        string decoded = "";

        vector<int> mp(127, 0);
        for (char c : word) {
            mp[c]++;
        }
        
        vector<bool> has(127, false);
        for (char c : word) {
            if (has[c]) continue;
            has[c] = true;
            decoded += (char)(inRange(secretNum * mp[c] + c));
        }
        
        return decoded;
    }
};