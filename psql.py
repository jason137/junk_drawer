#!/usr/bin/env python
import os

import pandas as pd
from sqlalchemy import (create_engine, text)

_DB_1 = {'dbname': <db_1>,
    'host': <host_1>,
    'port': <port_1>,
    'user': <user_1>,

_DB_2 = {'dbname': <db_2>,
    'host': <host_2>,
    'port': <port_2>,
    'user': <user_2>,

_DB_3 = {'dbname': <db_3>,
    'host': <host_3>,
    'port': <port_3>,
    'user': <user_3>}

_HOST_AUTHS = {'db_1': _DB_1,
    'db_2': _DB_2,
    'db_3': _DB_3}

_CONN_TEMPLATE = 'redshift+psycopg2://{user}@{host}:{port}/{dbname}'

def run_query(host=None, default_host=None, query=None, query_file=None, data=None, chunksize=None):
    """api

    INPUTS
        host:           string
        default_host:   string
        query:          string (sql)
        query_file:     string (path/to/sql/file)
        data:           dictionary of params
        chunksize:      returns an iterator of dataframes (each with <= chunksize rows)

    OUTPUT
        results:        pd.DataFrame"""

    if host is None:
        host = default_host
    else:
        assert host in _HOST_AUTHS.keys()

    if query is None:
        assert query_file is not None

        with open(query_file, 'r') as f:
            query = f.read()

    else:
        assert query_file is None

    return _get_psql_response(host, query, data, chunksize)

def _get_psql_response(host, query, data=None, chunksize=None):
    """communicate w/ database"""

    auth = _HOST_AUTHS[host]
    if 'user' not in auth.keys():
        auth['user'] = os.getenv('PGUSER', default='snaplogic')

    conn_str = _CONN_TEMPLATE.format(**auth)
    engine = create_engine(conn_str)

    with engine.begin() as eng:
        return pd.read_sql_query(text(query), eng, params=data, chunksize=chunksize)
