#!/usr/bin/env python3
"""
Bond Selection Script
"""
# Standard library imports
from collections import deque
from itertools import product
from math import floor
from scipy.optimize import newton
import pandas as pd

# Local module imports
from modules import Console
from modules import constants as k
from modules import pd_utils as pdu
from modules import utilities as utl


# Tax Rates
TAXABLE_BASE_RATE = 0
TAX_EXEMPT_BASE_RATE = 0
FED_TAX = 0.22
VA_TAX = 0.0575
CAP_GAINS_TAX = 0.15
MAX_CREDIT_RISK = 7
TA_RF_RTN = 0.0401
TE_RF_RTN = 0.0413

# Data Management
CSV_FILENAMES = ["treasury", "cd", "agency", "municipal", "taxable_muni", 
                 "corporate"]
PATH_IN = "/home/bryant/Repositories/p3/in/"
PATH_OUT = "/home/bryant/Repositories/p3/out/"
BND_QTY_REGEX = r'([\d,]+)\(([\d,]+)\)'
HZ_MAPS = {
    "ANNUALLY": {"offset": -12, "periods": 1}, 
    "MONTHLY": {"offset": -1, "periods": 12}, 
    "QUARTERLY": {"offset": -3, "periods": 4}, 
    "SEMI-ANNUALLY": {"offset": -6, "periods": 2}
}

# Given Column Names
CUSIP = "Cusip"
STATE = "State"
DESCRIPTION = "Description"
COUPON_RATE = "Coupon"
COUPON_HZ = "Coupon Frequency"
MATURITY_DATE = "Maturity Date"
NEXT_CALL_DATE = "Next Call Date"
MOODY_RATING = "Moody's Rating"
S_P_RATING = "S&P Rating"
MOODY_STND_ALN = "Moody's Underlying Rating"
S_P_STND_ALN = "S&P Underlying Rating"
BID_PRICE = "Price Bid"
ASK_PRICE = "Price Ask"
BID_YIELD = "Yield Bid"
ASK_YTW = "Ask Yield to Worst"
ASK_YTM = "Ask Yield to Maturity"
BID_QTY = "Quantity Bid(min)"
ASK_QTY = "Quantity Ask(min)"
ATTRIBUTES = "Attributes"

# Applied Column Names
BOND_TYPE = "Bond Type"
ASK_TTL = "Total Ask Available"
ASK_MIN = "Minimum Ask Quantity"
HZ_MAP = "Frequency Map"
CR_SCORE = "Credit Score"
TA_RTN = "Taxable Return"
TE_RTN = "Tax Exempt Return"


def compute_accrued_interest(last_coupon_date: pd.Timestamp, 
                             settlement_date: pd.Timestamp, 
                             coupon_rate: float) -> float:
    Y1, M1, D1 = (last_coupon_date.year, last_coupon_date.month, 
                  last_coupon_date.day)
    Y2, M2, D2 = (settlement_date.year, settlement_date.month, 
                  settlement_date.day)
    if D1 == 31: D1 = 30
    if D2 == 31 and D1 == 30: D2 = 30 
    days = 360 * (Y2 - Y1) + 30 * (M2 - M1) + (D2 - D1)
    return (days / 360) * (coupon_rate / 100) * 1000


def compute_return(dates: list[pd.Timestamp], row: pd.Series, tax: bool
                   ) -> float:
    if dates:
        amounts = list_cashflow_amounts(dates, row, tax)
        cashflows = pd.Series(data=amounts[1:], index=dates[1:])
        xirr = compute_xirr(cashflows)
    else:
        xirr = pd.NA
    return xirr
    

def compute_xirr(cashflow: pd.Series, guess: float = 0.05) -> float:
    def npv(rate):
        t0 = cashflow.index[0]
        total = 0.0
        for date, amount in cashflow.items():
            if pd.isna(rate) or rate <= -1:
                continue  # invalid discount rate
            if pd.isna(date) or pd.isna(amount) or pd.isna(t0):
                continue  # skip missing data
            try:
                years = (date - t0).days / 365.0
                discount = (1 + rate) ** years
                total += amount / discount
            except Exception:
                continue  # catch math errors like invalid exponentiation
        return total

    try:
        return newton(npv, guess)
    except (RuntimeError, OverflowError, ZeroDivisionError, ValueError):
        return pd.NA


