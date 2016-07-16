import fileinput
for line in fileinput.FileInput("index.html",inplace=1):
    if line.rstrip():
        print(line, end='')