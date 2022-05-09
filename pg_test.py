import psycopg2
from pprint import pprint
from lib.varuables import private_yml


class PostGres:

    def __init__(self, **kwargs):
        self._connection = psycopg2.connect(
            host=kwargs['server'],
            database=kwargs['database'],
            user=kwargs['login'],
            password=kwargs['password'],
            port=kwargs['port']
        )
        self._cursor = self._connection.cursor()
        self._schema = kwargs['schema']
        self._table = kwargs['table']
        self.sql_path = f'{self._schema}{self._table}'

    def sql_query(self, query):
        self._cursor.execute(query)
        answer = self._cursor.fetchall()
        if answer is None:
            return False
        return answer

    def sql_update(self, query):
        self._cursor.execute(query)
        self._connection.commit()

    def sql_close(self):
        self._connection.close()


    def add_device(self, **kwargs):
        # spines_ip = f"{kwargs['spine1_ip']} {kwargs['spine2_ip']}"
        update = f""" 
        INSERT INTO {self.sql_path} (mac, hostname, location, port, number, network, finish_ztp, spines_ip, 
                                                 ip, loopback, vendor, pod)
        VALUES ('1a2s', 'test_name', 'test_dc', 'test_port', 13, 
                'test_network', 'test_status', 'test_spines', 'test_ip', 
                'test_loop', 'test_vendor', 3)"""
        # VALUES ('{kwargs['mac']}', '{kwargs['hostname']}', '{kwargs['dc']}', '{kwargs['port']}', '{kwargs['leaf_id']}',
        #         '{kwargs['db_production_network']}', '{kwargs['ztp_status']}', '{spines_ip}', '{kwargs['ip']}',
        #         '{kwargs['loopback']}', '{kwargs['vendor']}', '{kwargs['pod']}')"""
        # In new DC will'not kvm switches I think need to write sql update there is netbox,ise,zabbix = true for kvm
        print(update)
        self.sql_update(update)


if __name__ == '__main__':
    pg = PostGres(**private_yml['mysql'])
    scheme = private_yml['mysql']['schema']
    query = f'SELECT * from {pg.sql_path}'
    # query = 'select version()'
    pprint(pg.sql_query(query), width=120)
    pg.sql_close()
