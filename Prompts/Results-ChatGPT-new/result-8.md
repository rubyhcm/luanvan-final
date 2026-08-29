# Thực thi thí nghiệm kiểm chứng cải tiến mục tiêu

## 1. Mục tiêu thí nghiệm và độ truy vết
Bảng dưới đây liên kết các Câu hỏi/Nghiên cứu (RQ/H) với thí nghiệm, chỉ số chính và bằng chứng kỳ vọng: 

| Phần tử nghiên cứu | Thí nghiệm         | Chỉ số chính                | Bằng chứng kỳ vọng                                  |
|--------------------|---------------------|-----------------------------|-----------------------------------------------------|
| RQ1               | E2 (So sánh chính)  | Precision, Recall, F1, AUC  | Phương pháp cải tiến đạt F1/AUC cao hơn baseline.   |
| RQ2               | E3 (Phát hiện sớm)  | Thời gian phát hiện (Lead Time), Tỷ lệ cảnh báo sớm | Cải tiến cho kết quả cảnh báo sớm tốt hơn (thời gian phát hiện giảm, tỷ lệ cảnh báo sớm tăng). |
| RQ3               | E7 (Đa tập dữ liệu) | Precision, Recall, F1 trên tập dữ liệu ngoài | Cải tiến duy trì hiệu năng tốt trên tập dữ liệu mới (không suy giảm đáng kể). |
| H1                | E2                  | F1, ROC-AUC                 | Cải tiến cải thiện đáng kể F1/AUC so với baseline.  |
| H2                | E3                  | Thời gian phát hiện        | Cải tiến rút ngắn thời gian phát hiện trung bình.   |
| H3                | E7/E5               | F1 or Robustness           | Cải tiến duy trì hiệu quả (F1) trong điều kiện thử nghiệm bổ sung. |

Trong đó, **E2** là thí nghiệm so sánh chính giữa baseline và baseline+cải tiến; **E3** đánh giá phát hiện sớm; **E7** đánh giá tính tổng quát trên hệ thống/dữ liệu khác; **E5** đánh giá độ bền khi có nhiễu/biến đổi. Mỗi RQ/H yêu cầu thí nghiệm tương ứng để kiểm chứng. 

## 2. Môi trường thí nghiệm
- **Phần cứng:** Ví dụ, CPU Intel Xeon, GPU NVIDIA (ít nhất 1–2 GPU hiện đại như Tesla V100/A100), RAM ≥128 GB, ổ cứng SSD ≥1 TB.  
- **Phần mềm:** Hệ điều hành Linux (Ubuntu 20.04+), Python 3.x (>=3.8), thư viện ML (PyTorch 2.x hoặc TensorFlow 2.x), mô-đun NLP (HuggingFace Transformers nếu dùng LLM), công cụ xử lý dữ liệu (scikit-learn, pandas), cơ sở dữ liệu/inverted-index (FAISS, Elasticsearch) cho RAG nếu cần. Phiên bản CUDA/CUDNN phù hợp với GPU. Mọi thư viện/language runtime dùng kèm `requirements.txt` hay `conda` để xác định phiên bản cụ thể.  
- **Theo dõi thí nghiệm:** (nếu có) sử dụng công cụ như MLflow hoặc Weights & Biases để log kết quả mỗi lần chạy.  

Tất cả các bước được **ghi chép chi tiết** (từ commit mã nguồn cho đến cấu hình môi trường) để đảm bảo khả năng tái lập. Theo hướng dẫn của IEEE, bài nghiên cứu cần mô tả **chi tiết phương pháp** và chia sẻ dữ liệu/mã nguồn để người khác có thể tái lập kết quả.  

