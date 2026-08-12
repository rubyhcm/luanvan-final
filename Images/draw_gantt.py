import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 13))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 28)
ax.axis('off')

# Grid lines
for x in range(4, 11):
    ax.axvline(x, color='#eeeeee', linewidth=1, zorder=0)

# X axis labels
months = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
for i, m in enumerate(months):
    ax.text(i + 4.5, 27, m, ha='center', va='center', fontweight='bold', fontsize=12)

ax.text(7, 28, 'Kế hoạch thực hiện trong 6 tháng', ha='center', va='center', fontweight='bold', fontsize=16)

y_current = 25.5

def draw_summary_task(start, end, y, height=0.4):
    top = y + height/2
    bottom = y - height/4
    point = y - height/2
    dx = 0.1
    verts = [
        (start, bottom),
        (start, top),
        (end, top),
        (end, bottom),
        (end, point),
        (end - dx, bottom),
        (start + dx, bottom),
        (start, point)
    ]
    poly = patches.Polygon(verts, facecolor='black', edgecolor='none', zorder=2)
    ax.add_patch(poly)

def add_parent(text, start, end):
    global y_current
    ax.text(0.1, y_current, text, ha='left', va='center', fontweight='bold', fontsize=11)
    draw_summary_task(start + 3, end + 3, y_current)
    y_current -= 1.1

def add_child(text, start, end):
    global y_current
    ax.text(0.3, y_current, text, ha='left', va='center', color='#555555', fontsize=11)
    rect = patches.Rectangle((start + 3, y_current - 0.2), end - start, 0.4, facecolor='#3498db', zorder=2)
    ax.add_patch(rect)
    y_current -= 1.1

# ----------------- CONTENT -----------------
add_parent("Nội dung 1: Nghiên cứu và Tiền xử lý dữ liệu", 1, 3)
add_child("Khảo sát các kỹ thuật phân tích log", 1, 1.5)
add_child("Thu thập dữ liệu chuẩn (LogHub, OpenStack)", 1.4, 2.0)
add_child("Làm sạch và phân cụm log (Sessionization)", 2.0, 2.6)
add_child("Che giấu dữ liệu nhạy cảm", 2.5, 3.0)

y_current -= 0.4

add_parent("Nội dung 2: Xây dựng và Tích hợp mô hình", 3, 5)
add_child("Gán nhãn dữ liệu (Weak supervision)", 3.0, 3.5)
add_child("Xây dựng mô hình màng lọc sơ bộ (SLM)", 3.4, 4.0)
add_child("Tích hợp Agent/LLM và RAG", 4.0, 4.6)
add_child("Hoàn thiện luồng phân tích chuyên sâu", 4.5, 5.0)

y_current -= 0.4

add_parent("Nội dung 3: Thực nghiệm và Đánh giá", 5, 6)
add_child("Chạy baseline cổ điển và Deep Learning", 5.0, 5.5)
add_child("Đánh giá chỉ số (Accuracy, FPR, Latency)", 5.3, 5.8)
add_child("Tối ưu hóa hiệu năng và độ chính xác", 5.6, 6.0)

y_current -= 0.4

add_parent("Nội dung 4: Tổng hợp và Viết báo cáo", 6, 7)
add_child("Phân tích lỗi và rút ra khuyến nghị", 6.0, 6.5)
add_child("Viết và chỉnh sửa báo cáo luận văn", 6.3, 7.0)

y_current -= 0.8

add_parent("Quá trình thực hiện", 1, 7)

y_current -= 0.8
ax.text(0.6, y_current, "Gặp giảng viên hướng dẫn", ha='left', va='center', fontstyle='italic', color='#555555', fontsize=11)
milestones_gv = [1.2, 2.2, 3.2, 4.5, 5.5, 6.8]
labels_gv = ["Lần 1", "Lần 2", "Lần 3", "Giữa kỳ", "Lần 4", "Cuối kỳ"]

for m, label in zip(milestones_gv, labels_gv):
    ax.plot(m + 3, y_current, marker='D', color='#e74c3c', markersize=8)
    ax.text(m + 3, y_current - 0.4, label, ha='center', va='top', fontsize=10)

y_current -= 1.3
ax.text(0.9, y_current, "Báo cáo tiến độ", ha='left', va='center', fontstyle='italic', color='#555555', fontsize=11)
milestones_bc = [1.7, 2.7, 3.7, 4.0, 5.0, 6.3]
for m in milestones_bc:
    ax.plot(m + 3, y_current, marker='D', color='#e74c3c', markersize=8)

plt.tight_layout()
plt.savefig('gantt_chart.png', dpi=300, bbox_inches='tight')
