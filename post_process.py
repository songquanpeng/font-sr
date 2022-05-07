import argparse
import os

from PIL import Image
from tqdm import tqdm


def convert_img(img, threshold):
    foreground_img = img.convert("RGBA")
    datas = foreground_img.getdata()
    new_datas = list()
    for item in datas:
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_datas.append((255, 255, 255, 0))
        else:
            new_datas.append(item)
    foreground_img.putdata(new_datas)
    return foreground_img


def main(args):
    if args.input_path is None:
        args.input_path = input("Input path: ").strip('"').strip("'")
    if args.output_path is None:
        args.output_path = os.path.join('results', 'final', os.path.basename(args.input_path))
    print(f"Results will be save to: {args.output_path}")
    os.makedirs(args.output_path, exist_ok=True)
    img_names = os.listdir(args.input_path)
    for img_name in tqdm(img_names):
        img = Image.open(os.path.join(args.input_path, img_name))
        img = convert_img(img, args.binary_threshold)
        img.save(os.path.join(args.output_path, img_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--binary_threshold', type=int, default=200)
    main(parser.parse_args())
