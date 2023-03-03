Formatting Notes:
Windographer file is taken from the export menu, Time Series. The file must include:
  a timestamp, 10min increments
  Spd at mast height
  Dir
  Tmp
  Pres

  On export in the windographer file, the header should also be excluded. (one of the options in the export menu)

Windfarmer file is the whole farm binned production values (.fpm file)

Losses should be adjusted based on what is needed in the ini file

If you would like to produce an 8760, place the windographer file in the tmy-inputs folder and the windfarmer.fpm file and losses in the inputs folder

if you would like to produce a power time series, place all 3 files in the inputs folder.

The outputs will be exported to the exports folder
