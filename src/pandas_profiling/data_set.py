import uuid
from pathlib import Path

import jinja2


class DataSet:

    def __init__(self, name, reports):
        self._id = uuid.uuid4()
        self._reports = reports
        self._name = name

    def add_report(self, report):
        self._reports.append(report)

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def reports(self):
        return self._reports

    def __str__(self):
        return f'{self._name} - {self._id}'


class DataSetReport:

    def __init__(self, name, data_sets, lineage=None):
        self._id = uuid.uuid4()
        self._data_sets = data_sets
        self._name = name
        self._lineage = lineage

    def render(self):
        package_loader = jinja2.ChoiceLoader([
            jinja2.PackageLoader("pandas_extension", "templates"),
            jinja2.PackageLoader("pandas_profiling", "report/presentation/flavours/html/templates"),
        ])

        jinja2_env = jinja2.Environment(
            lstrip_blocks=True, trim_blocks=True, loader=package_loader,
        )

        return jinja2_env.get_template('dataset.html').render(datasets=self._data_sets, lineage=self._lineage)

    def write_to_file(self, file_name=None):
        output = self.render()
        output_file = file_name if file_name else self._name
        output_file = Path(str(f'{output_file}.html'))
        output_file.write_text(output, "utf-8")
