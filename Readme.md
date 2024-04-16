Vegetation Analysis Tool
This Python script provides an automated way to analyze vegetation from high-resolution NADIR photos. It calculates vegetation indices, applies a binary threshold to identify vegetation areas, and extracts GPS data from images. The results are saved in a CSV file for further analysis.

Features
Image Processing: Converts images to analyze vegetation using the Green Chromatic Coordinate (GCC) index.
Threshold Adjustment: Allows dynamic adjustment of the threshold for vegetation detection.
Morphological Operations: Applies morphological opening to remove isolated pixels, enhancing the quality of the binary mask.
GPS Data Extraction: Extracts GPS coordinates from images using ExifTool.
Batch Processing: Processes multiple images in a directory and summarizes the results in a CSV file.
GUI: Provides a graphical user interface for easy parameter adjustments and file management.
Requirements
Python 3.x
OpenCV-Python: pip install opencv-python
NumPy: pip install numpy
ExifTool (installed and accessible from the command line)
Setup
Install Python Dependencies:
Make sure Python is installed on your system, and then install the necessary Python libraries using pip:

bash
Copy code
pip install numpy opencv-python
ExifTool:
Download and install ExifTool from here. Ensure it's added to your system's PATH or modify the script to point directly to the ExifTool executable.

Usage
Start the GUI:
Run the script using Python from the command line:

bash
Copy code
python gcc_csv_guiV2.py
Configure Parameters:

Select Folder Containing Images: Choose the folder where your images are stored.
Select Output CSV File: Choose the location and name of the CSV file to save the results.
Set GCC Threshold: Adjust the threshold value to optimize vegetation detection based on your specific images.
Start Processing:
Click "Start Processing" to begin the analysis. The script will process each image in the selected folder, calculate the vegetation percentage, and save the results along with GPS data to the specified CSV file.

Review Results:
Open the output CSV file to see the results. Each row corresponds to an image, detailing its name, GPS coordinates, and vegetation percentage.

Troubleshooting
Image Not Found: Ensure the paths to your images are correct and accessible.
ExifTool Error: Confirm that ExifTool is properly installed and correctly referenced in the script.
Advanced Settings
Kernel Size for Morphological Opening: Adjust the kernel size in the script to increase or decrease the sensitivity of noise removal in the binary mask.
Contact
For further assistance or to report issues, contact Jesse Lawrence lawrence.jessejames@gmail.com 
