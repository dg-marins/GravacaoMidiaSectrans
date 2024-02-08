<?php
$sectrans = 'sectrans';
$conectasectrans = pg_connect("host=10.80.0.1 dbname=$sectrans user=sectrans password='sectrans' port=5433")
or die("Erro ao conectar no banco de dados $sectrans");

$arrLista = array();
$svrPendrive = '10.80.0.126';
$svrAdmPendrive = '10.80.3.22';
$dirPendrive = '/home/geracao';
$dirThor = '/home/pendrive';

$Lista = pg_query($conectasectrans, "SELECT d.username,a.tipo,a.estado,a.carro_id,b.empresa,b.id,c.carro,e.rede,e.chave,c.ip,e.ip_roteador,c.mac,c.numero_conexao,c.tipo_conexao,c.username_conexao,c.senha_conexao,c.fps,c.tamanho_video,c.particao,b.ip_servidor,b.rede_servidor,e.criptografia,f.url,a.cameras FROM pedidos a,empresas b,carros c,users d,redes e, dvrs f WHERE b.id = a.empresa_id AND c.id = a.carro_id AND a.user_id = d.id AND c.rede_id = e.id  AND a.estado = 'pendente'");

exec("rm /home/pendrive/* &");

while($tmp = pg_fetch_array($Lista)):
    $arrLista[] = array("empresa" => $tmp['empresa'],
                  "carro" => $tmp['carro'],
                  "tipo" => $tmp['tipo'],
                  "rede" => $tmp['rede'],
                  "chave" => $tmp['chave'],
                  "ip" => $tmp['ip'],
                  "ip_roteador" => $tmp['ip_roteador'],
                  "mac" => $tmp['mac'],
                  "numero_conexao" => $tmp['numero_conexao'],
                  "tipo_conexao" => $tmp['tipo_conexao'],
                  "username_conexao" => $tmp['username_conexao'],
                  "senha_conexao" => $tmp['senha_conexao'],
                  "fps" => $tmp['fps'],
                  "tamanho_video" => $tmp['tamanho_video'],
                  "particao" => $tmp['particao'],
                  "ip_servidor" => $tmp['ip_servidor'],
                  "rede_servidor" => $tmp['rede_servidor'],
                  "empresa_id" => $tmp['id'],
                  "cameras" => $tmp['cameras'],
                  "url" => $tmp['url'],
                  "criptografia" => $tmp['criptografia'], // comentar
                  "carro_id" => $tmp['carro_id']
                );
endwhile;

