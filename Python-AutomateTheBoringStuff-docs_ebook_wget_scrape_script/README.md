# CS Principles: Big Ideas in Programming — Offline Web E-book Package

This ZIP contains a ready-to-run crawler script for the Open Book Project / Runestone web book:

https://matt.curinga.com/think-js/

## Why the full mirror is not embedded here
The execution sandbox could access the page through the browsing tool, but its command-line network layer could not resolve `www.openbookproject.net`, so `wget` could not crawl the site from inside the sandbox.

## To generate the full offline web ebook
On a machine with internet access and `wget` installed:

```bash
unzip studentcsp_ebook_package.zip
cd studentcsp_ebook
./create_studentcsp_offline.sh
```

Then open:

```text
https://matt.curinga.com/think-js/index.html
```

## Windows
Install WSL, Git Bash, or wget for Windows, then run the same script. Alternatively, copy the wget command from the script and run it manually.
