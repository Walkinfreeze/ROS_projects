map=imread("map2.pgm");
occupied = 0;
free = 0;
% imshow(map);

l_map = logical(map);
imshow(l_map)
for i=1:size(l_map)
    for j=1:size(l_map)
        if l_map(i,j)==0
            occupied = occupied+1;
        else
            free = free + 1;
        end
     end
end

    