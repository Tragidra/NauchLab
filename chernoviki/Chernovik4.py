import fileinput
import io
import sys
from os import fdopen, remove
from shutil import copymode, move
from tempfile import mkstemp


def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w',encoding='utf8') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

value = "Хаха"
replace("C:/Users/astra/PycharmProjects/Laboratoria1.0/resour/cherteji/index.html","var dataToImport",value)