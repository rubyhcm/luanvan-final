import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Define the tasks, start dates, and durations
tasks = [
    ("Nghiên cứu cơ sở lý thuyết", "2026-06-01", 30),
    ("Thu thập và chuẩn hóa dữ liệu", "2026-07-01", 30),
    ("Gán nhãn & Xây dựng màng lọc SLM", "2026-08-01", 30),
    ("Tích hợp Agent/LLM & RAG", "2026-09-01", 30),
    ("Đánh giá thực nghiệm", "2026-10-01", 30),
    ("Viết luận văn & Bảo vệ", "2026-11-01", 30)
]

fig, ax = plt.subplots(figsize=(10, 5))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
y_pos = range(len(tasks))

for i, (task, start_date, duration) in enumerate(tasks):
    start = mdates.datestr2num(start_date)
    width = duration
    ax.barh(i, width, left=start, color=colors[i], height=0.5, edgecolor='black', align='center')

ax.set_yticks(y_pos)
ax.set_yticklabels([t[0] for t in tasks])
ax.invert_yaxis()

ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator())

plt.title('Kế hoạch thực hiện đề tài trong 6 tháng', fontsize=14, pad=15)
plt.xlabel('Thời gian', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('gantt_chart.png', dpi=300)
