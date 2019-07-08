from behave import given, when, then
import subprocess
import hashlib
import os
import shutil


ERROR_MSG = 'got "%s" but expected "%s"'


def run_command(command):
    proc = subprocess.run(command,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.decode('utf8')
    return output


def get_hash(filename):
    m = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()


@given('we have a "{grid}" file in CSV')
def we_have_a_grid_file_in_csv(context, grid):
    context.subprocess_cmd = ['python', 'csv2background.py', grid]


@given('we have a "{config}" file in JSON')
def we_have_a_config_file_in_json(context, config):
    context.subprocess_cmd.append(config)


@when('we run the composer')
def we_run_the_composer(context):
    output_filename = 'test.png'
    context.subprocess_cmd.extend(['--output', output_filename])
    subprocess.run(context.subprocess_cmd)
    context.got_hash = get_hash(output_filename)
    os.remove(output_filename)


@then('we get an output file in PNG like this "{image}"')
def we_get_an_output_file_in_png_like_this_image(context, image):
    hash = context.got_hash
    expected = get_hash(image)
    assert hash == expected, ERROR_MSG % (hash, expected)


@given('we have a scene "{grid}" file in CSV')
def we_have_a_scene_grid_file_in_csv(context, grid):
    context.subprocess_cmd = ['python', 'csv2scenes.py', grid]


@when('we run the generator')
def we_run_the_generator(context):
    output_dirname = 'test-output'
    context.subprocess_cmd.extend(['--output', output_dirname])
    os.makedirs(output_dirname, exist_ok=True)
    subprocess.run(context.subprocess_cmd)
    context.got_hashes = [get_hash(os.path.join(output_dirname, f))
                          for f in os.listdir(output_dirname)]
    shutil.rmtree(output_dirname)


@then('we get a series of PNG files like those in "{directory}"')
def we_get_a_series_of_png_files_like_those_in_directory(context, directory):
    hashes = context.got_hashes
    expected = [get_hash(os.path.join(directory, f))
                for f in os.listdir(directory)]
    assert hashes == expected, ERROR_MSG % (hashes, expected)
