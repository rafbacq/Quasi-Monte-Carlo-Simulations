#include <cstdint>  

#include <iostream> 

struct Xoshiro256 {  

uint64_t state[4]; //initialize state array to store four 64-bit unsigned integers.

// Constructor with a simple seed-to-state expansion 
	Xoshiro256(uint64_t seed) { 
    		state[0] = seed; 
    		state[1] = seed * 0x9E3779B97F4A7C15; // 11400714819323198485 in decimal
    		state[2] = seed ^ 0xBF58476D1CE4E5B9; // 13787848793156543929 in decimal
    		state[3] = ~seed + 0x94D049BB133111EB; //10723151780598845931 in decimal
			// ~ reverses bits in number
	} 
 
	// Bit rotation: left rotate by k bits 
	static uint64_t rotateLeft(uint64_t x, int k) { 
   	 	return (x << k) | (x >> (64 - k)); 
	} 
 
	// Official xoshiro256** output function 
	uint64_t next() { 
    		uint64_t result = rotateLeft(state[1] * 5, 7) * 9; 
 
    		uint64_t t = state[1] << 17; 
 
    		state[2] ^= state[0]; 
    		state[3] ^= state[1]; 
    		state[1] ^= state[2]; 
    		state[0] ^= state[3]; 
 
    		state[2] ^= t; 
    		state[3] = rotateLeft(state[3], 45); 
 
    		return result; 
	} 
 
	// Bounded output: random number in [0, max) 
	uint64_t nextBounded(uint64_t max) { 
    		return next() % max; 
	} 
 }; 

//Implemented to produce pairs of points: 
int main() {
    Xoshiro256 rng(12346); // seed
    const double scale = 1000.0;  // scale factor to normalize to [0, 1)

    for (int i = 0; i < 1000; ++i) {
        uint64_t x = rng.nextBounded(1000);
        uint64_t y = rng.nextBounded(1000);

        double fx = static_cast<double>(x) / scale;
        double fy = static_cast<double>(y) / scale;

        std::cout << fx << "," << fy << std::endl;
        // Now (fx, fy) ∈ [0,1)^2 — suitable for discrepancy analysis
    }

    return 0;
}