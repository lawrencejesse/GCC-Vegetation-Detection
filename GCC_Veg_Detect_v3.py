import cv2
import numpy as np
import subprocess
import os
import csv
from tkinter import Tk, Label, Button, IntVar, Entry, filedialog, simpledialog

def load_and_convert_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found. Please check the file path.")
    if np.sum(image[:, :, 0]) > np.sum(image[:, :, 2]):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image
    return image_rgb

def calculate_exg(image_rgb):
    exg = 2 * image_rgb[:, :, 1] - image_rgb[:, :, 0] - image_rgb[:, :, 2]
    exg = np.clip(exg, 0, 255)
    return exg.astype(np.uint8)

def calculate_gcc(image_rgb):
    sum_rgb = np.sum(image_rgb, axis=2, dtype=np.float32) + np.finfo(float).eps
    gcc = image_rgb[:, :, 1] / sum_rgb
    gcc_scaled = np.clip(gcc * 255, 0, 255).astype(np.uint8)
    return gcc_scaled

### This was my original script

#def apply_threshold(image, threshold):
#    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
#    return binary_image

#now i'm adding my revised script to remove single pixels#

def apply_morphological_opening(binary_image, kernel_size=3):##Adjust this kernel size to pixels removed#
    """Apply morphological opening to remove isolated pixels in the binary image."""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    return opening

def apply_threshold(image, threshold):
    _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    cleaned_binary_image = apply_morphological_opening(binary_image)
    return cleaned_binary_image

###back to orignial script###

def save_modified_image(image, folder_path, filename):
    output_filename = os.path.splitext(filename)[0] + "_modified.jpg"
    output_path = os.path.join(folder_path, output_filename)
    cv2.imwrite(output_path, image)

def get_gps_coordinates_with_exiftool(image_path):
    try:
        result = subprocess.run(['C:\\Users\\jesse\\Documents\\exiftool-12.65\\exiftool.exe', '-GPSLatitude', '-GPSLongitude', '-n', image_path], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        gps_data = {}
        for line in output.split('\n'):
            if 'GPS Latitude' in line:
                gps_data['latitude'] = float(line.split(':')[1].strip())
            elif 'GPS Longitude' in line:
                gps_data['longitude'] = float(line.split(':')[1].strip())
        return gps_data
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode()}")
        return None

def calculate_vegetation_percentage(binary_image):
    vegetation_pixels = np.count_nonzero(binary_image)
    total_pixels = binary_image.size
    vegetation_percentage = (vegetation_pixels / total_pixels) * 100
    return vegetation_percentage

def process_images(folder_path, output_csv_path, threshold):
    fields = ['Image Name', 'Latitude', 'Longitude', 'Vegetation Percentage']
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                image_rgb = load_and_convert_image(image_path)
                gcc = calculate_gcc(image_rgb)
                binary_gcc = apply_threshold(gcc, threshold)
                save_modified_image(binary_gcc, folder_path, filename)  # Save the modified image
                gps_data = get_gps_coordinates_with_exiftool(image_path)
                vegetation_percentage = calculate_vegetation_percentage(binary_gcc)
                writer.writerow({
                    'Image Name': filename,
                    'Latitude': gps_data.get('latitude', 'N/A'),
                    'Longitude': gps_data.get('longitude', 'N/A'),
                    'Vegetation Percentage': vegetation_percentage
                })

def gui():
    root = Tk()
    root.title("Vegetation Analysis Settings")

    def select_folder():
        folder = filedialog.askdirectory()
        folder_path_entry.delete(0, 'end')
        folder_path_entry.insert(0, folder)

    def select_output_file():
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        output_path_entry.delete(0, 'end')
        output_path_entry.insert(0, file)

    def start_processing():
        folder_path = folder_path_entry.get()
        output_path = output_path_entry.get()
        threshold = threshold_var.get()
        process_images(folder_path, output_path, threshold)
        Label(root, text="Processing Complete!").pack()

    Label(root, text="Select Folder Containing Images:").pack()
    folder_path_entry = Entry(root, width=50)
    folder_path_entry.pack()
    Button(root, text="Browse", command=select_folder).pack()

    Label(root, text="Select Output CSV File:").pack()
    output_path_entry = Entry(root, width=50)
    output_path_entry.pack()
    Button(root, text="Browse", command=select_output_file).pack()

    Label(root, text="Set GCC Threshold:").pack()
    threshold_var = IntVar(value=95)
    threshold_entry = Entry(root, textvariable=threshold_var, width=10)
    threshold_entry.pack()

    Button(root, text="Start Processing", command=start_processing).pack()

    root.mainloop()

if __name__ == "__main__":
    gui()
