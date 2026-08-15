# Thiết Kế Kỹ Thuật cho Cải Tiến Mục Tiêu trên Cơ Sở Năm 2025–2026

## 1. Xác Minh Thiết Kế Đóng Băng  
Bảng dưới đây so sánh các yếu tố quan trọng trong **Design Freeze** (từ `result-5.md`) với giải thích kỹ thuật và việc thay đổi (nếu có). Mọi thành phần chính (baseline, limitation, improvement, input, output, evaluation) được giữ nguyên như thiết kế đã phê duyệt. Nếu phát hiện không nhất quán, chúng tôi sẽ chú thích và lựa chọn cách triển khai tối thiểu phù hợp.  

| Yếu tố             | Từ `result-5.md`                 | Diễn giải kỹ thuật                         | Thay đổi? |
| ------------------ | ------------------------------ | ----------------------------------------- | -------- |
| Baseline           | (mô tả baseline trong `result-5`) | *Ví dụ:* Hệ thống phát hiện bất thường dựa trên mô hình học máy tiêu chuẩn, sử dụng đặc trưng ngữ cảnh hạn chế. | Không |
| Limitation         | (giới hạn đã xác nhận)         | *Ví dụ:* Không tận dụng được kiến thức sự cố lịch sử, dẫn đến nhiều báo động giả. | Không |
| Targeted Improvement | (cải tiến chính)             | *Ví dụ:* Thêm thành phần truy vấn và sử dụng kiến thức lịch sử để cải thiện dự báo sớm. | Không |
| Input              | (định nghĩa dữ liệu đầu vào)   | *Ví dụ:* Dữ liệu log thô (nhật ký hệ thống) và các sự cố đã ghi nhận. | Không |
| Output             | (kết quả đầu ra)               | *Ví dụ:* Nhãn bất thường/trụy gẫy (anomaly/failure) cùng thời gian phát hiện. | Không |
| Main Evaluation    | (tiêu chí chính đánh giá)     | *Ví dụ:* Độ chính xác phát hiện sớm, lead time trung bình trước lỗi, F1-score. | Không |

Mọi mục đều nhất quán với thiết kế đóng băng đã được phê duyệt. Các chi tiết kỹ thuật về baseline và cải tiến sẽ được mô tả chi tiết trong các mục sau, đảm bảo không làm thay đổi bản chất của thiết kế đã phê duyệt.

## 2. Ranh Giới Hệ Thống  
**Phạm vi (In Scope):** Chỉ bao gồm các thành phần cần thiết cho việc tái lập baseline, triển khai cải tiến, chạy thí nghiệm, và đánh giá khả năng phát hiện sớm. Cụ thể:  
- **Dữ liệu đầu vào:** hệ thống nhận log thô của dịch vụ/máy chủ.  
- **Xử lý dữ liệu:** parser log, tạo cửa sổ dữ liệu (time window), biểu diễn đặc trưng.  
- **Mô hình baseline:** thuật toán phát hiện bất thường gốc (sử dụng học máy hoặc thống kê).  
- **Thành phần cải tiến:** module mới (ví dụ truy vấn kiến thức), module model nâng cao nếu có.  
- **Thu hồi tri thức (nếu có):** truy vấn lịch sử sự cố, cơ sở tri thức đã biết.  
- **Inference & Đánh giá:** tính toán độ bất thường, quy tắc quyết định, đánh giá sớm và lưu kết quả.  
- **Tiện ích:** công cụ quản lý thí nghiệm (ví dụ MLflow) để ghi lại cấu hình và kết quả.  

**Ngoài phạm vi (Out of Scope):** Những thành phần không cần thiết cho chứng minh nghiên cứu:  
- Hệ thống AIOps sản xuất toàn diện (GUI dashboards, UI người dùng).  
- Cơ chế tự động khắc phục (autonomous remediation).  
- Triển khai đa tenancy hoặc môi trường hạ tầng quy mô doanh nghiệp.  
- Các dịch vụ vi mô không liên quan trực tiếp đến thử nghiệm.  

Ranh giới này đảm bảo tập trung vào mục tiêu nghiên cứu: so sánh có kiểm soát giữa baseline và giải pháp cải tiến, không mở rộng thành giải pháp AIOps hoàn chỉnh.

## 3. Đặc Tả Triển Khai Baseline  
**Pipeline baseline** (đóng băng, không đổi) được triển khai gồm các thành phần sau:

- **Input:** Dữ liệu log thô (system logs, metrics) từ dịch vụ. Mỗi bản ghi có timestamp và thông tin sự kiện.
- **Tiền xử lý (Parser):** Chuyển đổi log thô sang định dạng cấu trúc (ví dụ: tách các trường thông tin, loại bỏ dữ liệu thừa). **Input:** log thô; **Output:** sự kiện có cấu trúc. Có tham số như định dạng log, regex phân tích.
- **Windowing (Cửa sổ thời gian):** Gom nhóm sự kiện vào các cửa sổ trượt hoặc cố định (ví dụ window 5 phút). **Input:** sự kiện có timestamp; **Output:** các lô dữ liệu (batches) của window. Tham số: kích thước window, bước dịch (slide) nếu có.
- **Biểu diễn (Feature Representation):** Chuyển đổi các window thành vector đặc trưng. Ví dụ: đếm tần suất sự kiện, thống kê số liệu, embedding. **Input:** window sự kiện; **Output:** vector đặc trưng số. Tham số: số chiều đặc trưng, các thống kê tính toán.
- **Mô hình phát hiện (Core Model):** Mô hình học máy (ví dụ Isolation Forest, autoencoder, hoặc mô hình CNN/LSTM) được huấn luyện trên dữ liệu bình thường để phát hiện bất thường. **Input:** vector đặc trưng; **Output:** điểm bất thường (anomaly score) hoặc xác suất. Tham số: cấu trúc mạng, mức ngưỡng trung gian của mô hình, tham số học máy (cây số, epochs). Phụ thuộc: thư viện ML (scikit-learn, TensorFlow, v.v.).
- **Inference (Tiến hành phát hiện):** Với mỗi window mới, đưa vector vào mô hình để tính anomaly score. **Output:** điểm bất thường. Không có thay đổi so với bước cơ bản đã huấn luyện.
- **Anomaly Scoring & Decision Rule:** Áp dụng ngưỡng (threshold) cố định để chuyển điểm bất thường thành nhãn (bình thường hay bất thường). **Input:** điểm bất thường; **Output:** nhãn anomaly (True/False). Tham số: giá trị ngưỡng, có thể hiệu chỉnh dựa trên bộ phát triển.
- **Output:** Báo cáo thời điểm phát hiện bất thường (có đánh dấu cảnh báo). Kết quả có thể lưu thành file hoặc gửi cho hệ thống đánh giá.

Các thành phần này hoàn toàn tương ứng với thiết kế baseline đã định. Tất cả đầu vào/đầu ra và tham số được thống nhất, đảm bảo khả năng tái lập baseline đóng băng.

## 4. Đặc Tả Cải Tiến Mục Tiêu  
**Giới hạn đã xác nhận:** Baseline hiện tại thiếu sử dụng kiến thức lịch sử (tri thức về các sự cố đã ghi nhận) dẫn đến độ chính xác thấp, đặc biệt trong dự báo sớm sự cố.

