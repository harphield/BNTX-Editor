import os
import bntx as BNTX
import argparse
import pathlib


def replace_texture(bntx, dds_path, texture):
    # find the texture in the pack that we want replaced
    texture_to_replace = None
    replace_texture_index = None
    i = 0
    for t in bntx.textures:
        if t.name == texture:
            texture_to_replace = t
            replace_texture_index = i
            break
        i += 1

    if texture_to_replace is None:
        raise SystemExit('Cannot find texture to replace.')

    tile_mode = texture_to_replace.tileMode
    srgb = 1
    sparse_binding = 1
    sparse_residency = 1
    import_mips = 0

    replaced_texture = bntx.replace(texture_to_replace, tile_mode, srgb, sparse_binding, sparse_residency,
                                    import_mips,
                                    dds_path)
    if replaced_texture:
        bntx.textures[replace_texture_index] = replaced_texture

    return bntx


parser = argparse.ArgumentParser(description='Replace a texture in a BNTX file.')
parser.add_argument('bntx_file', type=pathlib.Path, help='File that we replace in.')
parser.add_argument('dds_file', type=pathlib.Path, help='A dds file or folder of ddses that we want to insert.')
parser.add_argument('-t', metavar='--texture_name', type=str, help='Name of the texture that you want to replace. If '
                                                                   'not set, it will use the dds file to deduce the '
                                                                   'texture name.')

args = parser.parse_args()

print(args)

btnx_file_path = args.bntx_file
dds_file_path = args.dds_file

if os.path.isdir(dds_file_path):
    if args.t is not None:
        raise SystemExit('-t is valid only for single files, not folders.')

    bntx_file = BNTX.File()
    returnCode = bntx_file.readFromFile(btnx_file_path)
    if returnCode:
        raise SystemExit('Error while opening the BNTX file.')

    for (dirpath, dirnames, filenames) in os.walk(dds_file_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            texture_name = os.path.splitext(dds_file_path)[0]

            bntx_file = replace_texture(bntx_file, file_path, texture_name)
else:
    if args.t is None:
        texture_name = os.path.splitext(dds_file_path)[0]
    else:
        texture_name = args.t

    bntx_file = BNTX.File()
    returnCode = bntx_file.readFromFile(btnx_file_path)
    if returnCode:
        raise SystemExit('Error while opening the BNTX file.')

    bntx_file = replace_texture(bntx_file, dds_file_path, texture_name)

# save to a new file
split = os.path.split(btnx_file_path)
new_path = os.path.join(split[0], split[1] + '.new')

with open(new_path, 'wb') as out:
    out.write(bntx_file.save())
