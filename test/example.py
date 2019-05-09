from comet.application import Application
#from comet.monitoring import Monitor

class ExampleApplication(Application):
    def __init__(self):
        super(ExampleApplication, self).__init__()
    def code(self):
        pass

def main():
    app = ExampleApplication()
    app.run()

if __name__ == '__main__':
    main()
