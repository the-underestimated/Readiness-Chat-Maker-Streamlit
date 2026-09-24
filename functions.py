import pandas as pd
import numpy as np

def dataReadiness(readinessFilePath, WG):
    match WG:
        case 1:
            WG1ChatMaker = pd.read_excel(readinessFilePath, sheet_name='WG 1 JT NEW', skiprows=9)
            WG1ChatMaker = WG1ChatMaker.replace(r'^\s*$', pd.NA, regex=True)
            WG1ChatMaker = WG1ChatMaker.replace('#REF!', pd.NA)
            WG1ChatMaker = WG1ChatMaker.dropna(axis=0, how='all')
            WG1ChatMaker = WG1ChatMaker.dropna(axis=1, how='all')
            WG1ChatMaker['AIRCRAFT STATUS'] = WG1ChatMaker['AIRCRAFT STATUS'].ffill()
            WG1ChatMaker['REG'] = WG1ChatMaker['REG'].ffill()
            WG1ChatMaker['REG'] = WG1ChatMaker['REG'].str[:6]

            importantColumns = ["RESTRICTION I", 'RESTRICTION II', 'RESTRICTION III', 'REDUCE CYCLE ENGINE']

            colsToDrop = [
                col for col in WG1ChatMaker.columns
                if col not in importantColumns and WG1ChatMaker[col].isna().all()
            ]

            WG1ChatMaker = WG1ChatMaker.drop(columns=colsToDrop)

            WG1ChatMaker = WG1ChatMaker[WG1ChatMaker['REG'].str.contains('PK', regex=True, na=False)]
            WG1ChatMaker['WG'] = 1

            excludeStatus = [
                'D. AIRCRAFFT WITH SCHEDULE MAINT'
            ]

            pattern = '|'.join(excludeStatus)
            WG1ChatMaker = WG1ChatMaker[~WG1ChatMaker['AIRCRAFT STATUS'].str.contains(pattern, regex=True, na=False)]

            WG1Clean = WG1ChatMaker[WG1ChatMaker['AIRCRAFT STATUS'] == 'A. CLEAN AIRCRAFT']

            WG1Clean = WG1Clean.drop(columns='NO')
            WG1Clean = WG1Clean.reset_index(drop=True)
            WG1Clean['AIRCRAFT STATUS'] = 'CLEAN AIRCRAFT'
            WG1Clean['DUE DATE'] = pd.to_datetime(WG1Clean['DUE DATE'], errors='coerce')
            WG1Clean['REMAIN DAYS'] = WG1Clean['DUE DATE'] - pd.Timestamp.today().normalize()
            cleanCountWG1 = len(WG1Clean)

            WG1WithDMI = WG1ChatMaker[WG1ChatMaker['AIRCRAFT STATUS'] == 'B. AIRCRAFT WITH DMI']
            WG1WithDMI = WG1WithDMI.drop('NO', axis=1)
            WG1WithDMI = WG1WithDMI.reset_index(drop=True)
            WG1WithDMI['AIRCRAFT STATUS'] = 'AIRCRAFT WITH DMI'
            WG1WithDMI['DUE DATE'] = pd.to_datetime(WG1WithDMI['DUE DATE'], errors='coerce')
            WG1WithDMI['REMAIN DAYS'] = WG1WithDMI['DUE DATE'] - pd.Timestamp.today().normalize()
            DMICountWG1 = len(WG1WithDMI)

            WG1WithCDL = WG1ChatMaker[WG1ChatMaker['AIRCRAFT STATUS'] == 'C. AIRCRAFT WITH CDL']
            WG1WithCDL = WG1WithCDL.drop('NO', axis=1)
            WG1WithCDL = WG1WithCDL.reset_index(drop=True)
            WG1WithCDL['AIRCRAFT STATUS'] = 'AIRCRAFT WITH CDL'
            WG1WithCDL['DUE DATE'] = pd.to_datetime(WG1WithCDL['DUE DATE'], errors='coerce')
            WG1WithCDL['REMAIN DAYS'] = WG1WithCDL['DUE DATE'] - pd.Timestamp.today().normalize()
            CDLCountWG1 = len(WG1WithCDL)

            WG1GoodData = pd.concat([WG1Clean, WG1WithDMI, WG1WithCDL], ignore_index=True)
            WG1GoodData['DUE DATE'] = WG1GoodData['DUE DATE'].dt.strftime('%d %b %Y')
            WG1GoodData = WG1GoodData.rename({'DMI CAT':'DMI CATEGORY', 'AC REG':'AC REGISTRATION', 'DEFFER STATUS': 'DEFER STATUS', 'REMAIN DAYS':'REMAINING DAYS'}, axis=1)
            return WG1GoodData

        case 2:
            WG2ChatMaker = pd.read_excel(readinessFilePath, sheet_name='WG 2 JT NEW', skiprows=9)
            WG2ChatMaker = WG2ChatMaker.replace(r'^\s*$', pd.NA, regex=True)
            WG2ChatMaker = WG2ChatMaker.replace('#REF!', pd.NA)
            WG2ChatMaker = WG2ChatMaker.dropna(axis=0, how='all')
            WG2ChatMaker = WG2ChatMaker.dropna(axis=1, how='all')
            WG2ChatMaker['AIRCRAFT STATUS'] = WG2ChatMaker['AIRCRAFT STATUS'].ffill()
            WG2ChatMaker['REG'] = WG2ChatMaker['REG'].ffill()
            WG2ChatMaker['REG'] = WG2ChatMaker['REG'].str[:6]

            importantColumns = ["RESTRICTION I", 'RESTRICTION II', 'RESTRICTION III', 'REDUCE CYCLE ENGINE']

            colsToDrop = [
                col for col in WG2ChatMaker.columns
                if col not in importantColumns and WG2ChatMaker[col].isna().all()
            ]

            WG2ChatMaker = WG2ChatMaker.drop(columns=colsToDrop)

            WG2ChatMaker = WG2ChatMaker[WG2ChatMaker['REG'].str.contains('PK', regex=True, na=False)]
            WG2ChatMaker['WG'] = 2

            excludeStatus = [
                'D. AIRCRAFFT WITH SCHEDULE MAINT'
            ]

            pattern = '|'.join(excludeStatus)
            WG2ChatMaker = WG2ChatMaker[~WG2ChatMaker['AIRCRAFT STATUS'].str.contains(pattern, regex=True, na=False)]

            WG2Clean = WG2ChatMaker[WG2ChatMaker['AIRCRAFT STATUS'] == 'A. CLEAN AIRCRAFT']

            WG2Clean = WG2Clean.drop(columns='NO')
            WG2Clean = WG2Clean.reset_index(drop=True)
            WG2Clean['AIRCRAFT STATUS'] = 'CLEAN AIRCRAFT'
            WG2Clean['DUE DATE'] = pd.to_datetime(WG2Clean['DUE DATE'], errors='coerce')
            WG2Clean['REMAIN DAYS'] = WG2Clean['DUE DATE'] - pd.Timestamp.today().normalize()
            cleanCountWG2 = len(WG2Clean)

            WG2WithDMI = WG2ChatMaker[WG2ChatMaker['AIRCRAFT STATUS'] == 'B. AIRCRAFT WITH DMI']
            WG2WithDMI = WG2WithDMI.drop('NO', axis=1)
            WG2WithDMI = WG2WithDMI.reset_index(drop=True)
            WG2WithDMI['AIRCRAFT STATUS'] = 'AIRCRAFT WITH DMI'
            WG2WithDMI['DUE DATE'] = pd.to_datetime(WG2WithDMI['DUE DATE'], errors='coerce')
            WG2WithDMI['REMAIN DAYS'] = WG2WithDMI['DUE DATE'] - pd.Timestamp.today().normalize()
            DMICountWG2 = len(WG2WithDMI)

            WG2WithCDL = WG2ChatMaker[WG2ChatMaker['AIRCRAFT STATUS'] == 'C. AIRCRAFT WITH CDL']
            WG2WithCDL = WG2WithCDL.drop('NO', axis=1)
            WG2WithCDL = WG2WithCDL.reset_index(drop=True)
            WG2WithCDL['AIRCRAFT STATUS'] = 'AIRCRAFT WITH CDL'
            WG2WithCDL['DUE DATE'] = pd.to_datetime(WG2WithCDL['DUE DATE'], errors='coerce')
            WG2WithCDL['REMAIN DAYS'] = WG2WithCDL['DUE DATE'] - pd.Timestamp.today().normalize()
            CDLCountWG2 = len(WG2WithCDL)

            WG2GoodData = pd.concat([WG2Clean, WG2WithDMI, WG2WithCDL], ignore_index=True)
            WG2GoodData['DUE DATE'] = WG2GoodData['DUE DATE'].dt.strftime('%d %b %Y')
            WG2GoodData = WG2GoodData.rename({'DMI CAT':'DMI CATEGORY', 'AC REG':'AC REGISTRATION', 'DEFFER STATUS': 'DEFER STATUS', 'REMAIN DAYS':'REMAINING DAYS'}, axis=1)
            return WG2GoodData

        case 3:
            WG3ChatMaker = pd.read_excel(readinessFilePath, sheet_name='WG 3 JT NEW', skiprows=9)
            WG3ChatMaker = WG3ChatMaker.replace(r'^\s*$', pd.NA, regex=True)
            WG3ChatMaker = WG3ChatMaker.replace('#REF!', pd.NA)
            WG3ChatMaker = WG3ChatMaker.dropna(axis=0, how='all')
            WG3ChatMaker = WG3ChatMaker.dropna(axis=1, how='all')
            WG3ChatMaker['AIRCRAFT STATUS'] = WG3ChatMaker['AIRCRAFT STATUS'].ffill()
            WG3ChatMaker['REG'] = WG3ChatMaker['REG'].ffill()
            WG3ChatMaker['REG'] = WG3ChatMaker['REG'].str[:6]

            importantColumns = ["RESTRICTION I", 'RESTRICTION II', 'RESTRICTION III', 'REDUCE CYCLE ENGINE']

            colsToDrop = [
                col for col in WG3ChatMaker.columns
                if col not in importantColumns and WG3ChatMaker[col].isna().all()
            ]

            WG3ChatMaker = WG3ChatMaker.drop(columns=colsToDrop)

            WG3ChatMaker = WG3ChatMaker[WG3ChatMaker['REG'].str.contains('PK', regex=True, na=False)]
            WG3ChatMaker['WG'] = 3

            excludeStatus = [
                'D. AIRCRAFFT WITH SCHEDULE MAINT'
            ]

            pattern = '|'.join(excludeStatus)
            WG3ChatMaker = WG3ChatMaker[~WG3ChatMaker['AIRCRAFT STATUS'].str.contains(pattern, regex=True, na=False)]

            WG3Clean = WG3ChatMaker[WG3ChatMaker['AIRCRAFT STATUS'] == 'A. CLEAN AIRCRAFT']

            WG3Clean = WG3Clean.drop(columns='NO')
            WG3Clean = WG3Clean.reset_index(drop=True)
            WG3Clean['AIRCRAFT STATUS'] = 'CLEAN AIRCRAFT'
            WG3Clean['DUE DATE'] = pd.to_datetime(WG3Clean['DUE DATE'], errors='coerce')
            WG3Clean['REMAIN DAYS'] = WG3Clean['DUE DATE'] - pd.Timestamp.today().normalize()
            cleanCountWG3 = len(WG3Clean)

            WG3WithDMI = WG3ChatMaker[WG3ChatMaker['AIRCRAFT STATUS'] == 'B. AIRCRAFT WITH DMI']
            WG3WithDMI = WG3WithDMI.drop('NO', axis=1)
            WG3WithDMI = WG3WithDMI.reset_index(drop=True)
            WG3WithDMI['AIRCRAFT STATUS'] = 'AIRCRAFT WITH DMI'
            WG3WithDMI['DUE DATE'] = pd.to_datetime(WG3WithDMI['DUE DATE'], errors='coerce')
            WG3WithDMI['REMAIN DAYS'] = WG3WithDMI['DUE DATE'] - pd.Timestamp.today().normalize()
            DMICountWG3 = len(WG3WithDMI)

            WG3WithCDL = WG3ChatMaker[WG3ChatMaker['AIRCRAFT STATUS'] == 'C. AIRCRAFT WITH CDL']
            WG3WithCDL = WG3WithCDL.drop('NO', axis=1)
            WG3WithCDL = WG3WithCDL.reset_index(drop=True)
            WG3WithCDL['AIRCRAFT STATUS'] = 'AIRCRAFT WITH CDL'
            WG3WithCDL['DUE DATE'] = pd.to_datetime(WG3WithCDL['DUE DATE'], errors='coerce')
            WG3WithCDL['REMAIN DAYS'] = WG3WithCDL['DUE DATE'] - pd.Timestamp.today().normalize()
            CDLCountWG3 = len(WG3WithCDL)

            WG3GoodData = pd.concat([WG3Clean, WG3WithDMI, WG3WithCDL], ignore_index=True)
            WG3GoodData['DUE DATE'] = WG3GoodData['DUE DATE'].dt.strftime('%d %b %Y')
            WG3GoodData = WG3GoodData.rename({'DMI CAT':'DMI CATEGORY', 'AC REG':'AC REGISTRATION', 'DEFFER STATUS': 'DEFER STATUS', 'REMAIN DAYS':'REMAINING DAYS'}, axis=1)
            return WG3GoodData

        case 13:
            WG13ChatMaker = pd.read_excel(readinessFilePath, sheet_name='WG 13 330', skiprows=9)
            WG13ChatMaker = WG13ChatMaker.replace(r'^\s*$', pd.NA, regex=True)
            WG13ChatMaker = WG13ChatMaker.replace('#REF!', pd.NA)
            WG13ChatMaker = WG13ChatMaker.dropna(axis=0, how='all')
            WG13ChatMaker = WG13ChatMaker.dropna(axis=1, how='all')
            WG13ChatMaker['AIRCRAFT STATUS'] = WG13ChatMaker['AIRCRAFT STATUS'].ffill()
            WG13ChatMaker['REG'] = WG13ChatMaker['REG'].ffill()
            WG13ChatMaker['REG'] = WG13ChatMaker['REG'].str[:6]

            importantColumns = ["RESTRICTION I", 'RESTRICTION II', 'RESTRICTION III', 'REDUCE CYCLE ENGINE']

            colsToDrop = [
                col for col in WG13ChatMaker.columns
                if col not in importantColumns and WG13ChatMaker[col].isna().all()
            ]

            WG13ChatMaker = WG13ChatMaker.drop(columns=colsToDrop)
            WG13ChatMaker = WG13ChatMaker[WG13ChatMaker['REG'].str.contains('PK', regex=True, na=False)]

            WG13Clean = WG13ChatMaker
            WG13Clean['WG'] = 13

            excludeStatus = [
                'D. AIRCRAFFT WITH SCHEDULE MAINT'
            ]

            pattern = '|'.join(excludeStatus)
            WG13ChatMaker = WG13ChatMaker[~WG13ChatMaker['AIRCRAFT STATUS'].str.contains(pattern, regex=True, na=False)]

            WG13Clean = WG13ChatMaker[WG13ChatMaker['AIRCRAFT STATUS'] == 'A. CLEAN AIRCRAFT']
            WG13Clean = WG13Clean.drop(columns='NO')
            WG13Clean = WG13Clean.reset_index(drop=True)
            WG13Clean['AIRCRAFT STATUS'] = 'CLEAN AIRCRAFT'
            WG13Clean['DUE DATE'] = pd.to_datetime(WG13Clean['DUE DATE'], errors='coerce')
            WG13Clean['REMAIN DAYS'] = WG13Clean['DUE DATE'] - pd.Timestamp.today().normalize()
            cleanCountWG13 = len(WG13Clean)

            WG13WithDMI = WG13ChatMaker[WG13ChatMaker['AIRCRAFT STATUS'] == 'B. AIRCRAFT WITH DMI']
            WG13WithDMI = WG13WithDMI.drop('NO', axis=1)
            WG13WithDMI = WG13WithDMI.reset_index(drop=True)
            WG13WithDMI['AIRCRAFT STATUS'] = 'AIRCRAFT WITH DMI'
            WG13WithDMI['DUE DATE'] = pd.to_datetime(WG13WithDMI['DUE DATE'], errors='coerce')
            WG13WithDMI['REMAIN DAYS'] = WG13WithDMI['DUE DATE'] - pd.Timestamp.today().normalize()
            DMICountWG13 = len(WG13WithDMI)

            WG13WithCDL = WG13ChatMaker[WG13ChatMaker['AIRCRAFT STATUS'] == 'C.AIRCRAFT WITH CDL']
            WG13WithCDL = WG13WithCDL.drop('NO', axis=1)
            WG13WithCDL = WG13WithCDL.reset_index(drop=True)
            WG13WithCDL['AIRCRAFT STATUS'] = 'AIRCRAFT WITH CDL'
            WG13WithCDL['DUE DATE'] = pd.to_datetime(WG13WithCDL['DUE DATE'], errors='coerce')
            WG13WithCDL['REMAIN DAYS'] = WG13WithCDL['DUE DATE'] - pd.Timestamp.today().normalize()
            CDLCountWG13 = len(WG13WithCDL)

            WG13GoodData = pd.concat([WG13Clean, WG13WithDMI, WG13WithCDL], ignore_index=True)
            WG13GoodData['DUE DATE'] = WG13GoodData['DUE DATE'].dt.strftime('%d %b %Y')
            WG13GoodData = WG13GoodData.rename({'DMI CAT':'DMI CATEGORY', 'AC REG':'AC REGISTRATION', 'DEFFER STATUS': 'DEFER STATUS', 'REMAIN DAYS':'REMAINING DAYS'}, axis=1)

            return WG13GoodData