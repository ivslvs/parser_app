from . import app

# запускаю локально:
# "from . import app
# ImportError: attempted relative import with no known parent package"

# в докере ок

if __name__ == '__main__':
    app.run()
