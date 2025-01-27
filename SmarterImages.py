# Instructions:
# Create a folder and use script on the Desktop. I will use this created folder as my control box. 
# For validation, use an image that does not compromise your home location, submit into an online metadata reader, to see what is there now by default.
# or use https://github.com/ianare/exif-samples for some samples
# Next, put the image to be cleansed. Put that in the folder and run the script. 

#imports, fun fact you can watch the size of the file reduce in real time.

import os
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import messagebox

# define Function that gets source info to extract EXIF data from it
def get_exfDATA(image):
    try:
        exfDATA = image._getexif()
        if exfDATA is not None:
            exif_info = {}
            for tag, value in exfDATA.items():
                tag_name = ExifTags.TAGS.get(tag, tag)  # Get the human-readable tag name since the Exif Tags are not readable (idk it kinda works)
                exif_info[tag_name] = value 
            return exif_info
        else:
            return None
    except Exception as e:
        return f"Error reading EXIF data: {e}"

# Main function to wipe EXIF and process images
def wipe(input_folder, output_text, status_label):
    # Validation that the input is a folder directory
    if not os.path.isdir(input_folder):
        output_text.insert(tk.END, f"Error: Folder '{input_folder}' does not exist.\n")
        status_label.config(text="No Folder", fg="red")
        return

    # Process the first 100 image files with the given extensions
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][:100]

    for file_name in files:
        try:
            input_path = os.path.join(input_folder, file_name)

            # Get the original file size
            original_size = os.path.getsize(input_path)
            output_text.insert(tk.END, f"Original size of {file_name}: {original_size / 1024:.2f} KB\n")
            
            # Open the imagez
            with Image.open(input_path) as img:
                # Extract and display EXIF data
                exif_info = get_exfDATA(img)
                if exif_info:
                    output_text.insert(tk.END, f"EXIF data for {file_name}:\n")
                    for tag_name, value in exif_info.items():
                        output_text.insert(tk.END, f"{tag_name}: {value}\n")
                else:
                    output_text.insert(tk.END, f"No EXIF data found for {file_name}\n")

                # Save the image to a temporary file (wipes the EXIF valuez)
                temp_path = os.path.join(input_folder, f"{os.path.splitext(file_name)[0]}_temp{os.path.splitext(file_name)[1]}")
                img.save(temp_path)
                output_text.insert(tk.END, f"Saved without EXIF: {temp_path}\n")
                
                # Replace the original file by renaming the temporary file back to the original name (finalized the wipe)
                os.replace(temp_path, input_path)
                output_text.insert(tk.END, f"Replaced original: {input_path}\n")

            # Get the new file size after processing
            new_size = os.path.getsize(input_path)
            output_text.insert(tk.END, f"New size of {file_name}: {new_size / 1024:.2f} KB\n")
            output_text.insert(tk.END, "-" * 50 + "\n")

            # After processing, the gui will update status unless there was a processing error.
            # NOTE: its just confirms the proccess finished, this is non-specific error handling.
            status_label.config(text="✔", fg="green")

        except Exception as e:
            output_text.insert(tk.END, f"Error processing file '{file_name}': {e}\n")
            status_label.config(text="X", fg="red")

# Create the GUI window;
def create_gui():
    root = tk.Tk()
    # Window Title & Size
    root.title("Smarter Images")
    root.geometry("1000x500")

    # asks for folder input (this is the input box)
    folder_label = tk.Label(root, text="Enter Folder Path:")
    folder_label.pack(pady=5)
    folder_entry = tk.Entry(root, width=50)
    folder_entry.pack(pady=5)

    # Pre-fill the entry field with a default windows directory that user can change on the fly
    folder_entry.insert(0, "C:/Users/ExampleUsername/Desktop/folder")  # Set default path here

    # Output box for history of changes and statistics on the process
    output_text = tk.Text(root, height=15, width=120)
    output_text.pack(pady=10)

    # Frame for the checkmark and start button
    action_frame = tk.Frame(root)
    action_frame.pack(pady=5)

    # Status label for validation
    status_label = tk.Label(action_frame, text="❌", font=('Arial', 20), fg="red")
    status_label.pack(side=tk.LEFT, padx=10)

    # Submit button
    def on_submit():
        folder_path = folder_entry.get()
        output_text.delete(1.0, tk.END)  # Clear the output box
        wipe(folder_path, output_text, status_label)

    submit_button = tk.Button(action_frame, text="Start", command=on_submit)
    submit_button.pack(side=tk.LEFT)

    # Start the GUI loop
    root.mainloop()

# Run the GUI
create_gui()
