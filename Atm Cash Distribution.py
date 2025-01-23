import tkinter as tk
from tkinter import messagebox
import random
import networkx as nx
import datetime
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# تعداد گره‌ها (ATMها) و مسیرها (یال‌ها)
num_atms = random.randint(5, 15)
graph = nx.Graph()

# ساخت گراف با گره‌ها و مسیرهای تصادفی
for i in range(num_atms):
    graph.add_node(i)

# اضافه کردن یال‌ها به گراف با مسافت‌های تصادفی (1 تا 20 کیلومتر)
for i in range(num_atms):
    for j in range(i + 1, num_atms):
        if random.random() < 0.4:  # 40% احتمال برای اضافه کردن یال
            weight = random.randint(1, 20)
            graph.add_edge(i, j, weight=weight)

# انتخاب دستگاه‌های اولویت‌دار به صورت تصادفی
priority_atms = random.sample(range(num_atms), random.randint(2, 4))

# انتخاب دستگاه‌های معمولی (غیر از دستگاه‌های اولویت‌دار)
regular_atms = [atm for atm in range(num_atms) if atm not in priority_atms]

# انتخاب گره ابتدایی (کامیون حمل پول)
start_node = random.choice(range(num_atms))
current_node = start_node

# ثبت آمار دستگاه‌های سرویس شده
priority_atms_serviced = []
regular_atms_serviced = []

# ثبت آمار دزدی
theft_logs = []

# زمان شروع پر کردن دستگاه‌ها
start_time = datetime.datetime.now()

# تابع برای محاسبه زمان سفر بین دو گره
def calculate_travel_time(current, next_node):
    distance = graph[current][next_node]["weight"]
    # سرعت کامیون 60 کیلومتر در ساعت
    travel_time = distance / 60  # زمان سفر به ساعت
    return travel_time

# تابع برای پر کردن دستگاه‌ها
def service_atm(atm, current_time):
    service_time = 0.5  # 30 دقیقه برای پر کردن هر دستگاه
    service_end_time = current_time + datetime.timedelta(hours=service_time)
    return service_end_time

# تابع برای پیدا کردن کوتاه‌ترین مسیر از گره کنونی به هدف
def shortest_path(current, target):
    return nx.shortest_path(graph, source=current, target=target, weight='weight')

# شبیه‌سازی حرکت کامیون
current_time = start_time
visited_nodes = []  # برای ذخیره گره‌های طی‌شده
while len(priority_atms_serviced) < len(priority_atms):
    for atm in priority_atms:
        if atm not in priority_atms_serviced:
            path = shortest_path(current_node, atm)
            visited_nodes.extend(path)
            current_time = service_atm(atm, current_time)
            priority_atms_serviced.append((atm, current_time, path))
            current_node = atm

while len(priority_atms_serviced) + len(regular_atms_serviced) < num_atms:
    for atm in regular_atms:
        if atm not in regular_atms_serviced:
            path = shortest_path(current_node, atm)
            visited_nodes.extend(path)
            current_time = service_atm(atm, current_time)
            regular_atms_serviced.append((atm, current_time, path))
            current_node = atm

# شبیه‌سازی دزدی‌ها
time_left_for_theft = 3  # دزدها پس از 3 ساعت شروع به سرقت می‌کنند
time_after_service = current_time + datetime.timedelta(hours=time_left_for_theft)

