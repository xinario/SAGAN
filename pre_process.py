import cv2
import h5py
import os
import errno
import numpy as np
import dicom
import argparse

def mkdir_p(path):
#function  by @tzot from stackoverflow
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise





parser = argparse.ArgumentParser(description='create test images from raw dicom')
parser.add_argument('-s','--sequence', help='whether store output images in sequence according to the z axis value', required=True)
parser.add_argument('-i','--input', help='input folder where raw dicoms are stored', required=True)
parser.add_argument('-o','--output', help='output folder where test images are stored', required=True)

args = vars(parser.parse_args())



root = args['input']
output_root = args['output']
mkdir_p(output_root)




sequence = []
for (dirpath, dirname, filelist) in os.walk(root):
	for filename in filelist:
		if not filename.startswith('._'):
			# if ".dcm" in filename.lower():  # check whether the file's DICOM

			dicom_raw = dicom.read_file(os.path.join(dirpath,filename))
			sequence.append(int(dicom_raw.SliceLocation))


if args['sequence'] == '1':
	idx = [i[0] for i in sorted(enumerate(sequence), key=lambda s:s[1])]
else:
	idx = [i for i in range(len(sequence))]


count = 0
for (dirpath, dirname, filelist) in os.walk(root):
	for filename in filelist:
		if not filename.startswith('._'):
			# if ".dcm" in filename.lower():  # check whether the file's DICOM

			dicom_raw = dicom.read_file(os.path.join(dirpath,filename))
			img_raw = dicom_raw.pixel_array

			mask = img_raw == img_raw.min()
			img_raw[mask] = 0

			assert(img_raw.min()>=0)


			img_out = np.array([np.tile(np.concatenate((img_raw,img_raw),axis=1), [1,1]) for i in xrange(3) ])
			img_out = np.transpose(img_out, [1,2,0])*22
			# print(img_out.shape)
			output_filename = '%7.7d.png' % idx.index(count)
			cv2.imwrite(os.path.join(output_root, output_filename), img_out.astype(np.uint16))
			count += 1


print('%d files in the folder' % len(sequence))


