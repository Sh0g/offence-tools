import os

from subprocess import call

def open_py_file(app):
    call(["python", app])

def menu():
    print("Welcome to the Menu!")
    print("Please select an option:")
    print ("1 - Google Dorking")
    print("2 - Associated Domains Finder")
    print ("3 - Subdomain Finder")
    print("4 - Port Scanner")
    print("5 - DNS Scanner")
    print ("6 - Wappalyzer")
    print("7 - Web Application Firewall Detector")
    print("8 - WordPress Scan")
    print("9 - Joomla Scan")
    print("10 - Drupal Scan")
    print("11 - SQLi Scanner")
    print("12 - Sub404")
    print("13 - XSS Tool")
    print("14 - Cloud Scanner")
    print("15 - AutoPWN-Suite")
    print("16 - OWASP ZAP (Warning! Required to install OWASP ZAP client and change in the owasp_wap.py api_key!)")
    print("Other number. Exit")

    choice = input("Enter your choice (1-13): ")

    if choice == "1":
        open_py_file("dorking.py")
    elif choice == "2":
        open_py_file("associated_domains.py")
    elif choice == "3":
        open_py_file("subdomains.py")
    elif choice == "4":
        open_py_file("scan_port.py")
    elif choice == "6":
        open_py_file("wappalyzer.py")
    elif choice == "7":
        open_py_file("waf.py")
    elif choice == "8":
        open_py_file("wpscan.py")
    elif choice == "9":
        open_py_file("joomscan.py")
    elif choice == "10":
        open_py_file("dscan/droopescan.py")
    elif choice == "11":
        open_py_file("sqli-exploiter/sqli-exploiter.py")
    elif choice == "12":
        open_py_file("sub404.py")
    elif choice == "13":
        open_py_file("xss-tool/xss-scanner.py.py")
    elif choice == "14":
        open_py_file("cloudscan.py")
    elif choice == "15":
        open_py_file("autopwn.py")
    elif choice == "16":
        open_py_file("owasp_zap.py")
    else:
        print("Exiting...")
        return

if __name__ == "__main__":
    menu()