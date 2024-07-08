import paramiko
from scp import SCPClient


class Sender:

    def __init__(self, hostname, port, username, password) -> None:
        pass
    
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def create_ssh_connection_and_send_file(self, local_file_path, remote_file_path):
        # Cria um cliente SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        # Usa SCP para transferir o arquivo
        scp = SCPClient(ssh.get_transport())
        scp.put(local_file_path, remote_file_path)

        # Fecha a conexão SCP e SSH
        scp.close()
        ssh.close()