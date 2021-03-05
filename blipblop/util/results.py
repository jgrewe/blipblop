import datetime as dt

class MeasurementResults():

    def __init__(self, task_name, metadata={}):
        self._task_name = task_name
        self._task_timestamp = dt.datetime.now()
        self._reaction_times = []
        self._metadata = metadata

    def append(self, reaction_time):
        self._reaction_times.append(reaction_time)

    @property
    def results(self, reaction_times):
        self._reaction_times = reaction_times
    
    @property
    def name(self):
        return self._task_name

    @property
    def starttime(self):
        return self._task_timestamp
    
    @property
    def starttime(self, starttime):
        self._task_timestamp = starttime

    @property
    def results(self):
        return self._reaction_times
