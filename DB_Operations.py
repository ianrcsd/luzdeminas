import pymysql
from typing import Tuple, Any, List

database="luzdeminasdb"
database="sql8615957"

# database connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="#Ir@010620",
    #database=database,
	cursorclass=pymysql.cursors.DictCursor
)


connection = pymysql.connect(
    host="sql8.freemysqlhosting.net",
    user="sql8615957",
    password="Vp5bIcR8He",
    database=database,
	cursorclass=pymysql.cursors.DictCursor
)

print(database)

def get_data_menu():
    with connection.cursor() as cursor:
        #cursor.execute("SELECT cat.nome_pt FROM `menu.categoria` as cat")
        #cat = [item['nome_pt'] for item in cursor.fetchall()]
        #print(cat)

        cursor.execute(f"""
            SELECT cat.nome_pt , car.nome_pt, car.descricao_pt, car.preco, car.url_img
            FROM {database}.`menu.cardapio` as car
            INNER JOIN `menu.categoria` as cat on (car.`menu.categoria.id` = cat.id)
        """)
        rows = cursor.fetchall()
        print(rows)
    
    return rows

def get_data_categoria():
    with connection.cursor() as cursor:
        cursor.execute("SELECT cat.id, cat.nome_pt FROM `menu.categoria` as cat")
        #rows = cursor.fetchall()
        cat = [item['nome_pt'] for item in cursor.fetchall()]
        print(type(cat))
    return cat

def get_login(username, password):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM usuario WHERE nome = %s AND senha = %s', (username, password))
        usuario = cursor.fetchone()
        print(usuario)
    
    return usuario

def get_registro(username):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario WHERE nome LIKE %s", [username])
        usuario = cursor.fetchone()
    
    return usuario

def post_registro(username, password):
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO usuario VALUES (NULL, %s, %s)', (username, password))
    
    connection.commit()

''' CRUD SITE '''
def get_tables():
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        tabelas = [x['Tables_in_sql8615957'] for x in tables]        
    
    return tabelas

def get_fields(table):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table}`")
        campos = cursor.fetchall()
    return campos

def get_columns(table):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table}`")
        colunas = [desc[0] for desc in cursor.description]
    return colunas

def get_menu_item(id):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT cat.nome_pt FROM `menu.categoria` as cat")
        #cat = [item['nome_pt'] for item in cursor.fetchall()]
        #print(cat)

        cursor.execute(f"""
            SELECT car.id , car.nome_pt, car.descricao_pt, car.nome_en, car.descricao_en,  car.preco, car.url_img, cat.nome_pt
            FROM luzdeminasdb.`menu.cardapio` as car
            INNER JOIN `menu.categoria` as cat on (car.`menu.categoria.id` = cat.id)
            WHERE car.id = {id}
        """)
        rows = cursor.fetchall()
        print(rows)
    
    return rows

def get_busca(tabela,id):
    with connection.cursor() as cursor:
        #cursor.execute("SELECT cat.nome_pt FROM `menu.categoria` as cat")
        #cat = [item['nome_pt'] for item in cursor.fetchall()]
        #print(cat)

        cursor.execute(f"""
            SELECT * FROM `{tabela}` WHERE id = {id}
        """)
        rows = cursor.fetchall()
        print(rows)
    
    return rows

def update_row(table_name, row_id, data):
    with connection.cursor() as cursor:
         
            # monta a consulta SQL para atualizar a linha na tabela
            sql = f"UPDATE `{table_name}` SET "
            for column, value in data.items():
                sql += f" `{column}` = '{value}', "
            sql = sql[:-2]  # remove a última vírgula e espaço
            sql += f" WHERE id = {row_id}"
            print(sql)
            # executa a consulta SQL
            cursor.execute(sql)
        # faz commit na transação
    connection.commit()
    

def get_row_data(table_name, row_id):
    with connection.cursor() as cursor:
        # executar a consulta SQL
        sql = f"SELECT * FROM `{table_name}` WHERE id = %s"
        cursor.execute(sql, (row_id,))
        result = cursor.fetchone()
        if result:
            row_data = result
        else:
            row_data = None

    return row_data

def get_table_data(table_name: str) -> Tuple[List[str], List[Tuple]]:
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table_name}`")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return columns, rows
    
def insert_row(table_name,data):
    with connection.cursor() as cursor:
        columns = "`, `".join(data.keys())
        values_template = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO `{table_name}` (`{columns}`) VALUES ({values_template})"
        print(query)
        cursor.execute(query, values)
        # faz commit na transação
    connection.commit()


def delete_row(table_name, row_id):
    with connection.cursor() as cursor:
        # executar a consulta SQL
        sql = f"DELETE FROM `{table_name}` WHERE id = %s"
        cursor.execute(sql, (row_id,))
    connection.commit()