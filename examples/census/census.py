import json
from pathlib import Path

import numpy as np
import pandas as pd
import jinja2

from pandas_profiling import ProfileReport
from pandas_profiling.data_set import DataSet, DataSetReport
from pandas_profiling.utils.cache import cache_file


def report_html():
    file_name = cache_file(
        "census_train.csv",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    )

    # Names based on https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
    df = pd.read_csv(
        file_name,
        header=None,
        index_col=False,
        names=[
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
        ],
    )

    # Prepare missing values
    df = df.replace("\\?", np.nan, regex=True)
    profile = ProfileReport(df, title='DEMO', explorative=True)

    # show column definition
    definitions = json.load(open(f"census_column_definition.json"))
    profile.set_variable(
        "dataset",
        {
            "description": 'Predict whether income exceeds $50K/yr based on census data. Also known as "Census Income" dataset. Extraction was done by Barry Becker from the 1994 Census database. A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1)&& (HRSWK>0)). Prediction task is to determine whether a person makes over 50K a year.',
            "copyright_year": "1996",
            "author": "Ronny Kohavi and Barry Becker",
            "creator": "Barry Becker",
            "url": "https://archive.ics.uci.edu/ml/datasets/adult",
        },
    )
    profile.set_variable("variables.descriptions", definitions)

    # Only show the descriptions in the overview
    profile.set_variable("progress_bar", False)
    profile.set_variable("title", 'DEMO')
    profile.set_variable("show_variable_description", False)
    profile.set_variable("html.style.theme", "flatly")
    profile.set_variable("html.inline", True)
    profile.set_variable("html.minify_html", False)
    profile.set_variable("html.style.additional", "crayon.css")
    profile.to_file('demo.html')


def get_report(df, custom_report, report_title, custom_templates):
    # Initialize the report
    print(f'Report: {custom_report} Title: {report_title}')
    profile = ProfileReport(df, title=report_title, explorative=True, custom_report=custom_report)

    # show column definition
    definitions = json.load(open(f"census_column_definition.json"))
    profile.set_variable(
        "dataset",
        {
            "description": 'Predict whether income exceeds $50K/yr based on census data. Also known as "Census Income" dataset. Extraction was done by Barry Becker from the 1994 Census database. A set of reasonably clean records was extracted using the following conditions: ((AAGE>16) && (AGI>100) && (AFNLWGT>1)&& (HRSWK>0)). Prediction task is to determine whether a person makes over 50K a year.',
            "copyright_year": "1996",
            "author": "Ronny Kohavi and Barry Becker",
            "creator": "Barry Becker",
            "url": "https://archive.ics.uci.edu/ml/datasets/adult",
        },
    )
    profile.set_variable("variables.descriptions", definitions)

    # Only show the descriptions in the overview
    profile.set_variable("progress_bar", True)
    profile.set_variable("title", report_title)
    profile.set_variable("show_variable_description", False)
    profile.set_variable("html.style.theme", "flatly")
    profile.set_variable("html.inline", True)
    profile.set_variable("html.minify_html", False)
    profile.set_variable("html.style.additional", "crayon.css")
    if custom_templates is not None:
        profile.set_variable("custom_template_loader_path", "pandas_extension")

    output_file = Path(str(f'{report_title}.json'))
    output_file.write_text(profile.to_json(), 'utf-8')

    return profile


if __name__ == "__main__":

    # get input data
    file_name = cache_file(
        "census_train.csv",
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
    )

    # Names based on https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
    df1 = pd.read_csv(
        file_name,
        header=None,
        index_col=False,
        names=[
            "age",
            "workclass",
            "fnlwgt",
            "education",
            "education-num",
            "marital-status",
            "occupation",
            "relationship",
            "race",
            "sex",
            "capital-gain",
            "capital-loss",
            "hours-per-week",
            "native-country",
        ],
    )

    # Prepare missing values
    df1 = df1.replace("\\?", np.nan, regex=True)

    # create second demo dataframe
    df2 = df1[df1["age"] <= 35]

    # define the custom template path
    custom_template_path = ("pandas_extension", "templates")

    # generate reports for DF1
    reports_df1 = [get_report(df1, report, title, ctp) for (report, title, ctp) in [
        ("basic_report", "Basic", custom_template_path),
        ("sales_report", "Sales", custom_template_path),
        (None, "Full", custom_template_path),
    ]]

    # generate reports for DF2
    reports_df2 = [get_report(df2, report, title, ctp) for (report, title, ctp) in [
        ("basic_report", "Basic", custom_template_path),
        ("sales_report", "Sales", custom_template_path),
    ]]

    ds1 = DataSet('Census All Ages', reports_df1)
    ds2 = DataSet('Census Young Ages', reports_df2)

    ds_report = DataSetReport('demo', [ds1, ds2], lineage='A[All Ages DataSet] -->|age < 35| B[Young Timers Dataset]')
    ds_report.write_to_file()


