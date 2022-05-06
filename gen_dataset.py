import argparse
import os
import pathlib
import random

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Obtaining characters from .ttf')
parser.add_argument('--ttf_path', type=str, default='./archive/ttf_10', help='ttf directory')
parser.add_argument('--chara', type=str, default='./archive/character_3588.txt', help='characters')
parser.add_argument('--save_path', type=str, help='images directory')
parser.add_argument('--img_sizes', type=int, default=[64, 256], help='The size of generated images')  # 80, 64
parser.add_argument('--char_sizes', type=int, default=[56, 224], help='The size of generated characters')  # 70, 56
parser.add_argument('--offset_coefficients', type=int, default=[-1, -1])
parser.add_argument('--align_list', type=int, nargs='+', default=[])
parser.add_argument('--shuffle', action='store_true')
parser.add_argument('--test_font_num', type=int, default=3)
parser.add_argument('--seed', type=int, default=0)

args = parser.parse_args()

file_object = open(args.chara, encoding='utf-8')
try:
    characters = file_object.read()
finally:
    file_object.close()

if args.shuffle:
    characters = list(characters)
    random.seed(args.seed)
    random.shuffle(characters)
    characters = "".join(characters)

if not args.save_path:
    args.save_path = os.path.join('archive',
                                  f"FONT_SR_{args.img_sizes[0]}to{args.img_sizes[1]}_{os.path.basename(args.ttf_path)}_test{args.test_font_num}")

os.makedirs(args.save_path, exist_ok=True)


def draw_char(ch, font, img_size, char_size, offset_coefficient=1, align=False):
    x_offset, y_offset = (img_size - char_size) / 2, (img_size - char_size) / 2
    if align:
        y_offset *= offset_coefficient
    img = Image.new("RGB", (img_size, img_size), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((x_offset, y_offset), ch, (0, 0, 0), font=font)
    return img


def main():
    data_dir = args.ttf_path
    data_root = pathlib.Path(data_dir)
    print(data_root)

    all_font_paths = list(data_root.glob('*.ttf*')) + list(data_root.glob('*.TTF*'))
    all_font_paths += list(data_root.glob('*.ttc*')) + list(data_root.glob('*.TTC*'))
    all_font_paths = list(set(all_font_paths))
    all_font_paths = [str(path) for path in all_font_paths]
    all_font_paths.sort()

    print(f"Total {len(all_font_paths)} fonts:")
    for i in range(len(all_font_paths)):
        print(all_font_paths[i])
    for which, font_paths in zip(['train', 'test'], [all_font_paths[:-3], all_font_paths[-3:]]):
        for label, img_size, char_size, offset_coefficient in zip([f'{which}A', f'{which}B'], args.img_sizes,
                                                                  args.char_sizes, args.offset_coefficients):
            output_path = os.path.join(args.save_path, label)
            os.makedirs(output_path, exist_ok=True)
            for i, item in enumerate(font_paths):
                font = ImageFont.truetype(item, size=char_size)
                font_name = os.path.basename(item)
                align = i in args.align_list
                for (chara, cnt) in tqdm(zip(characters, range(len(characters))), total=len(characters)):
                    img = draw_char(chara, font, img_size, char_size, offset_coefficient, align)
                    if img_size != args.img_sizes[1]:
                        img = img.resize((args.img_sizes[1], args.img_sizes[1]), Image.ANTIALIAS)
                    img.save(os.path.join(output_path, f"{font_name}_{cnt:04}.png"))


if __name__ == '__main__':
    main()
