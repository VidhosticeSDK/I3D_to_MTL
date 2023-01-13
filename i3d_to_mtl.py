import _config_VidhosticeSDK_
import sys
import untangle
from pathlib import Path
#pip install untangle


FS22_data = _config_VidhosticeSDK_.FS22_data
#FS22_data = 'c:/FS22/Data_FS22/data'


def fileId_Texture_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if 'Texture' in dir(material):
            if material['materialId'] == materialId:
                return material.Texture['fileId']
        else:
            return None

def fileId_Normalmap_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if 'Normalmap' in dir(material):
            if material['materialId'] == materialId:
                return material.Normalmap['fileId']
        else:
            return None

def fileId_Glossmap_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if 'Glossmap' in dir(material):
            if material['materialId'] == materialId:
                return material.Glossmap['fileId']
        else:
            return None

def Filename_from_fileId(fileId):
    if fileId is None:
        return None
    for file in obj.i3D.Files.File:
        if file['fileId'] == fileId:
            return file['filename']

def export_mtl(shape, prefix=''):
    str_shapeId = F"{int(shape['shapeId']):03}"
    print(prefix+'List of materialIds:', shape['materialIds'])
    print(prefix+'Output file:', str_shapeId+'_'+shape['name']+'_'+shape['nodeId']+'.mtl')
    file = open(str_shapeId+'_'+shape['name']+'_'+shape['nodeId']+'.mtl', "w")
    sys.stdout = file
    materials = shape['materialIds']
    i = 1
    for material in materials.split(","):
        print('newmtl', i)

        texture = Filename_from_fileId(fileId_Texture_from_materialId(material))
        if texture is not None:
            file_texture = Path(texture.replace('$data', FS22_data))
            if file_texture.with_suffix('.png').exists():
                file_texture = file_texture.with_suffix('.png')
            print('map_Kd ' + str(file_texture.as_posix()))

        normalmap = Filename_from_fileId(fileId_Normalmap_from_materialId(material))
        if normalmap is not None:
            file_normalmap = Path(normalmap.replace('$data', FS22_data))
            if file_normalmap.with_suffix('.png').exists():
                file_normalmap = file_normalmap.with_suffix('.png')
            print('map_Bump ' + str(file_normalmap.as_posix()))

        glossmap = Filename_from_fileId(fileId_Glossmap_from_materialId(material))
        if glossmap is not None:
            file_glossmap = Path(glossmap.replace('$data', FS22_data))
            if file_glossmap.with_suffix('.png').exists():
                file_glossmap = file_glossmap.with_suffix('.png')
            print('map_Ks ' + str(file_glossmap.as_posix()))

        i = i + 1

    sys.stdout = sys.__stdout__
    file.close()

def parse_scene(children, t=0):
    for ele in children:
        if ele._name == 'Shape':
            text = '( shapeId: ' + ele['shapeId'] + ' name: ' + ele['name'] + ' )'
            print(" "*t*2 + "\\", ele._name, text)
            export_mtl(ele, " "*t*2 + "   ")
        elif ele._name == 'TransformGroup':
            text = '( name: ' + ele['name'] + ' )'
            print(" "*t*2 + "\\", ele._name, text)
        else:
            text = ''
            print(" "*t*2 + "\\", ele._name, text)
        if len(ele.children):
            parse_scene(ele.children, t+1)

#-------------------------------------------------------------------------------
print('I3D to MTL by VidhosticeSDK')

if len(sys.argv) < 2:
    print('Error: Missing argument I3D file')
    sys.exit()
if not Path(sys.argv[1]).exists():
    print('Error: File not found:', sys.argv[1])
    sys.exit()

print('Input file: ', sys.argv[1])
print()

obj = untangle.parse(sys.argv[1])

parse_scene(obj.i3D.Scene.children)

print('Done')
