# -*- coding: utf-8 -*-

import subprocess
from dto import banco

# Parâmetros de conexão PostgreSQL
host_pg = "localhost"
dbname_pg = "sectrans"
user_pg = "postgres"
password_pg = "a5ztq3ej"
port_pg = 5432

# Parâmetros do sistema
svrPendrive = '10.80.0.126'
svrAdmPendrive = '10.80.3.22'
dirPendrive = '/home/geracao'
dirThor = 'C:/Users/Douglas/Desktop/pendrive'

db = banco.Banco(host_pg, dbname_pg, user_pg, password_pg, port_pg)

pedidosPendentes = db.get_pedidos_pendentes()

# #Apaga arquivos de configuracao pre existente
# subprocess.run("rm /home/pendrive/* &", shell=True)

arrLista = []

for pedido in pedidosPendentes:
    arrLista.append({
        "empresa": pedido[4],  # Índice 4 corresponde a 'b.empresa'
        "carro": pedido[6],    # Índice 6 corresponde a 'c.carro'
        "tipo": pedido[1],     # Índice 1 corresponde a 'a.tipo'
        "rede": pedido[7],     # Índice 7 corresponde a 'e.rede'
        "chave": pedido[8],    # Índice 8 corresponde a 'e.chave'
        "ip": pedido[9],       # Índice 9 corresponde a 'c.ip'
        "ip_roteador": pedido[10],  # Índice 10 corresponde a 'e.ip_roteador'
        "mac": pedido[11],     # Índice 11 corresponde a 'c.mac'
        "numero_conexao": pedido[12],  # Índice 12 corresponde a 'c.numero_conexao'
        "tipo_conexao": pedido[13],    # Índice 13 corresponde a 'c.tipo_conexao'
        "username_conexao": pedido[14],  # Índice 14 corresponde a 'c.username_conexao'
        "senha_conexao": pedido[15],    # Índice 15 corresponde a 'c.senha_conexao'
        "fps": pedido[16],     # Índice 16 corresponde a 'c.fps'
        "tamanho_video": pedido[17],    # Índice 17 corresponde a 'c.tamanho_video'
        "particao": pedido[18],         # Índice 18 corresponde a 'c.particao'
        "ip_servidor": pedido[19],      # Índice 19 corresponde a 'b.ip_servidor'
        "rede_servidor": pedido[20],    # Índice 20 corresponde a 'b.rede_servidor'
        "empresa_id": pedido[5],        # Índice 5 corresponde a 'b.id'
        "cameras": pedido[23],          # Índice 23 corresponde a 'a.cameras'
        "url": pedido[22],              # Índice 22 corresponde a 'f.url'
        "criptografia": pedido[21],     # Índice 21 corresponde a 'e.criptografia'
        "carro_id": pedido[3]           # Índice 3 corresponde a 'a.carro_id'
    })

