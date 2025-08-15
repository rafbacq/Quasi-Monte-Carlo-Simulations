class Xoshiro256:
    def __init__(self, seed):
        self.state = [0] * 4
        self.state[0] = seed
        self.state[1] = seed * 0x9E3779B97F4A7C15
        self.state[2] = seed ^ 0xBF58476D1CE4E5B9
        self.state[3] = ~seed + 0x94D049BB133111EB

    @staticmethod
    def rotate_left(x, k):
        return (x << k) | (x >> (64 - k))

    def next(self):
        result = self.rotate_left(self.state[1] * 5, 7) * 9
        t = self.state[1] << 17

        self.state[2] ^= self.state[0]
        self.state[3] ^= self.state[1]
        self.state[1] ^= self.state[2]
        self.state[0] ^= self.state[3]

        self.state[2] ^= t
        self.state[3] = self.rotate_left(self.state[3], 45)

        return result

    def next_bounded(self, max):
        return self.next() % max


rng = Xoshiro256(12346)

for i in range(1000):
    x = rng.next_bounded(1000)
    y = rng.next_bounded(1000)
    print(x, y)