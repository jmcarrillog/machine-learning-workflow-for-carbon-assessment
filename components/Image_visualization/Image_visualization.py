import os
import sys
import subprocess

def main():
    # input land cover image
    land_cover = sys.argv[1]
    # input lut coloring file
    lut_file = sys.argv[2]
    # output visualization ready image
    out_image = sys.argv[3]
    
    # create a visualization ready image
    image_viz(land_cover, lut_file, out_image)


def image_viz(land_cover, lut_file, out_image):

    # prepare the system call
    otb_call = []
    otb_call.append('otbcli_ColorMapping')
    otb_call.append('-in')
    otb_call.append(land_cover)
    otb_call.append('-method')
    otb_call.append('custom')
    otb_call.append('-method.custom.lut')
    otb_call.append(lut_file)
    otb_call.append('-out')
    otb_call.append(out_image)
    
    subprocess.call(otb_call)

main()