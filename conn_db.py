import pyodbc


# conexao banco de dados
def conexao_sql():
    cx = pyodbc.connect('Driver={SQL Server};'
                        'Server=192.168.3.46;'
                        'Database=vmoney;'
                        'UID=sa;'
                        'PWD=vs@vmsql;')
    return cx.cursor()