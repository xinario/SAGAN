import cv2
import os
import numpy as np
import pydicom
import argparse
import glob
from tqdm import tqdm

def mkdir_p(path):
    if not os.path.exists(path):
        os.makedirs(path)





parser = argparse.ArgumentParser(description='create test images from raw dicom')
parser.add_argument('--input', help='input folder where raw dicoms are stored', required=True)
parser.add_argument('--output', help='output folder where test images are stored', required=True)

args = vars(parser.parse_args())







def pre_process(root_in, root_out):
	sequence = []
	filelist = glob.glob("{}/*.dcm".format(root_in))
	print('%d files in the folder, start preprocessing' % len(filelist))

	for filename in filelist:
		dicom_raw = pydicom.dcmread(filename)
		sequence.append(int(dicom_raw.SliceLocation))


	idx = [i[0] for i in sorted(enumerate(sequence), key=lambda s:s[1])]



	count = 0
	for filename in tqdm(filelist):
		dicom_raw = pydicom.dcmread(filename)
		img_raw = dicom_raw.pixel_array.copy()

		mask = img_raw == img_raw.min()
		img_raw[mask] = 0

		assert(img_raw.min()>=0)


		img_out = np.array([np.tile(np.concatenate((img_raw,img_raw),axis=1), [1,1]) for i in range(3) ])
		img_out = np.transpose(img_out, [1,2,0])*22
		# print(img_out.shape)
		output_filename = '%7.7d.png' % idx.index(count)
		cv2.imwrite(os.path.join(root_out, output_filename), img_out.astype(np.uint16))
		count += 1
		
	print('pre-processing finished')




if __name__=='__main__':

	root_in = args['input']
	root_out = args['output']
	mkdir_p(root_out)
	pre_process(root_in, root_out)
