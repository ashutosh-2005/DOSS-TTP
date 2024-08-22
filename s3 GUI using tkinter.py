import boto3
from tkinter import *
from tkinter import filedialog, messagebox

# Initialize the Tkinter window
root = Tk()
root.title("Amazon S3 GUI")
root.geometry("400x300")

# Set up S3 client
s3 = boto3.client('s3')

# Function to upload a file to S3
def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        bucket_name = "your-bucket-name"  # Replace with your S3 bucket name
        file_name = file_path.split('/')[-1]
        try:
            s3.upload_file(file_path, bucket_name, file_name)
            messagebox.showinfo("Success", "File uploaded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Function to download a file from S3
def download_file():
    bucket_name = "your-bucket-name"  # Replace with your S3 bucket name
    file_name = "file-name-in-s3"  # Replace with the S3 file name to download
    save_path = filedialog.asksaveasfilename()
    if save_path:
        try:
            s3.download_file(bucket_name, file_name, save_path)
            messagebox.showinfo("Success", "File downloaded successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create buttons for uploading and downloading files
upload_button = Button(root, text="Upload File", command=upload_file)
download_button = Button(root, text="Download File", command=download_file)

# Place buttons on the window
upload_button.pack(pady=10)
download_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
