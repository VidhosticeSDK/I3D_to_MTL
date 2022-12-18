import sys
import untangle
#pip install untangle

obj = untangle.parse(sys.argv[1])

def fileId_Texture_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if material['materialId'] == materialId:
            return material.Texture['fileId']

def fileId_Normalmap_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if material['materialId'] == materialId:
            return material.Normalmap['fileId']

def fileId_Glossmap_from_materialId(materialId):
    for material in obj.i3D.Materials.Material:
        if material['materialId'] == materialId:
            return material.Glossmap['fileId']

def Filename_from_fileId(fileId):
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
        print('map_Kd '+Filename_from_fileId(fileId_Texture_from_materialId(material)))
        print('map_Bump '+Filename_from_fileId(fileId_Normalmap_from_materialId(material)))
        print('map_Ks '+Filename_from_fileId(fileId_Glossmap_from_materialId(material)))
        i = i + 1
    sys.stdout = sys.__stdout__
    file.close()
    print('Done')
