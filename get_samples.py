"""
Downloads the 10 emails used in this project into samples/.

They come from Phishing Pot (https://github.com/rf-peixoto/phishing_pot, CC BY-NC 4.0),
real phishing and spam caught by honeypot inboxes.

Don't double-click the .eml files. That opens them in a mail app, which can load
remote images and tell the sender the email was opened. Open them in VS Code instead.
"""
from pathlib import Path
from urllib.request import urlopen

SAMPLES = [7978, 8062, 8216, 8265, 8342, 8370, 8419, 8568, 8582, 8614]
BASE = "https://raw.githubusercontent.com/rf-peixoto/phishing_pot/main/email/sample-{}.eml"

out = Path("samples")
out.mkdir(exist_ok=True)
for n in SAMPLES:
    target = out / f"sample-{n}.eml"
    if target.exists():
        print(f"{target.name} already there")
        continue
    with urlopen(BASE.format(n)) as r:
        target.write_bytes(r.read())
    print(f"got {target.name}")
