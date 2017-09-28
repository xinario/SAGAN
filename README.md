## SAGAN
This repo provides the trained denoising model and testing code for low dose CT denoising as described in our [paper](https://arxiv.org/abs/1708.06453).
Here are some randomly picked denoised results on low dose CTs from this [kaggle challenge](https://www.kaggle.com/c/data-science-bowl-2017/data). 
<img src="imgs/sample.jpg" width="900px"/>

## How to use

### Prerequistites
- Linux or OSX
- NVIDIA GPU

### Getting Started
- Install [torch7](http://torch.ch/docs/getting-started.html#_)
- Install torch packages nngraph and hdf5
```bash
luarocks install nngraph
luarocks install hdf5
```
- Clone this repo:
```bash
git clone git@github.com:xinario/SAGAN.git
cd SAGAN
```
- Download the pretrained denoising model from [here](https://1drv.ms/u/s!Aj4IQl4ug0_9gj4TTqVW1JhhHG5f) and put it into the "checkpoints/SAGAN" folder

- Prepare your test set with the provided python script
```bash
#make a directory inside the root SAGAN folder
mkdir dicoms
#then put all your low dose CT images of dicom format into this folder and run
python pre_process.py
#all your test images would now be saved as uint16 png format inside folder datasets/experiment/test
#note: in order to use the python script, make sure you have the follwing packages installed
#opencv, pydicom, numpy, h5py
```
- Test the model:
```bash
DATA_ROOT=./datasets/experiment name=SAGAN which_direction=AtoB phase=test th test.lua
#the results are saved in result/SAGAN/latest_net_G_test/result.h5
```
- Display the result with a specific window, e.g. abdomen. Window type can be changed in `opt` in post_process.py
```bash
python post_process.py
```
Now you can view the result by open the html file:result/SAGAN/latest_net_G_test/index.html

### Citations
If you find it useful and are using the code/model provoided here in a publication, please cite our paper:

	@article{yi2017sharpness,
	  title={Sharpness-aware Low dose CT denoising using conditional generative adversarial network},
	  author={Yi, Xin and Babyn, Paul},
	  journal={arXiv preprint arXiv:1708.06453},
	  year={2017}
	}



### Acknowlegements
Code borrows heavily from [pix2pix](https://github.com/phillipi/pix2pix)
