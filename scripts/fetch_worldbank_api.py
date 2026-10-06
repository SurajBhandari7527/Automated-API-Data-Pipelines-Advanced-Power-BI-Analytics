import pandas as pd
import requests

# 1. Fetch country metadata from the World Bank API
country_api_url = "https://api.worldbank.org/v2/country?format=json&per_page=350"
country_resp = requests.get(country_api_url)

if country_resp.status_code == 200:
    # World Bank API returns pagination info at index 0 and data list at index 1
    countries_raw = country_resp.json()[1]

    country_meta_list = []
    for c in countries_raw:
        country_meta_list.append({
            "country": c.get("name"),
            "region": c.get("region", {}).get("value"),
            "latitude": c.get("latitude"),
            "longitude": c.get("longitude")
        })

    country_meta_df = pd.DataFrame(country_meta_list)
else:
    print(f"Failed to fetch data. HTTP Status Code: {country_resp.status_code}")
    country_meta_df = pd.DataFrame(columns=["country", "region", "latitude", "longitude"])

# Create the country_region_details table (contains only country and region)
country_region_details = (
    country_meta_df[["country", "region"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Export to CSV
country_region_details.to_csv("country_region_details.csv", index=False)

# 2. DEFINE INDICATOR GROUPS
indicator_groups = {
    "economic_activity_growth": [
        "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
        "NY.GDP.PCAP.CD"      # GDP per capita (current US$)
    ],
    "labour_market_indicators": [
        "SL.UEM.TOTL.ZS",      # Unemployment total
        "SL.UEM.1524.ZS",      # Unemployment youth total
        "SL.TLF.TOTL.IN"       # Labour force, total
    ],
    "trade_globalization": [
        "NE.EXP.GNFS.CD",      # Exports of goods and services
        "NE.IMP.GNFS.CD"       # Imports of goods and services
    ],
    "poverty_inequality": [
        "SI.POV.NAHC",         # Poverty headcount ratio
        "SI.POV.GINI"          # Gini index
    ],
    "environmental_indicators": [
        "EG.FEC.RNEW.ZS",      # Renewable energy consumption
        "AG.LND.FRST.ZS"       # Forest area (% of land area)
    ],
    "health_indicators": [
        "SP.DYN.LE00.IN",      # Life expectancy at birth
        "SP.DYN.IMRT.IN",      # Infant mortality rate
        "SH.H2O.BASW.ZS",      # Access to at least basic water services
        "SH.XPD.CHEX.GD.ZS",   # Current health expenditure (% of GDP)
        "SH.IMM.IDPT",         # Immunization, DPT
        "SH.IMM.MEAS",         # Immunization, measles
        "SH.MMR.RISK.ZS",      # Risk of maternal death
        "SH.DTH.COMM.ZS",      # Deaths from communicable diseases
        "SH.TBS.INCD",         # Tuberculosis incidence
        "SH.STA.BRTC.ZS",      # Births attended by skilled health staff
        "SH.STA.MMRT",         # Maternal mortality ratio
        "SP.POP.65UP.TO.ZS",   # Population ages 65 and above
        "SH.HIV.INCD.ZS"       # HIV incidence rate
    ],
    "technology_indicators": [
        "IT.NET.USER.ZS",      # Individuals using the Internet
        "IT.CEL.SETS.P2"       # Mobile cellular subscriptions
    ]
}


# 3. FETCH INDICATORS AND BUILD CATEGORY TABLES
# Set per_page=1000 to fetch data faster
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/{}?format=json&per_page=1000&page={}"
target_columns = ["indicator_name", "country", "date", "value", "category", "latitude", "longitude", "region"]

for category, indicators in indicator_groups.items():
    category_rows = []
    
    for ind_code in indicators:
        page_no = 1
        while True:
            url = BASE_URL.format(ind_code, page_no)
            resp = requests.get(url)
            
            if resp.status_code != 200:
                break
                
            res_json = resp.json()
            if not res_json or len(res_json) < 2 or res_json[1] is None:
                break
                
            header_info = res_json[0]
            data = res_json[1]
            
            for item in data:
                category_rows.append({
                    "indicator_name": item.get("indicator", {}).get("value"),
                    "country": item.get("country", {}).get("value"),
                    "date": item.get("date"),
                    "value": item.get("value"),
                    "category": category
                })
                
            total_pages = header_info.get("pages", 1)
            if page_no >= total_pages:
                break
            page_no += 1

    # Create category DataFrame
    if category_rows:
        cat_df = pd.DataFrame(category_rows)
        # Merge latitude, longitude, and region from metadata
        cat_df = pd.merge(cat_df, country_meta_df, on="country", how="left")
        cat_df = cat_df[target_columns]
    else:
        cat_df = pd.DataFrame(columns=target_columns)

    # Save CSV file locally
    cat_df.to_csv(f"{category}.csv", index=False)
    
    # Assign DataFrame to dynamic variable name in global scope for Power BI recognition
    globals()[category] = cat_df
