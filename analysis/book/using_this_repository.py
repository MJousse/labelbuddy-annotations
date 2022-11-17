# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Using this repository

# The documents, labels and annotations are stored in JSON or JSONLines files in the `projects/` directory.

# ## Building the database
#
# We can easily create a SQLite database containing all the information these files contain:
# ```bash
# make database
# ```
# or
# ```bash
# python3 ./scripts/make_database.py
# ```
# We can then use this database to query the contents of the repository, either with the `sqlite3` interactive command:
# ```bash
# sqlite3 analysis/data/database.sqlite3
# ```
# or using `sqlite3` bidings that are available in many languages, including Python's standard library module `sqlite3`.
#
# A small Python package containing a few utilities for working with this repository is also provided in `analysis/labelrepo`. You can install it with
# ```bash
# pip install -e analysis/labelrepo
# ```


# The main tables are `annotation`, `document` and `label`.
# `detailed_annotation` is a view gathering detailed information about each annotation, such as the `selected_text`, a snippet of surrounding text (`context`), the `label_name` and `annotator_name`, etc.
# For example, to display a few annotations:

# +
from labelrepo import database, displays

connection = database.get_database_connection()

annotations = connection.execute("SELECT * FROM detailed_annotation limit 10")
displays.AnnotationsDisplay(annotations)
# -

# As another example, selecting all snippets of text that have been annotated with "Diagnosis":

# +
import pandas as pd

snippets = pd.read_sql(
    """
    SELECT selected_text, COUNT(*) as occurrences
    FROM detailed_annotation
    WHERE label_name = "Diagnosis"
    GROUP BY selected_text
    ORDER BY occurrences DESC
    """,
    connection,
)

snippets
# -


# ## Using a CSV rather than a database

# If you prefer working with CSVs and Pandas than SQL, you can also run (at the root of the repository)
# ```bash
# make csv
# ```
# That will create a file `analysis/data/detailed_annotation.csv` containing that same table:

# +
import pandas as pd

from labelrepo import repo

csv_file = repo.data_dir() / "detailed_annotation.csv"
annotations = pd.read_csv(csv_file, nrows=3)
print(annotations.columns.values)

displays.AnnotationsDisplay(annotations)
# -

# ## Using the JSON and JSONLines files directly

# `.jsonl` (JSONLines) files contain one JSON dictionary per line.
# They can be parsed like this:

# +
import json

annotations_file = (
    repo.repo_root()
    / "projects"
    / "participant_demographics"
    / "annotations"
    / "Jerome_Dockes.jsonl"
)
with open(annotations_file, encoding="UTF-8") as stream:
    for i, row_json in enumerate(stream):
        row = json.loads(row_json)
        print(row)
        # We don't want to print dozens of lines here
        if i == 3:
            break
# -

# Loading labels from a JSON file:

# +
labels_file = (
    repo.repo_root()
    / "projects"
    / "autism_mri"
    / "labels"
    / "Article_Terms.json"
)
json.loads(labels_file.read_text("UTF-8"))
# -
