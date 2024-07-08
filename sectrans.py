# -*- coding: utf-8 -*-

from dto import banco
import json
import os
from utils import sender

class Main():

    def __init__(self) -> None:
        self._source_path = os.path.dirname(os.path.realpath(__file__))

    def read_json(self):
        
        self._config_folder = os.path.join(self._source_path, 'config')

        config_file = 'config.json'
        arquivo = os.path.join(self._config_folder, config_file)

        with open(arquivo, 'r') as json_file:
            dados = json.load(json_file)

            return dados

    def main(self):
#       
        data = self.read_json()

        # Lê as informações do banco de dados
        data_base_info = data['data_base']
        host_pg = data_base_info['host_pg']
        dbname_pg = data_base_info['dbname_pg']
        user_pg = data_base_info['user_pg']
        password_pg = data_base_info['password_pg']
        port_pg = data_base_info['port_pg']

        # Lê as informações da máquina do pendrive
        pendrive_machine_info = data['pendrive_machine']
        pendriveMachineIp = pendrive_machine_info['machineIp']
        pendriveSshPort = pendrive_machine_info['sshPort']
        pendriveUsername= pendrive_machine_info['sshUsername']
        pendrivePassowrd= pendrive_machine_info['sshPassword']
        pendrivePathFiles = pendrive_machine_info['pathToSaveFiles']
        defaultFilePath = pendrive_machine_info['defaultFilePath']

        db = banco.Banco(host_pg, dbname_pg, user_pg, password_pg, port_pg)

        ### --------------------------------- ###
        #  TESTES                           #
        registred_companies = db.get_companies()
        for company in registred_companies:
            id, name = company
            print(id, name)

        selectet_company_id = input("\nSelecione Id da Empresa: ")

        registred_cars = db.get_all_cars(selectet_company_id)
        for carro in registred_cars:
            id, car = carro
            print(car)

        selected_car_name = input("\nInforme número do carro: ")
            
        car_id = db.get_car_id_by_name(selected_car_name)

        equipament_select = int(input(f"\nModelos: \n1 - RaspDvr\n2 - NX\nInforme Número: "))
        
        if equipament_select == 1:
            equipament_model = 'RaspDvr'

            dvr_id = 2
            cameras = 4

        elif equipament_select == 2:
            equipament_model = 'NX'
            dvr_id = 3
            cameras = 4

        else:
            print("Equipamento não reconhecido")
            exit()

        ## REFATORAR
        user_id = 279

        if db.set_pedido_pendente(user_id, selectet_company_id, car_id, equipament_model, dvr_id, cameras):
            print("Pedido inserido com sucesso.")

        else:
            print("Não foi possível adicionar requisição")

        pedidosPendentes = db.get_pedidos_pendentes()

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
                "carro_id": pedido[3],          # Índice 3 corresponde a 'a.carro_id'
                "troca_midia": pedido[24]       # Índice 24 corresponde a 'a.troca_midia'
            })

        for ListaCompleta in arrLista:
            config_file_name = f"{ListaCompleta['empresa']}%{ListaCompleta['carro']}%{ListaCompleta['rede']}%{ListaCompleta['tipo']}".replace('"', '')
            config_file_full_path = os.path.join(defaultFilePath, config_file_name)

            if ListaCompleta['mac'] == '':
                ListaCompleta['mac'] = "00:00:00:00:00:00"
            
            if ListaCompleta['tipo'] == "RaspDvr":
                with open(config_file_full_path, "w", encoding='utf-8') as file:
                    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    file.write('<sectrans>\n')
                    file.write('<!--   BÁSICAS -->\n')
                    file.write(f'<empresa>{ListaCompleta["empresa"]}</empresa>\n')
                    file.write(f'<carro>{ListaCompleta["carro"]}</carro>\n')
                    file.write('<ip_default>192.168.10.100</ip_default>\n')
                    file.write(f'<cameras>{ListaCompleta["cameras"]}</cameras>\n')
                    file.write(f'<troca_midia>{ListaCompleta["troca_midia"]}</troca_midia>\n')
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
                    file.write('<captura_framerate>5</captura_framerate>\n')
                    file.write('<captura_bitrate>100000</captura_bitrate>\n')
                    file.write('<captura_sensibilidade>3000</captura_sensibilidade>\n')
                    file.write('<captura_resolucao>448x256</captura_resolucao>\n')
                    file.write('<captura_rotate>180</captura_rotate>\n')
                    file.write('<captura_codec>mp4</captura_codec>\n')
                    file.write('<!--   WIRELESS -->\n')
                    file.write('<wireless_modo>cliente</wireless_modo>\n')
                    file.write('<!--   RTSP -->\n')

                    for qtdCams in range(1, ListaCompleta['cameras']+1):
                        url = "rtsp://192.168.10.101:554/user=admin&amp;password=&amp;channel=x&amp;stream=1.sdp"
                        novaUrl = url.replace("channel=x", f"channel={qtdCams}")
                        file.write(f'<rtsp_url_{qtdCams}>{novaUrl}</rtsp_url_{qtdCams}>\n')
                
                    file.write('<!--   BOOLEANS -->\n')
                    file.write('<encoda>false</encoda> <!--ENCODAR VIDEOS-->\n')
                    file.write('<reverse>false</reverse> <!--DESCARREGAMENTO REVERSO-->\n')
                    file.write('</sectrans>\n')
                
                print(f'Arquivo do carro {ListaCompleta["carro"]} criado.')
                
            else:
                with open(config_file_full_path, "w") as file:
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

                print(f'Arquivo do carro {ListaCompleta["carro"]} criado.')

            
            db.set_pedido_to_gravado(ListaCompleta['carro_id'])[0]
            print("Pedido Atualizado no banco")

            senderClass = sender.Sender(pendriveMachineIp, pendriveSshPort, pendriveUsername, pendrivePassowrd)
            senderClass.create_ssh_connection_and_send_file(config_file_full_path, pendrivePathFiles)
            print(f'Arquivo do carro {ListaCompleta["carro"]} enviado para máquina de pendrive')

if __name__ == '__main__':

    mr = Main()
    mr.main()
