#!/bin/bash
CUDA_VISIBLE_DEVICES=0 python train.py \
--dataroot ./archive/FONT_SR_32to256_ttf_10_test3_resizeFalse_anti_aliasFalse \
--name super_font_cyclegan3 --model cycle_gan