## 3. Bộ dữ liệu và phân chia
- **Nguồn dữ liệu:** Sử dụng tập log sự kiện thật hoặc chuẩn (theo baseline). Ví dụ có thể là log hệ thống HDFS, BGL, Thunderbird,… (dựa trên tài liệu thiết kế).  
- **Mục đích và phân chia:** Chia dữ liệu thành tập huấn luyện (chỉ log bình thường), tập kiểm định (tinh chỉnh ngưỡng, chưa dùng trong huấn luyện), và tập kiểm tra (gồm cả log bất thường). Ngoài ra có thể có tập kiểm tra ngoài (external) nếu có sẵn. Chú ý phân chia theo thời gian: ví dụ *train* lấy log đến thời điểm T, *test* lấy log sau đó để tránh trích xuất thông tin tương lai.  
- **Chi tiết dữ liệu:** Ghi rõ quy mô (số bản ghi), loại log (hệ điều hành, ứng dụng), loại bất thường (thất bại hệ thống, lỗ hổng, tấn công), đặc tính thời gian (tần suất log, cửa sổ thời gian). Mục tiêu là đảm bảo **điều kiện sớm phát hiện**: không sử dụng thông tin từ tương lai (no leakage). Nếu bộ dữ liệu không hỗ trợ tình huống phát hiện sớm thực thụ, cần ghi rõ hạn chế này.  

## 4. Baseline và so sánh công bằng
- **Baseline chính:** Là phương pháp Q1/Q2 đã chọn (theo `result-4/5`). Ghi rõ cấu hình: commit/code cụ thể, quy trình tiền xử lý, mô hình/mạng thần kinh, tham số, ngưỡng kích hoạt. Kết quả đã báo cáo ban đầu (trên dataset chuẩn) và kết quả tái lập (nếu có).  
- **So sánh có kiểm soát:** Luôn giữ cố định tối đa các yếu tố ngoại trừ phần cải tiến mục tiêu. Cụ thể, giữa A (baseline gốc) và B (baseline + cải tiến), sử dụng cùng tập dữ liệu, cùng split, cùng tiền xử lý, cùng kiến trúc mô hình (như kích thước, loại thuật toán), cùng phần prompt (nếu LLM), cùng phần cài đặt phần cứng và phần mềm. Việc tăng thêm thành phần cải tiến (ví dụ thành phần RAG) sẽ không thay đổi các thành phần khác. Nếu có sự khác biệt nào trong cài đặt (ví dụ thuật toán cải tiến yêu cầu tham số thêm), cần giải thích rõ và phân tích tác động. Các baseline phụ chỉ dùng khi cần so sánh ngữ cảnh hoặc kiểm tra bổ trợ.  

## 5. Các kịch bản thí nghiệm
Mô tả các thí nghiệm chính (theo E1–E7):  
- **E1 – Tái lập baseline:** Chạy lại baseline nguyên gốc để xác nhận kết quả báo cáo và tạo benchmark tham chiếu.  
- **E2 – Kiểm thử cải tiến chính:** Thử nghiệm so sánh trực tiếp Baseline vs Baseline+Improv. Đây là thí nghiệm trung tâm để kiểm tra cải tiến có tác dụng lên RQ1 (hiệu năng chung).  
- **E3 – Phát hiện sớm:** Đánh giá khả năng phát hiện trước sự cố: ví dụ đo thời gian Lead Time so với mốc thực sự. So sánh Baseline vs Baseline+Improv về tỷ lệ cảnh báo trước xác nhận sự cố.  
- **E4 – Ablation:** Thực hiện các biến thể: Baseline + đầy đủ cải tiến, Baseline + các phần cải tiến bị loại bỏ một phần. Mục tiêu chứng minh thành phần mới đóng góp như thế nào.  
- **E5 – Độ bền (Robustness):** Thử các trường hợp nhiễu liên quan đến giới hạn đã xác nhận: thêm nhiễu ngẫu nhiên, bớt dữ liệu quan trọng, sửa đổi định dạng log, shift thời gian, nhiễu truy vấn RAG, giảm kích thước ngữ cảnh,… Chỉ tập trung vào các thay đổi liên quan giới hạn đã đề cập.  
- **E6 – Hiệu quả/Tính toán:** Đánh giá chi phí thêm: độ trễ, công suất xử lý, bộ nhớ, chi phí token (nếu dùng LLM) khi thêm cải tiến.  
- **E7 – Tổng quát hóa (Generalization):** Đánh giá trên hệ thống hoặc bộ dữ liệu khác. Kiểm tra xem cải tiến có vẫn giữ lợi ích khi chuyển sang ngữ cảnh khác hay không.  

