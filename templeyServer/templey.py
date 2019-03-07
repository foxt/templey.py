#templey.py by thelmgn
#view the node.js version at https://github.com/thelmgn/templey
#theres a bit of a difference

import time
import os
import sys
import urllib.request
import subprocess
import base64



def process(text,fn,ind):
    split = text.split("|")
    out = ""
    textual = True
    escaped = False
    for s in split:
        if textual == True:
            if s.endswith("\\"):
                out = out + s[:-1]
                escaped = True
            else:
                out = out + s
            textual = False
        else:
            if escaped:
                out = out + "|" + s + "|"
            else:
                try:
                    schemepathsplit = s.split(":")
                    if len(schemepathsplit) == 2:
                        if schemepathsplit[0] == "file":
                            out = out + processFile(schemepathsplit[1],ind+" ")
                        elif schemepathsplit[0] == "min":
                            out = out + processFile(schemepathsplit[1],ind+" ").replace("\n","")
                        elif schemepathsplit[0] == "http":
                            with urllib.request.urlopen("http://" +schemepathsplit[1]) as response:
                                out = out + response.read
                        elif schemepathsplit[0] == "https":
                            with urllib.request.urlopen("https://" +schemepathsplit[1]) as response:
                                out = out + response.read
                        elif schemepathsplit[0] == "procarg":
                            a = sys.argv
                            a.insert(0, sys.path)
                            if schemepathsplit[1] == "all":
                                out = out + " ".join(a)
                            else:
                                out = out + str(a[int(schemepathsplit[1])])
                        elif schemepathsplit[0] == "filename":
                            out = out + fn
                        elif schemepathsplit[0] == "command":
                            out = out + str(subprocess.run(schemepathsplit[1].split(" "), stdout=subprocess.PIPE).stdout)
                        elif schemepathsplit[0] == "b64":
                            bf = open(schemepathsplit[1],"rb")
                            bfc = bf.read()
                            bf.close()
                            out = out + base64.b64encode(bfc).decode('ascii')
                        else:
                            out = out + "!templey:unknownscheme:" + schemepathsplit[0] + "!"
                    else:
                        out = out + "!templey:morethanone\:!"
                except Exception as e:
                    out = out + "!templey:" + str(e) + "!"
            textual = True
            escaped = False

    return out

def processFile(file,ind):
    if os.path.isfile(file):
        print(ind+"building " + file)
        fo = open(file,"r")
        f = fo.read()
        return process(f,file,ind+" ")
    else:
        return "!templey:file doesn't exist:" + file + "!"

