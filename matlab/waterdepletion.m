depletionPercent = [];
year = [];
hold on;
for d = 1:100                           %cycling through percent usage
    lastVolume = 129430000000000;
    volume = 129430000000000;
    for y = 2013:5000                  %cycling through years up to year 5000. Note: for some measures, usage is decreased to below replenishment rates for 
                                        %much of the near future (until 3000); these years are not plotted
        if ((volume + replenish(y) - waterusage(y,d)) <0) && (lastVolume>0) %checks for first instance of volume dropping below 0
            year = [year, y-2022]; 
            depletionPercent = [depletionPercent, d];       %last two lines add entries into vectors of % decrease in usage and years until depletion
            volume = volume - 1000000000000000; %done to ensure no further interations such as when volume may dip below 0 but increases again after
        end
        lastVolume = volume;
        volume = volume + replenish(y) - waterusage(y,d); % decreasing water usage to account for next year
    end         
end

plot(depletionPercent, year);

xlabel('Percent Demand Usage of Water');
ylabel('Years until Depletion');
title('Distribution of Years Until Depletion of Aquifer by Percent Water Use');

function p = pop(y) %function that takes year y and returns the population 
    p = 669310000/(1+6.41637*exp(-0.0168833*(y-1910)));
end 

function d = demand(y)
    d = 2/3 * 1996 * 0.057 * pop(y);
end

function w = waterusage(y, d) %function that returns the water supply in some year y with d% water usage
    waterUsage2021 = 4776985806438;
    demand2021 = 25575739705;
    w = d/100 * waterUsage2021 * demand(y)./demand2021;
end

function t = temp(y) %function that returns average temperature in year y
    t = 287.37 + 0.008*(y-2005);
end

function r = replenish(y) %function that returns replenishment rate in year y
    replenish2005 = 4691658250306;
    r = replenish2005.*exp(1/(temp(2005)-1/temp(y)));
end