for ListaCompleta in arrLista:
    log = f"{ListaCompleta['empresa']}%{ListaCompleta['carro']}%{ListaCompleta['rede']}%{ListaCompleta['tipo']}".replace('"', '')
    if ListaCompleta['mac'] == '':
        ListaCompleta['mac'] = "00:00:00:00:00:00"
    
    if ListaCompleta['tipo'] == "RaspDvr":
        with open(f"{dirThor}/{log}", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<sectrans>\n')
            file.write('<!--   BÁSICAS -->\n')
            file.write(f'<empresa>{ListaCompleta["empresa"]}</empresa>\n')
            file.write(f'<carro>{ListaCompleta["carro"]}</carro>\n')
            file.write('<ip_default>192.168.10.100</ip_default>\n')
            file.write(f'<cameras>{ListaCompleta["cameras"]}</cameras>\n')
            file.write('<!--   REDE -->\n')
            file.write(f'<transferencia_usuario>{ListaCompleta["rede"]}</transferencia_usuario>\n')
            file.write(f'<transferencia_senha>{ListaCompleta["chave"]}</transferencia_senha>\n')
            file.write(f'<ip_servidor>{ListaCompleta["ip_servidor"]}</ip_servidor>\n')
            file.write(f'<rede_servidor>{ListaCompleta["rede_servidor"]}</rede_servidor>\n')
            file.write(f'<ip_equipamento>{ListaCompleta["ip"]}</ip_equipamento>\n')
            file.write(f'<gw_equipamento>{ListaCompleta["ip_roteador"]}</gw_equipamento>\n')
            file.write('<mascara_equipamento>255.255.255.0</mascara_equipamento>\n')
            file.write(f'<criptografia>{ListaCompleta["criptografia"]}</criptografia>\n')
            file.write('<!--   CAPTURA -->\n')
            file.write(f'<captura_tempo>{ListaCompleta["tamanho_video"]}</captura_tempo>\n')
            file.write('<captura_framerate>15</captura_framerate>\n')
            file.write('<captura_bitrate>100000</captura_bitrate>\n')
            file.write('<captura_sensibilidade>3000</captura_sensibilidade>\n')
            file.write('<captura_resolucao>448x256</captura_resolucao>\n')
            file.write('<captura_rotate>180</captura_rotate>\n')
            file.write('<captura_codec>mp4</captura_codec>\n')
            file.write('<!--   WIRELESS -->\n')
            file.write('<wireless_modo>cliente</wireless_modo>\n')
            file.write('<!--   RTSP -->\n')

            for qtdCams in range(1, ListaCompleta['cameras']+1):
                url = "rtsp://192.168.10.101:554/?user=admin&password=&channel=x&stream=1.sdp?real_stream"
                novaUrl = url.replace("channel=x", f"channel={qtdCams}")
                file.write(f'<rtsp_url_{qtdCams}>{novaUrl}</rtsp_url_{qtdCams}>\n')
        
                file.write('<!--   BOOLEANS -->\n')
                file.write('<encoda>true</encoda> <!--ENCODAR VIDEOS-->\n')
                file.write('<reverse>false</reverse> <!--DESCARREGAMENTO REVERSO-->\n')
                file.write('</sectrans>\n')
        
        # # file.write(f"scp {dirThor}/{log}.xml {svrPendrive}:/{dirPendrive}\n")
        # subprocess.run(["scp", "-P", "2222", f"{dirThor}/{log}", f"root@{svrPendrive}:/{dirPendrive}"])

        print("Arquivo enviado")

    else:
        log_path = f"{dirThor}/{log}"
        with open(log_path, "w") as file:
            file.write(f"{log_path}\n")
            file.write(f"{ListaCompleta['empresa']}\n")
            file.write("sim\n")
            file.write(f"{ListaCompleta['carro']}\n")
            file.write("sim\n")
            file.write(f"{ListaCompleta['rede']}\n")
            file.write(f"{ListaCompleta['mac']}\n")
            file.write(f"{ListaCompleta['chave']}\n")
            file.write(f"{ListaCompleta['ip_servidor']},{ListaCompleta['rede_servidor']},\n")
            file.write("/home/publico/imagens\n")
            file.write("2,10,320,240,\n")
            file.write(f"{ListaCompleta['particao']}\n")
            file.write("60,0,400000,\n")
            file.write(f"{ListaCompleta['ip']},{ListaCompleta['ip_roteador']},255.255.255.0,\n")
            file.write("1,1,\n")
            file.write("100,100,\n")
            file.write("3000,4000,\n")
            file.write("nao,nao,vivo,*99#,vivo,vivo,\n")
            file.write("11,12,\n")
            file.write("8,8,\n")
            file.write("modulo\n")
            file.write("off,off,\n")
            file.write("128,128,\n")
            file.write("50,nao,nao,\n")
            file.write("sectrans.no-ip.org:8080,\n")
            file.write("mp4,\n")
            if ListaCompleta['tipo'] == 'RaspDvr' and ListaCompleta['criptografia'] == 'taWpa':
                file.write("taWpa\n")

            # subprocess.run(f"scp {dirThor}/{log} {svrAdmPendrive}:{dirPendrive}", shell=True)

    # pg_query(conectasectrans, f"UPDATE pedidos SET estado = 'gravado' WHERE estado = 'pendente' AND empresa_id = '{ListaCompleta['empresa_id']}' AND carro_id = '{ListaCompleta['carro_id']}'")

# Fechar a conexão com o PostgreSQL
# conectasectrans.close()
