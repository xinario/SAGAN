import cv2
import h5py
import os
import errno
import numpy as np
import argparse


def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise



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
parser.add_argument('-w','--window', help='window to display the image', required=True)

args = vars(parser.parse_args())


opt = {
	'name': 'SAGAN',
	'window_type': args['window'], #lung, abdomen, bone, none
	'results_dir': './results',
	'which_epoch': 'latest'

}


result_root = os.path.join(opt['results_dir'], opt['name'], opt['which_epoch'] + '_net_G_test')

result_file_name = os.path.join(result_root,  'result.h5' );
output_root = os.path.join(result_root,  'output' );
input_root = os.path.join(result_root,  'input' );
target_root = os.path.join(result_root,  'target' );

index_file = os.path.join(result_root,'index.html')

mkdir_p(output_root)
mkdir_p(input_root)
mkdir_p(target_root)



f = h5py.File(result_file_name, 'r')




for i in xrange(len(f.keys())):
	group_key = f.keys()[i]
	name_lists = group_key.split('_')

	output_type = name_lists[1]
	filename = name_lists[2]

	img = np.array(f.get(group_key))
	img = img/22*65535
	img = np.transpose(img.astype(np.uint16), (1,2,0))

	if opt['window_type'] != 'none':
		img = transfer2window(img, opt['window_type'])


	if output_type == 'output':
		cv2.imwrite(os.path.join(output_root, filename), img)
	elif output_type == 'target':
		cv2.imwrite(os.path.join(target_root, filename), img)
	elif output_type == 'input':
		cv2.imwrite(os.path.join(input_root, filename), img)


with open(index_file, 'w') as the_file:
	the_file.write('<table style="text-align:center;">\n')

	for i in xrange(len(f.keys())/3):
		group_key = f.keys()[i]
		name_lists = group_key.split('_')
		filename = name_lists[2]

		the_file.write('<tr><td>Image #</td><td>input</td><td>target</td><td>sagan</td></tr>\n')
		the_file.write('<tr>')
		the_file.write('<td>' + filename + '</td>')
		the_file.write('<td><img src="./input/' + filename + '"/></td>')
		the_file.write('<td><img src="./target/' + filename + '"/></td>')
		the_file.write('<td><img src="./output/' + filename +'"/></td>')
		the_file.write('</tr>\n')



	the_file.write('</table>')



f.close()




