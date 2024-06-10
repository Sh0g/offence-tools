import urllib.parse
import whois
import socket
from subprocess import call
import dns.resolver

def find_associated_domains(domain):
    associated_domains = []

    # Extract domain name from URL
    parsed_domain = urllib.parse.urlparse(domain).netloc

    # Find associated domains using WHOIS
    try:
        whois_info = whois.whois(parsed_domain)
        if whois_info.emails:
            for email in whois_info.emails:
                domain_from_email = email.split('@')[1]
                if domain_from_email not in associated_domains and domain_from_email != parsed_domain:
                    associated_domains.append(domain_from_email)
    except Exception as e:
        print(f"Error: {e}")

    # Find associated domains using DNS
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(parsed_domain, 'NS')
        for answer in answers:
            nameserver = str(answer)
            nameserver_domain = nameserver.split('.')[-2] + '.' + nameserver.split('.')[-1]
            if nameserver_domain not in associated_domains and nameserver_domain != parsed_domain:
                associated_domains.append(nameserver_domain)
    except dns.resolver.NXDOMAIN:
        print(f"Error: Domain {parsed_domain} does not exist.")
    except Exception as e:
        print(f"Error: {e}")

    return associated_domains

def main():
    domain = input("Enter a domain or URL: ")
    associated_domains = find_associated_domains(domain)

    if associated_domains:
        print(f"Associated domains for {domain}:")
        for associated_domain in associated_domains:
            print(f"- {associated_domain}")
    else:
        print(f"No associated domains found for {domain}.")
    call(["python", "run.py"])

if __name__ == '__main__':
    main()