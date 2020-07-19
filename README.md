# Deep Differentiable Random Forests for Age Estimation

Code accompanying the paper [**Deep Differentiable Random Forests for Age Estimation**](https://arxiv.org/pdf/1907.10665.pdf).

## How to use

1. Download the Morph dataset. The Morph dataset is not free availabel, but you can request for it from [here](https://ebill.uncw.edu/C20231_ustores/web/store_main.jsp?STOREID=4).
2. Download pre-trained VGG model [VGG_ILSVRC_16_layers.caffemodel](http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_16_layers.caffemodel) .
3. Create a symbolic link to the Morph dataset with the name 'data/morph'

    `ln -s 'the directory for Morph dataset' data/morph`  

    or change the dir in scripts.  
4. Create the train set list and test set list.

    `python split_setting*.py`
5. Start to train.

    `python run.py`
    
    You can choose DRF or DLDLF by argument `--method`
    (and `morph2lmdb.py` is used to create LMDB for DLDLF)

Please cite the following paper if it helps your research:

@article{ShenTPAMI2019,
  author    = {Wei Shen and
               Yilu Guo and
               Yan Wang and
               Kai Zhao and
               Bo Wang and
               Alan L. Yuille},
  title     = {Deep Differentiable Random Forests for Age Estimation},
  journal   = {{IEEE} Trans. Pattern Anal. Mach. Intell.},
  volume    = {},
  year      = {2019}
}

If you have any issues using the code please email us at shenwei1231@gmail.com, gyl.luan0@gmail.com