foreach($arrLista as $ListaCompleta):
    $log = $ListaCompleta['empresa']."%".$ListaCompleta['carro']."%".$ListaCompleta['rede']."%".$ListaCompleta['tipo'];
    if($ListaCompleta['mac'] == '') $ListaCompleta['mac'] = "00:00:00:00:00:00";
    switch($ListaCompleta['tipo']):
        case "RaspDvr":
            exec("echo '<?xml version=\"1.0\" encoding=\"UTF-8\"?>' > $dirThor/$log");
            exec("echo '<sectrans>' >> $dirThor/$log");
            exec("echo '<!--   BÁSICAS -->' >> $dirThor/$log");
            exec("echo '<empresa>'".$ListaCompleta['empresa']."'</empresa>' >> $dirThor/$log");
            exec("echo '<carro>'".$ListaCompleta['carro']."'</carro>' >> $dirThor/$log");
            exec("echo '<ip_default>192.168.10.100</ip_default>' >> $dirThor/$log");
            exec("echo '<cameras>'".$ListaCompleta['cameras']."'</cameras>' >> $dirThor/$log");
            exec("echo '<!--   REDE -->' >> $dirThor/$log");
            exec("echo '<transferencia_usuario>'".$ListaCompleta['rede']."'</transferencia_usuario>' >> $dirThor/$log");
            exec("echo '<transferencia_senha>'".$ListaCompleta['chave']."'</transferencia_senha>' >> $dirThor/$log");
            exec("echo '<ip_servidor>'".$ListaCompleta['ip_servidor']."'</ip_servidor>' >> $dirThor/$log");
            exec("echo '<rede_servidor>'".$ListaCompleta['rede_servidor']."'</rede_servidor>' >> $dirThor/$log");
            exec("echo '<ip_equipamento>'".$ListaCompleta['ip']."'</ip_equipamento>' >> $dirThor/$log");
            exec("echo '<gw_equipamento>'".$ListaCompleta['ip_roteador']."'</gw_equipamento>' >> $dirThor/$log");
            exec("echo '<mascara_equipamento>255.255.255.0</mascara_equipamento>' >> $dirThor/$log");
            exec("echo '<criptografia>'".$ListaCompleta['criptografia']."'</criptografia>' >> $dirThor/$log");
            exec("echo '<!--   CAPTURA -->' >> $dirThor/$log");
            exec("echo '<captura_tempo>'".$ListaCompleta['tamanho_video']."'</captura_tempo>' >> $dirThor/$log");
            exec("echo '<captura_framerate>15</captura_framerate>' >> $dirThor/$log");
            exec("echo '<captura_bitrate>100000</captura_bitrate>' >> $dirThor/$log");
            exec("echo '<captura_sensibilidade>3000</captura_sensibilidade>' >> $dirThor/$log");
            exec("echo '<captura_resolucao>448x256</captura_resolucao>' >> $dirThor/$log");
            exec("echo '<captura_rotate>180</captura_rotate>' >> $dirThor/$log");
            exec("echo '<captura_codec>mp4</captura_codec>' >> $dirThor/$log");
            exec("echo '<!--   WIRELESS -->' >> $dirThor/$log");
            exec("echo '<wireless_modo>cliente</wireless_modo>' >> $dirThor/$log");
            exec("echo '<!--   RTSP -->' >> $dirThor/$log");

            for($qtdCams=1;$qtdCams<=$ListaCompleta['cameras'];$qtdCams++):
                $url = "rtsp://192.168.10.101:554/?user=admin&amp;password=&amp;channel=x&amp;stream=1.sdp?real_stream";
                $novaUrl = str_replace("channel=x","channel=$qtdCams",$url);
                exec("echo '<rtsp_url_$qtdCams>$novaUrl</rtsp_url_$qtdCams>' >> $dirThor/$log");
            endfor;

            exec("echo '<!--   BOOLEANS -->' >> $dirThor/$log");
            exec("echo '<encoda>true</encoda> <!--ENCODAR VIDEOS-->' >> $dirThor/$log");
            exec("echo '<reverse>false</reverse> <!--DESCARREGAMENTO REVERSO-->' >> $dirThor/$log");
            exec("echo '</sectrans>' >> $dirThor/$log");
            exec("scp $dirThor/$log $svrPendrive:/".$dirPendrive);
            break;
        default:
            echo "$dirThor/$log";
            exec("echo '".$ListaCompleta['empresa']."' > $dirThor/$log");
            exec("echo 'sim' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['carro']."' >> $dirThor/$log");
            exec("echo 'sim' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['rede']."' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['mac']."' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['chave']."' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['ip_servidor'].",".$ListaCompleta['rede_servidor'].",' >> $dirThor/$log");
            exec("echo '/home/publico/imagens' >> $dirThor/$log");
            exec("echo '2,10,320,240,' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['particao']."' >> $dirThor/$log");
            exec("echo '60,0,400000,' >> $dirThor/$log");
            exec("echo '".$ListaCompleta['ip'].",".$ListaCompleta['ip_roteador'].",255.255.255.0,' >> $dirThor/$log");
            exec("echo '1,1,' >> $dirThor/$log");
            exec("echo '100,100,' >> $dirThor/$log");
            exec("echo '3000,4000,' >> $dirThor/$log");
            exec("echo 'nao,nao,vivo,*99#,vivo,vivo,' >> $dirThor/$log");
            exec("echo '11,12,' >> $dirThor/$log");
            exec("echo '8,8,' >> $dirThor/$log");
            exec("echo 'modulo' >> $dirThor/$log");
            exec("echo 'off,off,' >> $dirThor/$log");
            exec("echo '128,128,' >> $dirThor/$log");
            exec("echo '50,nao,nao,' >> $dirThor/$log");
            exec("echo 'sectrans.no-ip.org:8080,' >> $dirThor/$log");
            exec("echo 'mp4,' >> $dirThor/$log");
            if($ListaCompleta['tipo'] == 'RaspDvr' && $ListaCompleta['criptografia'] == 'taWpa') exec("echo 'taWpa' >> $dirThor/$log");
//          exec("echo '".$ListaCompleta['criptografia']."' >> $dirThor/$log"); // comentar
            exec("scp $dirThor/$log $svrPendrive:/".$dirPedfndrive);
//          exec("scp $dirThor/$log $svrAdmPendrive:/".$dirPendrive);
            break;
    endswitch;
    pg_query($conectasectrans, "UPDATE pedidos SET estado = 'gravado' WHERE estado = 'pendente' AND empresa_id = '".$ListaCompleta['empresa_id']."' AND carro_id = '".$ListaCompleta['carro_id']."'");
endforeach;

pg_close($conectasectrans);

?>