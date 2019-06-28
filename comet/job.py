import time
from .component import ControlComponent

class Job(ControlComponent):
    """Job base class, inherit to create custom jobs.

    Jobs can be executed in custom applications at any state.
    """

    def __init__(self, app, name, label=None):
        super(Job, self).__init__(app, name, label)
        self.__progress = 0.0
        self.setup()

    @property
    def progress(self):
        """Returns job progress in percent."""
        return self.__progress

    @progress.setter
    def progress(self, percent):
        """Set job progress in percent."""
        self.__progress = max(0.0, min(100.0, float(percent)))

    def update_progress(self, part, full):
        """Update progress helper, provided for convienience.

        >>> self.update_progress(3, 12) # 3 out of 12 done
        >>> self.progress
        25.0
        """
        self.progress = 100. * part / full

    def setup(self):
        pass

    def configure(self):
        pass

    def run(self):
        pass
