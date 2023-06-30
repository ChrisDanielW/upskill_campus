import pyshorteners as pys

Lurl = input(f"Enter a URL to be shortened\n")
Surl = pys.Shortener().tinyurl.short(Lurl)

print(Surl)