import uuid


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
