import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread


class DownloadManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Download Manager")
        self.window.geometry("400x150")
        self.window.configure(bg="black")

        self.url_entry = tk.Entry(self.window, width=40)
        self.url_entry.pack(pady=10)

        self.start_button = tk.Button(
            self.window, text="Start Download", command=self.start_download
        )
        self.start_button.pack()

        self.progress_bar = tk.Label(
            self.window, text="", relief=tk.SUNKEN, anchor=tk.W, width=50
        )
        self.progress_bar.pack(pady=10)

        self.download_speed = tk.Label(self.window, text="")
        self.download_speed.pack()

        self.menu = tk.Menu(self.window)
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.settings_menu.add_command(label="Switch to Light Mode", command=self.light_mode)
        self.settings_menu.add_command(label="Switch to Dark Mode", command=self.dark_mode)
        self.settings_menu.add_command(label="Change Download Location", command=self.change_download_location)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.window.config(menu=self.menu)

        self.download_location = self.get_default_download_location()
        self.dark_mode()

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showinfo("Error", "Please enter a valid URL.")
            return

        download_thread = Thread(target=self.download_file, args=(url,))
        download_thread.start()

    def download_file(self, url):
        command = f'wget "{url}" -P "{self.download_location}"'
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        while process.poll() is None:
            output = process.stderr.readline().decode("utf-8").strip()
            if output.startswith("Saving to:"):
                file_name = output[11:]
                self.window.title(f"Download Manager - {file_name}")
            elif output.startswith("Length:"):
                file_size = output[8:].split()[0]
            elif output.startswith("100%"):
                self.progress_bar.config(text="Download complete!")
            elif output.startswith(" "):
                download_speed = output.split()[1]
                self.download_speed.config(text=f"Download Speed: {download_speed}B/s")
            else:
                self.progress_bar.config(text=output)

    def get_default_download_location(self):
        return filedialog.askdirectory()

    def change_download_location(self):
        self.download_location = self.get_default_download_location()

    def light_mode(self):
        self.window.config(bg="white")
        self.progress_bar.config(bg="white", fg="black")
        self.download_speed.config(bg="white", fg="black")

    def dark_mode(self):
        self.window.config(bg="black")
        self.progress_bar.config(bg="black", fg="white")
        self.download_speed.config(bg="black", fg="white")


if __name__ == "__main__":
    app = DownloadManager()
    app.window.mainloop()


