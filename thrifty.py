#!/usr/bin/python27
from contextlib import contextmanager

from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

HIVE_HOST = 'blahblahblah'
HIVE_PORT = 10000

SAMPLE_QUERY = 'use jason_l99; show partitions final;'

class HiveWrapper(object):

    def __init__(self, host=HIVE_HOST, port=HIVE_PORT):

        try:
            self.__transport = TSocket.TSocket(host, port)
            self.__transport = TTransport.TBufferedTransport(self.__transport)
            self.__protocol = TBinaryProtocol.TBinaryProtocol(self.__transport)

            self.__client = ThriftHive.Client(self.__protocol)
            self.__transport.open()

        except Thrift.TException, tx:
            print tx.message

        print 'hive connection established'

    def execute(self, hql):

        print 'running query...'

        # need to pass query to thrift as an array of stmts (w/o semicolons)
        query_array = [k.lstrip() for k in hql.split(';')[: -1]]

        try:
            for stmt in query_array:
                if stmt:
                    print stmt
                    self.__client.execute(stmt)
                else:
                    break

        except Thrift.TException, tx:
            print tx.message

    def fetch_all(self):
        print 'getting all results...'
        return self.__client.fetchAll()

    def get_batched_results(self, batch_size=1000):
        results = list()

        while True:
            try:
                rows = self.__client.fetchN(batch_size)

                if len(rows) == 0:
                    break

                else:
                    results += rows

            except HiveServerException, hsx:
                print hsx.message
                break

        self.__transport.close()
        return results

    def get_results(self, max_rows=500):

        i, result = 0, list()
        while True:

            try:
                row = self.__client.fetchOne()
                if row == None:
                    break

                else:
                    result.append(row)
                    i += 1

                    if i % 1000 == 0:
                        print 'executing query {}'.format(i)

                # ignore max_rows
                if max_rows == -1:
                    continue

                # check max_rows
                elif i > max_rows:
                    print """WARNING: results set exceeded max number of rows; \
                        returning partial results set"""

                    break

            except HiveServerException, hsx:
                print hsx.message
                break

        self.__transport.close()
        return result

if __name__ == '__main__':

    hive_client = HiveWrapper(HIVE_HOST, HIVE_PORT)
    hive_client.execute(SAMPLE_QUERY)
    results = hive_client.get_results()

    print results
