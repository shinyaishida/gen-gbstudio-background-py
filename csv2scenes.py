#!/usr/bin/python3

import argparse
import csv
import os
from csv2background import CSV2Scene


class Scene:

    def __init__(self, tile_grid, row, column):
        self.grid = tile_grid
        self.filename = 'scene-%d-%d.png' % (row + 1, column + 1)


class SceneGrid:

    def __init__(self):
        self.scenes = []

    def load_grid(self, grid_file):
        grid = self._parse_grid(grid_file)
        row_count = len(grid) // 16
        col_count = len(grid[0]) // 16
        for row in range(0, row_count):
            roffset = row * 16
            r_range = grid[roffset:roffset+16]
            for col in range(0, col_count):
                coffset = col * 16
                tile_grid = [r[coffset:coffset+16] for r in r_range]
                self.scenes.append(Scene(tile_grid, row, col))

    def _parse_grid(self, grid_file):
        with open(grid_file, 'r') as gf:
            grid = [row for row in csv.reader(gf) if row]
            height = len(grid)
            assert height % 16 == 0
            if height:
                width = len(grid[0])
            assert width % 16 == 0
            for row in grid:
                if len(row) != width:
                    print('CSV format error')
                    grid = []
                    break
        return grid


if __name__ == '__main__':
    ARGPARSE = argparse.ArgumentParser(description='Generate GB scene images.')
    ARGPARSE.add_argument('grid', metavar='GRID',
                          help='Path to scene grid file')
    ARGPARSE.add_argument('config', metavar='CONFIG',
                          help='Path to configuration file')
    ARGPARSE.add_argument('-o', '--output', help='Output directory')
    ARGS = ARGPARSE.parse_args()
    scene_grid = SceneGrid()
    scene_grid.load_grid(ARGS.grid)
    csv2scene = CSV2Scene(ARGS.config)
    for scene in scene_grid.scenes:
        csv2scene.generate(scene.grid,
                           os.path.join(ARGS.output, scene.filename))
