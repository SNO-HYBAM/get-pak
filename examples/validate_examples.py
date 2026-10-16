"""Run all Python cells in a bundled notebook without a Jupyter server.

From the repository root, in the GET-Pak + Matplotlib environment:
    python examples/validate_examples.py examples/Notebook_single_image_tutorial.ipynb
    python examples/validate_examples.py examples/l2b_workflow.ipynb
"""
import argparse
import json
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook', type=Path)
    args = parser.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    scope = {'__name__': '__main__'}
    start = time.perf_counter()
    try:
        notebook = json.loads(args.notebook.read_text())
        for index, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                print(f'Executing {args.notebook.name} cell {index}', flush=True)
                exec(compile(''.join(cell['source']), f'{args.notebook}:cell-{index}', 'exec'), scope)
        print(f'PASS {args.notebook} {time.perf_counter() - start:.2f}s', flush=True)
    finally:
        for name in ('grs', 'source'):
            dataset = scope.get(name)
            if hasattr(dataset, 'close'):
                dataset.close()


if __name__ == '__main__':
    main()
