#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 03:13:23 2024

@author: abc

"""
import pandas as pd
import numpy as np

def calculate_severity(row):
    """Calculate severity based on specified conditions."""
    total = row['Power Outage'] + row['Water Pipeline Problem'] + row['Road Blockage'] + row['Medical Emergency']
    if total > 40:
        return 4
    elif 30 <= total <= 40:
        return 3
    elif 20 <= total < 30:
        return 2
    elif 10 <= total < 20:
        return 1
    else:
        return 0

def generate_mitigation_strategies(row):
    """
    Generate mitigation strategies based on conditions, tailored to address
    the cascading effects of a large earthquake and tsunami.
    """
    strategies = []
    if row['Disease Propagation Risk'] >= 1:
        strategies.append("Launch mass vaccination programs and public health campaigns to prevent disease outbreaks. Implement emergency sanitation facilities to prevent disease spread.")
   
    if row['Health System Disruption'] >= 1:
        strategies.append("Deploy mobile medical units for emergency healthcare services and vaccinations. Enhance public health monitoring and community education on hygiene practices.")

    if row['Water Pipeline Problem'] > 2:
        strategies.append("Distribute portable water purification kits and establish mobile desalination units. Upgrade water systems to be more resilient against natural disasters.")
    
    if row['Power Outage'] >= 1:
        strategies.append("Deploy mobile power units and prioritize restoring power to critical infrastructure. Invest in decentralized energy solutions like solar panels and microgrids for resilience.")

    if row['Infrastructure Damage'] >= 1:
        strategies.append("Implement rapid building inspections and repairs using drones and mobile technology. Rebuild with earthquake and tsunami-resistant designs.")

    if row['Port Damage'] >= 2:
        strategies.append("Establish temporary supply routes via unaffected ports and inland transportation. Invest in tsunami-resistant port infrastructure for future resilience.")

    if row['Road Blockage'] >= 1:
        strategies.append("Deploy portable bridges and establish emergency supply lines using alternate modes. Focus on quick restoration of critical transportation links.")
    
    return ', '.join(strategies)

def assign_organizations(severity):
    """
    Assign organizations based on the severity of the problem.
    Severity 4: Pool in resources from UNICEF, Red Cross, Doctors Without Borders, and FEMA.
    Severity 3: National Guard, Local Emergency Services, and Red Cross.
    Severity 2: Local Emergency Services, Local NGOs.
    Severity 1: Community-based organizations, Local NGOs.
    """
    if severity == 4:
        return "UNICEF, Red Cross, Doctors Without Borders, FEMA"
    elif severity == 3:
        return "National Guard, Local Emergency Services, Red Cross"
    elif severity == 2:
        return "Local Emergency Services, Local NGOs"
    elif severity == 1:
        return "Community-based organizations, Local NGOs"
    else:
        return "No action required"
    
def add_severity_and_strategies(file_path):
    """Read the CSV file, add severity and mitigation strategies, sort by severity, and save."""
    # Load the CSV file
    df = pd.read_csv(file_path)
    np.random.seed(42)  # For reproducibility
    df['Infrastructure Damage'] = np.random.randint(0, 5, size=len(df))
    df['Health System Disruption'] = np.random.randint(0, 5, size=len(df))
    df['Port Damage'] = np.random.randint(0, 5, size=len(df))
    df['Disease Propagation Risk'] = np.random.randint(0, 5, size=len(df))
    
    # Apply functions to calculate severity and generate mitigation strategies for each row
    df['Severity'] = df.apply(calculate_severity, axis=1)
    df['Mitigation Strategies'] = df.apply(generate_mitigation_strategies, axis=1)
    df['Assigned Organizations'] = df['Severity'].apply(assign_organizations)

    # Sort the DataFrame by the 'Severity' column in descending order
    df_sorted = df.sort_values(by='Severity', ascending=False)
    
    # Save the modified DataFrame to a new CSV file
    output_file_path = file_path.replace('.csv', '_with_severity_strategies_sorted.csv')
    df_sorted.to_csv(output_file_path, index=False)
    print(f"File saved with severity and mitigation strategies, sorted by severity, as: {output_file_path}")


# Replace the placeholder path with your actual file path

file_path = '/Users/abc/downloads/data_sf 2.csv'
add_severity_and_strategies(file_path)


