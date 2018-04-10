% get_ct_window_size -- get the display window size.
%   Paras:
%   @type        : window type
%   Author: Xin Yi (xiy525@mail.usask.ca)
%   Date  : 03/22/2017
function [center, width] = get_ct_window_size(type)

if strcmp(type, 'lung')
    center = -700;
    width = 1500;
elseif strcmp(type, 'abdomen')
    center = 40;
    width = 400;
elseif strcmp(type, 'bone')
    center = 300;
    width = 2000;
elseif strcmp(type, 'narrow')
    center = 40;
    width = 80;
end