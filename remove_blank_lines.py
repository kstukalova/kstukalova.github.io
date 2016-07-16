import fileinput
for line in fileinput.FileInput("mobile.html",inplace=1):
    if line.rstrip():
        print(line, end='')