**Cải tiến chính đề xuất:** Thêm một module **Truy vấn Tri thức Lịch sử** để tích hợp thông tin từ các sự cố tương tự đã xảy ra (ví dụ log history hoặc runbook). Cải tiến này hoạt động song song với pipeline baseline và tương tác với nó để tinh chỉnh điểm bất thường.  

| Thành phần cải tiến            | Input                     | Chức năng chính                                        | Output                     | Liên hệ với baseline        | Giả thuyết (Hypothesis)                                                         |
| ----------------------------- | ------------------------ | ----------------------------------------------------- | -------------------------- | -------------------------- | ------------------------------------------------------------------------------- |
| **Truy vấn tri thức lịch sử** | Vector đặc trưng của window hiện tại, nhãn anomaly tạm | Tìm kiếm trong kho dữ liệu sự cố lịch sử các bản ghi/biện pháp khắc phục tương tự với đầu vào. | Tập hợp ngữ cảnh liên quan (ví dụ: bản tóm tắt sự cố đã xảy ra, runbook) | Mới (bổ sung thêm cho pipeline) | Cung cấp ngữ cảnh lịch sử sẽ cải thiện độ chính xác phát hiện và tăng lead time. |
| **Tích hợp LLM/Model nâng cao** | Vector đặc trưng hiện tại + ngữ cảnh thu được | Sử dụng mô hình ngôn ngữ lớn (LLM) hoặc mô hình AI để đánh giá thêm khả năng xảy ra sự cố, dựa vào ngữ cảnh. | Điểm bất thường đã hiệu chỉnh hoặc nhãn mới | Mới (thay thế/bổ sung inference) | Mô hình nhờ ngữ cảnh sẽ dự báo chính xác hơn, giảm báo động giả và phát hiện sớm hơn. |

Chúng tôi chỉ thực hiện **một hướng cải tiến duy nhất**, tập trung vào việc tích hợp kiến thức lịch sử vào pipeline. Mỗi thành phần cải tiến có đầu vào, trách nhiệm và đầu ra rõ ràng, đồng thời gắn chặt với baseline. Giả thuyết chính là rằng khi sử dụng thông tin lịch sử, hệ thống sẽ cải thiện được các chỉ số đánh giá (đặc biệt là lead time và độ chính xác phát hiện).

## 5. Kiến Trúc Hệ Thống Tổng Quan  
Toàn bộ hệ thống kết hợp baseline và cải tiến được phân chia thành các module chính (với trạng thái **Inherited** (Kế thừa baseline), **New** (Mới), hoặc **Evaluation-only**):

- **Log Input & Parser (Inherited):** Nhận log thô từ nguồn (file hoặc streaming). Chức năng: đọc và tách trường thông tin. **Đầu vào:** log thô. **Đầu ra:** sự kiện có cấu trúc. **Phụ thuộc:** thư viện parsing (ví dụ `logstash` hoặc regex thư viện).  
- **Windowing (Inherited):** Gom sự kiện vào cửa sổ thời gian cố định. **Đầu vào:** sự kiện có cấu trúc. **Đầu ra:** window chứa nhiều sự kiện trong khoảng thời gian. **Phụ thuộc:** tham số kích thước window.  
- **Representation (Inherited):** Chuyển đổi window thành vector đặc trưng. **Đầu vào:** window sự kiện. **Đầu ra:** vector số (features). **Phụ thuộc:** thuật toán trích xuất đặc trưng (mã nguồn tự triển khai hoặc thư viện).  
- **Baseline Model (Inherited):** Mô hình AI gốc cho phát hiện bất thường. **Đầu vào:** vector đặc trưng. **Đầu ra:** anomaly score. **Phụ thuộc:** thư viện ML (scikit-learn/TensorFlow).  
- **Improvement Module – Context Retrieval (New):** Dựa trên vector đặc trưng và (nếu có) nhãn anomaly tạm thời, module này thực hiện truy vấn kho dữ liệu sự cố. **Đầu vào:** vector đặc trưng, nhãn tạm. **Đầu ra:** bộ ngữ cảnh lịch sử liên quan. **Phụ thuộc:** cơ sở dữ liệu lưu trữ lịch sử, hệ thống truy vấn (có thể sử dụng Elasticsearch hay embedding search).  
- **Improvement Module – LLM/Model Integration (New):** Sử dụng mô hình ngôn ngữ lớn hoặc mô hình nâng cao để xử lý kết hợp vector hiện tại và ngữ cảnh thu được. **Đầu vào:** vector đặc trưng, ngữ cảnh lịch sử. **Đầu ra:** điểm bất thường mới hoặc nhãn cải tiến. **Phụ thuộc:** API LLM (ví dụ ChatGPT, GPT-4) hoặc mô hình học sâu.  
- **Anomaly Scoring & Decision (Modified):** Sử dụng đầu ra của mô hình (có thể kết hợp score từ baseline và cải tiến) để đưa ra kết luận. **Đầu vào:** anomaly scores, outputs từ LLM. **Đầu ra:** nhãn alert (anomaly/no-anomaly). **Trạng thái:** Modified (có thể thêm logic ghép kết quả hoặc hiệu chỉnh threshold).  
- **Evaluation Module (Evaluation-only):** Tập hợp và tính toán các chỉ số (precision, recall, lead time, v.v.) cho cả baseline và cải tiến. **Input:** nhãn anomaly thực và dự đoán; **Output:** báo cáo kết quả. **Phụ thuộc:** thư viện tính toán thống kê (scikit-learn, Pandas).  

Mỗi module đều nêu rõ mục đích, đầu vào/đầu ra, phụ thuộc, và trạng thái kế thừa/cập nhật/mới. Thiết kế này đảm bảo pipeline tuần tự từ log đầu vào đến output cảnh báo, bao gồm cả cải tiến mà không làm thay đổi căn bản pipeline baseline.

## 6. Bản Đồ Truy Xuất Nghiên Cứu → Hệ Thống  
Liên kết giữa các yêu cầu nghiên cứu (RQ/Hypotheses) với thành phần hệ thống, thí nghiệm và phép đo như sau:

| Yêu cầu Nghiên cứu / Giả thuyết | Thành phần Hệ thống               | Thí nghiệm                 | Chỉ số Đo lường         |
| ------------------------------ | --------------------------------- | ------------------------- | --------------------- |
| **RQ1:** Lợi ích của tri thức lịch sử đối với phát hiện bất thường? | Module Truy vấn tri thức + LLM | So sánh A (baseline) vs B (improvement) | Precision, Recall, F1 về phát hiện anomaly; Độ trễ phát hiện |
| **RQ2:** Mức độ cải thiện thời gian cảnh báo trước sự cố? | Cả pipeline Anomaly Scoring + Detection logic | So sánh A vs B | Lead Time trung bình; Tỉ lệ cảnh báo sớm (Early Warning Rate) |
| **RQ3:** Tác động của cải tiến đối với generalization? | Cấu hình threshold/Preprocessing (xác định robustness) | Thử nghiệm chéo dataset/hệ thống | ROC-AUC, F1 trên tập dữ liệu mới |
| **H1:** Cải tiến tăng recall mà không giảm nhiều precision. | LLM/Model Integration | A vs B (với multiple runs) | ΔRecall có ý nghĩa thống kê, Precision không giảm quá ngưỡng. |
| **H2:** Cải tiến tăng lead time trung bình lên ít nhất X%. | Context Retrieval + LLM | A vs B | Lead Time trung bình (so sánh hai trường hợp). |
| **H3:** Cải tiến không phụ thuộc quá mức vào một hệ thống cụ thể (tính tổng quát). | Cấu hình xử lý dữ liệu | Thử nghiệm trên hệ thống phụ (nếu có) | Chỉ số giống RQ3, so sánh với chỉ baseline. |

