from io import StringIO
import csv
import os

class DataWriter:

    def __init__(self):
        pass

class FileWriter(DataWriter):

    def __init__(self, filename):
        super(FileWriter, self).__init__()
        self.filename = filename

    def create(self):
        with open(self.filename, 'w') as f:
            pass

    def append(self, d):
        with open(self.filename, 'a') as f:
            f.write(format(d))
            f.write(os.linesep)

class CSVFileWriter(FileWriter):

    def __init__(self, filename, fieldnames):
        super(CSVFileWriter, self).__init__(filename)
        self.fieldnames = fieldnames

    def create(self):
        with open(self.filename, 'w') as f:
            writer = csv.DictWriter(context, fieldnames=self.fieldnames)
            writer.writeheader()

    def append(self, d):
        with open(self.filename, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(d)

class HephyDBFileWriter(FileWriter):

    def __init__(self, filename):
        super(HephyDBFileWriter, self).__init__(filename)

    def create(self, tags=[]):
        # write tags
        self.append_header('tags')
        with open(self.filename, 'w') as f:
            f.write(",".join([format(tag) for tag in tags]))
            f.write(os.linesep)

    def append_header(self, name):
        with open(self.filename, 'a') as f:
            f.write(os.linesep)
            f.write("[{}]".format(name))
            f.write(os.linesep)

    def create_table(self, name, fieldnames):
        self.append("{}[{}]".format(os.linesep, name))
        return CSVFileWriter(self.filename, fieldnames)
