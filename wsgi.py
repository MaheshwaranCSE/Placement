import os
from backend.app import create_app

env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == "__main__":
    app.run()
