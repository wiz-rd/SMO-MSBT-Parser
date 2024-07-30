import binascii

filepath = input("Input the path of the file to read: ")

with open(filepath, "rb") as f:
    contents = f.readlines()

print(binascii.hexlify(contents[-1], sep=","))
print(str(contents[-1]).replace("\\x00", ""))