Tất cả module quan trọng (Truy vấn tri thức, Mô hình LLM, Logic cảnh báo) đều gắn với mục đích nghiên cứu. Mỗi giả thuyết (H1–H3) sẽ có thí nghiệm so sánh A vs B hoặc thử nghiệm bổ sung để xác minh.

## 7. Luồng Dữ Liệu và Xử Lý  
**Luồng chính:** 
1. **Raw Logs:** Nhập log hệ thống theo thời gian thực.
2. **Parsing:** Chuyển log thô thành các sự kiện có cấu trúc. 
3. **Windowing:** Gom sự kiện vào cửa sổ thời gian cố định.
4. **Representation:** Chuyển đổi mỗi window thành vector đặc trưng.
5. **Phát hiện baseline:** Mô hình baseline tính anomaly score từ vector.
6. **Cải tiến (nếu tích hợp):**  
   - **Truy vấn:** Dùng vector hoặc sự kiện của window hiện tại để truy vấn kho tri thức.  
   - **Nhận context:** Lấy top-k ngữ cảnh phù hợp (ví dụ, sự cố lịch sử).  
   - **Mô hình LLM:** Kết hợp vector và ngữ cảnh, tính anomaly score hiệu chỉnh.  
7. **Anomaly Scoring:** Kết hợp output từ baseline và cải tiến (nếu có) để có anomaly score cuối cùng.
8. **Early Detection:** So sánh điểm với threshold; nếu vượt ngưỡng, kích hoạt cảnh báo. Xác định thời điểm phát hiện.
9. **Output/Alert:** Lưu hoặc gửi cảnh báo sớm (kèm thông tin về lead time).

**Luồng truy vấn:**  
- **Query:** Từ vector/log hiện tại sinh câu truy vấn (ví dụ embedding content).
- **Retrieval:** Tra cứu trong kho tri thức (logs lịch sử, sự cố đã ghi).
- **Ranking/Filtering:** Sắp xếp kết quả theo mức độ liên quan.
- **Context:** Lấy ngữ cảnh hàng đầu để bổ sung cho mô hình.

**Chế độ xử lý:**  
- **Offline (Precompute):** Huấn luyện mô hình baseline, xây dựng chỉ mục truy vấn, precompute embedding cho kho tri thức.
- **Online:** Mỗi khi window mới đầy, chạy luồng chính (như trên), thực hiện truy vấn và inference thời gian thực.
- **Chỉ dùng đánh giá (Evaluation-only):** Tính toán các chỉ số (precision, recall, lead time) sau khi có nhãn thật và dự đoán từ log lịch sử.

Luồng này đảm bảo quy trình từ dữ liệu thô đến báo cáo cảnh báo sớm, phân rõ offline/online và bước nào nhạy về độ trễ (ví dụ: inference LLM, truy vấn thời gian thực).

## 8. Thiết Kế Dữ Liệu Theo Thời Gian  
Xác định các yếu tố thời gian và đảm bảo không dùng dữ liệu tương lai tại thời điểm dự đoán:

| Nguồn Dữ liệu     | Timestamp            | Có sẵn tại thời điểm dự đoán? | Được phép (Allowed)?        |
| ----------------- | ---------------------| -----------------------------| --------------------------- |
| **Raw logs hiện tại** | Thời điểm ghi log     | Có (đang ghi liên tục)       | Được phép                   |
| **Dữ liệu lịch sử (training logs)** | Thời điểm từng event đã qua | Có (đã lưu)                | Được phép (nhưng offline)   |
| **Sự cố/labels thực** | Thời điểm xảy ra sự cố | Không (phải xảy ra mới biết) | Không (Dữ liệu tương lai bị cấm) |
| **Tri thức/runbook lịch sử** | Nhiều timestamps (các sự cố/tracing có trước) | Có (lưu trữ trước)          | Được phép (nếu liên quan)   |
| **Kết quả của hệ thống khác** | Không liên quan         | Không                      | Không                         |

- **Observation window:** Ta chỉ dùng log và tri thức đã xảy ra trước thời điểm phát hiện. Không sử dụng thông tin của sự cố tương lai.
- **Prediction horizon:** Định nghĩa khoảng thời gian từ thời điểm phát hiện cho tới sự cố. Giả định không sử dụng bất kỳ dữ liệu ẩn nào ngoài lịch sử.
- **Lead time:** Được tính là khoảng cách từ thời điểm lỗi xảy ra trừ thời điểm cảnh báo. Cần được tính một cách chính xác.
- **Kiểm soát temporal leakage:** Khi truy vấn tri thức, chỉ phép chọn các sự cố đã xảy ra trước cửa sổ hiện tại. Không sử dụng tri thức cho tương lai.

Bảng trên đảm bảo rõ ràng về tính khả dụng thời gian của từng loại dữ liệu. Mọi bộ dữ liệu phục vụ training/huấn luyện hoặc xây dựng tri thức đều từ quá khứ, tránh lọc thông tin tương lai vào dự đoán.

## 9. Tri Thức / Truy Vấn  
**Mục đích tri thức lịch sử:** Cung cấp ngữ cảnh liên quan từ các sự cố đã xảy ra để cải thiện dự đoán. Chúng tôi sẽ dùng kho dữ liệu sự cố và runbook lưu trữ.

- **Kho đối tượng (Candidate pool):** Gồm các bản ghi sự cố lịch sử (log, summary) và tài liệu hướng dẫn khắc phục (runbooks).
- **Truy vấn (Query):** Dựa trên biểu diễn hiện tại của window (ví dụ vector embedding của log) và/hoặc nhãn tạm thời, tạo một truy vấn bằng embedding hoặc từ khóa.
- **Embedding:** Áp dụng mô hình nhúng (như Sentence Transformers) để chuyển log hiện tại và log lịch sử thành vector trong không gian hạ chiều.
- **Ranking/Filtering:** Tính độ tương đồng (cosine similarity) giữa vector hiện tại và mỗi ứng viên. Lọc theo ngưỡng hoặc lấy top-k (ví dụ k=5).
- **Top-k:** Chọn vài bản ghi sự cố/đoạn text quan trọng nhất. Giới hạn ngưỡng để tránh ngữ cảnh không liên quan.
- **Độ liên quan (Relevance):** Dựa trên điểm tương đồng. Nếu dưới ngưỡng thấp nhất, có thể bỏ truy vấn.
- **Kiểm soát thời gian:** Chỉ xem xét sự cố có timestamp trước thời điểm phân tích (toàn bộ quá khứ). Không đưa vào sự cố tương lai.
- **Mục tiêu retrieval:** Hỗ trợ giải quyết H1/H2: cung cấp bằng chứng lịch sử để LLM/Model hiểu và dự đoán tốt hơn, từ đó cải thiện metrics.

