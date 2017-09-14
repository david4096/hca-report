"""
hcareport: generates reports from Human Cell Atlas studies.

Usage:

```

hca-report StudyID

```

Will run download the study in question and run the reporting notebooks. The
resulting files are stored with the study.

"""

import tempfile
import shutil
import argparse
import os

import nbformat

from nbconvert.preprocessors import ExecutePreprocessor


def run_report(bucket_id, path):
    """
    Runs the report notebook located in ../notebooks and puts it in a local
    path.
    :param study_id:
    :param path:
    :return:
    """
    # Call to system or Jupyter API to run notebooks
    cwd = os.path.dirname(os.path.realpath(__file__))
    notebook_path = os.path.join(cwd, 'notebooks', 'python.ipynb')
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=1800)
    ep.preprocess(nb, {'metadata': {'path': path}})
    with open(os.path.join(path, 'python.ipynb'), mode='wt') as f:
        nbformat.write(nb, f)
    # Place results in temporary file location
    with open(os.path.join(path, 'python.ipynb'), mode='r') as f:
        print(f.readlines())
    # Upload to s3

    return

def main(args=None):
    """
    The console script that coordinates creating the demo environment.

    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(
        description='Generate a report for a study in the Human Cell Atlas.')
    parser.add_argument("study_id", type=str,
                        help="The identifier of the study to generate a"
                             "report for.")

    parsed = parser.parse_args(args)
    print(parsed)

    temp_path = tempfile.mkdtemp()

    run_report(parsed.study_id, temp_path)
    shutil.rmtree(temp_path)
