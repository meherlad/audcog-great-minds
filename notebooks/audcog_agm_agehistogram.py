import pandas as pd
import json
import re
import matplotlib.pyplot as plt
import numpy as np

# Set matplotlib style for better looking plots
plt.style.use('default')
plt.rcParams['figure.figsize'] = (16, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# --- 1. LOAD THE DATA ---
filename = 'audcog_data.json'

try:
    # Load the JSON data
    with open(filename, 'r') as f:
        data = json.load(f)
    
    print('Successfully loaded audcog_data.json')
    print('Top-level keys:', list(data.keys()))
    
    # --- 2. EXTRACT THE AUDCOG DATA ---
    if 'audcog-online' in data:
        audcog_data = data['audcog-online']
        print(f'\nFound audcog-online data with {len(audcog_data)} participants')
        
        # Show first few participant IDs
        participant_ids = list(audcog_data.keys())
        print('First 5 participant IDs:', participant_ids[:5])
        
        # --- 3. EXTRACT AWM DATA FOR EACH PARTICIPANT ---
        awm_records = []
        skipped_participants = []
        
        for participant_id, participant_data in audcog_data.items():
            # Check if participant_data is a dictionary (has data) or just a number (no data)
            if isinstance(participant_data, dict):
                if 'awm' in participant_data:
                    awm_data = participant_data['awm']
                    
                    # Each participant might have multiple sessions
                    for session_timestamp, session_data in awm_data.items():
                        record = {
                            'participant_id': participant_id,
                            'session_timestamp': session_timestamp,
                            **session_data  # Unpack all the AWM data
                        }
                        awm_records.append(record)
                else:
                    skipped_participants.append(f'{participant_id} (no awm data)')
            else:
                # participant_data is likely just a number (e.g., sessions count)
                skipped_participants.append(f'{participant_id} (sessions: {participant_data})')
        
        print(f'\nSkipped {len(skipped_participants)} participants without AWM data')
        print('First 5 skipped:', skipped_participants[:5])
        
        if awm_records:
            # --- 4. CREATE CLEAN DATAFRAME ---
            df_clean = pd.DataFrame(awm_records)
            
            print('\n--- Success! ---')
            print(f'Extracted {len(df_clean)} AWM records')
            print('\nOriginal DataFrame shape:', df_clean.shape)
            print('\nColumns:', df_clean.columns.tolist())
            
            # --- 5. FILTER FOR AGM PARTICIPANTS ---
            print('\n--- Filtering for AGM Participants ---')
            
            # Create a function to check if participant ID matches AGM pattern
            def is_agm_participant(participant_id):
                # Pattern: AGM followed by 4-6 digits
                pattern = r'^AGM\d{4,6}$'
                return bool(re.match(pattern, str(participant_id)))
            
            # Filter the DataFrame
            df_agm = df_clean[df_clean['participant_id'].apply(is_agm_participant)]
            
            print(f'\nAGM participants found: {len(df_agm)} records')
            print(f'AGM participants shape: {df_agm.shape}')
            
            if not df_agm.empty:
                print('\nUnique AGM participant IDs:')
                print(df_agm['participant_id'].unique())
                
                print('\nAGM DataFrame preview:')
                print(df_agm.head())
                
                # --- 6. EXTRACT AGE DATA FROM ORIGINAL JSON STRUCTURE ---
                print('\n--- Extracting Age Data from Original JSON Structure ---')
                
                # Extract age data during the initial data processing
                agm_records_with_age = []
                
                for participant_id, participant_data in audcog_data.items():
                    if participant_id.startswith('AGM'):
                        # Check if participant has misc data with age
                        if 'misc' in participant_data and isinstance(participant_data['misc'], dict):
                            # Get age from any timestamp in misc data
                            age = None
                            sex = 'unknown'
                            computer_type = 'unknown'
                            hearing_aids = 'unknown'
                            headphones = 'unknown'
                            
                            for timestamp, misc_data in participant_data['misc'].items():
                                if isinstance(misc_data, dict) and 'age' in misc_data:
                                    age = misc_data['age']
                                    # Convert age to integer if it's a string
                                    try:
                                        age = int(age)
                                    except (ValueError, TypeError):
                                        age = None
                                    
                                    if age is not None:
                                        sex = misc_data.get('sex', 'unknown')
                                        computer_type = misc_data.get('comp', 'unknown')
                                        hearing_aids = misc_data.get('haids', 'unknown')
                                        headphones = misc_data.get('headphones', 'unknown')
                                        break  # Found age data, no need to check other timestamps
                            
                            # If we found age data, get AWM data from any timestamp
                            if age is not None and 'awm' in participant_data:
                                for awm_timestamp, awm_data in participant_data['awm'].items():
                                    record = {
                                        'participant_id': participant_id,
                                        'session_timestamp': awm_timestamp,
                                        'age': age,
                                        'sex': sex,
                                        'computer_type': computer_type,
                                        'hearing_aids': hearing_aids,
                                        'headphones': headphones
                                    }
                                    # Add AWM data
                                    record.update(awm_data)
                                    agm_records_with_age.append(record)
                
                print(f'Found {len(agm_records_with_age)} AGM records with age data')
                
                if agm_records_with_age:
                    # Create DataFrame with age data
                    df_agm_with_age = pd.DataFrame(agm_records_with_age)
                    
                    print('\nSample AGM records with age:')
                    print(df_agm_with_age[['participant_id', 'age', 'sex', 'computer_type']].head(10))
                    
                    # --- 7. CREATE BEAUTIFUL AGE HISTOGRAM WITH MATPLOTLIB ---
                    print('\n--- Creating Beautiful Age Histogram ---')
                    
                    # Filter out None values for plotting
                    valid_ages = df_agm_with_age['age'].dropna()
                    
                    if len(valid_ages) > 0:
                        # Create the plot with subplots
                        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                        
                        # Left plot: Enhanced histogram with KDE-like styling
                        n, bins, patches = ax1.hist(valid_ages, bins=20, edgecolor='black', 
                                                   alpha=0.7, color='skyblue', linewidth=1.2)
                        
                        # Add a smooth curve overlay (KDE approximation)
                        bin_centers = (bins[:-1] + bins[1:]) / 2
                        ax1.plot(bin_centers, n, 'o-', color='darkblue', linewidth=2, 
                                markersize=4, alpha=0.8)
                        
                        ax1.set_title('Age Distribution of AGM Participants', 
                                    fontsize=16, fontweight='bold', pad=20)
                        ax1.set_xlabel('Age (years)', fontsize=14, fontweight='bold')
                        ax1.set_ylabel('Frequency', fontsize=14, fontweight='bold')
                        ax1.grid(True, alpha=0.3, linestyle='--')
                        
                        # Add statistics lines with better styling
                        mean_age = valid_ages.mean()
                        median_age = valid_ages.median()
                        ax1.axvline(mean_age, color='red', linestyle='--', linewidth=2.5, 
                                   label=f'Mean: {mean_age:.1f} years')
                        ax1.axvline(median_age, color='orange', linestyle='--', linewidth=2.5, 
                                   label=f'Median: {median_age:.1f} years')
                        ax1.legend(fontsize=12, framealpha=0.9)
                        
                        # Right plot: Enhanced box plot
                        box_plot = ax2.boxplot(valid_ages, patch_artist=True, 
                                             boxprops=dict(facecolor='lightgreen', alpha=0.7),
                                             medianprops=dict(color='darkgreen', linewidth=2),
                                             whiskerprops=dict(color='darkgreen', linewidth=1.5),
                                             capprops=dict(color='darkgreen', linewidth=1.5))
                        
                        ax2.set_title('Age Distribution (Box Plot)', 
                                    fontsize=16, fontweight='bold', pad=20)
                        ax2.set_ylabel('Age (years)', fontsize=14, fontweight='bold')
                        ax2.grid(True, alpha=0.3, linestyle='--')
                        
                        # Add some statistics text on the box plot
                        stats_text = f'Mean: {mean_age:.1f}\nMedian: {median_age:.1f}\nStd: {valid_ages.std():.1f}'
                        ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes, 
                                verticalalignment='top', fontsize=11, 
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                        
                        plt.tight_layout()
                        plt.show()
                        
                        # Print comprehensive age statistics
                        print(f'\n📊 Age Statistics:')
                        print(f'Mean age: {mean_age:.1f} years')
                        print(f'Median age: {median_age:.1f} years')
                        print(f'Min age: {valid_ages.min()} years')
                        print(f'Max age: {valid_ages.max()} years')
                        print(f'Age range: {valid_ages.max() - valid_ages.min()} years')
                        print(f'Standard deviation: {valid_ages.std():.1f} years')
                        print(f'Total participants with age data: {len(valid_ages)}')
                        
                        # Save the AGM data with age
                        df_agm_with_age.to_csv('audcog_agm_with_age.csv', index=False)
                        print('\n💾 AGM data with age saved to audcog_agm_with_age.csv')
                        
                        # Also save summary statistics
                        age_summary = df_agm_with_age.groupby('participant_id')['age'].first().describe()
                        print('\n📈 Age Summary by Participant:')
                        print(age_summary)
                        
                    else:
                        print('\n❌ No valid age data found for histogram')
                else:
                    print('\n❌ No age data could be extracted from the JSON structure')
                    print('This suggests the age data might be stored differently than expected')
                
            else:
                print('\n❌ No AGM participants found in the data')
                print('\nSample of participant IDs to check pattern:')
                print(df_clean['participant_id'].unique()[:10])
        else:
            print('\n❌ No AWM data found in any participants')
    else:
        print('\n❌ Error: Could not find audcog-online key in the data')
        print('Available keys:', list(data.keys()))

except FileNotFoundError:
    print(f'❌ Error: The file {filename} was not found. Make sure it is in the same folder as your notebook.')
except Exception as e:
    print(f'❌ An unexpected error occurred: {e}')
    import traceback
    traceback.print_exc()
