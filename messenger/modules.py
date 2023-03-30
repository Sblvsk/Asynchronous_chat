import subprocess
from ipaddress import ip_address
from ipaddress import IPv4Address
from tabulate import tabulate


def host_ping(hosts):
    for host in hosts:
        ip = str(ip_address(host))
        result = subprocess.run(['ping', '-n', '1', '-w', '500', ip], capture_output=True)
        if result.returncode == 0:
            print(f"Узел {ip} доступен")
        else:
            print(f"Узел {ip} недоступен")


hosts = ['google.com', 'yandex.ru', '192.168.1.1']
host_ping(hosts)


def host_range_ping(start_ip, end_ip):
    start = IPv4Address(start_ip)
    end = IPv4Address(end_ip)
    while start <= end:
        result = subprocess.run(['ping', '-n', '1', '-w', '500', str(start)], capture_output=True)
        if result.returncode == 0:
            print(f"Узел {start} доступен")
        else:
            print(f"Узел {start} недоступен")
        start += 1


start_ip = '192.168.1.1'
end_ip = '192.168.1.10'
host_range_ping(start_ip, end_ip)


def host_range_ping_tab(start_ip, end_ip):
    results = {'Reachable': [], 'Unreachable': []}
    start = IPv4Address(start_ip)
    end = IPv4Address(end_ip)
    while start <= end:
        result = subprocess.run(['ping', '-n', '1', '-w', '500', str(start)], capture_output=True)
        if result.returncode == 0:
            results['Reachable'].append(str(start))
        else:
            results['Unreachable'].append(str(start))
        start += 1

    print(tabulate(results, headers='keys'))


start_ip = '192.168.1.1'
end_ip = '192.168.1.10'
host_range_ping_tab(start_ip, end_ip)

read_process = subprocess.Popen(['python', 'read_chat.py'])
write_process = subprocess.Popen(['python', 'write_chat.py'])

input('Press Enter to exit...')

read_process.kill()
write_process.kill()


def run_clients(count):
    clients = []
    for i in range(count):
        client = subprocess.Popen(['python', 'client.py'])
        clients.append(client)

    input('Press Enter to exit...')

    for client in clients:
        client.kill()


run_clients(3)