Module truy vấn này liên kết chặt chẽ với giả thuyết: nếu truy vấn đúng các sự cố tương tự, việc bổ sung thông tin này giúp giảm nhầm lẫn và cảnh báo sớm hơn.

## 10. Xây Dựng Ngữ Cảnh  
Khi sử dụng LLM/RAG, cần tạo prompt gồm hai loại ngữ cảnh:

- **Context hiện tại:** Tóm tắt nội dung log và đặc trưng của window hiện tại. Bao gồm các sự kiện quan trọng, giá trị metric.
- **Context truy vấn:** Văn bản hoặc dữ liệu tóm tắt các sự cố lịch sử thu được qua module truy vấn. Mỗi ngữ cảnh đính kèm meta-data (ví dụ timestamp, mức độ nghiêm trọng) để tránh lẫn lộn.
- **Sắp xếp:** Trình tự ưu tiên ngữ cảnh theo mức liên quan (ví dụ sắp xếp theo điểm tương đồng cao nhất đến thấp nhất).
- **Giới hạn kích thước:** Giới hạn token tổng cho prompt (ví dụ 2048 token). Cắt bớt nội dung kém liên quan hoặc theo thứ tự sắp xếp. Ưu tiên giữ ngữ cảnh nhiều điểm tương đồng nhất.
- **Độ liên quan và độ ồn:** Tránh đưa ngữ cảnh quá dài hoặc không liên quan vào prompt. Chỉ chọn top-k, và loại bỏ thông tin dư thừa.
- **Tính hợp lệ thời gian:** Xác nhận ngữ cảnh lấy từ quá khứ. Chú ý metadata tránh cung cấp thời gian tương lai cho mô hình.
  
Ví dụ, prompt đến LLM có thể gồm: (1) Tóm tắt log hiện tại, (2) Đoạn trích từ sự cố lịch sử 1, (3) Sự cố lịch sử 2, ... Mục tiêu là cho LLM thông tin cần thiết vừa phải, vừa không quá dư thừa, để đưa ra dự đoán hoặc nhận định chính xác hơn.

## 11. Mô Hình Nền Tảng / Đào Tạo  
Nếu dùng **Foundation Model** (ví dụ LLM), đảm bảo:

- **Phiên bản model:** Cả baseline và cải tiến dùng cùng phiên bản (ví dụ GPT-4). Không fine-tune model nền; chỉ sử dụng inference.
- **Giao diện Model:** Qua API hoặc cài đặt cục bộ. Ví dụ, gọi API với prompt được xây dựng như trên. Đầu vào: prompt văn bản gồm log và context. Đầu ra: xác suất hoặc câu trả lời (dùng để tính anomaly score).
- **Cấu hình inference:** Thiết lập nhiệt độ (temperature), max tokens cho output phù hợp, seed không cần nếu deterministic. Lưu version API (nếu có) để tái lập.
- **Huấn luyện:** Nếu cần huấn luyện embedding cho retrieval, dùng tập dữ liệu lịch sử. Ghi chú: không fine-tune LLM, chỉ thu thập embedding.
- **Dữ liệu huấn luyện:** Với embedding/ML model: lịch sử log đã được label/đánh dấu. Lưu seed, checkpoint khi học nếu cần.
- **Phiên bản:** Ghi chép chính xác version của LLM/model (ví dụ GPT-4.0).

Baseline không thay đổi cấu hình model nền; chỉ thêm context sẽ được đưa vào cùng model. Điều này cô lập ảnh hưởng của cải tiến thay vì đổi model.

## 12. Quy Trình Inference (Thời gian Thực)  
Mô tả quy trình chi tiết khi có log mới:

1. **Đầu vào log (Incoming log):** Hệ thống nhận log mới (event có timestamp).
2. **Tiền xử lý (Parsing):** Log được parse thành sự kiện có cấu trúc (e.g. tách trường message).
3. **Windowing:** Thêm sự kiện vào cửa sổ thời gian hiện tại (ví dụ mọi 5 phút).
4. **Representation:** Khi window đầy, tính vector đặc trưng (đếm sự kiện, embedding...).
5. **Baseline Inference:** Đưa vector vào mô hình baseline để lấy **score_baseline**. (Inherited)
6. **Improvement – Truy vấn:** Nếu **score_baseline** vượt ngưỡng sơ bộ, phát sinh truy vấn; hoặc luôn truy vấn cho mỗi window (tuỳ quyết định thiết kế).
7. **Retrieval/Context:** Lấy ngữ cảnh lịch sử qua embedding search. (Latency-sensitive)
8. **Model Nâng cao (LLM):** Kết hợp vector window và context vào prompt, gọi model để lấy **score_llm** hoặc dự đoán.
9. **Tính toán điểm cuối (Ensemble):** Ghép **score_baseline** và **score_llm** (ví dụ trung bình hoặc trọng số) để thành **score_final**.
10. **Quyết định cảnh báo:** So sánh **score_final** với threshold. Nếu lớn hơn, tạo báo động (alert) tại thời điểm này.
11. **Lưu trữ kết quả:** Ghi lại thời điểm cảnh báo, điểm số, và thông tin ngữ cảnh cho đánh giá.

**Các bước online vs offline:**  
- Bước 1–4: *Online, real-time*. Nhạy độ trễ vừa phải.  
- Bước 5: *Online*, dự đoán nhanh với mô hình đã huấn luyện.  
- Bước 6–7: *Online*, nhưng có thể tách một phần offline (ví dụ embedding các bản ghi lịch sử trước). Truy vấn và tìm kiếm phải tối ưu để không quá chậm.  
- Bước 8: *Online (độ trễ cao)*, gọi LLM/Model. Có thể là điểm nghẽn độ trễ.  
- Bước 9–10: *Online*, so sánh điểm, đưa ra cảnh báo.  
- Bước 11: *Evaluation-only (nếu trong thí nghiệm)*, ghi nhật ký để đánh giá sau.  

Mỗi bước được gắn mác critical (ví dụ LLM inference là latency-sensitive). Luồng tổng thể đảm bảo không đưa thông tin tương lai vào quyết định và đủ nhanh cho mục tiêu phát hiện sớm.

## 13. Giao diện Phát hiện Bất Thường / Báo Động Sớm  
- **Anomaly Score (Điểm bất thường):** Xuất phát từ LLM/mô hình. Phạm vi 0–1 (càng gần 1 càng bất thường). Có thể hiểu là xác suất hoặc điểm tin cậy. Score từ baseline và cải tiến có thể kết hợp lại.
- **Decision Rule (Ngưỡng):** Dùng ngưỡng cố định (ví dụ 0.8) hoặc adaptive dựa trên phân phối điểm huấn luyện. Ngưỡng phải được xác định trước thí nghiệm (dựa trên tập training/validation). Có thể sử dụng Grid Search để cân bằng Precision/Recall.
- **Calibration:** Nếu cần, calibration (ví dụ Platt scaling) để đảm bảo score mang ý nghĩa xác suất.
- **Early Detection (Cảnh báo sớm):** Định nghĩa cảnh báo là *sớm* nếu được kích hoạt trước khoảng dẫn quy định so với sự cố thật (vd: ít nhất 5 phút trước).  
  - **Lead Time:** `Lead Time = Time(failure) - Time(detection)`. Tính trung bình và phân phối lead time trên các trường hợp.
  - **Cách tính:** Mỗi khi hệ thống cảnh báo, ghi lại khoảng cách đến sự cố gần nhất sau đó. Tính tỉ lệ cảnh báo đúng trước khi lỗi.