## 6. Các chỉ số đánh giá
- **Phát hiện bất thường:** Precision, Recall, F1-score, PR-AUC. Khi phù hợp, có thể đo thêm ROC-AUC. F1 là chỉ số chính cho RQ1 nếu liên quan đến hiệu năng chung.  
- **Phát hiện sớm:** Các chỉ số thời gian (Time-to-Detection, Detection Lead Time), tỷ lệ cảnh báo trước (Early Warning Rate), độ chính xác cảnh báo sớm (Detection Before Failure), tỷ lệ báo động giả (False Alarm Rate). Những chỉ số này đặc thù cho RQ2, và không dùng F1 đơn độc để đánh giá phát hiện sớm.  
- **Hiệu suất:** Khi cần, đo độ trễ trung bình, số token (LLM), thời gian truy vấn và tổng thời gian, tài nguyên GPU, throughput. Những chỉ số này phục vụ đánh giá E6.  
- **Thành phần cải tiến (nếu cần):** Ví dụ nếu dùng RAG: Recall@k, Precision@k, MRR/ngDCG cho retriever; tỷ lệ hallucination, độ nhất quán của LLM nếu có thành phần tạo sinh. Chỉ tính khi liên quan đến giả thuyết cụ thể.  

## 7. Phân tích thống kê
Thiết kế thí nghiệm phải **lặp nhiều lần** (ví dụ chạy ngẫu nhiên nhiều seed) để thu thập biến thiên. Báo cáo độ lệch chuẩn hoặc khoảng tin cậy (confidence interval) của các chỉ số chính. Thực hiện kiểm định có phù hợp (paired t-test hoặc Wilcoxon, tùy phân phối) giữa A và B để đánh giá ý nghĩa thống kê. Nếu nhiều kiểm định được thực hiện, áp dụng hiệu chỉnh đa so sánh (như Bonferroni). Cố gắng **cố định mọi yếu tố ngẫu nhiên** (seed cố định, nhiệt độ trên LLM cố định nếu có). Kết quả sẽ kèm phân tích độ biến thiên và giá trị p để khẳng định tính đáng kể. Theo khuyến cáo của NeurIPS, kết quả chính cần có sai số hoặc CI để hỗ trợ quyết định.  

## 8. Tiêu chí thành công
- **Tiêu chí chính:** Chọn một chỉ số trực tiếp phản ánh giới hạn đã xác nhận (ví dụ F1 nếu giới hạn là hiệu năng chung). Cải tiến thành công nếu có cải thiện đáng kể (đáng kể thống kê hoặc vượt ngưỡng thực tiễn) trên chỉ số này so với baseline.  
- **Tiêu chí phụ:** Bao gồm các chỉ số phát hiện sớm, tính ổn định, hiệu quả tính toán, tính tổng quát. Ví dụ cải tiến không làm tăng đáng kể tỷ lệ báo động giả hoặc chi phí tính toán quá cao.  
- **Quy tắc đánh đổi:** Không coi cải tiến tốt hơn chỉ vì F1 tăng nếu kèm theo độ trễ tăng quá mức, hoặc báo động giả tăng đáng kể, hoặc suy giảm khả năng tổng quát. Không đặt ngưỡng tùy ý nếu không có cơ sở trước; mọi tiêu chí cụ thể sẽ được xác định rõ trong phạm vi báo cáo thí nghiệm.  

## 9. Kịch bản Ablation
Nếu cải tiến bao gồm nhiều thành phần, xây dựng kịch bản ablation:  
- **Baseline gốc;**  
- **Baseline + toàn bộ cải tiến;**  
- **Baseline + loại bỏ từng thành phần con (nếu khả thi).**  
Mục tiêu chứng minh lợi ích thu được chỉ đến từ thành phần **cải tiến mục tiêu**. Ví dụ nếu dùng RAG, có thể thử với retriever tần suất thấp hoặc không dùng retriever để thấy giảm hiệu năng.  

