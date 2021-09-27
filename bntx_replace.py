import os
import bntx as BNTX
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Replace a texture in a BNTX file.')
parser.add_argument('bntx_file', type=pathlib.Path, help='File that we replace in.')
parser.add_argument('dds_file', type=pathlib.Path, help='A dds file that we want to insert.')
parser.add_argument('-t', metavar='--texture_name', type=str, help='Name of the texture that you want to replace. If '
                                                                   'not set, it will use the dds file to deduce the '
                                                                   'texture name.')

args = parser.parse_args()

print(args)

btnx_file_path = args.bntx_file
dds_file_path = args.dds_file

if args.t is None:
    texture_name = os.path.splitext(dds_file_path)[0]
else:
    texture_name = args.t

bntx_file = BNTX.File()
returnCode = bntx_file.readFromFile(btnx_file_path)
if returnCode:
    raise SystemExit('Error while opening the BNTX file.')

# find the texture in the pack that we want replaced
replace_texture = None
replace_texture_index = None
i = 0
for t in bntx_file.textures:
    if t.name == texture_name:
        replace_texture = t
        replace_texture_index = i
        break
    i += 1

if replace_texture is None:
    raise SystemExit('Cannot find texture to replace.')

tileMode = replace_texture.tileMode
SRGB = 1
sparseBinding = 1
sparseResidency = 1
importMips = 0

replaced_texture = bntx_file.replace(replace_texture, tileMode, SRGB, sparseBinding, sparseResidency, importMips, dds_file_path)
if replaced_texture:
    bntx_file.textures[replace_texture_index] = replaced_texture

with open(btnx_file_path, 'wb') as out:
    out.write(bntx_file.save())
