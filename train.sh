#!/bin/bash
CUDA_VISIBLE_DEVICES=0 python train.py \
--dataroot ./archive/FONT_SR_64to256_ttf_10_test3 \
--name super_font_cyclegan --model cycle_gan