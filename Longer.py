import pyshorteners as pys

sh = pys.Shortener()

Lurl = input(f"Enter a URL to be shortened\n")
Surl = sh.tinyurl.short(Lurl)
print()
L2 = sh.tinyurl.expand(Surl) + "  -> Original"

print(f"Converted URL:\n{Surl}\n")
print(L2)