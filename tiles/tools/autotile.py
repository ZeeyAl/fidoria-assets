#!/usr/bin/env python3
"""
autotile.py - implementasi referensi dual-grid autotile (top-down) untuk tile terrain Fidoria.

  python3 autotile.py --demo OUT.png [--size 64]     # peta contoh
  python3 autotile.py MAP.txt OUT.png [--size 64]    # render dari file ASCII
  python3 autotile.py MAP.txt --validate             # daftar vertex yang kena fallback

MAP.txt: satu baris = satu baris grid, satu huruf = satu cell
  g grass | d dirt | s sand | w water | c cobblestone | r rocky   (baris berawalan # diabaikan)
Sebagai modul:
  at = Autotiler('autotile_rules.json', size=64)
  at.vertex_tiles(grid)  # grid[y][x] = nama terrain -> [(vx, vy, path_png), ...]
"""
import json, os, sys, random, argparse
from PIL import Image

class Autotiler:
    def __init__(self, rules_path, size=None):
        self.root = os.path.dirname(os.path.abspath(rules_path))
        self.r = json.load(open(rules_path))
        self.size = size or self.r['default_size']
        self.prio = {t: i for i, t in enumerate(self.r['priority'])}
        self.pairs = {frozenset((p['a'], p['b'])): p for p in self.r['pairs']}
        self._img = {}

    def path(self, tpl): return tpl.replace('{size}', str(self.size))

    def img(self, tpl):
        if tpl not in self._img:
            self._img[tpl] = Image.open(os.path.join(self.root, self.path(tpl))).convert('RGB')
        return self._img[tpl]

    @staticmethod
    def quadrants(grid, vx, vy):
        h, w = len(grid), len(grid[0])
        c = lambda x, y: grid[min(max(y, 0), h - 1)][min(max(x, 0), w - 1)]
        return [c(vx - 1, vy - 1), c(vx, vy - 1), c(vx, vy), c(vx - 1, vy)]  # NW NE SE SW

    def resolve(self, q):
        """-> (('base', terrain) | ('tile', pair, mask), kena_fallback)"""
        q = list(q); orig = list(q)
        while True:
            S = set(q)
            if len(S) == 1:
                return ('base', q[0]), q != orig
            if len(S) == 2:
                p = self.pairs.get(frozenset(S))
                if p:
                    mask = ''.join('a' if t == p['a'] else 'b' for t in q)
                    if mask in p['tiles']:
                        return ('tile', p, mask), q != orig
                    low = min(S, key=lambda t: self.prio[t])
                    q[q.index(low)] = next(t for t in S if t != low)   # patahkan diagonal
                else:
                    t = max(S, key=lambda t: (q.count(t), self.prio[t]))
                    q = [t] * 4                                         # tepi keras
            else:
                drop = min(S, key=lambda t: (q.count(t), self.prio[t]))
                rest = S - {drop}
                repl = max(rest, key=lambda t: (q.count(t), self.prio[t]))
                q = [repl if t == drop else t for t in q]

    def vertex_tiles(self, grid, seed=0):
        rng = random.Random(seed); out = []
        for vy in range(len(grid) + 1):
            for vx in range(len(grid[0]) + 1):
                res, _ = self.resolve(self.quadrants(grid, vx, vy))
                if res[0] == 'base':
                    t = self.r['terrains'][res[1]]
                    tpl = rng.choice(t.get('variants', [t['base']]))
                else:
                    tpl = res[1]['tiles'][res[2]]
                out.append((vx, vy, tpl))
        return out

    def validate(self, grid):
        return [(vx, vy, q) for vy in range(len(grid) + 1) for vx in range(len(grid[0]) + 1)
                for q in [self.quadrants(grid, vx, vy)] if self.resolve(q)[1]]

    def render(self, grid, seed=0):
        S = self.size; h, w = len(grid), len(grid[0])
        canvas = Image.new('RGB', (w * S, h * S))
        for vx, vy, tpl in self.vertex_tiles(grid, seed):
            canvas.paste(self.img(tpl), (vx * S - S // 2, vy * S - S // 2))   # tepi luar terpotong rapi
        return canvas

def parse_map(path, legend):
    rows = [l.rstrip('\n') for l in open(path) if l.strip() and not l.startswith('#')]
    return [[legend[ch] for ch in r] for r in rows]

def demo_grid(n=18):
    g = [['grass'] * n for _ in range(n)]
    def blob(cx, cy, rx, ry, t):
        for y in range(n):
            for x in range(n):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1: g[y][x] = t
    blob(11.5, 10.5, 5.6, 4.6, 'sand'); blob(11.5, 10.5, 3.6, 2.8, 'water')   # danau + pantai pasir
    blob(3.5, 4, 3.6, 3.2, 'dirt')                                            # petak tanah
    for y in range(3, 6):                                                     # bercak pasir 3x3 di dalam tanah
        for x in range(2, 5): g[y][x] = 'sand'
    return g

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('map', nargs='?'); ap.add_argument('out', nargs='?')
    ap.add_argument('--demo', metavar='OUT'); ap.add_argument('--validate', action='store_true')
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--size', type=int, default=None)
    ap.add_argument('--rules', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'autotile_rules.json'))
    a = ap.parse_args(); at = Autotiler(a.rules, a.size)
    if a.demo:
        at.render(demo_grid(), a.seed).save(a.demo); print('ok', a.demo); sys.exit()
    grid = parse_map(a.map, at.r['ascii_legend'])
    if a.validate:
        bad = at.validate(grid); print(f'{len(bad)} vertex kena fallback')
        for vx, vy, q in bad: print(f'  vertex ({vx},{vy}) kuadran NW,NE,SE,SW = {q}')
        sys.exit()
    at.render(grid, a.seed).save(a.out); print('ok', a.out)
