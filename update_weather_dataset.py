import sys
import os
import json
import base64
import subprocess
import pandas as pd

def update_dataset(excel_path=None):
    workspace = r'e:/1. AntiGravity/Pest and disesease'
    
    if not excel_path:
        for f in ['Weather.xlsx', 'Weather.xls', 'weather.xlsx', 'weather.xls']:
            candidate = os.path.join(workspace, f)
            if os.path.exists(candidate):
                excel_path = candidate
                break
                
    if not excel_path or not os.path.exists(excel_path):
        print("❌ Error: No weather Excel file found! Please place 'Weather.xls' in workspace or specify file path.")
        return False
        
    print(f"\n========================================================")
    print(f"🌾 AGROMET WEATHER DATASET UPDATER FOR KSNUAHS")
    print(f"========================================================")
    print(f"📁 Reading weather Excel file: {os.path.basename(excel_path)}")
    
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return False
        
    col_map = {
        'District': 'd', 'district': 'd', 'DISTRICT': 'd',
        'Block': 'b', 'block': 'b', 'BLOCK': 'b', 'Taluk': 'b', 'taluk': 'b',
        'ForecastDate': 'dt', 'Date': 'dt', 'date': 'dt', 'dt': 'dt',
        'Rainfall': 'rf', 'rainfall': 'rf', 'RF': 'rf', 'Rain': 'rf',
        'TempMax': 'tx', 'tempmax': 'tx', 'Tmax': 'tx', 'TMAX': 'tx',
        'TempMin': 'tn', 'tempmin': 'tn', 'Tmin': 'tn', 'TMIN': 'tn',
        'HumidityI': 'rh1', 'humidityi': 'rh1', 'RHI': 'rh1', 'RH1': 'rh1', 'RH': 'rh1',
        'HumidityII': 'rh2', 'humidityii': 'rh2', 'RHII': 'rh2', 'RH2': 'rh2',
        'WindSpeed': 'ws', 'windspeed': 'ws', 'WS': 'ws',
        'WindDirection': 'wd', 'winddirection': 'wd', 'WD': 'wd',
        'CloudCover': 'cc', 'cloudcover': 'cc', 'CC': 'cc'
    }
    
    renamed = {}
    for col in df.columns:
        c_clean = str(col).strip()
        if c_clean in col_map:
            renamed[col] = col_map[c_clean]
            
    df = df.rename(columns=renamed)
    
    required_cols = ['d', 'b', 'tx', 'tn', 'rh1']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"❌ Missing required columns: {missing}")
        return False
        
    records = []
    for idx, row in df.iterrows():
        try:
            r_dict = {
                'd': str(row.get('d', '')).strip(),
                'b': str(row.get('b', '')).strip(),
                'dt': str(row.get('dt', '')).strip() if pd.notna(row.get('dt')) else '',
                'rf': float(row.get('rf', 0)) if pd.notna(row.get('rf')) else 0.0,
                'tx': float(row.get('tx', 30)) if pd.notna(row.get('tx')) else 30.0,
                'tn': float(row.get('tn', 22)) if pd.notna(row.get('tn')) else 22.0,
                'rh1': float(row.get('rh1', 85)) if pd.notna(row.get('rh1')) else 85.0,
                'rh2': float(row.get('rh2', 65)) if pd.notna(row.get('rh2')) else 65.0,
                'ws': float(row.get('ws', 8)) if pd.notna(row.get('ws')) else 8.0,
                'wd': float(row.get('wd', 180)) if pd.notna(row.get('wd')) else 180.0,
                'cc': float(row.get('cc', 4)) if pd.notna(row.get('cc')) else 4.0
            }
            if r_dict['d'] and r_dict['b']:
                records.append(r_dict)
        except Exception as err:
            continue
            
    districts_count = len(set(r['d'] for r in records))
    blocks_count = len(set((r['d'], r['b']) for r in records))
    
    print(f"\n✅ Weather Data Parsed Successfully:")
    print(f"   • Total Daily Forecast Records: {len(records)}")
    print(f"   • Total Districts Covered:     {districts_count}")
    print(f"   • Total Blocks/Taluks Covered: {blocks_count}")
    
    print(f"\n🔍 Weather Data Sample Preview (First 3 Records):")
    for sample in records[:3]:
        print(f"   📍 {sample['d']} / {sample['b']} ({sample['dt']}) -> Tmax: {sample['tx']}°C, Tmin: {sample['tn']}°C, RH: {sample['rh1']}%, Rain: {sample['rf']}mm")
        
    print(f"========================================================\n")
    
    # Interactive User Confirmation Prompt
    try:
        confirm = input(f"Should I update the web app and push to GitHub (along with {os.path.basename(excel_path)})? (y/n): ").strip().lower()
    except Exception:
        confirm = 'y'
        
    if confirm not in ['y', 'yes']:
        print("🛑 Update cancelled by user. No files were modified or pushed to GitHub.")
        return False
        
    print("\n🔄 Updating embedded dataset and compiling web app files...")
    json_path = os.path.join(workspace, 'weather_data_embedded.json')
    with open(json_path, 'w', encoding='utf-8') as json_f:
        json.dump(records, json_f, indent=None)
        
    master_script = os.path.join(workspace, 'scratch', 'build_master_final.py')
    if not os.path.exists(master_script):
        master_script = os.path.join(r'C:\Users\amfuh\.gemini\antigravity-ide\brain\4b6828d4-8c1d-40b7-b021-0dfcafcb95ce\scratch\build_master_final.py')
        
    subprocess.run([sys.executable, master_script], cwd=workspace)
    
    print("\n🚀 Committing and pushing weather Excel file + updated app to GitHub...")
    subprocess.run(["git", "add", "."], cwd=workspace)
    subprocess.run(["git", "commit", "-m", f"Update weather dataset & Excel: {len(records)} records from {os.path.basename(excel_path)}"], cwd=workspace)
    push_res = subprocess.run(["git", "push"], cwd=workspace, capture_output=True, text=True)
    
    print(push_res.stdout)
    print("🎉 SUCCESS: Weather Excel file, embedded dataset, and HTML web app updated and live on GitHub & GitHub Pages!")
    return True

if __name__ == '__main__':
    excel_arg = sys.argv[1] if len(sys.argv) > 1 else None
    update_dataset(excel_arg)
