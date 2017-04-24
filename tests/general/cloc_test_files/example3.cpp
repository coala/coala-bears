#include <cstdio>

#define PI 3.1415926
using namespace std;


int main()
{
    const double radii = 1.0;
    const double area = PI * radii * radii;
    cout << 'Area for the circle with radii ' << radii <<
            ' is ' << area << endl;
    return 0;
}