# شبیه‌سازی دزدی‌ها
theft_time = time_after_service
for atm, _, _ in priority_atms_serviced + regular_atms_serviced:
    # دزدی از هر دستگاه 1 ساعت زمان می‌برد
    theft_end_time = theft_time + datetime.timedelta(hours=1)
    # انتخاب مسیر تصادفی
    theft_path = random.sample(visited_nodes, len(visited_nodes) // 2)
    theft_logs.append((atm, theft_end_time, theft_path))
    theft_time = theft_end_time

# ذخیره آمار سرویس دستگاه‌ها در فایل CSV
header_service = ['ATM', 'Time Served', 'Path']
data_service = []

# جمع آوری داده‌ها از دستگاه‌های سرویس شده
for atm, time, path in priority_atms_serviced + regular_atms_serviced:
    data_service.append([atm, time.strftime('%H:%M:%S'), ' -> '.join(map(str, path))])

# ذخیره داده‌ها در یک فایل CSV
with open('atm_service_log.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header_service)
    writer.writerows(data_service)

# ذخیره آمار دزدی در فایل CSV
header_theft = ['ATM', 'Time of Theft', 'Path']
data_theft = []

# جمع آوری داده‌ها از دزدی‌ها
for atm, time, path in theft_logs:
    data_theft.append([atm, time.strftime('%H:%M:%S'), ' -> '.join(map(str, path))])

# ذخیره داده‌ها در یک فایل CSV
with open('atm_theft_log.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header_theft)
    writer.writerows(data_theft)

# خواندن آمار از فایل CSV
def read_service_log():
    with open('atm_service_log.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # پرش از خط عنوان
        return list(reader)

# خواندن آمار دزدی از فایل CSV
def read_theft_log():
    with open('atm_theft_log.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # پرش از خط عنوان
        return list(reader)

# نمایش آمار سرویس‌ها در GUI
def display_service_log():
    # خواندن داده‌ها از فایل
    data = read_service_log()

    # ایجاد پنجره جدید برای نمایش آمار
    log_window = tk.Toplevel(root)
    log_window.title("Service Log")

    # ایجاد لیست برای نمایش داده‌ها
    listbox = tk.Listbox(log_window, width=50, height=10)
    listbox.pack(pady=10)

    # اضافه کردن داده‌ها به لیست
    for row in data:
        listbox.insert(tk.END, f"ATM {row[0]} - Time: {row[1]} - Path: {row[2]}")

# نمایش آمار دزدی‌ها در GUI
def display_theft_log():
    # خواندن داده‌ها از فایل
    data = read_theft_log()

    # ایجاد پنجره جدید برای نمایش آمار
    theft_window = tk.Toplevel(root)
    theft_window.title("Theft Log")

    # ایجاد لیست برای نمایش داده‌ها
    listbox = tk.Listbox(theft_window, width=50, height=10)
    listbox.pack(pady=10)

    # اضافه کردن داده‌ها به لیست
    for row in data:
        listbox.insert(tk.END, f"ATM {row[0]} - Theft Time: {row[1]} - Path: {row[2]}")

# ایجاد پنجره Tkinter
root = tk.Tk()
root.title("ATM Network")

# تابع برای نمایش گراف
def show_graph():
    # ترسیم گراف با matplotlib
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph)  # چیدمان گراف
    # تنظیم رنگ گره‌ها: گره‌های اولویت‌دار با رنگ قرمز، بقیه با رنگ آبی
    node_colors = ['red' if node in priority_atms else 'skyblue' for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_weight="bold", edge_color="gray")

    # نمایش وزن یال‌ها (مسافت‌ها)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    # ترسیم درون Tkinter
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)  # ارتباط matplotlib با Tkinter
    canvas.draw()
    canvas.get_tk_widget().pack()

# دکمه نمایش گراف
button_show_graph = tk.Button(root, text="نمایش گراف ATM‌ها", command=show_graph)
button_show_graph.pack(pady=10)

# دکمه نمایش آمار سرویس‌ها
button_display_log = tk.Button(root, text="نمایش آمار سرویس‌ها", command=display_service_log)
button_display_log.pack(pady=10)

# دکمه نمایش آمار دزدی‌ها
button_display_theft_log = tk.Button(root, text="نمایش آمار دزدی‌ها", command=display_theft_log)
button_display_theft_log.pack(pady=10)

# اجرای پنجره
root.mainloop()
