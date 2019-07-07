import pytest
import hashlib
import csv2background


def get_hash(filename):
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


def test_load_field_grid():
    field_grid = csv2background.FieldGrid()
    field_grid.load_field_grid('sample/field.csv')
    assert field_grid.width == 32
    assert field_grid.height == 32
    for row in field_grid.rows():
        assert len(row) == 32


def test_config_has_default_values():
    config = csv2background.Configurations()
    assert config['gridsize'] == csv2background.Configurations.GRIDSIZE
    assert config['basecolor'] == csv2background.Configurations.BASECOLOR


def test_load_config():
    config = csv2background.Configurations()
    config.load_config('sample/config.json')
    margins = config['margins']
    assert margins['top'] == 0
    assert margins['bottom'] == 0
    assert margins['left'] == 16
    assert margins['right'] == 0
    layout = config['layout']
    assert layout['1'] == ''
    assert layout['2'] == '#86c06c'
    assert layout['3'] == ''
    assert layout['4'] == ''
    assert layout['5'] == ''
    assert layout['6'] == ''
    assert layout['7'] == ''
    assert layout['8'] == ''
    assert layout['9'] == './sample/tiles/tree.png'


def test_generate_scene_image():
    csv2scene = csv2background.CSV2Scene('sample/config.json')
    test_scene = [['2'] * 16] * 16
    output_filename = 'test.png'
    csv2scene.generate(test_scene, output_filename)
    hash = get_hash(output_filename)
    expected = 'c2026d0e576de9cc612a38ef525a7c3f79c542fb5df699563719574795a65a4b'
    assert hash == expected, 'got "%s" but expect "%s"' % (hash, expected)