## 10. Phân tích lỗi
Phân tích các lỗi xảy ra để hiểu sâu:  
- **False Positive:** Log bình thường bị gắn nhãn bất thường;  
- **False Negative:** Log bất thường bị bỏ sót;  
- **Miss/Delay phát hiện sớm:** Sự cố xảy ra nhưng model báo muộn;  
- **Retrieval/Context Failure:** Đầu vào truy vấn RAG không tìm ra thông tin đúng;  
- **LLM/Hallucination Failure:** LLM tạo ra thông tin sai/vô ích;  
- **Knowledge Gap:** Thiếu thông tin trong corpus/ngữ cảnh.  

Với mỗi trường hợp: xác định điều kiện xuất hiện lỗi, bối cảnh, nguyên nhân gốc rễ (ví dụ lỗi tiền xử lý, ngưỡng không phù hợp, model suy yếu), ảnh hưởng đến giả thuyết. Không coi việc phân tích lỗi là phương pháp mới, mà dùng để giải thích kết quả.  

## 11. Phân tích độ bền (Robustness)
Chỉ xem xét các biến đổi liên quan đến giới hạn được xác nhận. Ví dụ:  
- Thêm nhiễu (noise) vào log;  
- Bỏ bớt sự kiện (missing events);  
- Xuất hiện pattern mới (chưa gặp trước);  
- Shifts theo thời gian (temporal concept drift);  
- Nhiễu trong thành phần truy vấn RAG;  
- Giảm thông tin ngữ cảnh (cắt bớt history).  

Đánh giá xem cải tiến có duy trì hiệu năng hay không dưới các điều kiện này.  

## 12. Phân tích hiệu quả và chi phí
Nếu cải tiến sử dụng LLM/RAG/cơ chế nhớ, đo chi phí đi kèm: độ trễ inference, số token gọi API, thời gian truy vấn RAG, số lần gọi mô hình, mức sử dụng GPU/bộ nhớ, tính toán cộng thêm. So sánh với baseline gốc để đánh giá trade-off chi phí – lợi ích.  

## 13. Quy trình tái lập
Mọi thí nghiệm ghi lại đầy đủ cấu hình: seed ngẫu nhiên, phiên bản tập dữ liệu và split, commit hoặc tag của mã nguồn baseline và mã cải tiến, phiên bản mô hình (có thể dùng pretrained hoặc tham số checkpoint), phiên bản các thư viện, cấu hình prompt và RAG (corpus, chỉ mục, retriever). Nếu dùng API/Mô hình bên ngoài, lưu thông tin provider và phiên bản model (nhưng không lưu key). Mọi thông số experimental (ngưỡng phân lớp, chính sách dừng) cũng được ghi. Theo hướng dẫn của NeurIPS và IEEE, bài sẽ công khai chi tiết thiết lập để đảm bảo tái lập.  

## 14. Ma trận thí nghiệm

| Thí nghiệm | Baseline | Cải tiến  | Mục đích chính        |
|-----------|:--------:|:--------:|-----------------------|
| E1        | ✓       |          | Tái lập baseline      |
| E2        | ✓       | ✓        | So sánh chính         |
| E3        | ✓       | ✓        | Phát hiện sớm         |
| E4        | ✓       | ✓/partial| Ablation              |
| E5        | ✓       | ✓        | Độ bền (Robustness)   |
| E6        | ✓       | ✓        | Hiệu quả/Chi phí      |
| E7        | ✓       | ✓        | Tổng quát hóa         |

## 15. Mẫu báo cáo kết quả
1. Tái lập baseline  
2. So sánh chính (Baseline vs Cải tiến)  
3. Phát hiện sớm  
4. Ablation  
5. Độ bền  
6. Hiệu quả/Chi phí  
7. Bằng chứng thống kê  
8. Phân tích lỗi  
9. Hạn chế (nếu có)  

## 16. Quy tắc diễn giải
- **Supported (Được hỗ trợ):** Có bằng chứng đủ mạnh.  
- **Weakly Supported (Hỗ trợ yếu):** Có tín hiệu nhưng bằng chứng/lỗi biến thiên lớn.  
- **Not Supported (Không chứng minh):** Không có bằng chứng.  
- **Contradicted (Phủ định):** Cải tiến làm kết quả tệ đi.  

Không kết luận cải tiến tốt hơn chỉ dựa trên một metric hoặc một bộ dữ liệu duy nhất. Nếu cải tiến không hiệu quả, vẫn báo cáo trung thực, phân tích nguyên nhân.  

