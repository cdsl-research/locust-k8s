import sys
args = sys.argv
with open("/(path).yaml", "r") as f:
    x = f.readlines()
    o = []
    for i in x:
        if "replicas:" in i:
            i = f"  replicas: {args[1]}\n"
        o.append(i)
with open("/(same path)yaml", "w") as f:
    f.writelines(o)
