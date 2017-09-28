import cv2
import h5py
import os
import errno
import numpy as np
import dicom


def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

root = './dicoms'

output_root = './test'

mkdir_p(output_root)


count = 0

for (dirpath, dirname, filelist) in os.walk(root):
	for filename in filelist:
		# if ".dcm" in filename.lower():  # check whether the file's DICOM

		dicom_raw = dicom.read_file(os.path.join(dirpath,filename))
		img_raw = dicom_raw.pixel_array

		mask = img_raw == img_raw.min()
		img_raw[mask] = 0

		assert(img_raw.min()>=0)


		img_out = np.array([np.tile(np.concatenate((img_raw,img_raw),axis=1), [1,1]) for i in xrange(3) ])
		img_out = np.transpose(img_out, [1,2,0])*22
		# print(img_out.shape)
		output_filename = '%7.7d.png' % count
		cv2.imwrite(os.path.join(output_root, output_filename), img_out.astype(np.uint16))
		count += 1


print('%d files in the folder' % count)