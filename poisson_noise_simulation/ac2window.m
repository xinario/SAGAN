% ac2window -- rescale the ct slice to a specific window range
%   Paras:
%   @im_ac        : image of attenuation coefficients 
%   @window_type  : dispaly window type
%   Author: Xin Yi (xiy525@mail.usask.ca)
%   Date  : 03/22/2017
function im_dicom = ac2window(im_ac, window_type)
im_dicom_raw = (im_ac - 0.17)/0.17*1000;

[center, width] = get_ct_window_size(window_type);



im_dicom =   uint8(((double(im_dicom_raw) - (center-0.5))/(width-1)+0.5)*255);
im_dicom(im_dicom_raw<=center-0.5-(width-1)/2) = 0;
im_dicom(im_dicom_raw>center-0.5+(width-1)/2) = 255;

end