import tkinter as tk
from tkinter import messagebox, filedialog
import yagmail
import time
import webbrowser
import os

print("UI của tool có thể bị đơ khi chọn gửi nhiều mail")
print("Cái này tôi không fix dc! khi có tb (Python is not responding), làm ơn đừng tắt vì tool đang chạy! ")

file_path = "miku.txt"

def send_email():
    sender_email = sender_entry.get()
    app_password = password_entry.get()
    receiver_email = receiver_entry.get()
    subject = subject_entry.get()
    content = email_body_text.get("1.0", tk.END).strip()
    
    attachments = attached_files 
    
    try:
        yag = yagmail.SMTP(user=sender_email, password=app_password)
        yag.send(to=receiver_email, subject=subject, contents=content, attachments=attachments)
        messagebox.showinfo("Thành công", "Thư đã được gửi!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể gửi : {e}")

def send_bulk_emails(sender_email, app_password, receiver_email, subject, content, attachments, count, delay):
    try:
        root.withdraw()
        
        yag = yagmail.SMTP(user=sender_email, password=app_password)
        for i in range(count):
            yag.send(to=receiver_email, subject=f"{subject} (#{i + 1})", contents=content, attachments=attachments)
            print(f"\rĐã gửi {i + 1}/{count} - để dừng vui lòng bấm Ctrl+C 2 lần", end="", flush=True)
            time.sleep(delay)
        
        root.deiconify()  
        messagebox.showinfo("Thành công", f"{count} thư đã được gửi!")
    except Exception as e:
        root.deiconify()  
        print(f"Lỗi: {e}")
        messagebox.showerror("Lỗi", f"Không thể gửi: {e}")

def open_link():
    webbrowser.open("https://myaccount.google.com/apppasswords")

def open_bulk_email_window():
    bulk_window = tk.Toplevel(root)
    bulk_window.title("Gửi Nhiều Thư")
    bulk_window.geometry("350x280")

    tk.Label(bulk_window, text="số lượng:").pack(anchor=tk.W, padx=10, pady=5)
    count_entry = tk.Entry(bulk_window, width=30)
    count_entry.pack(padx=10)

    tk.Label(bulk_window, text="thời gian delay thư (giây):").pack(anchor=tk.W, padx=10, pady=5)
    delay_entry = tk.Entry(bulk_window, width=30)
    delay_entry.pack(padx=10)

    warning_label = tk.Label(bulk_window, text="", fg="red")
    warning_label.pack(pady=5)

    def validate_delay():
        try:
            delay = float(delay_entry.get())
            if delay < 1:
                raise ValueError("Thời gian phải lớn hơn hoặc bằng 1 giây.")
            warning_label.config(text="")  
        except ValueError:
            warning_label.config(text="Vui lòng nhập số lớn hơn hoặc bằng 1 giây.")
            delay_entry.focus_set()  

    delay_entry.bind("<FocusOut>", validate_delay)

    def bulk_send():
        try:
            count = int(count_entry.get())
            delay = float(delay_entry.get())
            if delay < 1:
                raise ValueError("Thời gian phải lớn hơn hoặc bằng 1 giây.")
            send_bulk_emails(
                sender_entry.get(),
                password_entry.get(),
                receiver_entry.get(),
                subject_entry.get(),
                email_body_text.get("1.0", tk.END).strip(),
                attached_files,
                count,
                delay
            )
            start_countdown(5)  
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng và thời gian hợp lệ.")

    send_button = tk.Button(bulk_window, text="Spam Thư", command=bulk_send, bg="lightblue")
    send_button.pack(pady=20)

    countdown_label = tk.Label(bulk_window, text="", font=("Arial", 12), fg="red")
    countdown_label.pack(pady=10)

    def start_countdown(seconds):
        if seconds > 0:
            countdown_label.config(text=f"Đóng cửa sổ sau {seconds} giây...")
            bulk_window.after(1000, start_countdown, seconds - 1)
        else:
            bulk_window.destroy()  

def attach_files():
    files = filedialog.askopenfilenames(title="Chọn tệp đính kèm")
    if files:
        for file in files:
            if file not in attached_files:
                attached_files.append(file)
                files_listbox.insert(tk.END, file)

def find_and_open_txt_file():
    current_directory = os.path.dirname(os.path.realpath(__file__))

    for filename in os.listdir(current_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(current_directory, filename)
            os.startfile(file_path)
            return  
        
def remove_selected_files():
    selected_indices = list(files_listbox.curselection())
    selected_indices.reverse() 
    for index in selected_indices:
        attached_files.pop(index)
        files_listbox.delete(index)

def open_txt_file():
    if os.path.exists(file_path):
        os.startfile(file_path)  

attached_files = []

# main
root = tk.Tk()
root.title("Spam email")
window_width = 400
window_height = 680
root.resizable(False, False)  # disable maximize
common_width = 70

open_txt_file()
# UI main
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

find_and_open_txt_file()

tk.Label(root, text="mail gửi:").pack(anchor=tk.W, padx=10, pady=5)
sender_entry = tk.Entry(root, width=common_width)
sender_entry.pack(padx=10)

tk.Label(root, text="mk ứng dụng:").pack(anchor=tk.W, padx=10, pady=5)
password_entry = tk.Entry(root, width=common_width, show="*")
password_entry.pack(padx=10)

button = tk.Button(root, text="lấy mk ứng dụng ở đây", command=open_link, bg="lightblue", font=("Arial", 12))
button.pack(pady=10)

tk.Label(root, text="email nhận:").pack(anchor=tk.W, padx=10, pady=5)
receiver_entry = tk.Entry(root, width=common_width)
receiver_entry.pack(padx=10)

tk.Label(root, text="tiêu đề email:").pack(anchor=tk.W, padx=10, pady=5)
subject_entry = tk.Entry(root, width=common_width)
subject_entry.pack(padx=10)

tk.Label(root, text="nội dung email:").pack(anchor=tk.W, padx=10, pady=5)
email_body_text = tk.Text(root, width=common_width, height=10)
email_body_text.pack(padx=10, pady=5)

attach_button = tk.Button(root, text="đính kèm tệp (ảnh, zip,......)", command=attach_files, bg="lightgreen")
attach_button.pack(pady=10)

files_frame = tk.Frame(root)
files_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

files_listbox = tk.Listbox(files_frame, selectmode=tk.MULTIPLE, width=common_width, height=2)
files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(files_frame, orient="vertical")
scrollbar.config(command=files_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

files_listbox.config(yscrollcommand=scrollbar.set)

remove_button = tk.Button(root, text="xóa tệp đã chọn", command=remove_selected_files, bg="salmon")
remove_button.pack(pady=5)

send_button = tk.Button(root, text="gửi Email (test only)", command=send_email, bg="lightblue")
send_button.pack(pady=5)

bulk_send_button = tk.Button(root, text="spam email", command=open_bulk_email_window, bg="orange")
bulk_send_button.pack(pady=5)

# run
root.mainloop()


