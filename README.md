# gas_monitor

### Goal
Better understand fluctuations in air pollutants arising from natural gas operations:
- Natural gas (a mix of gases)
- Methane (making up 80%–95% of natural gas)
- CO2 (combustion output of burning natural gas)
- CO (combustion output of burning natural gas with insufficient oxygen)
- NOx (combustion by-product output of burning natural gas)
- Ammonia (used for emission control to reduce NOx)
- Formaldehyde

### Requirements

The basic setup of this air system is:
- A monitor made up of sensors connected to a Raspberry Pi device running client code
- Web server to receive and display measurements
- Cloud sharing program

While the sensors react very fast, they are not exclusively sensitive to just 
one type of gas. Therefore, readings might be skewed by other gases. 

### More info

Natural gas is a fossil fuel composed almost entirely of methane, but also contains other hydrocarbon gases, including ethane, propane, butane and pentane. It also commonly includes varying amounts of other higher alkanes, and sometimes a small percentage of carbon dioxide, nitrogen, hydrogen sulfide, or helium. Natural gas that is derived from shale gas could include other chemical used in the extraction process of the gas. If mixed with biogas or landfill gas, it can also contain acids and other corrosive substances.

In order to assist in detecting leaks, an odorizer is added to the otherwise colorless and almost odorless natural gas. The odor has been compared to the smell of rotten eggs, due to the added tert-Butylthiol (t-butyl mercaptan). Sometimes, a related compound, thiophane, may be used in the mixture. These additives are also a deferent for humans to inhale the gas. The additives themselves are irritants that can cause nausea in humans, and have more severe health effects with prolonged exposure to the skin, eyes, kidneys, lungs and liver.

Natural gas extraction also produces radioactive isotopes of polonium (Po-210), lead (Pb-210) and radon (Rn-220). Radon is a gas with initial activity from 5 to 200,000 becquerels per cubic meter of gas. It decays rapidly to Pb-210 which can build up as a thin film in gas extraction equipment.

[Project notes](https://docs.google.com/document/d/1aLgA85S5O9_SXOJqAhFqrD8NQ2f40Iqx_LMBxXcsqhk)

[Formulas to convert raw data into ppm gas readings](https://docs.google.com/spreadsheets/d/1bb9lcmV_HsYXKDZiz5pghnakAcYF63pO5d78DDjXMT4/edit?usp=sharing)

[Components for the gas sensor device](https://docs.google.com/spreadsheets/d/18XvdZh5N7-iELkv8ZHe7yIzBQmGSkL3IdELiQ5KsU-c/edit?usp=sharing)

https://www.gofundme.com/gas-monitor-project

https://raspberry-gas-monitor.weebly.com/

http://www.protectplayanow.org/
