

class Reference:
    def __init__(self):
        self.lu_exchanges = {
            'A': 'AMEX (NYSE MKT)',
            'B': 'NASDAQ OMX BX (Boston)',
            'C': 'National Stock Exchange (Cincinnati)',
            'D/1': 'NASD ADF (FINRA)',
            'E': 'Market Independent (SIP - Generated)',
            'I': 'ISE (International Securities Exchange)',
            'J': 'DirectEdge A',
            'K': 'DirectEdge X',
            'M': 'Chicago',
            'N': 'NYSE',
            'O': 'Instinct',
            'P': 'ARCA (formerly Pacific)',
            'S': 'Consolidated Tape System',
            'T/Q': 'NASDAQ',
            'V': 'IEX',
            'W': 'CBOE',
            'X': 'NASDAQ OMX PSX (Philadelphia)',
            'Y': 'BATS Y-Exchange, Inc',
            'Z': 'BATS'
        }
        self.lu_sales_conditions = {
            'A': 'Regular Way',
            'B': 'Bunched',
            'C': 'Cash Sale',
            'D': 'Next-day Settlme Only',
            'E': 'NYSE Direct+',
            'F': 'Intermarket Sweep Order',
            'G': 'Bunched Sold',
            'H': 'Price Variation Trade',
            'I': 'Odd Lot Trade',
            'J': 'Rule 127 Trade',
            'K': 'Rule 155 Trade',
            'L': 'Sold Last',
            'M': 'Market Center Official Closing Price',
            'N': 'Next Day',
            'O': 'Market Center Opening Price',
            'P': 'Prior Reference Price',
            'Q': 'Market Center Official Opening Price',
            'R': 'Seller',
            'S': 'Split Trade',
            'T': 'Pre- and Post-Market Close Trades',
            'U': 'Out of Sequence After-hours',
            'V': 'Contingent Trade',
            'W': 'Average Price Trades',
            'X': 'Cross Trade',
            'Y': 'Yellow Flag Regular Trade',
            'Z': 'Sold Out of Sequence',
            '2': 'Stopped Stock Sold Last',
            '4': 'Derivatively Priced',
            '5': 'Market Center Reopening Trade',
            '6': 'Market Center Closing Trade',
            '7': 'Qualified Contingent Trade',
            '8': 'Trade Cancelled',
            '9': 'Correct Consolidated Close Price per the Listing Market'

        }
        self.lu_correction_indicator = {
            '00': 'Regular trade that was not corrected',
            '1': 'Original trade was later corrected',
            '7': 'Trade cancelled due to error',
            '8': 'Trade cancelled',
            '9': 'Trade cancelled due to symbol correction',
            '10': 'Cancel record',
            '11': 'Error record',
            '12': 'Correction record'
        }
