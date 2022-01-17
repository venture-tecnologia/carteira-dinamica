from flask.json import jsonify
from conn_db import conexao_sql

# abre conexao com banco de dados
def conn_db():
    cursor = conexao_sql()
    return cursor

# Executa STMT , conforme indicação do parametro enviado pelo moneyNOW
def moneynow_requisicao(data):
    json_retorno = buscar_dados_do_titulos(data)
    return json_retorno

# Busca de dados do titulos
def buscar_dados_do_titulos(parametros_selecao):
    
    codCedente = parametros_selecao['codigoCedente']
    dataInicial = parametros_selecao['dataInicial']
    dataFinal = parametros_selecao['dataFinal']
    stsPago = parametros_selecao['statusdoTitulo']

    sql = "SELECT F.NUM_LANCAMENTO, F.VLR_PREVISTO " \
          " FROM FATITUL0 F " \
          " WHERE F.COD_FORN='" + str(codCedente) + \
        "' AND F.STS_PAGO='" + stsPago + "'"

    cursor = conn_db()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Convert query to file json
    djson = []
    for row in rows:
        djson.append({"lancamento": row[0], "valor": float(row[1])})

    cursor.close()

    return djson

