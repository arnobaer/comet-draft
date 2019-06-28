import unittest
import env

from comet.application import Application
from comet.job import Job

class MyApplication(Application):
    pass

class MyJob(Job):

    def __init__(self, app, name):
        super(MyJob, self).__init__(app, name)

    def configure(self):
        self.update_progress(3, 12)

    def run(self):
        self.update_progress(12, 12)

class JobTest(unittest.TestCase):

    # TODO

    def testJob(self):
        app = MyApplication('MyApp')
        name = 'MyTestJob'

        job = MyJob(app, name)
        self.assertIs(job.app, app)
        self.assertEqual(job.name, name)

        self.assertEqual(job.progress, 0.0) # 0%
        job.configure()
        self.assertEqual(job.progress, 25.0) # 25%
        job.run()
        self.assertEqual(job.progress, 100.0) # 100%

if __name__ == '__main__':
    unittest.main()
