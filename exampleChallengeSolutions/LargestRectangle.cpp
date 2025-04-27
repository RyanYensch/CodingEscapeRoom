#include "ALL_H_FILES.h"
using namespace std;


class LargetRectangle {
public:
    int largestRectangle(vector<int> heights) {
        stack<int> st;
        st.push(-1);
        int maxA = 0;

        for (int i = 0; i < (int)heights.size(); i++) {
            while (st.top() != -1 && heights[i] <= heights[st.top()]) {
                int height = heights[st.top()];
                st.pop();
                int width = i - st.top() - 1;
                maxA = max(maxA, height * width);
            }
            st.push(i);
        }

        while (st.top() != -1) {
            int height = heights[st.top()];
            st.pop();
            int width = heights.size() - st.top() - 1;
            maxA = max(maxA, height * width);
        }

        return maxA;
    }
};

