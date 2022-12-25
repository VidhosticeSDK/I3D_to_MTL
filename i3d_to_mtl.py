import sys
import untangle
#pip install untangle


FS22_data = 'c:/FS22/Data_FS22/data'


obj = untangle.parse(sys.argv[1])

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


for shape in obj.i3D.Scene.Shape:
    print('I3D to MTL by VidhosticeSDK')
    print('Input file: ', sys.argv[1])
    print('Output file:', shape['name']+'_'+shape['nodeId']+'.mtl')
    print('  list of materials:', shape['materialIds'])
    file = open(shape['name']+'_'+shape['nodeId']+'.mtl', "w")
    sys.stdout = file
    materials = shape['materialIds']
    i = 1
    for material in materials.split(","):
        print('newmtl', i)

        texture = Filename_from_fileId(fileId_Texture_from_materialId(material))
        if texture is not None:
            print('map_Kd '+texture.replace('$data', FS22_data))

        normalmap = Filename_from_fileId(fileId_Normalmap_from_materialId(material))
        if normalmap is not None:
            print('map_Bump '+normalmap.replace('$data', FS22_data))

        glossmap = Filename_from_fileId(fileId_Glossmap_from_materialId(material))
        if glossmap is not None:
            print('map_Ks '+glossmap.replace('$data', FS22_data))

        i = i + 1

    sys.stdout = sys.__stdout__
    file.close()
    print('Done')
