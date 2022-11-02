cscript

/*
import delimited https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv
desc
rename v83 confirmed
drop if missing(fips)
save covid19_adj, replace

use ../data/covid19_adj.dta, clear

spshape2dta ../cb_2018_us_county_500k/cb_2018_us_county_500k.shp,  saving(usacounties) replace
use usacounties.dta, clear
generate fips = real(GEOID)
save usacounties.dta, replace	

merge 1:1 fips using ../usacounties.dta
keep if _merge == 3
drop _merge

import delimited https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv

generate fips = state*1000 + county
save census_popn, replace

merge 1:1 fips using census_popn
keep if _merge == 3

generate confirmed_adj = 100000*(confirmed/popestimate2019)
label var confirmed_adj "Cases per 100,000"
format %16.0fc confirmed_adj

save covid19_adj, replace
*/

use ./data/covid19_adj, replace
grmap, activate
drop if province_state == "Alaska" | province_state == "Hawaii"
spset, modify shpfile(usacounties_shp)
grmap confirmed_adj, clnumber(7)