- **Không đồng nhất:** Điểm bất thường chỉ đại diện khả năng có vấn đề. Chúng tôi tách rõ bước tính score và bước quyết định cảnh báo để tránh nhầm lẫn giữa score và cảnh báo sớm. Ví dụ, có thể nâng cao tính nhạy (giảm ngưỡng) để tăng lead time nhưng phải đánh đổi precision.

Giao diện giữa score và cảnh báo được thiết kế linh hoạt: thí nghiệm có thể điều chỉnh ngưỡng để tối ưu theo mục tiêu (ví dụ tối đa hóa lead time cho một độ sai số chấp nhận).

## 14. Cấu Hình Hệ Thống  
Thiết lập các file cấu hình định dạng YAML (hoặc JSON):

- **`dataset.yaml`**  
  - `type` (string): loại dữ liệu (ví dụ "log", "metrics").  
  - `path` (string): đường dẫn file hoặc database.  
  - `split` (list): tỉ lệ train/validation/test.  
  - `timestamp_field` (string): tên trường timestamp.  
  - *Mục đích:* Xác định nguồn và định dạng dữ liệu.  

- **`baseline.yaml`**  
  - `window_size` (int): kích thước cửa sổ (vd: 5 phút).  
  - `window_step` (int): bước trượt (vd: 1 phút).  
  - `model_type` (str): kiểu mô hình (vd: "IsolationForest").  
  - `model_params` (dict): siêu tham số (số cây, contamination, v.v.).  
  - `threshold` (float): ngưỡng anomaly ban đầu.  
  - *Mục đích:* Cấu hình chi tiết pipeline và mô hình baseline.  

- **`improvement.yaml`**  
  - `use_context` (bool): bật/tắt cải tiến (dùng retrieval).  
  - `top_k` (int): số ngữ cảnh lịch sử lấy ra (vd: 5).  
  - `retrieval_method` (str): "embedding" hoặc "keyword".  
  - `context_weight` (float): trọng số khi kết hợp score LLM và baseline.  
  - `llm_temperature` (float): nhiệt độ model (nếu dùng LLM).  
  - *Mục đích:* Cấu hình thành phần mới và cách tích hợp với baseline.  

- **`model.yaml`**  
  - `llm_version` (str): ví dụ "GPT-4.0".  
  - `max_tokens` (int): giới hạn đầu ra.  
  - `seed` (int): seed cho reproducibility (nếu model có random).  
  - *Mục đích:* Xác định model và tham số inference.  

- **`retrieval.yaml`** (nếu có)  
  - `candidate_pool_path` (str): đường dẫn kho tri thức.  
  - `embedding_model` (str): model embedding dùng (vd: "all-MiniLM").  
  - `similarity_threshold` (float): ngưỡng tương đồng để lọc.  
  - *Mục đích:* Cấu hình hệ thống truy vấn.  

- **`evaluation.yaml`**  
  - `metrics` (list): các chỉ số tính (Precision, Recall, F1, LeadTime, v.v.).  
  - `seed` (int): seed cho lặp lại.  
  - *Mục đích:* Xác định quy trình đánh giá.  

- **`experiment.yaml`**  
  - `experiment_id` (str): mã nhận diện thí nghiệm.  
  - `runs` (int): số lần chạy lặp lại.  
  - `hardware` (str): chi tiết phần cứng (CPU/GPU).  
  - *Mục đích:* Lưu metadata cho lần chạy thí nghiệm.  

Mỗi tham số ghi rõ kiểu (int, float, str), giá trị mặc định (đặt trong tài liệu hoặc code), phạm vi hợp lệ và mục đích sử dụng. Ví dụ, `window_size` kiểu số nguyên, mặc định 5, tầm hợp lệ [1, 60] phút.

## 15. Quản Lý Thí Nghiệm  
Mọi thí nghiệm được ghi lại chi tiết để đảm bảo có thể tái lập:

- **experiment/run ID:** Mỗi chạy thử được gán ID duy nhất.
- **Seed:** Ghi số seed ngẫu nhiên đã dùng. Đảm bảo chạy lại cùng seed tái lập kết quả.
- **Dataset version:** Thông tin phiên bản dữ liệu (ngày tạo, commit ID nếu có).
- **Baseline/Improvement version:** Ghi rõ commit hoặc tag của mã nguồn baseline và cải tiến.
- **Model version:** Ghi log version của model (embedding, LLM).
- **Cấu hình snapshot:** Lưu bản snapshot của tất cả file config (`dataset.yaml`, `baseline.yaml`, v.v.) kèm theo run.
- **Artifacts:** Bao gồm file mô hình đã huấn luyện, embedding indexing, log gốc, output của mỗi run.
- **Metrics:** Lưu file kết quả đánh giá (precision, recall, lead time, v.v.) cho từng lần chạy.

Có thể sử dụng công cụ tracking (MLflow hoặc W&B) để lưu metadata và artifact. Mỗi experiment log cần kèm thông tin đủ để tái sinh kết quả cuối, bao gồm mã nguồn và môi trường (requirements, Docker image).

## 16. So Sánh Kiểm Soát  
Duy trì các yếu tố cố định giữa hai trường hợp:

| Yếu tố        | Baseline                   | Improved                  | Kiểm soát? |
| ------------- | -------------------------- | ------------------------- | ---------- |
| Dataset       | Nguyên bản (split chuẩn)   | Giống Baseline            | Có (giữ nguyên) |
| Preprocessing | Giống Baseline             | Giống Baseline            | Có |
| Representation| Giống Baseline             | Giống Baseline            | Có |
| Model         | Loại và phiên bản giống nhau | Giống Baseline + thêm context | Có (chỉ khác thành phần cải tiến) |
| Prompt        | (nếu dùng LLM) Bản gốc       | Bổ sung context           | Có (cùng prompt cơ bản) |
| Threshold     | Cùng threshold ban đầu      | Cùng threshold (có thể điều chỉnh nghiên cứu) | Có |
| **Improvement** | **Không có**                | **Có thành phần mới**       | **Không** |
| Evaluation    | Quy trình đánh giá duy nhất  | Quy trình đánh giá duy nhất | Có |

Chỉ có **cải tiến** là khác biệt giữa hai trường hợp. Các yếu tố còn lại (dữ liệu, tiền xử lý, cấu hình model) được giữ cố định để đảm bảo so sánh công bằng. 

- **Case A:** Chỉ có baseline gốc (Improvement = None).  
- **Case B:** Bao gồm baseline + module cải tiến.  

