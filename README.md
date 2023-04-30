# TSETMC-SCRAPER

This library allows users to obtain data from the [tsetmc](http://tsetmc.com) website, and it is separated into 5 subcomponents, each serving a specific purpose.

## Installation

To install this library, simply use the following command:

`pip install git+https://github.com/mmfarahmand/tsetmc-scraper`

## Usage

- **Symbol:** Enables users to work with the main symbol page and live data, such as [this page](http://www.tsetmc.com/loader.aspx?ParTree=151311&i=43362635835198978).
- **Market Watch:** Allows users to access data visible on the [market watch page](http://www.tsetmc.com/Loader.aspx?ParTree=15131F).
- **Day Details:** Provides users with detailed information on a single day's history for a given symbol, as seen on [this page](http://cdn.tsetmc.com/History/43362635835198978/20221029).
- **Market Map:** Returns data that is visible on the [market map page](http://main.tsetmc.com/marketmap).
- **Group:** Retrieves a list of available symbol groups.

## Error Handling

Tsetmc may sometimes return a 403 error, in which case you should try again.

## Credits

Credit for the core functionality of this library goes to [this repository](https://github.com/mahs4d/tsetmc-api). I have simply made my own changes and modifications for personal use.
