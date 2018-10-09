#templey.py by thelmgn
#view the node.js version at https://github.com/thelmgn/templey
#theres a bit of a difference

a = "" # you can put a static file name to start with if theres no argv input



print("loading modules")
import time
start= time.time()
import os
import sys
import urllib.request
import subprocess
import base64

if len(sys.argv) == 2:
    a = sys.argv[1]
else:
    if a == "":
        a = input("what file?")



def process(text,fn,ind):
    split = text.split("|")
    out = ""
    textual = True
    escaped = False
    for s in split:
        if textual == True:
            if s.endswith("\\"):
                out = out + s
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
                        elif schemepathsplit[0] == "http":
                            print(ind+"sending http request to " + schemepathsplit[1])
                            with urllib.request.urlopen("http://" +schemepathsplit[1]) as response:
                                out = out + response.read
                        elif schemepathsplit[0] == "https":
                            print(ind+"sending https request to " + schemepathsplit[1])
                            with urllib.request.urlopen("https://" +schemepathsplit[1]) as response:
                                out = out + response.read
                        elif schemepathsplit[0] == "procarg":
                            a = sys.argv
                            a.insert(0, sys.path[0])
                            if schemepathsplit[1] == "all":
                                out = out + " ".join(a)
                            else:
                                out = out + str(a[int(schemepathsplit[1])])
                        elif schemepathsplit[0] == "filename":
                            out = out + fn
                        elif schemepathsplit[0] == "command":
                            print(ind+"running command " + schemepathsplit[1])
                            out = out + str(subprocess.run(schemepathsplit[1].split(" "), stdout=subprocess.PIPE).stdout)
                        elif schemepathsplit[0] == "b64":
                            bf = open(schemepathsplit[1],"rb")
                            bfc = bf.read()
                            bf.close()
                            out = out + base64.b64encode(bfc).decode('ascii')
                        else:
                            print(ind+"!templey:unknownscheme:" + schemepathsplit[0] + "!")
                            out = out + "!templey:unknownscheme:" + schemepathsplit[0] + "!"
                    else:
                        print(ind+"!templey:morethanone\:!")
                        out = out + "!templey:morethanone\:!"
                except Exception as e:
                    print(ind+str(e))
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
        print("!templey:file doesn't exist:" + file + "!")
        return "!templey:file doesn't exist:" + file + "!"

if os.path.isfile(a):
    filename, file_extension = os.path.splitext(a)
    ff = open(filename + ".templeybuild" + file_extension,"w")
    ff.write(processFile(a,""))
    ff.close()
    print("done in " + str(time.time() - start) + "s!")
else:
    print("crit! " + a + " doesn't exist!")