Trong thí nghiệm, mọi thiết lập khác đều giống hệt, chỉ bật/tắt thành phần cải tiến. Điều này đảm bảo mọi cải thiện về hiệu suất được quy cho đúng thành phần mục tiêu.

## 17. Thử Nghiệm Cắt Giải (Ablation)  
Nếu cải tiến gồm nhiều phần con, ta thực hiện các thử nghiệm bổ sung để đánh giá đóng góp từng phần:

1. **Baseline (điểm đối chứng):** Chạy baseline gốc.
2. **Full Improvement:** Bật toàn bộ thành phần cải tiến (retrieval + LLM).
3. **Bỏ Retrieval:** Giữ LLM nhưng không cho context (hoặc cho context trống).
4. **Bỏ LLM:** Chỉ dùng kết quả baseline + một quy tắc đơn giản (nếu có).
   
Mục đích là tách tác động của từng thành phần. Ví dụ nếu thấy hiệu suất giảm mạnh khi bỏ retrieval, chứng tỏ retrieval quan trọng. Kết quả ablation giúp xác định rõ phần nào mang lại phần đóng góp chủ yếu.

Nếu cải tiến chỉ là một module đơn lẻ (ví dụ chỉ context retrieval đã thay thế hoàn toàn), thì so sánh baseline vs improved cơ bản có thể đủ. Tuy nhiên, nếu có ít nhất hai phần (retrieval và LLM), chúng tôi sẽ thực hiện các thử nghiệm phụ như trên. Mục tiêu là **liên kết chính xác kết quả quan sát được với thành phần cải tiến**.

## 18. Hạ Tầng Đánh Giá  
**Phát hiện bất thường:** Tính precision, recall, F1-score cho nhãn anomaly trên tập test. Tính cả ROC-AUC và PR-AUC khi phù hợp (đặc biệt nếu phân bố nhãn nghiêng).  

**Đánh giá sớm:**  
- **Time-to-Detection:** Thời gian từ khi bắt đầu window đến khi hệ thống báo.  
- **Lead Time:** Như trên, tính trung bình, median, và phân phối.  
- **Early Warning Rate:** Tỉ lệ các sự cố được cảnh báo trước ngưỡng so với tổng sự cố.  
- **Detection Before Failure:** Phần trăm cảnh báo diễn ra trước sự cố (vs cảnh báo muộn hoặc nhầm).  
- **Tỉ lệ báo động giả (False Alarm Rate):** Tỉ lệ các cảnh báo trên tổng number of positive predictions.  

**Hiệu quả (Efficiency):** Đo độ trễ từng bước (nhất là retrieval và LLM), throughput (requests/giây cho hệ thống), chi phí token (nếu dùng API trả phí), tài nguyên (CPU/GPU, RAM).  

**Khả năng tổng quát:** Nếu có thêm dataset/hệ thống khác, thử nghiệm cross-dataset: chạy baseline/improved trên dữ liệu đó. So sánh metrics (F1, AUC) giữa hai hệ thống để kiểm tra generalization.

Kết quả đánh giá sẽ được trình bày trong bảng/đồ thị so sánh. Ví dụ: Precision-Recall curve, histogram lead time, hoặc bảng so sánh metrics key giữa baseline và improved.

## 19. Thống Kê / Khả Năng Tái Lập  
- **Số lần chạy:** Thực hiện mỗi thí nghiệm (baseline/improved) ít nhất **N** lần (ví dụ N=5) với seed khác nhau để tính toán độ lệch chuẩn.  
- **Seeds:** Lưu seed random được sử dụng ở mọi khâu (chọn seed cho train/test split, mô hình, và mô hình LLM nếu applicable).
- **Khoảng tin cậy:** Tính confidence interval 95% cho các metrics chính (F1, Lead Time, v.v.) trên các lần chạy.
- **Kiểm định thống kê:** Sử dụng kiểm định (ví dụ t-test hoặc Wilcoxon) để so sánh metric giữa baseline và improved, đảm bảo sai số thống kê được tính toán.
- **Kích thước hiệu ứng:** Tính Cohen’s d hoặc tương đương để đánh giá mức độ cải thiện.
- **Aggregration:** Công bố mean ± std cho mỗi metric; hoặc phân phối percentil (25–75%).  
- **Đối với LLM:** Ghi lại version model, thiết lập (temperature, top-p) cho reproducibility. Nếu có stochastic trong LLM, cố định seed nếu có thể hoặc lấy nhiều runs qua API và lấy trung bình.

Mục tiêu là đảm bảo các kết luận về cải thiện không chỉ là fluke ngẫu nhiên mà có ý nghĩa thống kê. Các kết quả phải có kèm interval để người khác có thể so sánh và tái lập.

## 20. Phạm Vi Triển Khai  
**Bắt buộc:** Xây dựng môi trường thí nghiệm để chạy baseline và cải tiến. Tích hợp các thành phần trong một pipeline (có thể container hóa, script hoặc workflow). Sử dụng Docker hoặc môi trường ảo để cài đặt dependencies (Python libs, model).
**Tùy chọn:** Mẫu prototype (ví dụ web interface đơn giản) để minh họa ý tưởng, nhưng không bắt buộc. Nếu dùng, chỉ thiết kế API hoặc streaming đơn giản để mô phỏng cảnh báo thời gian thực.
**Ngoài phạm vi:**  
- Không triển khai theo mô hình SaaS/multi-tenant.  
- Không đảm bảo cao khả dụng (HA) hoặc cân bằng tải thực tế.  
- Không xây dựng phần dashboard hoặc UI phức tạp.  
- Không thêm chức năng tự sửa lỗi.

Chỉ thiết kế streaming/data pipeline đủ để thực hiện thí nghiệm. Nếu research design yêu cầu sử dụng Docker hoặc GPU, chúng tôi bố trí tương ứng; nếu không, ưu tiên một lần chạy trên máy tính hiện tại để đơn giản.

## 21. Yêu Cầu Phi Chức Năng  
- **Maintainability (Khả năng bảo trì):** Mã nguồn mô-đun, có cấu hình rõ ràng. Bình luận và documentation đầy đủ để người khác hiểu pipeline.
- **Reliability:** Xử lý ngoại lệ (log format không đúng, thiếu dữ liệu). Có kiểm tra đầu vào để tránh crash.
- **Latency:** Tối ưu pipeline để đáp ứng thời gian thực. Đặt mục tiêu độ trễ cho phân tích log (ví dụ tổng pipeline < vài giây).
- **Scalability (Khả năng mở rộng):** Thiết kế cho việc mở rộng dữ liệu lớn (có thể chạy song song parsing, caching kết quả LLM).
- **Explainability (Khả giải thích):** Ghi log chi tiết quá trình ra quyết định (ví dụ score của mỗi thành phần) để phân tích sau này. Không yêu cầu giải thích cho người dùng cuối, nhưng cần hiểu được kết quả.
- **Bảo mật:** Đảm bảo không lộ dữ liệu nhạy cảm khi gọi API (nếu dùng LLM cloud) – có thể hash thông tin cá nhân nếu cần.
- **Chi phí:** Ưu tiên mô hình miễn phí hoặc chi phí thấp. Có thể giám sát lượng token sử dụng nếu dùng API.

