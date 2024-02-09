# -*- coding: utf-8 -*-

import psycopg2

class Banco:

    def __init__(self, hostPg, dbName, userPg, passwordPg, portPg):

        self.conn = self.conect_db(hostPg, dbName, userPg, passwordPg, portPg)

    def conect_db(self, hostPg, dbName, userPg, passwordPg, portPg):
        # Criar uma conexão PostgreSQL
        conn = psycopg2.connect(host=hostPg, dbname=dbName, user=userPg, 
                                           password=passwordPg, port=portPg)
        return conn

    def do_query(self, sql_query):
        # Criar um cursor para file.writeutar a consulta SQL
        with self.conn.cursor() as cursor:

            # file.writeutar a consulta SQL
            cursor.execute(sql_query)

            # Recuperar os resultados
            return cursor.fetchall()

    def get_pedidos_pendentes(self):

        sql_query = """
            SELECT d.username, a.tipo, a.estado, a.carro_id, b.empresa, b.id, c.carro, e.rede, e.chave, c.ip, e.ip_roteador, c.mac, c.numero_conexao, c.tipo_conexao, 
            c.username_conexao, c.senha_conexao, c.fps, c.tamanho_video, c.particao, b.ip_servidor, b.rede_servidor, e.criptografia, f.url, a.cameras 
            FROM pedidos a, empresas b, carros c, users d, redes e, dvrs f 
            WHERE b.id = a.empresa_id AND c.id = a.carro_id AND a.user_id = d.id AND c.rede_id = e.id AND a.estado = 'pendente'
        """

        return self.do_query(sql_query)
    
    def get_companies(self):

        sql_query = """
            SELECT id, nome FROM empresas
            ORDER BY nome ASC;;
        """

        return self.do_query(sql_query)
    
    def get_all_cars(self, company_id):

        sql_query = f"""
            SELECT id, carro 
            FROM carros
            WHERE empresa_id = {company_id} AND fora=FALSE
            ORDER BY carro ASC;;
        """
        
        return self.do_query(sql_query)
    
    def get_car_by_name(self, car_name):

        sql_query = f"""
            SELECT *
            FROM carros
            WHERE carro = '{car_name}';
        """
        return self.do_query(sql_query)
    
