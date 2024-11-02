from netmiko import ConnectHandler

# 1. Создать два словаря для роутера и коммутатора
router = {
    "device_type": "cisco_ios",
    "ip": "192.168.94.20",
    "username": "admin",
    "password": "cisco",
}

switch = {
    "device_type": "cisco_ios",
    "ip": "192.168.94.30",
    "username": "admin",
    "password": "cisco",
}

# Функция для подключения и выполнения команд
def connect_and_run(device, commands):
    connection = ConnectHandler(**device)
    connection.enable()
    output = connection.send_config_set(commands)
    connection.disconnect()
    return output

# 2. Подключение к устройству по SSH и переход в enable
def connect_to_device(device):
    connection = ConnectHandler(**device)
    connection.enable()
    return connection

# Подключаемся к роутеру и коммутатору
router_conn = connect_to_device(router)
switch_conn = connect_to_device(switch)

# 3. Перейти в режим enable (уже сделано при подключении)

# 4. Получить текущую конфигурацию оборудования
router_config = router_conn.send_command("show running-config")
switch_config = switch_conn.send_command("show running-config")
print("Router Config:\n", router_config)
print("Switch Config:\n", switch_config)

# 5. Получить информацию об интерфейсах оборудования
router_interfaces = router_conn.send_command("show ip interface brief")
switch_interfaces = switch_conn.send_command("show ip interface brief")
print("Router Interfaces:\n", router_interfaces)
print("Switch Interfaces:\n", switch_interfaces)

# 6. Удалить vlan4 на коммутаторе и заново его создать
delete_vlan_commands = [
    "no vlan 4"
]

switch_vlan_output = connect_and_run(switch, delete_vlan_commands)
print("VLAN Deleting Output:\n", switch_vlan_output)

switch_vlans_info = switch_conn.send_command("show vlan")
print("VLANs information: ", switch_vlans_info)

vlan_commands = [
    "vlan 4",
    "name test_4",
    "interface vlan 4",
    "ip address 192.168.144.2 255.255.255.0",
    "no shutdown",
    "interface range Gi1/0 - 1",
    "switchport mode access",
    "switchport access vlan 4"
]
switch_vlan_output = connect_and_run(switch, vlan_commands)
print("VLAN Configuration Output:\n", switch_vlan_output)

switch_vlans_info = switch_conn.send_command("show vlan")
print("VLANs information: ", switch_vlans_info)

# 7. Посмотреть используемые IP и MAC-адреса в сети
router_arp = router_conn.send_command("show arp")
switch_mac_address_table = switch_conn.send_command("show mac address-table")
print("Router ARP Table:\n", router_arp)
print("Switch MAC Address Table:\n", switch_mac_address_table)

# Закрываем соединения
router_conn.disconnect()
switch_conn.disconnect()
