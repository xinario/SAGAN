clc;
clear;
close all;

%X-ray source intensity N_0, the lower number the higher noise
xray_influx = 30000;
%window type, supports lung, abdomen, bone
display_window_type = 'bone';

im_ac = dicom_read_ac('000048.dcm');
im = ac2window(im_ac, display_window_type);



im_ac_noise = add_poisson_noise(im_ac, xray_influx);
im_noise = ac2window(im_ac_noise, display_window_type);

imshowpair(im, im_noise, 'montage');

































