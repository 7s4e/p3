"""
Constants Module

This module provides mappings for credit ratings and date formats.
"""


CREDIT_RATINGS = {
    "S&P": {
        "AAA": 1,                           # Highest credity quality
        "AA+": 2, "AA": 3, "AA-": 4,        # Very high credity quality
        "A+": 5, "A": 6, "A-": 7,           # High credity quality
        "BBB+": 8, "BBB": 9, "BBB-": 10,    # Good credity quality
        "BB+": 11, "BB": 12, "BB-": 13,     # Speculative
        "B+": 14, "B": 15, "B-": 16,        # Highly speculative
        "CCC+": 17, "CCC": 18, "CCC-": 19,  # Substantial credit risk
        "CC": 20,                           # Very high levels of credit risk
        "C": 21,                            # Near default
        "D": 22                             # Default
    },
    "Moody's": {
        "Aaa": 1,                            # Highest credit quality
        "Aa1": 2, "Aa2": 3, "Aa3": 4,        # Very high credit quality
        "A1": 5, "A2": 6, "A3": 7,           # High credit quality
        "Baa1": 8, "Baa2": 9, "Baa3": 10,    # Good credit quality
        "Ba1": 11, "Ba2": 12, "Ba3": 13,     # Speculative
        "B1": 14, "B2": 15, "B3": 16,        # Highly speculative
        "Caa1": 17, "Caa2": 18, "Caa3": 19,  # Substantial credit risk
        "Ca": 21,                            # Near default
        "C": 22                              # Default
    },
    "Fitch": {
        "AAA": 1,                         # Highest credit quality
        "AA+": 2, "AA": 3, "AA-": 4,      # Very high credit quality
        "A+": 5, "A": 6, "A-": 7,         # High credit quality
        "BBB+": 8, "BBB": 9, "BBB-": 10,  # Good credit quality
        "BB+": 11, "BB": 12, "BB-": 13,   # Speculative
        "B+": 14, "B": 15, "B-": 16,      # Highly speculative
        "CCC": 18,                        # Substantial credit risk
        "CC": 20,                         # Very high levels of credit risk
        "C": 21,                          # Near default
        "D": 22                           # Default
    }
}

DATE_FORMATS = {
    # Default fallback
    "default": "%Y-%m-%d %H:%M:%S",

    # Year-First
    "yyyy-mm-dd": "%Y-%m-%d",
    "yyyy/mm/dd": "%Y/%m/%d",
    "yyyy.mm.dd": "%Y.%m.%d",
    "yyyymmdd": "%Y%m%d",

    # Day-First
    "dd-mm-yyyy": "%d-%m-%Y",
    "dd/mm/yyyy": "%d/%m/%Y",
    "dd.mm.yyyy": "%d.%m.%Y",
    "ddmmyyyy": "%d%m%Y",
    "d Month yyyy": "%d %B %Y",   # e.g., 1 July 2025
    "d Mon yyyy": "%d %b %Y",     # e.g., 1 Jul 2025

    # Month-First
    "mm-dd-yyyy": "%m-%d-%Y",
    "mm/dd/yyyy": "%m/%d/%Y",
    "mm.dd.yyyy": "%m.%d.%Y",
    "mmddyyyy": "%m%d%Y",
    "Month d, yyyy": "%B %d, %Y",  # e.g., July 1, 2025
    "Mon d, yyyy": "%b %d, %Y",    # e.g., Jul 1, 2025

    # Timestamps with Time
    "yyyy-mm-dd hh:mm:ss": "%Y-%m-%d %H:%M:%S",
    "yyyy-mm-dd hh:mm": "%Y-%m-%d %H:%M",
    "yyyy/mm/dd hh:mm:ss": "%Y/%m/%d %H:%M:%S",
    "yyyy/mm/dd hh:mm": "%Y/%m/%d %H:%M",
    "mm/dd/yyyy hh:mm:ss": "%m/%d/%Y %H:%M:%S",
    "dd/mm/yyyy hh:mm:ss": "%d/%m/%Y %H:%M:%S",

    # ISO 8601 Variants
    "iso8601": "%Y-%m-%dT%H:%M:%S",
    "iso8601z": "%Y-%m-%dT%H:%M:%SZ"
}
