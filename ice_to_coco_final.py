import csv
import os
import json
from PIL import Image
from tqdm import tqdm
from glob import glob
import argparse

# filename,x_from,y_from,width,height,sign_class,sign_id

def convert_tsv2coco(baseDir, tsvPaths, outPath, batch, stride, name):

    id_images = 0
    batch_num = 0

    if not os.path.exists(outPath):
        os.mkdir(outPath)

    data_json_val = {}
    data_json_val['images'] = []
#    data_json_val['annotations'] = []
    data_json_val["categories"] = [{"supercategory": "person","id": 1,"name": "person"},{"supercategory": "vehicle","id": 2,"name": "bicycle"},{"supercategory": "vehicle","id": 3,"name": "car"},{"supercategory": "vehicle","id": 4,"name": "motorcycle"},{"supercategory": "vehicle","id": 5,"name": "airplane"},{"supercategory": "vehicle","id": 6,"name": "bus"},{"supercategory": "vehicle","id": 7,"name": "train"},{"supercategory": "vehicle","id": 8,"name": "truck"},{"supercategory": "vehicle","id": 9,"name": "boat"},{"supercategory": "outdoor","id": 10,"name": "traffic light"},{"supercategory": "outdoor","id": 11,"name": "fire hydrant"},{"supercategory": "outdoor","id": 13,"name": "stop sign"},{"supercategory": "outdoor","id": 14,"name": "parking meter"},{"supercategory": "outdoor","id": 15,"name": "bench"},{"supercategory": "animal","id": 16,"name": "bird"},{"supercategory": "animal","id": 17,"name": "cat"},{"supercategory": "animal","id": 18,"name": "dog"},{"supercategory": "animal","id": 19,"name": "horse"},{"supercategory": "animal","id": 20,"name": "sheep"},{"supercategory": "animal","id": 21,"name": "cow"},{"supercategory": "animal","id": 22,"name": "elephant"},{"supercategory": "animal","id": 23,"name": "bear"},{"supercategory": "animal","id": 24,"name": "zebra"},{"supercategory": "animal","id": 25,"name": "giraffe"},{"supercategory": "accessory","id": 27,"name": "backpack"},{"supercategory": "accessory","id": 28,"name": "umbrella"},{"supercategory": "accessory","id": 31,"name": "handbag"},{"supercategory": "accessory","id": 32,"name": "tie"},{"supercategory": "accessory","id": 33,"name": "suitcase"},{"supercategory": "sports","id": 34,"name": "frisbee"},{"supercategory": "sports","id": 35,"name": "skis"},{"supercategory": "sports","id": 36,"name": "snowboard"},{"supercategory": "sports","id": 37,"name": "sports ball"},{"supercategory": "sports","id": 38,"name": "kite"},{"supercategory": "sports","id": 39,"name": "baseball bat"},{"supercategory": "sports","id": 40,"name": "baseball glove"},{"supercategory": "sports","id": 41,"name": "skateboard"},{"supercategory": "sports","id": 42,"name": "surfboard"},{"supercategory": "sports","id": 43,"name": "tennis racket"},{"supercategory": "kitchen","id": 44,"name": "bottle"},{"supercategory": "kitchen","id": 46,"name": "wine glass"},{"supercategory": "kitchen","id": 47,"name": "cup"},{"supercategory": "kitchen","id": 48,"name": "fork"},{"supercategory": "kitchen","id": 49,"name": "knife"},{"supercategory": "kitchen","id": 50,"name": "spoon"},{"supercategory": "kitchen","id": 51,"name": "bowl"},{"supercategory": "food","id": 52,"name": "banana"},{"supercategory": "food","id": 53,"name": "apple"},{"supercategory": "food","id": 54,"name": "sandwich"},{"supercategory": "food","id": 55,"name": "orange"},{"supercategory": "food","id": 56,"name": "broccoli"},{"supercategory": "food","id": 57,"name": "carrot"},{"supercategory": "food","id": 58,"name": "hot dog"},{"supercategory": "food","id": 59,"name": "pizza"},{"supercategory": "food","id": 60,"name": "donut"},{"supercategory": "food","id": 61,"name": "cake"},{"supercategory": "furniture","id": 62,"name": "chair"},{"supercategory": "furniture","id": 63,"name": "couch"},{"supercategory": "furniture","id": 64,"name": "potted plant"},{"supercategory": "furniture","id": 65,"name": "bed"},{"supercategory": "furniture","id": 67,"name": "dining table"},{"supercategory": "furniture","id": 70,"name": "toilet"},{"supercategory": "electronic","id": 72,"name": "tv"},{"supercategory": "electronic","id": 73,"name": "laptop"},{"supercategory": "electronic","id": 74,"name": "mouse"},{"supercategory": "electronic","id": 75,"name": "remote"},{"supercategory": "electronic","id": 76,"name": "keyboard"},{"supercategory": "electronic","id": 77,"name": "cell phone"},{"supercategory": "appliance","id": 78,"name": "microwave"},{"supercategory": "appliance","id": 79,"name": "oven"},{"supercategory": "appliance","id": 80,"name": "toaster"},{"supercategory": "appliance","id": 81,"name": "sink"},{"supercategory": "appliance","id": 82,"name": "refrigerator"},{"supercategory": "indoor","id": 84,"name": "book"},{"supercategory": "indoor","id": 85,"name": "clock"},{"supercategory": "indoor","id": 86,"name": "vase"},{"supercategory": "indoor","id": 87,"name": "scissors"},{"supercategory": "indoor","id": 88,"name": "teddy bear"},{"supercategory": "indoor","id": 89,"name": "hair drier"},{"supercategory": "indoor","id": 90,"name": "toothbrush"}]

    for tsvPath in tsvPaths:

        if baseDir == None:
            baseDir = os.path.dirname(tsvPath)

        # Read filenames from index.tsv
        with open(tsvPath, 'r') as fp:
            reader = csv.reader(fp, delimiter='\t', quotechar='"')
            tsv_data = list(reader)
            tsv_data.pop(0)

        # Check img/tsv correspondence
        imgPathList = []
        
        for data in tsv_data:
            imgPathList.append(data[0])

        # Write images field in the JSON
        width = 2448
        height = 2048

        for i, rawImgPath in tqdm(enumerate(imgPathList)):
            if i % stride == 0:

                imgPath = os.path.join(baseDir, rawImgPath + '.pnm')
                # print(imgPath)
                if os.path.exists(imgPath):

                    # Check size of the first image
                    if id_images == 0:
                        im = Image.open(imgPath)
                        width, height = im.size
                    id_images += 1                        
                    data_json_val['images'].append({'file_name': imgPath, 'id': id_images, 'width': width, 'height': height})
                if (batch > 0) and (id_images > batch):
                    print('Annotated', id_images, 'images, from the total', len(tsv_data),'images in the index.tsv)')

                    json_data_val = json.dumps(data_json_val, indent=4)
                    outFN = os.path.join(outPath, 'instances_' + name + str(batch_num) + '.json')
                    f = open(outFN, "w+")
                    f.write(json_data_val)
                    f.close()

                    print('Saved to', outFN)
                    
                    data_json_val['images'] = []
                    batch_num += 1
                    id_images = 0

    print('Annotated', id_images, 'images, from the total', len(tsv_data),'images in the index.tsv)')
    json_data_val = json.dumps(data_json_val, indent=4)
    outFN = os.path.join(outPath, 'instances_' + name + str(batch_num) + '.json')    
    f = open(outFN, "w+")
    f.write(json_data_val)
    f.close()
    print('Saved to', outFN)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Icevision final datasets to COCO format. Input a list of tsv files, each lies in a corresponding dir with its images. Optional input is dataset name.')
    parser.add_argument('tsvfiles', metavar='index.tsv', nargs='+', help='input table with image names')
    parser.add_argument('-i', '--in_path', nargs='?', default=None, help='define the input folder, absolute is more preferable')
    parser.add_argument('-o', '--out_path', nargs='?', default='coco_format/', help='define the output path, where instances_set_name1.json files will be saved')
    parser.add_argument('-n', '--name', nargs='?', default='fin', help='dataset name (will be added after instances_)')
    parser.add_argument('-b', '--batch', type=int, nargs='?', default=0, help='number of frames in each json')
    parser.add_argument('-s', '--stride', type=int, nargs='?', default=1, help='interval between processed frames >= 1. Default 1.')

    args = parser.parse_args()

    print('Converting', args.name)
    convert_tsv2coco(args.in_path, args.tsvfiles, args.out_path, args.batch, args.stride, args.name)
