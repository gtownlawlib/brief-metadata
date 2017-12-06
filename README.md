# Brief Metadata
Command line application using CourtListener API to retrieve case metadata from docket number and populate a Google Sheet

## CourtListener
This project stemmed from the desire to automatically populate a spreadsheet with additional metadata by entering only the docket number and jurisdiction.

The best available data to obtain this metadata was the **[CourtListener REST API](https://www.courtlistener.com/api/rest-info/)**, which is what this application uses. You'll need to obtain a [CourtListener access token](https://www.courtlistener.com/sign-in/?next=/api/rest-info/) and then add it to the appropriate line in brief-metadata.py before using this script:

`# Set Authentication Token`

`token = [YOUR_COURTLISTENER_ACCESS_TOKEN]`

## Google Sheets
The application uses the [Google Sheets API](https://developers.google.com/sheets/api/) and the [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/start/installation) to populate a Sheet, so the code in gsheets.py follows closely on the sample provided by Google at (https://developers.google.com/sheets/api/quickstart/python).

You will first need to turn on the Google Sheets API by following the Step 1 instructions in [Google's Python Quickstart tutorial](https://developers.google.com/sheets/api/quickstart/python). The client_secret.json file you obtain at the end of this process should be placed in the same folder as this application.

You also need to add the ID for your sheet to the appropriate line in gsheets.py:

`APPLICATION_NAME = [YOUR_GOOGLE_API_APPLICATION_NAME]`

The first time you run the application, you will be provided a URL to visit in your browser to grant the script access to your sheet. This will provide you an access token to paste in the command line prompt, which will create the access token the application will use from then on to log into your Google Sheet.

The script expects a spreadsheet with the following columns (in this order):
1. **pdf** (The source PDF number; see the Using the Application section below for more info about the PDF Number value)
2. **docket** (The docket number of the case)
3. **year** (The year the case was decided)
4. **name** (The short version of the case name, as used in citations)
5. **full** (The long version of the case name)

You can, of course, use whatever Sheet format you wish, but you'll need to adapt gsheets.py to your needs as well as rewrite brief-metadata.py to find the metadata fields you wish to use.

## Using the application
brief-metadata.py expects up to three arguments, the first two of which are required.
1. **PDF Number**
2. **Docket Number**
3. **Court Code** (optional)

### PDF Number
This is a local convention we use to identify the source document we're obtaining metadata for, which in our case is a digitized court brief. The PDF Number is our in-house unique identifier for these briefs.

### Docket Number
The docket number of the case we want to obtain metadata for.

If there are any spaces in your docket number, be sure to either escape them with a backslash or put the entire docket number in quotation marks.

The formatting of docket numbers across media varies wildly, so be prepared to add/remove spaces/dashes etc. multiple times if you don't get a matching result.

### Court Code
This optional argument specifies the jurisdiction/court of the case. For this to work, you'll need to use the same format CourtListener uses for its court codes in the abbreviation column of its list of [Available Jurisdictions](https://www.courtlistener.com/api/jurisdictions/).

### Running the Script
`$ python3 brief-metadata.py 34 70-18 scotus`

This command will retrieve metadata for Roe v. Wade. The metadata will be shown onscreen and you will be asked to confirm that's the case you wish to add. If you respond 'y,' a new row will be created in your Google Sheet for PDF #34 that includes the docket number (70-18), year of decision (1973), short case name (Roe v. Wade), and long case name (Roe et al. v. Wade, District Attorney of Dallas County.). _See the Google Sheets section above for more info about the expected columns in your Google Sheet._

If you do not include a court code argument, the application will search all jurisdictions. If only one matching docket number is found, that case will be displayed and you'll be asked to confirm that it's the one you want to enter. If more than one match is found, a list of all matches will be displayed along with their court codes, and you'll be asked to run your command again with the court code corresponding to the case you want.