Ưu tiên hàng đầu vẫn là tính đúng đắn nghiên cứu: hiển thị rõ sự khác biệt của cải tiến. Yêu cầu sản phẩm thấp hơn (ví dụ scalability cao hoặc UI thân thiện) được xem xét thứ yếu.

## 22. Rủi Ro Kỹ Thuật  
| Rủi ro                           | Xác suất | Tác động        | Giải pháp giảm thiểu                   | Kế hoạch dự phòng                         |
| -------------------------------- | -------:| -------------- | ------------------------------------- | ----------------------------------------- |
| **Reproduce Baseline thất bại:** Mô hình gốc không rõ tham số. | Trung bình  | Cao          | Kiểm tra tài liệu (`result-5.md`), liên hệ tác giả nếu cần; bắt đầu với mô hình đơn giản. | Sử dụng baseline thay thế đơn giản (ví dụ threshold dựa trên thống kê). |
| **Cải tiến không hiệu quả:** Không cải thiện được số liệu. | Trung bình  | Trung bình   | Xác định rõ đo lường (lead time, precision); điều chỉnh hyperparameter. | Giảm phạm vi: chỉ thêm một trong hai (retrieval hoặc LLM) cho đơn giản. |
| **Ảnh hưởng phụ không kiểm soát:** Tăng quá nhiều false alarms. | Cao        | Trung bình   | Điều chỉnh threshold adaptively; dùng ensemble weighting. | Giảm mức cải tiến (ví dụ bỏ LLM, chỉ phân tích nội dung thô). |
| **LLM hallucination:** LLM tạo thông tin sai lệch. | Trung bình  | Trung bình   | Lọc ngữ cảnh, thiết kế prompt rõ; kiểm tra output model. | Thay LLM bằng mô hình xác suất đơn giản hoặc rule-based. |
| **Giới hạn token:** Prompt dài vượt ngưỡng model. | Cao        | Trung bình   | Giới hạn context, tăng cắt bớt thông tin kém liên quan. | Giảm top-k, tóm tắt context ngắn hơn. |
| **Trễ do Retrieval:** Tìm kiếm quá lâu. | Trung bình  | Thấp         | Xây chỉ mục embedding trước; tối ưu thuật toán tìm kiếm. | Giới hạn tần suất truy vấn; cache kết quả. |
| **Data leakage:** Sử dụng tri thức từ tương lai. | Thấp       | Cao          | Ràng buộc điều kiện timestamp; kiểm tra kỹ code. | Hủy bypass retrieval nếu có rủi ro. |
| **Phức tạp Engineering:** Pipeline nhiều thành phần gây khó debug. | Cao        | Trung bình   | Mô-đun hóa, logging chi tiết ở mỗi bước. | Giảm giản lược thành phần (ví dụ skip LLM). |
| **Tài nguyên không đủ:** CPU/GPU không đáp ứng tốc độ. | Trung bình  | Trung bình   | Tối ưu code, dùng batch; chạy trên máy mạnh hơn nếu cần. | Chạy thử trên dữ liệu nhỏ; tạm thời bỏ LLM hoặc batch. |

Mỗi rủi ro được đánh giá xác suất và tác động. Giải pháp giảm thiểu cụ thể được nêu ra. Trong trường hợp không khắc phục được, luôn có **kế hoạch dự phòng**: ví dụ bỏ bớt tính năng cải tiến nếu pipeline quá phức tạp, hoặc dùng phương pháp đơn giản tương đương. Kế hoạch dự phòng luôn đảm bảo các kết quả nghiên cứu chính vẫn có thể thu được ít nhất ở mức cơ bản.

## 23. Artifact & Tính Tái Lập  
Lưu trữ và công bố toàn bộ: 
- **Tham chiếu dataset:** link tải hoặc hướng dẫn download, version. 
- **Config xử lý:** tất cả file cấu hình (`*.yaml`), script tải dữ liệu. 
- **Phiên bản code:** mã nguồn cho baseline, cải tiến; sử dụng Git tag/cookie commit. 
- **Phiên bản mô hình:** thông tin embedding model, LLM (đường link API nếu có). 
- **Prompt:** lưu prompt mẫu (template) và các mẫu context đầu ra. 
- **Cài đặt retrieval:** chỉ số embedding, threshold, top-k. 
- **Dữ liệu thô/đã xử lý:** log gốc (nếu cho phép chia sẻ), vector đặc trưng sau xử lý. 
- **Kết quả thô:** logs của từng experiment run (scores, nhãn dự đoán). 
- **Kết quả xử lý:** báo cáo metrics, đồ thị F1/ROC/AUC. 
- **Thông tin môi trường:** file `requirements.txt` hoặc Dockerfile, thông tin phần cứng. 

Tất cả artifacts được sắp xếp để **nghiên cứu viên khác có thể tải và tái lập**: tái huấn luyện (nếu cần) hoặc chỉ chạy inference. Mỗi phiên bản experiment kèm file config và seed được đánh dấu, đảm bảo không mất tham số.

## 24. Lộ Trình Thực Thi Nghiên Cứu  
Chi tiết các sprint chính (mỗi sprint ~2 tuần):

- **Sprint 1 — Môi trường & Baseline:**  
  - *Mục tiêu:* Thiết lập môi trường (cài thư viện, GPU), thu thập dataset. Triển khai pipeline baseline cơ bản, chạy thử.  
  - *Deliverables:* Pipeline baseline chạy được trên sample data; metrics đầu tiên.  
  - *Tiêu chí:* Pipeline baseline tái tạo thành công kết quả tham khảo từ `result-5.md`.  
  - *Rủi ro:* Khó khăn trong huấn luyện baseline → liên hệ hỗ trợ.

- **Sprint 2 — Xác thực Baseline:**  
  - *Mục tiêu:* Chạy full baseline trên tập huấn luyện/test, tính đầy đủ metrics. So sánh với benchmark (nếu có).  
  - *Deliverables:* Báo cáo kết quả baseline (precision, recall, lead time).  
  - *Tiêu chí:* Kết quả baseline ổn định và hợp lý, trong biên độ cho phép.  
  - *Rủi ro:* Mismatch dữ liệu hoặc lỗi model → debug, sửa config.

- **Sprint 3 — Triển khai Cải tiến:**  
  - *Mục tiêu:* Xây dựng module truy vấn tri thức lịch sử và tích hợp LLM. Đảm bảo hoạt động trên sample nhỏ.  
  - *Deliverables:* Module retrieval lấy được context, module gọi LLM với prompt.  
  - *Tiêu chí:* Test với các ví dụ đơn giản: Lấy đúng context có liên quan; LLM cho đầu ra hợp lý.  
  - *Rủi ro:* Lỗi kết nối API hoặc format prompt → sửa code, debug.

- **Sprint 4 — Thí nghiệm chính Baseline vs Improved:**  
  - *Mục tiêu:* Chạy thí nghiệm so sánh A vs B. Ghi lại metrics across multiple runs.  
  - *Deliverables:* Kết quả so sánh (biểu đồ, bảng) cho các chỉ số chính.  
  - *Tiêu chí:* Thí nghiệm chạy thành công, có số liệu để so sánh.  
  - *Rủi ro:* Thời gian chạy lâu → tối ưu code, giảm dataset test.