def combine_data(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    dfs = process_dataframes(dfs)
    source_dataframes(dfs)
    df = pd.concat(dfs.values(), ignore_index=True)
    df = process_dataframe(df)
    return df


def get_capital_gains_rate(row: pd.Series, purchase_dt: pd.Timestamp, 
                           maturity_dt: pd.Timestamp) -> float:
    hold_period = utl.get_calendar_difference(purchase_dt, maturity_dt).years
    de_minimus_threshold = 0.0025 * hold_period * 100.
    is_ordinary_income = row[ASK_PRICE] < 100. - de_minimus_threshold
    return FED_TAX + VA_TAX if is_ordinary_income else CAP_GAINS_TAX


def get_marginal_tax_rate(row: pd.Series) -> float:
    fed_rate = 0. if row[BOND_TYPE] == "MUNICIPAL" else FED_TAX
    st_rate = (0. 
               if (row[BOND_TYPE] == "TREASURY" or 
                   (pd.notna(row[STATE]) and "VA" in row[STATE])) 
               else VA_TAX)
    return fed_rate + st_rate


def evaluate_bonds(row: pd.Series, settlement: pd.Timestamp) -> pd.Series:
    print(row[DESCRIPTION])
    row = set_returns(row, settlement)
    return row


def find_bonds() -> None:
    settlement = pdu.offset_date(pd.Timestamp.today().normalize(), biz_dys=1)
    df = prepare_data()
    df = df.apply(lambda row: evaluate_bonds(row, settlement), axis=1)
    put_data(df)


def filter_credit(df: pd.DataFrame) -> pd.DataFrame:
    acceptable_risk = df[CR_SCORE].isna() | (df[CR_SCORE] <= MAX_CREDIT_RISK)
    return df[acceptable_risk]


def filter_frequency(df: pd.DataFrame) -> pd.DataFrame:
    interest_calculable = df[COUPON_HZ] != "AT MATURITY"
    return df[interest_calculable]


def filter_returns(df: pd.DataFrame, tax_exempt: bool) -> pd.DataFrame:
    if tax_exempt:
        acceptable_return = df[TE_RTN] > TE_RF_RTN
        df.drop(columns=TA_RTN, inplace=True)
    else:
        acceptable_return = df[TA_RTN] > TA_RF_RTN * (1. - FED_TAX - VA_TAX)
        df.drop(columns=TE_RTN, inplace=True)
    return df[acceptable_return]


def list_cashflow_amounts(dates: list[pd.Timestamp], row: pd.Series, tax: bool
                          ) -> list[float]:
    # Extract Dates
    if len(dates) == 0: return []
    last_coupon = dates[0]
    settlement = dates[1]
    pending_coupons = dates[2:-1] if len(dates) > 3 else []
    redemption = dates[-1]

    # Set Tax Rates
    income_tax = get_marginal_tax_rate(row) if tax else 0.
    cap_gains = (get_capital_gains_rate(row, settlement, redemption) 
                 if tax else 0.)
    
    # Amounts
    purchase_price = row[ASK_PRICE] * 10 + 1
    accr_interest = (0. 
                     if row[COUPON_RATE] == 0. 
                     else compute_accrued_interest(last_coupon, settlement, 
                                                   row[COUPON_RATE]))
    cost = -purchase_price - accr_interest

    period_rate = row[COUPON_RATE] / 100 / row[HZ_MAP]["periods"]
    coupon_payment = period_rate * 1000 * (1 - income_tax)
    coupon_payments = [coupon_payment] * len(pending_coupons)
        
    tax_on_gain = (1000 - min(purchase_price, 1000)) * cap_gains
    redemption = 1000 - tax_on_gain + coupon_payment
        
    return [0., cost] + coupon_payments + [redemption]


def list_cashflow_dates(end_dt: str, settlement_dt: pd.Timestamp, 
                        row: pd.Series) -> list[pd.Timestamp]:
    if pd.isna(row[end_dt]) or row[end_dt] <= settlement_dt:
        return []
    dates = deque()
    coupon_dt = row[end_dt]
    while coupon_dt > settlement_dt:
        dates.appendleft(coupon_dt)
        coupon_dt = pdu.offset_date(coupon_dt, mos=row[HZ_MAP]["offset"])
    dates.appendleft(settlement_dt)
    dates.appendleft(coupon_dt)
    return list(dates)
    

def modify_data(df: pd.DataFrame) -> pd.DataFrame:
    df = set_frequency_map(df)
    df = set_credit_score(df)
    return df


def prepare_data() -> pd.DataFrame:
    dfs = read_files()
    df = combine_data(dfs)
    df = filter_frequency(df)
    df = modify_data(df)
    df = filter_credit(df)
    return df


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = pdu.cast_as_string(df, [CUSIP, STATE, DESCRIPTION, MOODY_RATING, 
                                 S_P_RATING])
    df = pdu.convert_to_number(df, [COUPON_RATE, ASK_PRICE])
    df = pdu.split_columns(df, ASK_QTY, (ASK_TTL, ASK_MIN), BND_QTY_REGEX, 
                           pd.Int64Dtype())
    return df


def process_dataframes(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {
        bond_type: (
            pdu.ensure_column(
                pdu.format_dates(
                    df.drop(
                        columns=[MOODY_STND_ALN, S_P_STND_ALN, BID_PRICE, 
                                 BID_YIELD, ASK_YTW, ASK_YTM, BID_QTY, 
                                 ATTRIBUTES], 
                        errors="ignore"
                    ),
                    [MATURITY_DATE, NEXT_CALL_DATE],
                    "mm/dd/yyyy"
                ),
                COUPON_HZ,
                "SEMI-ANNUALLY"
            )
        )
        for bond_type, df in dfs.items()
    }


def put_data(df: pd.DataFrame) -> None:
    for exemption_status in [True, False]:
        df_copy = df.copy()
        df_filtered = filter_returns(df_copy, tax_exempt=exemption_status)
        df_filtered.sort_values(
            by=TE_RTN if exemption_status else TA_RTN,
            ascending=False
        ).to_csv(f"{PATH_OUT}{'exempt' if exemption_status else 'taxable'}.csv")


def read_files() -> dict[str, pd.DataFrame]:
    return {
        utl.snake_to_allcaps(filename): 
            pdu.read_csv_until_blank_line(f"{PATH_IN}{filename}.csv")
        for filename in CSV_FILENAMES
    }


def set_credit_score(df: pd.DataFrame) -> pd.DataFrame:
    moody_map = {k.upper(): v for k, v in k.CREDIT_RATINGS["Moody's"].items()}
    s_p_map = k.CREDIT_RATINGS["S&P"]
    df["moody_score"] = df[MOODY_RATING].map(moody_map)
    df["s_p_score"] = df[S_P_RATING].map(s_p_map)
    df[CR_SCORE] = df[["moody_score", "s_p_score"]].max(axis=1, skipna=True)
    no_score = df["moody_score"].isna() & df["s_p_score"].isna()
    df.loc[no_score, CR_SCORE] = pd.NA
    df.drop(columns=["moody_score", "s_p_score", MOODY_RATING, S_P_RATING], 
            inplace=True)
    return df
    

def set_frequency_map(df: pd.DataFrame) -> pd.DataFrame:
    df[HZ_MAP] = df[COUPON_HZ].map(HZ_MAPS)
    df.drop(columns=COUPON_HZ, inplace=True)
    return df
    

def set_returns(row: pd.Series, settlement_dt: pd.Timestamp) -> pd.Series:
    def min_if_not_na(a, b):
        return a if pd.isna(b) else min(a, b)
    
    def round_percentage(n):
        return round(n * 100, 2) if pd.notna(n) else pd.NA

    end_dates = [MATURITY_DATE, NEXT_CALL_DATE]
    tax_options = [True, False]
    xirr_types = product(end_dates, tax_options)
    dates_map = {end_date: list_cashflow_dates(end_date, settlement_dt, row) 
                 for end_date in end_dates}
    returns_map = {(end, tax): compute_return(dates_map[end], row, tax) 
                   for end, tax in xirr_types}
    row[TA_RTN] = min_if_not_na(returns_map[(MATURITY_DATE, True)], 
                                returns_map[(NEXT_CALL_DATE, True)])
    row[TE_RTN] = min_if_not_na(returns_map[(MATURITY_DATE, False)], 
                                returns_map[(NEXT_CALL_DATE, False)])
    row[TA_RTN] = round_percentage(row[TA_RTN])
    row[TE_RTN] = round_percentage(row[TE_RTN])
    row.drop(labels=HZ_MAP, inplace=True)
    return row


def source_dataframes(dfs: dict[str, pd.DataFrame]) -> None:
    for bond_type, df in dfs.items(): df[BOND_TYPE] = bond_type


def main() -> None:
    Console.clear_screen()
    find_bonds()


if __name__ == "__main__":
    main()
