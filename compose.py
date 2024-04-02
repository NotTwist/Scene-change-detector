import argparse
import json


_expected_graded = [
    'scene_change_detector',
]


def _read_notebook(path):
    with open(path, 'r') as f:
        return json.load(f)


def _extract_graded(notebook):
    graded_cells = filter(
        lambda x: x['cell_type'] == 'code' and x['source'] and
                  x['source'][0].startswith('# GRADED CELL:'),
        notebook['cells'])

    graded_source = {
        x['source'][0].split()[-1]: ''.join(x['source'][1:])
        for x in graded_cells
    }

    return graded_source


def _read_context(path):
    with open(path, 'r') as f:
        return f.read()


def _write_test(test, path):
    with open(path, 'w') as f:
        f.write(test)


def compose_test(notebook_path, output_path):
    context = _read_context("context.py")
    runner = _read_context("test.py")
    notebook = _read_notebook(notebook_path)
    graded_source = _extract_graded(notebook)

    for name in _expected_graded:
        if name not in graded_source:
            raise RuntimeError(f"Not enough graded functions, {name} is missing")

    _write_test(context + '\n\n'.join([graded_source[name] for name in graded_source]) + '\n\n' + runner, output_path)


def main():
    parser = argparse.ArgumentParser(description='Extract graded cells from notebook and compose output file')
    parser.add_argument('--notebook', type=str, default="scd.ipynb")
    parser.add_argument('--output', type=str, default="scd.py")

    args = parser.parse_args()

    compose_test(args.notebook, args.output)


if __name__ == "__main__":
    main()
