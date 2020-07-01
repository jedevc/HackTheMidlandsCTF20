import hashlib

base = "INITIAL_VALUE"
for i in range(7594653):
    md5 = hashlib.md5()
    md5.update(base.encode())
    base = md5.hexdigest()
print("HTM{" + base + "}")
