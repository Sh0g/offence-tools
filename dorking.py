import webbrowser
import argparse
import os
from subprocess import call
import re

def dorking(domain):
    # GOOGLE DORKING
    if os.path.exists(f'./dorking.html'):
        os.remove(f'./dorking.html')
    f = open(f'./dorking.html', 'a')
    f.write(
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"> <title>Dorks for {domain}</title> </head> <body><br>')
    f.write('<h2>Choose one of links:</h2>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Adoc+%7C+ext%3Adocx+%7C+ext%3Aodt+%7C+ext%3Artf+%7C+ext%3Asxw+%7C+ext%3Apsw+%7C+ext%3Appt+%7C+ext%3Apptx+%7C+ext%3Appc+%7C+ext%3Acsw"
    f.write(f'<a target="_blank" href="{url}">Publicly explosed documents</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+intitle%3Aindex+of"
    f.write(f'<a target="_blank" href="{url}">Directory listing vulnerabilities</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Axml+%7C+ext%3Aconf+%7C+ext%3Acnf+%7C+ext%3Areg+%7C+ext%3Ainf+%7C+ext%3Ardp+%7C+ext%3Acfg+%7C+ext%3Atxt+%7C+ext%3Aora+%7C+ext%3Aini+%7C+ext%3Aenv"
    f.write(f'<a target="_blank" href="{url}">Configuration files exposed</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Asql+%7C+ext%3Adbf+%7C+ext%3Amdb"
    f.write(f'<a target="_blank" href="{url}">Database files exposed</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Alog"
    f.write(f'<a target="_blank" href="{url}">Log files exposed</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Abkf+%7C+ext%3Abkp+%7C+ext%3Abak+%7C+ext%3Aold+%7C+ext%3Abackup"
    f.write(f'<a target="_blank" href="{url}">Backup and old files</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+inurl%3Alogin+%7C+inurl%3Asignin+%7C+intitle%3ALogin+%7C+intitle%3A%22sign in%22+%7C+inurl%3Aauth"
    f.write(f'<a target="_blank" href="{url}">Login pages</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+intext%3A%22sql syntax near%22+%7C+intext%3A%22syntax error has occurred%22+%7C+intext%3A%22incorrect syntax near%22+%7C+intext%3A%22unexpected end of SQL command%22+%7C+intext%3A%22Warning: mysql_connect()%22+%7C+intext%3A%22Warning: mysql_query()%22+%7C+intext%3A%22Warning: pg_connect()%22"
    f.write(f'<a target="_blank" href="{url}">SQL errors</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+%22PHP Parse error%22+%7C+%22PHP Warning%22+%7C+%22PHP Error%22"
    f.write(f'<a target="_blank" href="{url}">PHP Errors / warning</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+ext%3Aphp+intitle%3Aphpinfo+%22published by the PHP Group%22"
    f.write(f'<a target="_blank" href="{url}">phpinfo()</a><br>')
    url = f"https://www.google.com/search?q=site%3Apastebin.com+%7C+site%3Apaste2.org+%7C+site%3Apastehtml.com+%7C+site%3Aslexy.org+%7C+site%3Asnipplr.com+%7C+site%3Asnipt.net+%7C+site%3Atextsnip.com+%7C+site%3Abitpaste.app+%7C+site%3Ajustpaste.it+%7C+site%3Aheypasteit.com+%7C+site%3Ahastebin.com+%7C+site%3Adpaste.org+%7C+site%3Adpaste.com+%7C+site%3Acodepad.org+%7C+site%3Ajsitor.com+%7C+site%3Acodepen.io+%7C+site%3Ajsfiddle.net+%7C+site%3Adotnetfiddle.net+%7C+site%3Aphpfiddle.org+%7C+site%3Aide.geeksforgeeks.org+%7C+site%3Arepl.it+%7C+site%3Aideone.com+%7C+site%3Apaste.debian.net+%7C+site%3Apaste.org+%7C+site%3Apaste.org.ru+%7C+site%3Acodebeautify.org+%7C+site%3Acodeshare.io+%7C+site%3Atrello.com+%22{domain}%22"
    f.write(f'<a target="_blank" href="{url}">Search pastebin.com / pasting sites</a><br>')
    url = f"https://www.google.com/search?q=site%3Agithub.com+%7C+site%3Agitlab.com+%22{domain}%22"
    f.write(f'<a target="_blank" href="{url}">Search github.com and gitlab.com</a><br>')
    url = f"https://www.google.com/search?q=site%3Astackoverflow.com+%22{domain}%22"
    f.write(f'<a target="_blank" href="{url}">Search stackoverflow.com</a><br>')
    url = f"https://www.google.com/search?q=site%3A{domain}+inurl%3Asignup+%7C+inurl%3Aregister+%7C+intitle%3ASignup"
    f.write(f'<a target="_blank" href="{url}">Signup pages</a><br>')
    url = f"https://www.google.com/search?q=site%3A%2A.{domain}"
    f.write(f'<a target="_blank" href="{url}">Find Subdomains</a><br>')
    url = f"https://www.google.com/search?q=site%3A%2A.%2A.{domain}"
    f.write(f'<a target="_blank" href="{url}">Find Sub-Subdomains</a><br>')
    url = f"https://web.archive.org/web/*/{domain}/*"
    f.write(f'<a target="_blank" href="{url}">Search in web.archive.org</a><br>')
    url = f"https://www.google.com/search?q=({domain}) (site:*.*.29.* |site:*.*.28.* |site:*.*.27.* |site:*.*.26.* |site:*.*.25.* |site:*.*.24.* |site:*.*.23.* |site:*.*.22.* |site:*.*.21.* |site:*.*.20.* |site:*.*.19.* |site:*.*.18.* |site:*.*.17.* |site:*.*.16.* |site:*.*.15.* |site:*.*.14.* |site:*.*.13.* |site:*.*.12.* |site:*.*.11.* |site:*.*.10.* |site:*.*.9.* |site:*.*.8.* |site:*.*.7.* |site:*.*.6.* |site:*.*.5.* |site:*.*.4.* |site:*.*.3.* |site:*.*.2.* |site:*.*.1.* |site:*.*.0.*)"
    f.write(f'<a target="_blank" href="{url}">Show only IP addresses</a><br>')
    f.close()

domain = input("Enter a domain or URL: ")
dorking(domain)
print(f"\n[+] Success. Now the html-file is opening...\n")
webbrowser.open_new_tab('dorking.html')
call(["python", "run.py"])
