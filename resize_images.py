import argparse
import os

from PIL import Image
from tqdm import tqdm


def resize(input_path, output_path, target_size=256):
    os.makedirs(output_path, exist_ok=True)
    img_paths = os.listdir(input_path)
    for img_path in tqdm(img_paths):
        img = Image.open(os.path.join(input_path, img_path))
        img = img.resize((target_size, target_size), Image.ANTIALIAS)
        img.save(os.path.join(output_path, img_path))


resample_modes = [Image.NEAREST, Image.BOX, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS,
                  Image.ANTIALIAS]

resample_mode_names = ['Image.NEAREST', 'Image.BOX', 'Image.BILINEAR', 'Image.HAMMING', 'Image.BICUBIC',
                       'Image.LANCZOS', 'Image.ANTIALIAS']


def test_resize(input_path, output_path, target_size=256):
    os.makedirs(output_path, exist_ok=True)
    img_paths = os.listdir(input_path)
    for i, img_path in tqdm(enumerate(img_paths)):
        if i == 10:
            break
        img = Image.open(os.path.join(input_path, img_path))
        for mode, name in zip(resample_modes, resample_mode_names):
            tmp_img = img.resize((target_size, target_size), mode)
            tmp_img.save(os.path.join(output_path, f"{name}_{img_path}"))


def main(args):
    if args.test:
        resize(args.input_path, args.output_path, args.target_size)
    else:
        test_resize(args.input_path, args.output_path, args.target_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--target_size', type=int, default=256)
    parser.add_argument('--test', action='store_true')
    main(parser.parse_args())
