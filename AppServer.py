from flask import Flask, url_for, render_template, send_file, request, json, Response, url_for

from ping import PingServer, Alerta

import sys

app = Flask(__name__)

listaURL = []

enviadosValor = 0
pingSucesso = 0
pingsPerdidos = 0
maiorPing = 0
aviso = 0
alerta = 0

@app.route('/')
def index():
    return render_template('index.html', primeiraURL='Sem URL', segundaURL='Sem URL', enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)

@app.route('/index.html')
def home():
    if len(listaURL)> 0:
        return render_template('index.html', primeiraURL=listaURL[0], segundaURL=listaURL[1], enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)
    else:
        return render_template('index.html', primeiraURL='Sem URL', segundaURL='Sem URL', enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)

@app.route('/verifyURL')
def geVerifytUrl():
    
    print(len(listaURL))
    if (len(listaURL) > 0):
        print(listaURL[0], listaURL[1])
        return render_template('index.html', primeiraURL=listaURL[0], segundaURL=listaURL[1], enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, URL1=listaURL[0], URL2=listaURL[1], aviso=aviso, alerta=alerta)
    else: 
        pass

@app.route('/resgister')
def getUrlRegister():
    if len(listaURL) > 0:
        listaURL.pop()
        listaURL.pop()
    user_url1 = request.args.get('url1')
    user_url2 = request.args.get('url2')
    listaURL.append(user_url1)
    listaURL.append(user_url2)

    return render_template('index.html', primeiraURL=listaURL[0], segundaURL=listaURL[1], enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)

@app.route('/aviso')
def getAviso():
    global aviso
    aviso = float(request.args.get('limite'))
    if len(listaURL) > 0:
        return render_template('index.html', primeiraURL=listaURL[0], segundaURL=listaURL[1], enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)
    else:
        return render_template('index.html', enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)
        

@app.route('/sendPing')
def postSendPing():
    global enviadosValor
    global pingSucesso
    global pingsPerdidos
    global maiorPing
    global listaURL
    global alerta

    alerta = 0
    teste = Alerta(listaURL[0], listaURL[1])
    try:
        dataPing = PingServer(listaURL[0], listaURL[1])
    except:
        if teste.verifica1() == 0:
            alerta = 1
        if teste.verifica2() == 0:
            if alerta == 1:
                alerta = 3
            else:
                alerta = 2
        return render_template("index.html", primeiraURL=listaURL[0], segundaURL=listaURL[1], enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)

    responseServer = dataPing.responseList()
    responseEstatisticas = dataPing.responseEstatisticas()
    responseResultados = dataPing.responseResultados()
    primeiroPing = responseEstatisticas[0]
    segundoPing = responseEstatisticas[1]
    enviadosValor += primeiroPing['enviados'] + segundoPing['enviados']
    pingSucesso += primeiroPing['recebidos'] + segundoPing['recebidos']
    pingsPerdidos += primeiroPing['perdidos'] + segundoPing['perdidos']

    if (maiorPing > primeiroPing['max'] and maiorPing > segundoPing['max']):
        pass
    elif (maiorPing < primeiroPing['max'] and maiorPing > segundoPing['max']):
        maiorPing = primeiroPing['max']

    elif (maiorPing > primeiroPing['max'] and maiorPing < segundoPing['max']):
        maiorPing = segundoPing['max']
    elif (segundoPing['max'] < primeiroPing['max'] and maiorPing < primeiroPing['max']):
        maiorPing = primeiroPing['max']
    elif (segundoPing['max'] > primeiroPing['max'] and maiorPing < segundoPing['max'] ):
        maiorPing = segundoPing['max']
    elif (segundoPing['max'] > primeiroPing['max']):
        maiorPing = segundoPing['max']
    elif (segundoPing['max'] < primeiroPing['max']):
        maiorPing = primeiroPing['max']
    else:
        maiorPing = primeiroPing['max']

    return render_template("index.html", primeiraURL=listaURL[0], segundaURL=listaURL[1], responseList=responseServer, estatisticaList=responseEstatisticas, resultadosList=responseResultados, enviados=enviadosValor, sucesso=pingSucesso, perdidos=pingsPerdidos, maiorPing=maiorPing, aviso=aviso, alerta=alerta)

if __name__ == '__main__':
    app.run()
