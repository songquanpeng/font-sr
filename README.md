# 字体超分辨

## 准备数据集
```shell
python gen_dataset.py
```

## 训练模型
```shell
python --dataroot ./archive/FONT_SR_64to256_ttf_10_test3 \
--name super_font_cyclegan --model cycle_gan
```

## 其他
代码基于：https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix