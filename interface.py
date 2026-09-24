import streamlit as st
import pandas as pd
import functions as fn
import numpy as np

st.title("Readiness Chat Maker by Gz.")


with st.sidebar:
    st.title("Procedures and Notes")
    with st.popover("Patch Notes v1.0.0"):
        st.write("Initial release of Readiness Chat Maker by Gz.")
    st.subheader("App usage procedures:")
    st.write("1. Download the GSS Daily Report WG from the GSS SharePoint site by clicking the 'File' tab, then 'Create a Copy', then 'Download a Copy'.")
    st.write("2. Upload the downloaded .xlsx file using the file uploader below.")
    st.write("3. Click the 'Process the Data!' button to process the data and generate the readiness report.")
    st.write("4. The generated report will be displayed below the button. You can copy and paste it into your chat application.")

dataRaw = st.file_uploader("Choose File .xlsx from GSS Daily Report WG", type='xlsx')

if dataRaw is not None:
    if st.button("Process the Data!", type="primary"): 
        try:
            dataReadinessWG1 = fn.dataReadiness(dataRaw, 1)
            dataReadinessWG2 = fn.dataReadiness(dataRaw, 2)
            dataReadinessWG3 = fn.dataReadiness(dataRaw, 3)
            dataReadinessWG13 = fn.dataReadiness(dataRaw, 13)
            allWGGoodData = pd.concat([dataReadinessWG1, dataReadinessWG2, dataReadinessWG3, dataReadinessWG13], ignore_index=True)
            reportLines = []

            narrowBodyWGs = [1, 2, 3]
            wideBodyWGs = [13]

            def generateSection(sectionTitle, df, wgList):

                sectionDf = df[df["WG"].isin(wgList)]

                if sectionDf.empty:
                    return

                reportLines.append(sectionTitle)

                # ===== AIRCRAFT WITH DMI/CDL TOTAL =====
                dmiCdlRegs = sectionDf[
                    sectionDf["AIRCRAFT STATUS"].isin(
                        ["AIRCRAFT WITH DMI", "AIRCRAFT WITH CDL"]
                    )
                ]["REG"].unique()

                dmiCdlTotal = len(dmiCdlRegs)

                # ===== CLEAN AIRCRAFT TOTAL =====
                cleanTotal = sectionDf[
                    (sectionDf["AIRCRAFT STATUS"] == "CLEAN AIRCRAFT")
                    & (~sectionDf["REG"].isin(dmiCdlRegs))
                ]["REG"].nunique()

                reportLines.append(f"CLEAN AIRCRAFT TOTAL: {cleanTotal}")
                reportLines.append(f"AIRCRAFT WITH DMI/CDL TOTAL: {dmiCdlTotal}")
                reportLines.append("")

                # ===== NOTES =====
                reportLines.append("NOTES:")
                reportLines.append("")

                notesDf = sectionDf[
                    sectionDf["AIRCRAFT STATUS"] != "CLEAN AIRCRAFT"
                ]

                for wg, wgDf in notesDf.groupby("WG"):
                    reportLines.append(f"*WG {wg}*")

                    for aircraftIndex, (reg, regDf) in enumerate(
                        wgDf.groupby("REG"), start=1
                    ):
                        reportLines.append(f"{aircraftIndex}. {reg}")

                        for _, row in regDf.iterrows():

                            category = (
                                "CDL"
                                if row["AIRCRAFT STATUS"] == "AIRCRAFT WITH CDL"
                                else row["DMI CATEGORY"]
                            )

                            noteParts = [
                                f"- {row['DMI DESCRIPTION AND REMARK']} ({category})"
                            ]

                            if pd.notna(row["DUE DATE"]) and str(row["DUE DATE"]).strip():
                                noteParts.append(f"- {row['DUE DATE']}")

                            if pd.notna(row["DEFER TYPE"]) and str(row["DEFER TYPE"]).strip():
                                noteParts.append(f"- {row['DEFER TYPE']}")

                            reportLines.append(" ".join(noteParts))

                    reportLines.append("")

                reportLines.append("")

            # Generate both sections
            generateSection("NARROW BODY", allWGGoodData, narrowBodyWGs)
            generateSection("WIDE BODY", allWGGoodData, wideBodyWGs)

            finalReport = "\n".join(reportLines)

            #output = io.BytesIO()

            #output.seek(0)
            #st.session_state['outputData'] = output
            st.divider()
            st.header("Generated Report")
            st.code(finalReport, language='markdown')

        except Exception as errorCode:
            st.error(f"Error: {errorCode}")