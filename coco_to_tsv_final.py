import csv
import os
import json
from tqdm import tqdm
from glob import glob
import argparse

def save_labels_TSV(image_path, output_dict, save_folder, threshold=0.3):
    content = 'class\txtl\tytl\txbr\tybr\ttemporary\toccluded\tdata\n' 
    for bbox, score, class_id in zip(output_dict['detection_boxes'], 
                                 output_dict['detection_scores'], 
                                 output_dict['detection_classes']):
        if score > threshold:
#             class_name = 1.0
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[0] + bbox[2])
            ymax = int(bbox[1] + bbox[3])
            content = content + '1.0\t' + str(xmin) + '\t' + str(ymin) + '\t' + str(xmax) + '\t' + str(ymax) + '\tfalse\tfalse\n'

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    out_tsv = open(os.path.join(save_folder, os.path.basename(image_path).split('.')[0] + '.tsv'), 'w')
    out_tsv.write(content)
    out_tsv.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert COCO JSON file from SNIPER to TSV files for a tracker. Input a json file and an output folder.')
    parser.add_argument('-r', '--result_json', type=str, nargs='?', help='define the json_result path, output by SNIPER, absolute is more preferable')
    parser.add_argument('-a', '--annotation_json', type=str, nargs='?', help='define the input json path used for SNIPER inference, absolute is more preferable')
    parser.add_argument('-o', '--out_path', type=str, nargs='?', default='coco_format/', help='define the output path, where tsv files will be saved')

    args = parser.parse_args()

    json_path = args.result_json
    json_img_anno = args.annotation_json
    img_list = json.load(open(json_img_anno, encoding="utf-8"))




    img_path_dict = {x['id']: x['file_name'] for x in img_list['images']}

    recog_list = json.load(open(json_path, encoding="utf-8"))

    # Dictionary of the format image_id: {bboxes: [], scores: [], classes: [], num_detections: n}
    grouped_dict = {}
    for recog in recog_list:
        if recog['image_id'] not in grouped_dict.keys():
            di = {}
            di['num_detections'] = 1
            di['detection_boxes'] = [recog['bbox']]
            di['detection_scores'] = [recog['score']]
            di['detection_classes'] = [recog['category_id']]

            grouped_dict[recog['image_id']] = di
            
        else:
            grouped_dict[recog['image_id']]['num_detections'] += 1
            grouped_dict[recog['image_id']]['detection_boxes'].append(recog['bbox'])
            grouped_dict[recog['image_id']]['detection_scores'].append(recog['score'])
            grouped_dict[recog['image_id']]['detection_classes'].append(recog['category_id'])

    for i, dic in tqdm(grouped_dict.items()):
        save_labels_TSV(img_path_dict[i], dic, args.out_path, 0.3)