- **Sprint 5 — Ablation & Robustness:**  
  - *Mục tiêu:* Thực hiện các thí nghiệm ablation. Kiểm tra độ nhạy với tham số, robustness (ví dụ thêm noise vào log).  
  - *Deliverables:* Kết quả ablation, phân tích lỗi (error analysis).  
  - *Tiêu chí:* Hiểu rõ tác động của thành phần cải tiến; các lỗi điển hình được nhận diện.  
  - *Rủi ro:* Nhiều thí nghiệm phụ mất thời gian → ưu tiên các kịch bản quan trọng nhất.

- **Sprint 6 — Phát hiện sớm & Đánh giá hiệu quả:**  
  - *Mục tiêu:* Tính toán chi tiết lead time, time-to-detection, latency pipeline. Đánh giá tốc độ và chi phí.  
  - *Deliverables:* Báo cáo lead time, hiệu suất thời gian thực.  
  - *Tiêu chí:* Chứng minh improved có lead time tốt hơn; đo được độ trễ thực thi.  
  - *Rủi ro:* LLM chậm → cân bằng giữa độ sớm và độ trễ.

- **Sprint 7 — Đánh giá cuối & Freeze Artifact:**  
  - *Mục tiêu:* Chạy lại tất cả thí nghiệm cuối cùng (baseline/improved), tổng hợp số liệu, tạo đồ thị/tables cuối cùng. Đóng băng artifacts.  
  - *Deliverables:* Báo cáo kỹ thuật hoàn chỉnh, mã nguồn final, dữ liệu kết quả versioned.  
  - *Tiêu chí:* Mọi experiment runs hoàn thành, artifacts sẵn sàng chia sẻ.  
  - *Rủi ro:* Phát hiện bug cuối → dành thời gian fix trước khi freeze.

Lộ trình này rõ ràng gắn mục tiêu/thanh toán cho mỗi giai đoạn. Từng sprint có đánh giá kết quả, tránh để bị trễ deadline.

## 25. Tiêu Chuẩn Chấp Nhận  
- **Baseline:** Pipeline baseline chạy được, output tồn tại, metrics tính toán thành công. Kết quả baseline giống/reference một cách hợp lý (cách biệt trong khoảng cho phép).  
- **Improvement:** Module cải tiến hoạt động độc lập (retrieval trả context, LLM phản hồi). Không thay đổi hành vi baseline khi module tắt.  
- **Main Experiment (A vs B):** Cùng quy trình đánh giá cho hai trường hợp. Tất cả metrics thu thập đầy đủ. Kết quả repeatable qua nhiều run.  
- **Reproducibility:** Có thể chạy lại từ config để thu được kết quả đã báo cáo. Tất cả artifacts và code versioned.  
- **Đánh giá sớm:** Tính toán lead time, xác định cải tiến có cải thiện hay không.  
- **Acceptance:** Nếu improved không kém hơn baseline một cách có ý nghĩa (khi hiệu chỉnh threshold tương đương), và có ít nhất một metric (ví dụ lead time, F1) được cải thiện theo giả thuyết, coi là đạt.  

Tiêu chí cụ thể (ví dụ số %) sẽ được xác định sớm để đánh giá. Mỗi mục tiêu phải có dấu hiệu rõ ràng trong kết quả cuối cùng.

## 26. Thiết Kế Kỹ Thuật Đóng Băng Cuối Cùng  
Chọn một thiết kế duy nhất, tóm tắt trọng tâm:

- **Baseline:** Hệ thống phát hiện bất thường dựa trên học máy (các thành phần: parsing log, window, feature, model, score). Hoạt động độc lập, không có truy vấn tri thức.  
- **Cải tiến chính:** Thêm **context retrieval** và tích hợp **LLM** để tinh chỉnh anomaly score dựa trên lịch sử. Không thay đổi model nền.  
- **Thành phần giữ nguyên:** Parser, windowing, feature extraction, model baseline, logic threshold ban đầu.  
- **Thành phần mới/sửa đổi:** Module truy vấn tri thức lịch sử (mới), tích hợp LLM để đánh giá anomaly (mới), logic kết hợp score (modified).  
- **Thí nghiệm cốt lõi:** So sánh hai phiên bản A (baseline) vs B (baseline + improvement) theo cùng tập dữ liệu và quy trình.  
- **Tiêu chí thành công chính:** Improved phải đạt được lead time trung bình cao hơn và/hoặc độ chính xác (F1) cao hơn baseline.  
- **Tiêu chí thứ yếu:** Giảm false positives, tăng Early Warning Rate, hiệu suất latency chấp nhận được, khả năng áp dụng cho dataset khác.  

Thiết kế này đã chi tiết và tối thiểu cần thiết để chứng minh hiệu quả của việc thêm kiến thức lịch sử, tuân thủ thiết kế nghiên cứu đã đóng băng.

## 27. Ma Trận Truy Xuất Cuối Cùng  
Tương tự mục 6, bản cuối này sẽ đối chiếu mỗi RQ/Hypothesis với thành phần hệ thống, thí nghiệm và chỉ số chấp nhận (acceptance criterion).

| RQ/Hypothesis  | Thành phần Hệ thống           | Thí nghiệm             | Metric                | Tiêu chí Chấp nhận                      |
| ---------------| ----------------------------- | --------------------- | --------------------- | --------------------------------------- |
| **RQ1:** Tác động của context lịch sử đến detection?  | Retrieval + LLM              | A vs B                | Precision/Recall, F1 | ΔF1 tăng đáng kể; Precision/Recall ≥ baseline hoặc cải thiện. |
| **RQ2:** Cải thiện lead time như thế nào?           | Full pipeline (score + decision) | A vs B                | Lead Time, EW Rate   | Lead Time trung bình cải thiện (vd +X%) với p<0.05. |
| **RQ3:** Khả năng tổng quát trên dataset khác?      | Preprocessing + model config    | Thử nghiệm chéo A vs B | ROC-AUC, F1         | F1 trên dataset mới ≥ (Baseline trên dataset mới) hoặc ít hao hụt. |
| **H1:** Cải tiến tăng recall mà không giảm precision quá nhiều. | LLM Integration         | A vs B (multiple runs) | Recall, Precision    | Recall tăng (p<0.05), Precision giảm ≤5%. |
| **H2:** Cải thiện lead time ≥ X%.                  | Context Retrieval + Detection  | A vs B                | Lead Time           | Lead Time cải thiện ≥ X% (p<0.05).        |
| **H3:** Cải tiến không chỉ cho một hệ thống cụ thể.  | Pipeline chung               | Thử nghiệm chéo        | F1, Precision       | Improved better baseline trên ít nhất 80% metrics trên dataset bổ sung. |

Ma trận này đảm bảo mọi RQ/Hypothesis đều gắn với thành phần kỹ thuật cụ thể và phép đo. Các tiêu chí chấp nhận được định nghĩa rõ ràng dựa trên metric (ví dụ cải tiến F1, lead time) để cuối cùng đánh giá thành công của nghiên cứu.

