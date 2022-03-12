meanLogIncome = log(53383.18);
sdLogIncome = sqrt(2*log(53383.18/34612.04));
totalIncomes = [];
meetsThreshold2022 = 0;
meetsThreshold2050 = 0;
meetsThreshold2100 = 0;
incomeThreshold2022 = 21252;
multiplier2050 = 1.890421175;
multiplier2100 = 2.406898457;
for i = 1:10000
    income = normrnd(meanLogIncome, sdLogIncome);
    if income <= log(incomeThreshold2022*multiplier2100)
        meetsThreshold2100 = meetsThreshold2100 + 1;
    end
    if income <= log(incomeThreshold2022*multiplier2050)
        meetsThreshold2050 = meetsThreshold2050 + 1;
    end
    if income <= log(incomeThreshold2022)
        meetsThreshold2022 = meetsThreshold2022 + 1;
    end
    totalIncomes = [totalIncomes, income];

end
histogram(totalIncomes, 100);
hold on;
xline(log(incomeThreshold2022), 'r', 'Linewidth', 2.0);
xline(log(incomeThreshold2022 * multiplier2050), 'g', 'Linewidth', 2.0);
xline(log(incomeThreshold2022 * multiplier2100), 'm', 'Linewidth', 2.0);
xlabel('ln(Income)');
ylabel('Frequency');
title('Simulated 10000 Income Earners');



