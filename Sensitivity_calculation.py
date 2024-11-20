import uproot
import numpy as np
import gatetools as gt
import os
from google.colab import drive

# Mount Google Drive to access files
drive.mount('/content/drive')

# Path to ROOT file in Google Drive
File = '/content/drive/MyDrive/path_to_your_file/your_simulation_file.root'

def compute_sensitivity(File, source_activity_MBq, duration_sec):
    """
    Function to compute the sensitivity of the PET system from a ROOT file using gatetools.
    Sensitivity is defined as the ratio of true count rate to source activity.

    Parameters:
    - File: str, path to the ROOT file.
    - source_activity_MBq: float, source activity in MBq.
    - duration_sec: float, duration of acquisition in seconds.

    Returns:
    - sensitivity: float, PET system sensitivity (counts rate per MBq).
    """
    # Open the ROOT file
    root_file = uproot.open(File)

    # Display available keys to analyze the data structure
    print("Available keys in the ROOT file:")
    print(root_file.keys())

    # Extract event data using gatetools
    event_counts = gt.get_pet_counts(root_file)

    # Print the different event counts
    print(f"Prompt events:    {event_counts.prompts_count}")
    print(f"Delayed events:   {event_counts.delays_count}")
    print(f"Random events:    {event_counts.randoms_count}")
    print(f"Scattered events: {event_counts.scatter_count}")

    # Calculate true events
    true_count = event_counts.prompts_count - (event_counts.randoms_count + event_counts.scatter_count)
    print(f"True events:      {true_count}")

    # Calculate true count rate
    true_count_rate = true_count / duration_sec
    print(f"True count rate: {true_count_rate} counts per second")

    # Calculate sensitivity (true count rate divided by source activity)
    sensitivity = true_count_rate / source_activity_MBq
    print(f"PET System Sensitivity: {sensitivity} counts rate per MBq")

    return sensitivity

# Example parameters
source_activity_MBq = 4  # 4 MBq
duration_sec = 10  # acquisition time 10 sec

# Compute sensitivity
sensitivity = compute_sensitivity(File, source_activity_MBq, duration_sec)
print(f"Computed PET system sensitivity: {sensitivity} counts rate per MBq")
