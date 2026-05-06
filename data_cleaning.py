import pandas as pd
import os

BASE_DIR = "/Users/zhoujingyuan/Desktop/FP - PHI Vis/Datasets"
BASE_OUT = "/Users/zhoujingyuan/Desktop/FP - PHI Vis/Datasets_Cleaned"

# ── 1. Load included school codes ─────────────────────────────────────────────
ref_raw = pd.read_excel(
    os.path.join(BASE_DIR, "Schools to Include for Absenteeism Visualizations_Final_4.10.2026.xlsx"),
    header=None
)

# Find the header row (contains 'SCHOOL' and 'Include')
header_row = None
for i in range(len(ref_raw)):
    vals = [str(v) for v in ref_raw.iloc[i].tolist()]
    if 'SCHOOL' in vals and any('Include' in v for v in vals):
        header_row = i
        break

ref_raw.columns = ref_raw.iloc[header_row]
ref = ref_raw.iloc[header_row + 1:].reset_index(drop=True)
include_col = [c for c in ref.columns if 'Include' in str(c)][0]
included_codes = set(
    ref[ref[include_col] == 'Include']['SCHOOL']
    .astype(str).str.strip().str.zfill(8)
)
print(f"Included school codes: {len(included_codes)}")

# ── 2. Year folders and file names ────────────────────────────────────────────
years = {
    "2017-2018": {"att": "'17-18 Attendance.xlsx",  "enr": "2017-2018 Enrollment.xlsx"},
    "2018-2019": {"att": "'18-19 Attendance.xlsx",  "enr": "2018-2019 Enrollment.xlsx"},
    "2019-2020": {"att": "'19-20 Attendance.xlsx",  "enr": "2019-2020 Enrollment.xlsx"},
    "2020-2021": {"att": "20-21 Attendance.xlsx",   "enr": "20-21 Enrollment.xlsx"},
    "2021-2022": {"att": "21-22 Attendance.xlsx",   "enr": "21-22 Enrollment.xlsx"},
    "2022-2023": {"att": "22-23 Attendance.xlsx",   "enr": "22-23 Enrollment.xlsx"},
    "2023-2024": {"att": "23-24 Attendance.xlsx",   "enr": "23-24 Enrollment.xlsx"},
    "2024-2025": {"att": "24-25 Attendance.xlsx",   "enr": "24-25 Enrollment.xlsx"},
}

def find_header_row(df_raw, keywords):
    """Return index of first row whose values contain all given keywords."""
    for i in range(len(df_raw)):
        vals = [str(v).strip() for v in df_raw.iloc[i].tolist()]
        if all(any(kw in v for v in vals) for kw in keywords):
            return i
    return None

# ── 3. Process each year ──────────────────────────────────────────────────────
for year, files in years.items():
    out_dir = os.path.join(BASE_OUT, year)
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'=' * 50}")
    print(f"Processing {year}  →  {out_dir}")

    # ── Attendance ─────────────────────────────────────────────────────────────
    att_src = os.path.join(BASE_DIR, year, files["att"])
    att_raw = pd.read_excel(att_src, header=None)
    att_header = find_header_row(att_raw, ["School Code"])
    att_raw.columns = att_raw.iloc[att_header]
    att_data = att_raw.iloc[att_header + 1:].reset_index(drop=True)

    before = len(att_data)
    att_data["School Code"] = att_data["School Code"].astype(str).str.strip().str.zfill(8)
    att_filtered = att_data[att_data["School Code"].isin(included_codes)].copy()
    print(f"  Attendance: {before} → {len(att_filtered)} rows")

    att_out = os.path.join(out_dir, files["att"])
    att_filtered.to_excel(att_out, index=False)

    # ── Enrollment ─────────────────────────────────────────────────────────────
    enr_src = os.path.join(BASE_DIR, year, files["enr"])
    enr_raw = pd.read_excel(enr_src, header=None)
    enr_header = find_header_row(enr_raw, ["SCHOOL"])
    enr_raw.columns = enr_raw.iloc[enr_header]
    enr_data = enr_raw.iloc[enr_header + 1:].reset_index(drop=True)

    before = len(enr_data)
    enr_data["SCHOOL"] = enr_data["SCHOOL"].astype(str).str.strip().str.zfill(8)
    enr_filtered = enr_data[enr_data["SCHOOL"].isin(included_codes)].copy()
    print(f"  Enrollment: {before} → {len(enr_filtered)} rows")

    enr_out = os.path.join(out_dir, files["enr"])
    enr_filtered.to_excel(enr_out, index=False)

print(f"\n✓ Done. All cleaned files saved to:\n  {BASE_OUT}")
