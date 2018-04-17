from flask import Flask, request
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
# Set CORS allow-origin from env ORIGINS, or set default to all.
CORS(app, resources={r"/*": {"origins": os.getenv('ORIGINS', '*')}})


class RequestFormatter(logging.Formatter):

    def __init__(self, request_attr, **kwds):
        self.request_attr = request_attr
        super(RequestFormatter, self).__init__(**kwds)

    def format(self, record):
        # Extract all desired request fields into the record.
        for a in self.request_attr:
            setattr(record, 'request_{0}'.format(a), getattr(request, a))

        # Receive component and status from path
        path_params = request.path.split('/')
        if len(path_params) == 3:
            setattr(record, 'component', path_params[1])
            setattr(record, 'status', path_params[2])

        return super(RequestFormatter, self).format(record)


# Remove all default handlers.
for h in app.logger.handlers:
    app.logger.removeHandler(h)

# Set werkzeug logger to only log ERRORS
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# add custom StreamHandler
ch = logging.StreamHandler()
ch.setFormatter(RequestFormatter(
    # Check if any env LOG_FORMAT was set, otherwise create default format.
    fmt=os.getenv(
        'LOG_FORMAT',
        'timestamp=%(asctime)s, remote_addr=%(request_remote_addr)s, user_agent=%(request_user_agent)s, component=%(component)s, status=%(status)s, data=%(message)s'),
    # Check for env REQUEST_ATTR to use for map requests attributes.
    request_attr=os.getenv(
        'REQUEST_ATTR',
        'remote_addr, user_agent').replace(' ', '').split(',')
))
app.logger.addHandler(ch)
app.logger.setLevel(logging.INFO)


@app.route('/<component>/<status>', methods=['GET', 'POST'])
def hello_world(component, status):
    app.logger.info(
        request.data.decode("utf-8"))
    return '', 204
