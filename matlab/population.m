fplot(@(x) 669.310000/(1+6.416.*exp(-0.0168833.*(x-1910))));
xlim([1900, 2100]);
hold on
yearhistorical = linspace(1910, 2020, 12);
pophistorical = [92.228531 106.021568 123.202660 132.165129 151.325798 179.323175 203.211926 226.545805 248.709873 281.421906 308.745538 331.449281];
scatter (yearhistorical, pophistorical, 'r');
xlabel('Year');
ylabel('US Population in Millions');
title('Population of US vs. Year');