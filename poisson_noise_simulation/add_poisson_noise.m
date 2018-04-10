% add_poisson_noise -- add poisson noise to a ct slice.
%   Paras:
%   @im        : attenuation coefficients of a single ct slice  
%   @N0        : x-ray source influx
%   Author: Xin Yi (xiy525@mail.usask.ca)
%   Date  : 03/22/2017
function im_noise = add_poisson_noise(im_ac, N0)
dtheta = 0.3;
dsensor = 0.1;
D = 500;
sinogram_in = fanbeam(im_ac, D, 'FanSensorSpacing', dsensor, 'FanRotationIncrement', dtheta);

%small number >0 that reflects the smallest possible detected photon count
epsilon = 5; 

% to detector count coefficients unit is cm-1
sinogramCT = N0 * exp(-sinogram_in*0.0625);

% add poison noise
sinogramCT_noise = poissrnd(sinogramCT);

sinogram_out = -log(sinogramCT_noise/N0)/0.0625;

idx = isinf(sinogram_out);
sinogram_out(idx) = -log(epsilon/N0)/0.0625;




im_noise = ifanbeam(sinogram_out, D, 'FanSensorSpacing', dsensor, 'OutputSize', max(size(im_ac)));

