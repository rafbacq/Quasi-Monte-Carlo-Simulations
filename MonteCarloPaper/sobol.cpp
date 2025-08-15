#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
#include <cmath>

const int MAX_BITS = 30;
const uint64_t SCALE = 1ULL << MAX_BITS;

uint32_t grayCode(uint32_t n) {
    return n ^ (n >> 1);
}

std::vector<std::vector<uint32_t>> getDirectionNumbers(int dim) {
    std::vector<std::vector<uint32_t>> V(dim, std::vector<uint32_t>(MAX_BITS, 0));

    // Dimension 1: v[i] = 1 << (31 - i)
    for (int i = 0; i < MAX_BITS; ++i) {
        V[0][i] = 1U << (31 - i);
    }

    // Dimension 2: use x^3 + x + 1, m = [1, 1, 5]
    if (dim > 1) {
        std::vector<uint32_t> m = {1, 1, 5};
        for (int i = 0; i < m.size(); ++i) {
            V[1][i] = m[i] << (31 - i);
        }
        for (int i = m.size(); i < MAX_BITS; ++i) {
            V[1][i] = V[1][i - 1] ^ (V[1][i - 3] >> 3);
        }
    }

    return V;
}

std::vector<std::vector<double>> sobol(int n_points, int dim) {
    auto V = getDirectionNumbers(dim);
    std::vector<std::vector<double>> result;
    std::vector<uint32_t> X(dim, 0);

    for (int n = 0; n < n_points; ++n) {
        uint32_t i = grayCode(n);
        int c = __builtin_ctz(n == 0 ? 1 : n); // count trailing zeros of n

        for (int d = 0; d < dim; ++d) {
            X[d] ^= V[d][c];
        }

        std::vector<double> point(dim);
        for (int d = 0; d < dim; ++d) {
            point[d] = static_cast<double>(X[d]) / static_cast<double>(1ULL << 32);
        }

        result.push_back(point);
    }

    return result;
}
int main() {
    int num_points = 100;
    int dim = 2;
    std::string filename = "sobol_output.csv";

    auto points = sobol(num_points, dim);

    // Write to CSV
    std::ofstream file(filename);
    if (!file) {
        std::cerr << "Error: Cannot open file " << filename << " for writing.\n";
        return 1;
    }

    // Optional header
    file << "x,y\n";

    for (const auto& p : points) {
        for (int j = 0; j < dim; ++j) {
            file << p[j];
            if (j < dim - 1)
                file << ",";
        }
        file << "\n";
    }

    file.close();
    std::cout << "Sobol sequence points written to: " << filename << "\n";
    return 0;
}
