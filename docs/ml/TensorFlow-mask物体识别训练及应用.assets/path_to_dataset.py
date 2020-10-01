import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


def main():
    logger.warning(
        "This script is aimed to demonstrate how to convert "
        "JSON files to image dataset from a dir."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("-o", "--out", default=None)
    parser.add_argument("-r", "--rename", default='N')
    args = parser.parse_args()

    _path = args.path
    _out_dir = ''
    if args.out is not None:
        _out_dir = osp.realpath(args.out)

    # 执行转换
    path_to_dataset(_path, _out_dir, args.rename == 'Y')


def path_to_dataset(path: str, out_dir: str, rename: bool):
    """
    将指定目录下的JSON文件转换为DataSet格式的目录

    @param {str} path - 要处理的目录
    @param {str} out_dir - 输出目录
    @param {bool} rename - 遇到输出目录存在是否修改文件名
    """
    # 遍历目录下的所有文件
    _file_names = os.listdir(path)
    for _file in _file_names:
        _fullname = os.path.join(path, _file)
        if osp.isdir(_fullname):
            # 是目录，递归处理
            path_to_dataset(_fullname, out_dir, rename)
        else:
            # 是文件
            if not _fullname.endswith('.json'):
                continue

            # 执行转换处理
            json_to_dataset(_fullname, out_dir, rename)


def json_to_dataset(json_file: str, out_dir: str, rename: bool):
    """
    JSON文件转换为DataSet格式文件夹

    @param {str} json_file - 要处理的JSON文件
    @param {str} out_dir - 输出目录
    @param {bool} rename - 遇到输出目录存在是否修改文件名
    """
    _json_path = osp.split(json_file)[0]
    _dir_name = osp.split(json_file)[1].replace(".", "_")
    if out_dir == '':
        _out_dir = osp.join(_json_path, _dir_name)
    else:
        _out_dir = osp.join(out_dir, _dir_name)

    if not osp.exists(_out_dir):
        os.makedirs(_out_dir)
    elif rename:
        # 遇到文件存在的情况，重命名
        _index = 1
        while osp.exists(_out_dir):
            _out_dir = osp.join(_json_path, '%s%d%s' % (_dir_name[0: -5], _index, '_json'))
            _index += 1

        os.makedirs(_out_dir)

    data = json.load(open(json_file))
    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)

    label_name_to_value = {"_background_": 0}

    # 修正json_to_dataset的bug, 按形状名进行排序，将hole放在最后面
    data["shapes"].sort(key=lambda x: x["label"] if x["label"] != "hole" else "zzzzzz")
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl, _ = utils.shapes_to_label(
        img.shape, data["shapes"], label_name_to_value
    )

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name

    lbl_viz = imgviz.label2rgb(
        label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
    )

    PIL.Image.fromarray(img).save(osp.join(_out_dir, "img.png"))
    utils.lblsave(osp.join(_out_dir, "label.png"), lbl)
    PIL.Image.fromarray(lbl_viz).save(osp.join(_out_dir, "label_viz.png"))

    with open(osp.join(_out_dir, "label_names.txt"), "w") as f:
        for lbl_name in label_names:
            f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(_out_dir))


if __name__ == "__main__":
    main()
    # json_to_dataset(
    #     r'D:\ccproject\mask_rcnn_resnet101\0000000003.json', '', False
    # )
