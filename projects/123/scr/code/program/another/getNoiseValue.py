from engine.special.exception import EngineError

import functools
import random
import math
import time


class PerlinNoise:
    tables = {}

    def __init__(self, seed=0):
        self.seed = seed

        if self.seed in self.tables:
            self.p = self.tables[self.seed]

        else:
            self.p = self.generate_permutation_table()

    def generate_permutation_table(self):
        random.seed(self.seed)

        p = list(range(256))
        random.shuffle(p)

        full_table = p + p
        self.tables[self.seed] = full_table

        return full_table

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a, b, t):
        ft = t * 3.1415
        f = (1 - math.cos(ft)) * 0.5
        return a * (1 - f) + b * f

        # return a + t * (b - a)

    def _grad(self, hash_val, x, y):
        h = hash_val & 3

        if h == 0:
            return x + y

        elif h == 1:
            return -x + y

        elif h == 2:
            return x - y

        else:
            return -x - y

    def noise(self, x, y, frequency=1.0, amplitude=1.0):
        x *= frequency
        y *= frequency

        X = int(x) & 255
        Y = int(y) & 255

        x -= int(x)
        y -= int(y)

        u = self._fade(x)
        v = self._fade(y)

        A = self.p[X] + Y
        AA = self.p[A & 255]
        AB = self.p[(A + 1) & 255]
        B = self.p[(X + 1) & 255] + Y
        BA = self.p[B & 255]
        BB = self.p[(B + 1) & 255]

        res = self._lerp(
            self._lerp(
                self._grad(AA, x, y),
                self._grad(BA, x - 1, y),
                u
            ),
            self._lerp(
                self._grad(AB, x, y - 1),
                self._grad(BB, x - 1, y - 1),
                u
            ),
            v
        )

        return res * amplitude

    def noise_with_range(self, x, y, frequency=1.0, min_val=0.0, max_val=1.0):
        noise_val = self.noise(x, y, frequency, 1.0)

        normalized = (noise_val + 1) / 2

        return min_val + normalized * (max_val - min_val)

    def octave_noise(self, x, y, octaves=4, frequency=1.0, amplitude=1.0, lacunarity=2.0, persistence=0.5, min_val=0.0, max_val=1.0):
        total = 0.0
        current_amplitude = amplitude
        current_frequency = frequency

        for i in range(octaves):
            noise_val = self.noise(x, y, current_frequency, 1.0)
            total += noise_val * current_amplitude
            current_amplitude *= persistence
            current_frequency *= lacunarity

        normalized = (total - min_val) / (max_val - min_val)

        return min_val + normalized * (max_val - min_val)

    def reset_noise_stats(self):
        self.noise_stats.clear()

    def get_noise_stats(self, octaves=4, frequency=1.0, amplitude=1.0, lacunarity=2.0, persistence=0.5):
        stats_key = (self.seed, octaves, frequency, amplitude, lacunarity, persistence)

        return self.noise_stats.get(stats_key, None)


def getNoiseValue(program, compiler, path: str, nodes: dict, id: int, variables: dict, **kwargs) -> dict:
    queue = []

    for name in nodes["objects"][str(id)]["outputs"]["path"]["value"].values():
        queue.append(name["id"])

    if nodes["objects"][str(id)]["inputs"]["seed"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["seed"]["value"]["value"] is not None:
        seed = int(nodes["objects"][str(id)]["inputs"]["seed"]["value"]["value"])

    else:
        seed = int(nodes["objects"][str(id)]["inputs"]["seed"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["x"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"] is not None:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["value"]["value"])

    else:
        x = float(nodes["objects"][str(id)]["inputs"]["x"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["y"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"] is not None:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["value"]["value"])

    else:
        y = float(nodes["objects"][str(id)]["inputs"]["y"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["min"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["min"]["value"]["value"] is not None:
        mn = float(nodes["objects"][str(id)]["inputs"]["min"]["value"]["value"])

    else:
        mn = float(nodes["objects"][str(id)]["inputs"]["min"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["max"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["max"]["value"]["value"] is not None:
        mx = float(nodes["objects"][str(id)]["inputs"]["max"]["value"]["value"])

    else:
        mx = float(nodes["objects"][str(id)]["inputs"]["max"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["octaves"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["octaves"]["value"]["value"] is not None:
        octaves = int(nodes["objects"][str(id)]["inputs"]["octaves"]["value"]["value"])

    else:
        octaves = int(nodes["objects"][str(id)]["inputs"]["octaves"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["frequency"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["frequency"]["value"]["value"] is not None:
        frequency = float(nodes["objects"][str(id)]["inputs"]["frequency"]["value"]["value"])

    else:
        frequency = float(nodes["objects"][str(id)]["inputs"]["frequency"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["amplitude"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["amplitude"]["value"]["value"] is not None:
        amplitude = float(nodes["objects"][str(id)]["inputs"]["amplitude"]["value"]["value"])

    else:
        amplitude = float(nodes["objects"][str(id)]["inputs"]["amplitude"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"]["value"] is not None:
        lacunarity = float(nodes["objects"][str(id)]["inputs"]["lacunarity"]["value"]["value"])

    else:
        lacunarity = float(nodes["objects"][str(id)]["inputs"]["lacunarity"]["standard"])

    if nodes["objects"][str(id)]["inputs"]["persistence"]["value"] is not None and nodes["objects"][str(id)]["inputs"]["persistence"]["value"]["value"] is not None:
        persistence = float(nodes["objects"][str(id)]["inputs"]["persistence"]["value"]["value"])

    else:
        persistence = float(nodes["objects"][str(id)]["inputs"]["persistence"]["standard"])

    if mn > mx:
        raise EngineError("maximum value must be bigger then minimum")

    if octaves <= 0:
        raise EngineError("octaves must be bigger than 0")

    if frequency <= 0:
        raise EngineError("frequency must be bigger than 0")

    if amplitude <= 0:
        raise EngineError("amplitude must be bigger than 0")

    if lacunarity <= 0:
        raise EngineError("lacunarity must be bigger than 0")

    noise = PerlinNoise(seed)

    answer = noise.octave_noise(x + random.uniform(-0.1, 0.1), y + random.uniform(-0.1, 0.1), octaves, frequency, amplitude, lacunarity, persistence, mn, mx)

    for ids, connector in nodes["objects"][str(id)]["outputs"]["value"]["value"].items():
        nodes["objects"][str(ids)]["inputs"][connector["name"]]["value"]["value"] = answer

    return queue
