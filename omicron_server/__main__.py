#! /usr/bin/env python
"""
Usage:
    __main__.py -h | --help
    __main__.py HOST PORT [--debug]

Arguments:
    HOST  Host IP Address that server will run on (Use DEFAULT for default)
    PORT  Port Number that server will run on (Use DEFAULT for default)

Options:
    -h --help  Show this
    --debug  Activate debug mode
"""
import logging
from omicron_server.api_server import app
from omicron_server.config import default_config as conf
from omicron_server.database.models.users import Administrator
from omicron_server.database.sessions import ContextManagedSession
from omicron_server.database.schema import metadata
from docopt import docopt

__author__ = 'Michal Kononenko'

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

db_session = ContextManagedSession(bind=conf.DATABASE_ENGINE)


def set_logfile(config_object=conf):
    """
    If the ```LOGFILE``` environment variable is defined in the server,
    this method configures the log to output to a logfile

    :param Config config_object: The application config parameters. Defaults
        to the master config object, but is left open as an argument for
        testability.
    """
    if config_object.LOGFILE is not None:
        logging.basicConfig(filename=config_object.LOGFILE)

set_logfile()


@db_session()
def create_root_user(session):
    """
    If no root user is found in the DB, it makes a root user with
    the credentials given in the config

    :param ContextManagedSession session: The session to be used for making
        the root user
    """
    user = session.query(Administrator).filter_by(
            username=conf.ROOT_USER).first()
    if not user:
        user = Administrator(
                conf.ROOT_USER, conf.ROOT_PASSWORD, conf.ROOT_EMAIL
        )
        session.add(user)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    metadata.create_all(bind=conf.DATABASE_ENGINE)
    create_root_user()

    if arguments['HOST'] == 'DEFAULT':
        host = conf.IP_ADDRESS
    else:
        host = arguments['HOST']

    if arguments['PORT'] == 'DEFAULT':
        port = conf.PORT
    else:
        port = arguments['PORT']

    if arguments['--debug']:
        debug = True
    else:
        debug = False

    app.run(host=host, port=port, debug=debug)
