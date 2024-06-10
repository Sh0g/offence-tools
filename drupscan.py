import requests
import re
import subprocess
import sys
import os
from bs4 import BeautifulSoup

def detect_drupal_core_vulns(url):
    # Check Drupal version
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    version_meta = soup.find('meta', {'name': 'Generator', 'content': re.compile(r'Drupal (\d+\.\d+)')})
    if version_meta:
        version = version_meta['content'].split(' ')[1]
        print(f"Drupal version: {version}")

        # Check for known Drupal core vulnerabilities
        vulns = {
            "CVE-2018-7600": "Drupal < 7.58, 8.x < 8.3.9, 8.4.x < 8.4.6, 8.5.x < 8.5.1",
            "CVE-2018-7602": "Drupal < 7.59, 8.x < 8.3.9, 8.4.x < 8.4.6, 8.5.x < 8.5.3",
            "CVE-2019-6340": "Drupal < 8.5.11, 8.6.x < 8.6.10, 8.7.x"
        }
        for cve, affected_versions in vulns.items():
            if version in affected_versions:
                print(f"Detected vulnerability: {cve}")
    else:
        print("Unable to detect Drupal version")

def detect_drupal_plugin_vulns(url):
    # Enumerate installed Drupal plugins
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all the Drupal modules/plugins
    modules = soup.find_all('a', href=re.compile(r'/project/'))

    # Check each module for known vulnerabilities
    for module in modules:
        module_name = module.text.strip()
        module_url = f"https://www.drupal.org/project/{module_name}"

        # Check the Drupal.org project page for the module
        try:
            project_response = requests.get(module_url)
            project_soup = BeautifulSoup(project_response.text, 'html.parser')

            # Check for known vulnerabilities
            vuln_section = project_soup.find('section', {'id': 'security-advisories'})
            if vuln_section:
                vulns = vuln_section.find_all('div', class_='security-advisory')
                for vuln in vulns:
                    vuln_title = vuln.find('h3').text.strip()
                    vuln_description = vuln.find('div', class_='content').text.strip()
                    print(f"Detected vulnerability in {module_name}: {vuln_title} - {vuln_description}")
        except requests.exceptions.RequestException:
            print(f"Error checking module: {module_name}")

def detect_drupal_config_issues(url):
    # Check for default admin credentials
    admin_credentials = [
        ('admin', 'admin'),
        ('admin', 'password'),
        ('root', 'root'),
        ('drupal', 'drupal')
    ]
    for username, password in admin_credentials:
        response = requests.post(f"{url}/user/login", data={'name': username, 'pass': password})
        if response.status_code == 200 and 'user/logout' in response.text:
            print(f"Detected default admin credentials: {username}/{password}")

    # Check for directory permissions issues
    directories_to_check = [
        '/sites/default/files',
        '/sites/default/settings.php',
        '/sites/default/services.yml'
    ]
    for directory in directories_to_check:
        try:
            response = requests.get(f"{url}{directory}")
            if response.status_code == 200:
                print(f"Detected potentially insecure directory permissions: {directory}")
        except requests.exceptions.RequestException:
            pass

    # Check for other configuration issues
    # (e.g., outdated Drupal version, missing security updates, etc.)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    version_meta = soup.find('meta', {'name': 'Generator', 'content': re.compile(r'Drupal (\d+\.\d+)')})
    if version_meta:
        version = version_meta['content'].split(' ')[1]
        print(f"Drupal version: {version}")

        # Check for known vulnerabilities in the detected Drupal version
        vulns = {
            "CVE-2018-7600": "Drupal < 7.58, 8.x < 8.3.9, 8.4.x < 8.4.6, 8.5.x < 8.5.1",
            "CVE-2018-7602": "Drupal < 7.59, 8.x < 8.3.9, 8.4.x < 8.4.6, 8.5.x < 8.5.3",
            "CVE-2019-6340": "Drupal < 8.5.11, 8.6.x < 8.6.10, 8.7.x"
        }
        for cve, affected_versions in vulns.items():
            if version in affected_versions:
                print(f"Detected vulnerability: {cve}")
    else:
        print("Unable to detect Drupal version")

def main():
    url = input("Enter a domain or URL: ")
    url = f"https://{url}"

    detect_drupal_core_vulns(url)
    detect_drupal_plugin_vulns(url)
    detect_drupal_config_issues(url)

if __name__ == "__main__":
    main()