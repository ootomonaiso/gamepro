from sshtunnel import SSHTunnelForwarder
import mariadb

def test_ssh_tunnel():
    with SSHTunnelForwarder(
        ('xs333002.xsrv.jp', 10022),
        ssh_username='xs333002',
        ssh_pkey=r'C:\00daizi\20721\2048\xs333002 (1).key',
        remote_bind_address=('localhost', 3306),
        local_bind_address=('localhost', 10022)
    ) as server:
        server.start()
        print("SSHトンネルが正常に開始されました")

        try:
            connection = mariadb.connect(
                host='localhost',
                port=10022,
                user='xs333002_root',
                password='Stemask1234',
                database='xs333002_stem'
            )
            print("MariaDBへの接続に成功しました")
        finally:
            server.stop()
            print("SSHトンネルが停止しました")

if __name__ == '__main__':
    test_ssh_tunnel()
