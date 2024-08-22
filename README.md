**Version 1.0**

This was made to view and manipulate spectrum data files (.ssm) taken using the Stellar Pro software by StellarNet Inc. While StellarPro can open multiple saved spectrum files and overlay them on the same plot, it does not seem to have ways of manipulating this data in useful ways - like setting custom axes ranges, and rescaling spectra to a 0-1 scale. The current version can do both of these things, for multiple spectrum files at the same time. More useful manipulations, like subtracting one spectrum from another, doing baseline subtraction, etc. will be added in as necessary.

To access the GUI that lets you do these manipulations, run `Silver_Nova_Spectrum_Reader.py`.

`reader.py` is the initial text-based version made before the GUI. With this, 2 files can be plotted together, but file paths must be hard-coded and changed each time.

The GUI code `Silver_Nova_Spectrum_Reader.py` is based on `GUI_template.py` which has the same functionality but for importing CSV files. The `GUI_template.py` file can be tested with the files `template_test_data.csv` and `template_test_data_2.csv`.

`NOVA_Spectra_reader.nb` is a Mathematica notebook that was the precursor to `reader.py`.