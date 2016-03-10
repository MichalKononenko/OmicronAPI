"""
Contains the database schema to be implemented or queried, from
which models in :mod:`database.models` will be populated. This describes the
database to be built on server initialization. This is the most current version
of the database schema.
"""
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, \
    ForeignKey, DateTime
from datetime import datetime
__author__ = 'Michal Kononenko'

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(20), nullable=False),
    Column('email_address', String(64)),
    Column('password_hash', String(128), nullable=False),
    Column('is_superuser', Boolean, nullable=False, default=False),
    Column('date_created', DateTime, default=datetime.now())
    )

users_projects_asoc_tables = Table(
    'user_to_projects', metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.project_id'),
           primary_key=True),
    Column('date_joined', DateTime, nullable=False, default=datetime.utcnow())
)

tokens = Table(
    'tokens', metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('token_hash', String(128), primary_key=True),
    Column('date_created', DateTime, nullable=False,
           default=datetime.utcnow()),
    Column('expiration_date', DateTime, nullable=False,
           default=datetime.utcnow())
)

projects = Table(
    'projects', metadata,
    Column('project_id', Integer, primary_key=True),
    Column('name', String(128), nullable=False),
    Column('date_created', DateTime, nullable=False,
           default=datetime.utcnow()),
    Column('owner_id', Integer, ForeignKey('users.user_id'), nullable=True),
    Column('description', String(1000), nullable=True)
)

files = Table(
    'files', metadata,
    Column('file_id', Integer, primary_key=True),
    Column('filename', String(64), nullable=False),
    Column('project_id', Integer, ForeignKey('projects.project_id'),
           nullable=False),
    Column('file_extension', String(10), nullable=False)
)
