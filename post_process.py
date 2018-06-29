import cv2
import h5py
import os
import numpy as np
import argparse
from tqdm import tqdm
from util import HTML


def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)



def get_window_size(window_type):
	if window_type == 'lung':
		center = -700;
		width = 1500;
	elif window_type == 'abdomen':
		center = 40
		width = 400
	elif window_type == 'bone':
		center = 300
		width = 2000
	else:
		raise ValueError("window type not recognized, expect 'lung|abdomen|bone") 
	return center, width
	

def transfer2window(input, window_type):
	center, width = get_window_size(window_type)

	dicom_raw_tmp = input.astype(np.float32) - 1024
	dicom_raw = dicom_raw_tmp[:,:,1];
	dicom_window = ((dicom_raw  -(center-0.5))/(width-1)+0.5)*255;


	dicom_window[dicom_raw<=center-0.5-(width-1)/2] = 0;
	dicom_window[dicom_raw>center-0.5+(width-1)/2] = 255;

	dicom_window.astype(np.uint8)

	return dicom_window




parser = argparse.ArgumentParser(description='extract images from .h5 file')
parser.add_argument('--window', help='window to display the image', required=True)
parser.add_argument('--results_dir', default='./results', help='folder of the results')
parser.add_argument('--name', type=str, default='SAGAN', help='experiment_name')
parser.add_argument('--which_epoch', type=str, default='latest', help='which epoch to use for evaluation')
parser.add_argument('--web_dir', help='root path to put the generated html file', default='.')


opt = parser.parse_args()



def post_process(input_root, target_root, output_root, opt):
	print('start post-processing ...')
	f = h5py.File(result_file_name, 'r')
	folder_dic = {'input': input_root, 'output': output_root, 'target': target_root }

	for i in tqdm(range(len(f.keys()))):
		group_key = list(f.keys())[i]
		name_lists = group_key.split('_')

		output_type = name_lists[1]
		filename = name_lists[2]

		img = np.array(f.get(group_key))
		img = img/22*65535
		img = np.transpose(img.astype(np.uint16), (1,2,0))

		if opt.window != 'none':
			img = transfer2window(img, opt.window)


		cv2.imwrite(os.path.join(folder_dic[output_type], filename), img)



	webpage = HTML(opt.web_dir, 'Experiment name = SAGAN', reflesh=1)
	webpage.add_header('SAGAN test results {} window'.format(opt.window))
	ims, txts, links = [], [], []
	for i in range(len(f.keys())):
		group_key = list(f.keys())[i]
		name_lists = group_key.split('_')
		filename = name_lists[2]

		for key, vp in folder_dic.items():
			ims.append(os.path.join(vp, filename))
			txts.append('{}: {}'.format(key, filename))
			links.append(os.path.join(vp, filename))

		webpage.add_images(ims, txts, links, width=256)
		ims, txts, links = [], [], []

	webpage.save('index.html')


	f.close()
	print('post-processing finished')



if __name__=='__main__':
	result_root = os.path.join(opt.results_dir, opt.name,  '{}_net_G_test'.format(opt.which_epoch))

	result_file_name = os.path.join(result_root,  'result.h5' );
	output_root = os.path.join(result_root,  'output' );
	input_root = os.path.join(result_root,  'input' );
	target_root = os.path.join(result_root,  'target' );

	index_file = os.path.join(result_root,'index.html')

	mkdir_p(output_root)
	mkdir_p(input_root)
	mkdir_p(target_root)

	post_process(input_root, target_root, output_root, opt)