## 17. Nguy cơ của thí nghiệm
- **Nội bộ:** Sai khác triển khai, điều chỉnh không công bằng, rò rỉ dữ liệu, cấu hình khác biệt. (Giảm thiểu: dùng cùng mã, seed, tách dữ liệu theo thời gian nghiêm ngặt.)  
- **Ngoại vi:** Giới hạn dữ liệu/tập benchmark, kết quả có thể không tổng quát cho mọi hệ thống.  
- **Xây dựng:** Các metric hoặc nhãn có thể không phản ánh đúng khái niệm Phát hiện sớm.  
- **Kết luận:** Số lần chạy quá ít, biến thiên cao, độ tin cậy thấp. (Giảm thiểu: chạy nhiều lần, báo CI.)  
- **Mô hình nền:** Độ phi định hướng/LSTM (model drift), phụ thuộc prompt. (Khắc phục: cố định phiên bản model, log prompt.)  
- **Truy vấn RAG:** Nội dung không liên quan, rò rỉ tương lai, thay đổi corpus. (Kiểm soát: khoá chỉ mục và corpus, đảm bảo không dùng dữ liệu tương lai.)  

## 18. Chuẩn bị công bố
Đảm bảo: tất cả RQ/H đã được kiểm chứng (dù thành công hay không); tái lập baseline rõ ràng; so sánh công bằng; có các metric phát hiện sớm; ablation đầy đủ; bằng chứng thống kê; artifact tái lập (mã, dữ liệu) sẵn sàng; và hạn chế được báo cáo trung thực.  

## 19. Xác minh tiêu chí baseline (Q1/Q2 + 2023–2026)
Theo quy định, baseline phải đáp ứng hết điều kiện Q1/Q2 và năm 2023–2026:  

| Tạp chí                    | Năm | Nguồn xếp hạng         | Hạng (Quartile)        | Công bố chính thức      | DOI                                    |
|----------------------------|-----|------------------------|------------------------|-------------------------|----------------------------------------|
| *Systems and Soft Computing* (Elsevier) | 2026| JournalMetrics/OpenAlex | Q1       | (peer-review, chính thức) | 10.1016/j.sasc.2026.200475 |

Cơ sở: Tạp chí *Systems and Soft Computing* (Academic Press/Elsevier, SCIE) công bố 2026 (Cabello et al., *Vol* 8). Tạp chí này xếp loại Q1 theo dữ liệu Journal Metrics (OpenAlex). DOI đã được xác nhận.  

## 20. Kết luận thí nghiệm
| Phần tử nghiên cứu | Bằng chứng                              | Kết luận                  | Độ tin cậy |
|-------------------|-----------------------------------------|---------------------------|-----------|
| RQ1               | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |
| RQ2               | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |
| RQ3               | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |
| H1                | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |
| H2                | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |
| H3                | Chưa thực hiện thí nghiệm               | Chưa đánh giá             | 0%        |

**Phát hiện chính:** (Chưa có vì chưa chạy thí nghiệm.)  
**Hạn chế chính:** (Quá trình thực nghiệm chưa diễn ra.)  
**Trade-off:** (Chưa đánh giá.)  
**Bước tiếp:** Tiếp tục thực hiện các thí nghiệm theo kế hoạch để thu thập bằng chứng trong cùng hướng cải tiến.  

**Tổng kết:** Kế hoạch thí nghiệm nhằm xác định bằng chứng xem cải tiến mục tiêu trên baseline Q1/Q2 (2023–2026) có giải quyết được hạn chế đã xác nhận hay không, và mức độ mạnh của bằng chứng. Các hướng dẫn ICSE/IEEE/NeurIPS về khả tái lập và minh bạch đã được tuân thủ trong thiết kế này.  

**Nguồn tham khảo chính:** Hướng dẫn kiểm tra tái lập của NeurIPS và IEEE, ví dụ: NeurIPS khuyến khích báo cáo sai số và kiểm định thống kê cho kết quả thí nghiệm; IEEE khuyến cáo mô tả chi tiết phương pháp và chia sẻ dữ liệu/mã nguồn.  

