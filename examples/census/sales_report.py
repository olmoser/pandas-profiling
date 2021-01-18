from typing import List

from tqdm.auto import tqdm

from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
)
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.report.presentation.core.root import Root
from pandas_profiling.report.structure.overview import get_dataset_items
from pandas_profiling.report.structure.report import render_variables_section


def get_report_structure(summary: dict) -> Renderable:
    disable_progress_bar = not config["progress_bar"].get(bool)
    with tqdm(
        total=1, desc="Generate report structure", disable=disable_progress_bar
    ) as pbar:
        warnings = summary["messages"]

        section_items: List[Renderable] = [
            Container(
                get_dataset_items(summary, warnings),
                sequence_type="tabs",
                name="Overview",
                anchor_id="overview",
            ),
            Container(
                render_variables_section(summary),
                sequence_type="accordion",
                name="Variables",
                anchor_id="variables",
            ),
        ]

        sections = Container(section_items, name="Root", sequence_type="sections")
        pbar.update()

    footer = HTML(
        content='Report generated with <a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling</a>.'
    )

    return Root("Root", sections, footer)
