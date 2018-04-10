% dicom_read_ac -- transfer the hunsfield units to attenuation coefficents.
%   Paras:
%   @file_path        : path to the dicom image
%   Author: Xin Yi (xiy525@mail.usask.ca)
%   Date  : 03/22/2017

function im_ac = dicom_read_ac(file_path)
    im_dicom_raw = dicomread(file_path);
    info = dicominfo(file_path);
    
    mask = im_dicom_raw == info.PixelPaddingValue;

    im_dicom_recaled = im_dicom_raw*info.RescaleSlope + info.RescaleIntercept;
    %0.17 is the attenuation coef (1/cm) of water at 100 keV

    im_ac = 0.17*double(im_dicom_recaled) /1000 + 0.17;
    
    im_ac(mask) = 0;
    
    im_ac(im_ac<0) = 0;
end