%% close and clear workspace
close all;
clear;
clc;
%% Initialize Figure
f=figure(1);
%% Choose Case to be analyzed
case_=8;

if case_ == 1
 addpath('Gmapping');
 dinfo = dir('Gmapping/*.mat');
elseif case_ == 2
 addpath('Google_cartographer');
 dinfo = dir('Google_cartographer/*.mat');  
elseif case_ == 3
 addpath('Hector_slam');
 dinfo = dir('Hector_slam/*.mat'); 
elseif case_ == 4
 addpath('Speed_0.75');
 dinfo = dir('Speed_0.75/*.mat');
elseif case_ == 5
 addpath('Speed_1');
 dinfo = dir('Speed_1/*.mat'); 
elseif case_ == 6
 addpath('Speed_1.5');
 dinfo = dir('Speed_1.5/*.mat');
elseif case_ == 7
 addpath('Hector_test');
 dinfo = dir('Hector_test/*.mat');
 elseif case_ == 8
 addpath('Gmapping_test');
 dinfo = dir('Gmapping_test/*.mat');
 elseif case_ == 9
 addpath('Cartographer_test');
 dinfo = dir('Cartographer_test/*.mat');
 
 
end

%% read in relevant data and plot
Colors = lines(length(dinfo));

for K = 1 : length(dinfo)
  thisfilename = dinfo(K).name;  %just the name
  thisdata = load(thisfilename);
  x_data{K}=round(thisdata.x_data,1);
  y_data{K} = thisdata.y_data;
  diff{K} = thisdata.diff;
  erased{K} = thisdata.erased_data;
  end_y_data(K) = y_data{K}(end);
  surface_diff(K)=0;
  difference(K) = 0;
  total_erased_surface(K)=0;
  subplot(2,2,1)
  p(K)=plot(x_data{K},y_data{K}, 'Color', Colors(K,:), 'LineWidth', 2);
  xlabel('time [s]')
  ylabel('Occupied Surface [m]')
  grid on
  
  %set title for each case
    if case_ == 1
        title('Total Occupied Surface of Gmapping')
    elseif case_ == 2
        title('Total Occupied Surface of Google Cartographer')  
    elseif case_ == 3
        title('Total Occupied Surface of Hector Slam')
    elseif case_ == 4
        title('Total Occupied Surface of Velocity=0.75 ')
    elseif case_ == 5
        title('Total Occupied Surface of Velocity=1 ')
    elseif case_ == 6
        title('Total Occupied Surface of Velocity=1.5')
    elseif case_ == 7
        title('Total Occupied Surface Hector test')
    elseif case_ == 8
        title('Total Occupied Surface Gmapping test')
    elseif case_ == 9
        title('Total Occupied Surface Cartographer test')
    end
    
  
  hold on
  clr = Colors(K,:);
  for i = 1:length(diff{K})
      if diff{K}(i)< 0
         surface_diff(K) = surface_diff(K)+abs(diff{K}(i)); 
         ver=xline(x_data{K}(i),'color',clr,'linestyle','-.');
         difference(K) = difference(K)+1;
         [~, ~,V(K)]=find(x_data{K}(i));
         time_instance(K,difference(K)) = V(K);
         ver.LabelVerticalAlignment = 'bottom';
         ver.LabelHorizontalAlignment = 'center';
         ver.LabelOrientation = 'aligned';
         
      end
  end
  hold on
  erased_surface{K}(1) = 0;
  for j =2:length(erased{K})
    erased_surface{K}(j) = erased_surface{K}(j-1) + erased{K}(j);
    total_erased_surface(K) = total_erased_surface(K) + erased{K}(j);
  end
  subplot(2,2,2)
  p2(K)=plot(x_data{K},[0 erased{K}],'Color', Colors(K,:), 'LineWidth', 1.5);
    if case_ == 1
        title('Method B of Gmapping')
    elseif case_ == 2
        title('Method B of Google Cartographer')  
    elseif case_ == 3
        title('Method B of Hector Slam')
    elseif case_ == 4
        title('Method B of Velocity=0.75 ')
    elseif case_ == 5
        title('Method B of Velocity=1 ')
    elseif case_ == 6
        title('Method B of Velocity=1.5')
    elseif case_ == 7
        title('Method B Hector test')
    elseif case_ == 8
        title('Method B Gmapping test')
    elseif case_ == 9
        title('Method B Cartographer test')
    end
  hold on
  
  grid on
end
    if case_== 1||case_==2||case_==3
        legend(p,{'velocity=0.75','velocity=1','velocity=1.5'},'location','southeast')
        legend(p2,{'velocity=0.75','velocity=1','velocity=1.5'},'location','southeast')    
    elseif case_==4 || case_ == 5 || case_ == 6 
        legend(p,{'Google Cartographer','Gmapping', 'Hector Slam'});
        legend(p2,{'Google Cartographer','Gmapping', 'Hector Slam'});
    elseif case_==7 || case_ == 8 || case_ == 9
        legend(p,{'test1','test2','test3','test4','test5'});
        legend(p2,{'test1','test2','test3','test4','test5'});
    end
hold off

%%
T = [end_y_data; difference; surface_diff; total_erased_surface];
% Create the column and row names in cell arrays 
cnames = {'1','2','3','4','5'};
rnames = {'1','2','3','4','5'};
% Create the uitable
t = uitable(f,'Data',T,...
            'ColumnName',cnames,... 
            'RowName',rnames,...
            'ColumnWidth',{93});
pos = get(subplot(2,2,[3,4]),'position');

set(subplot(2,2,[3,4]),'yTick',[]);
set(subplot(2,2,[3,4]),'xTick',[]);
set(t,'units','normalized');
set(t,'position',pos);
    if case_== 1||case_==2||case_==3
        set(t,'ColumnName',{'velocity=0.75','velocity=1','velocity=1.5'});
    elseif case_==4 || case_ == 5 || case_ == 6 
        set(t,'ColumnName',{'Google Cartographer','Gmapping', 'Hector Slam'});
    elseif case_==7 || case_ == 8 || case_ == 9
        set(t,'ColumnName',{'test1','test2','test3','test4','test5'});
    end
set(t,'RowName',{'Total S [m]', 'Occurance [-]','Method A [m]', 'Method B [m]'});
