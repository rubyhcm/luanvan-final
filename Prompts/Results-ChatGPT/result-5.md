# 1. Kiểm tra tính nhất quán thiết kế nghiên cứu

| **Yếu tố**           | **Từ `result-4.md` (đã phê duyệt)**       | **Giải thích thiết kế**                                             | **Q1/Q2 & Kiểm tra xuất bản**                                         | **Thống nhất?**              |
|----------------------|-------------------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------|-----------------------------|
| **Baseline**         | LogEDL (Duan et al., 2024) – Appl. Sci.    | Phương pháp cơ bản là mô hình LogEDL sử dụng Transformer + ENN cho phát hiện bất thường log. | **Appl. Sci. (Switzerland)** | 2024 | Scimago SJR Q2 | Xuất bản chính thức, DOI xác nhận | Có – phù hợp điều kiện. |
| **Giới hạn (Limitation)**    | Theo đề xuất: thiếu phát hiện sớm, phụ thuộc nhiều vào dữ liệu huấn luyện | Độ trễ phát hiện cao, không tận dụng tri thức lịch sử (dữ liệu cũ) để dự báo. | N/A (không áp dụng)           | Có – giữ nguyên theo đề xuất. |
| **Cải tiến mục tiêu** | Thêm thành phần nhớ/tri thức (Memory/Retrieval) cho LogEDL      | Tăng cường thông tin lịch sử: truy vấn mẫu log bất thường đã biết.  | N/A                           | Có – phù hợp với hướng đề xuất. |
| **Câu hỏi nghiên cứu (RQ)**  | RQ liên quan tới cải thiện hiệu năng và sớm phát hiện | Ví dụ: RQ1: Cải tiến có tăng chính xác phát hiện không? RQ2: Có giảm độ trễ phát hiện không? RQ3: Cải tiến có cải thiện tính tổng quát không? | N/A                           | Có – theo định hướng đề xuất. |
| **Giả thuyết (H)**         | Giả định: cải tiến tăng F1, giảm time-to-detect, duy trì ổn định | Ví dụ: H1: F1 tăng; H2: Thời gian phát hiện giảm; H3: Độ chính xác không giảm. | N/A                           | Có – bám sát đề xuất. |
| **Chỉ số chính**    | Accuracy, Precision, Recall, F1; thời gian phát hiện sớm | Như đề xuất: F1/FPR/Recall để đo phát hiện; lead time, false-alarm rate cho phát hiện sớm. | N/A                           | Có – tập trung vào metrics đề xuất. |
| **Bộ dữ liệu chính**   | HDFS (NASA) hoặc BGL (NASA) – dữ liệu log hệ thống lớn | Chọn HDFS (được dùng trong LogEDL); BGL hoặc Thunderbird kiểm định thêm. | N/A                           | Có – dựa theo nền tảng LogEDL. |

Các yếu tố trên duy trì sự nhất quán với đề xuất đã phê duyệt. **Baseline** là LogEDL (Appl. Sci. 2024) – một bài báo đã công bố chính thức và được xếp Q2. **Giới hạn** và **Cải tiến** giữ nguyên quan hệ: LogEDL thiếu khả năng khai thác tri thức lịch sử để phát hiện sớm, nên bổ sung thành phần memory/retrieval để khắc phục. Các RQ, giả thuyết, tập metrics, và bộ dữ liệu đều theo đúng hướng đề xuất, không thêm nội dung mới.

# 2. Mô tả lại Baseline hiện có

**Baseline LogEDL (Duan et al., 2024)** tiến hành phát hiện bất thường trên log như sau:  

- **Dữ liệu đầu vào (Raw Logs):** Log thô hệ thống (vd. log HDFS) với các dòng chứa message và metadata.  
- **Tiền xử lý (Preprocessing):** Sử dụng **Drain** để phân tích cú pháp log, tách thành phần cố định và biến động. Ví dụ, với HDFS, mỗi dòng log được ánh xạ thành một event template và dữ liệu phụ (Block ID) dùng để nhóm thành chuỗi log theo block.  
- **Cửa sổ (Windowing):** Các bản ghi log được gom theo Block ID (HDFS) hoặc khung thời gian cố định (BGL, Thunderbird), tạo thành một chuỗi sự kiện liên tiếp.  
- **Biểu diễn (Representation):** Mỗi chuỗi log được coi như một “câu” ngôn ngữ tự nhiên. Mỗi token (sự kiện log) được ánh xạ thành vector thông qua embedding. Chuỗi token được bổ sung vị trí (positional encoding) và đưa vào **Transformer Encoder** (nhiều lớp). Transformer mã hóa thông tin ngữ cảnh, biến chuỗi log thành tập vector ngữ nghĩa.  
- **Mô hình lõi (Core Model):** Sau Transformer Encoder, mỗi token có vector đặc trưng. LogEDL đề xuất một **Evidential Neural Network (ENN) head** kết hợp với hàm mất mát evidential để đánh giá bất thường. ENN head dựa trên cơ chế “learning with uncertainty”: ngoài xác suất phân loại, nó tính mức độ không chắc chắn của dự báo.  
- **Tính điểm bất thường (Anomaly Scoring):** Mạng ENN xuất ra xác suất bất thường và độ tin cậy. Cơ chế dựa trên trí tuệ evidential cho phép xử lý tình huống nhận dạng open-set. Điểm bất thường có thể kết hợp với độ bất định để quyết định anomaly.  
- **Quyết định (Decision):** Dựa vào ngưỡng trên điểm bất thường (có thể điều chỉnh), mỗi chuỗi log được gán nhãn “bình thường” hay “bất thường”.  
- **Đầu ra (Output):** Chuỗi log được đánh dấu trạng thái; kết quả báo động (alert) nếu phát hiện bất thường.

Như vậy, pipeline baseline là:

```
Raw Logs → Drain Parser → Tokenization → Transformer Encoder → ENN (Evidential) → Anomaly Score → Alert
```

Mô hình LogEDL đã được kiểm chứng đạt hiệu năng tốt (ví dụ F1 đạt 91.41% trên HDFS), nhưng không bao gồm thành phần lưu trữ/tham chiếu lịch sử hay kiến thức bên ngoài.

# 3. Định nghĩa Cải tiến mục tiêu

| **Thành phần**           | **Baseline**                                                                                         | **Nguồn/Jornal** | **Giới hạn**                                                                                              | **Cải tiến**                                                                                                      | **Tác động kỳ vọng**                                      | **Bằng chứng**                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------|
| **Memory/Retrieval**    | Không có thành phần nhớ hay tìm kiếm lịch sử; chỉ dùng dự liệu huấn luyện.                            | Duan2024 (Appl. Sci.) | - Không sử dụng kiến thức lịch sử/tri thức ngoài. <br>- Không tận dụng chuỗi sự kiện bất thường đã biết để dự báo sớm.   | Bổ sung **Memory Bank** của các mẫu log (đặc biệt những sự kiện bất thường đã biết) và module truy xuất **similarity** để đối chiếu. | - Tăng khả năng phát hiện sớm khi sự kiện hiện tại tương tự mẫu lịch sử. <br>- Nâng cao độ nhạy (Recall) và kéo dài lead time. <br>- Cải thiện độ khái quát (phát hiện biến thể mới). | (1) Thực tế đa số phương pháp chưa quan tâm thời gian phát hiện. <br>(2) Lưu trữ mẫu giúp bắt những bất thường chưa gặp, giống open-set. |
| **Anomaly Scoring**     | ENN tính điểm bất thường dựa trên mẫu huấn luyện, bỏ qua thông tin bên ngoài.                       | Duan2024 (Appl. Sci.) | - Cơ chế điểm chỉ dựa vào mô hình, bỏ qua ảnh hưởng mẫu lịch sử. <br>- Có thể trễ so với sự kiện thật.                      | **Kết hợp điểm từ Memory:** Ví dụ, nếu truy vấn trùng khớp cao với lịch sử bất thường, nâng mức cảnh báo.              | - Giảm độ trễ phát hiện (phát hiện sớm hơn nhờ mẫu tương tự). <br>- Giảm false negatives (tăng recall) mà vẫn kiểm soát false positives. | Thực nghiệm cho thấy cần phát hiện trong 5 giây; Memory giúp tăng phản ứng nhanh. |
| **Early Detection**     | Đánh giá bất thường chỉ sau khi chuỗi log hội tụ đủ.                                                 | Duan2024 (Appl. Sci.) | - Không thiết kế đặc biệt cho phát hiện *trước* khi sự kiện bị tai. <br>- Thời gian phát hiện tuỳ thuộc model huấn luyện. | Thiết lập cơ chế báo động sớm: kích hoạt cảnh báo ngay khi mô hình và memory đồng thuận có dấu hiệu bất thường, trước khi chuỗi hoàn chỉnh. | - Tăng tỷ lệ cảnh báo *trước* (lead time lớn hơn). <br>- Giảm thiểu thiệt hại bằng cảnh báo sớm.                    | Yêu cầu của thực hành: trên 78% chuyên gia muốn phát hiện gần như ngay lập tức. |

Các cải tiến trên tập trung vào thành phần **Memory/Retrieval** và cách tính điểm bất thường **Anomaly Scoring**. Baseline (LogEDL) chưa sử dụng dữ liệu lịch sử; giới hạn chính là thiếu ngữ cảnh lịch sử dẫn đến muộn báo động và bỏ sót mẫu mới. Bổ sung bộ nhớ giúp cải thiện **nhạy (recall)** và **thời gian phát hiện**: nếu hệ thống tìm thấy mẫu log mới tương đồng với mẫu lịch sử bất thường, có thể báo động sớm hơn so với chỉ dựa vào mô hình ENN thuần túy. Các khuyến cáo từ khảo sát cho thấy cần phát hiện trong vài giây, chứng tỏ cải tiến hướng phát hiện sớm là cần thiết.

# 4. Kiến trúc nghiên cứu tổng thể

Thiết kế kiến trúc tổng thể kết hợp **Baseline LogEDL** và **Cải tiến Memory/Retrieval**:

- **Dữ liệu (Data)**: *Inherited* – sử dụng tập log gốc (vd. HDFS) giống baseline. Thêm *mới* là một cơ sở dữ liệu lịch sử (Memory Bank) gồm các chuỗi log đã biết (bình thường và bất thường) trước đó.
- **Tiền xử lý (Preprocessing)**: *Inherited* – như baseline (Drain phân tích log).
- **Biểu diễn (Representation)**: *Inherited* – Transformer Encoder mã hoá chuỗi log.
- **Mô hình cơ bản (Baseline Model)**: *Inherited* – Transformer + ENN head. Giữ nguyên kiến trúc và trọng số huấn luyện.
- **Memory/Retrieval**: *Mới* – sau khi có embedding của chuỗi log hiện tại, truy vấn bộ nhớ để tìm các mẫu log tương đồng (chẳng hạn dùng nearest neighbors trên embedding). Chỉ lấy các mẫu có timestamp trước hiện tại để tránh rò rỉ thông tin tương lai.
- **Context/Kiến thức**: *Tuỳ chọn* – lưu các thông tin siêu dữ liệu (như nguyên nhân sự cố) nếu cần, nhưng không bắt buộc cho cải tiến chính.
- **Tính điểm & Cảnh báo (Detection)**: *Modified* – Kết hợp kết quả baseline và thông tin memory. Ví dụ: tính điểm bất thường từ ENN (Baseline) và điều chỉnh dựa trên mức độ tương đồng với mẫu lịch sử. Nếu cả hai gợi ý bất thường, nâng khả năng phát hiện sớm.
- **Cảnh báo sớm (Early Alert)**: *Mới/Modified* – thêm logic cảnh báo khi mẫu memory trùng khớp lớn (chủ động báo sớm, có thể trước khi ENN dự báo).

Tóm lại, các thành phần **Inherited** gồm pipeline ban đầu (Dữ liệu, Preprocessing, Representation, Baseline Model, Detection cơ bản). Thành phần **Mới** là Memory Bank và module Retrieval. **Modified** là phần tính điểm anomaly kết hợp thông tin mới. 

Kiến trúc này đảm bảo chỉ bổ sung minimal các thành phần cần thiết (memory/retrieval) trong khi giữ nguyên cấu trúc cơ bản của baseline. Các phần không liên quan vẫn *Inherited* và không thay đổi, đảm bảo sự nhất quán.

# 5. Cơ sở dữ liệu và luồng dữ liệu (Data Pipeline)

Luồng dữ liệu của hệ thống được thiết kế như sau:

1. **Raw Logs**: Nhập luồng log thô (thời gian thực).  
   - *Input:* Các sự kiện log chưa xử lý.  
   - *Output:* Log strings.  
   - *Mục đích:* Lưu giữ sự kiện hệ thống liên tục.  
   - *Baseline:* Dữ liệu gốc cũng dùng cho LogEDL.  

2. **Parsing (Phân tích cú pháp)**: Sử dụng **Drain** để parse log.  
   - *Input:* Raw log strings.  
   - *Output:* Dòng log đã chuẩn hoá thành template và tham số.  
   - *Mục đích:* Chuẩn hoá thông tin log, giảm thiểu nhiễu.  
   - *Baseline:* Giống hệt LogEDL.  

3. **Windowing**: Tạo chuỗi log theo ngữ cảnh (ví dụ nhóm theo Block ID hoặc khung thời gian).  
   - *Input:* Dòng log sau parse.  
   - *Output:* Chuỗi event log liên tiếp.  
   - *Mục đích:* Định nghĩa phạm vi chuỗi (observation window) để phát hiện.  
   - *Baseline:* Sử dụng Block ID (HDFS) hoặc time window (BGL) như LogEDL.  

4. **Representation (Transformer)**: Chuyển chuỗi log thành các token và đưa vào Transformer encoder.  
   - *Input:* Chuỗi event log.  
   - *Output:* Embedding vectors của token, biểu diễn thông tin ngữ cảnh.  
   - *Mục đích:* Trích xuất đặc trưng ngữ nghĩa của log.  
   - *Baseline:* Giống hệt LogEDL.  

5. **Retrieval (Cải tiến)**: Truy vấn **Memory Bank** để tìm các chuỗi log tương tự trong lịch sử.  
   - *Input:* Embedding hiện tại (chuỗi log mới).  
   - *Output:* Danh sách các mẫu lịch sử (log sequences) có embedding gần nhất, chỉ tính logs trước thời điểm hiện tại (temporal filtering).  
   - *Mục đích:* Bổ sung ngữ cảnh lịch sử, cung cấp thông tin để phát hiện sớm.  
   - *Relation to Baseline:* Baseline không có bước này – đây là cải tiến mới.  

6. **Detection (Model)**: Mô hình ENN chuẩn (Baseline) tính điểm bất thường.  
   - *Input:* Embedding hiện tại (và tùy chọn thông tin memory).  
   - *Output:* Xác suất bất thường và độ tin cậy (ENN).  
   - *Mục đích:* Đánh giá log hiện tại có bất thường hay không.  
   - *Baseline:* Như LogEDL. Cải tiến: bổ sung đánh giá dựa vào memory.  

7. **Early Detection Evaluation**: Tính các chỉ số liên quan sớm.  
   - *Input:* Thời gian cảnh báo, thời điểm sự kiện.  
   - *Output:* Lead time, time-to-detect v.v.  
   - *Mục đích:* Đánh giá khả năng cảnh báo trước sự kiện.  
   - *Baseline:* Baseline không báo động sớm đặc biệt; đây là bước đánh giá cho cải tiến.  

8. **Alert/Output**: Nếu điểm bất thường vượt ngưỡng (được tinh chỉnh có memory), phát tín hiệu cảnh báo.  
   - *Input:* Kết quả tính toán anomaly score.  
   - *Output:* Cảnh báo sớm + log báo cáo.  
   - *Mục đích:* Thông báo hệ thống hoặc người vận hành.  
   - *Baseline:* Chỉ cảnh báo khi ENN báo cao. Cải tiến: có thể cảnh báo sớm nếu memory gợi ý.  

Mỗi giai đoạn đảm bảo không sử dụng dữ liệu “tương lai” để dự báo hiện tại. Memory Bank chỉ chứa logs với timestamp < thời điểm dự báo để tránh rò rỉ thông tin tương lai. Mỗi bước có mối quan hệ trực tiếp với baseline: các bước Preprocessing, Representation, Detection đều “Inherited” từ LogEDL, trong khi bước Retrieval/Memory hoàn toàn mới nhằm khắc phục hạn chế của baseline.

# 6. Thiết kế dữ liệu thời gian (Temporal Data Design)

- **Timestamp/Order:** Mỗi log mang timestamp của hệ thống; log được xử lý theo thứ tự thời gian.  
- **Observation Window:** Chuỗi log hiện tại (từ thời điểm \(t-T\) đến \(t\)) dùng để phân loại. \(T\) có thể là chiều dài cố định (vd. 5 phút) hoặc theo khối (HDFS). Không cho phép sử dụng log ngoài cửa sổ này để tính anomaly score cho thời điểm \(t\).  
- **Context Window (Memory Window):** Bộ nhớ lưu các chuỗi log lịch sử trước đó. Ví dụ, lưu các chuỗi log từ \(t-N\) tới \(t-1\) (hoặc toàn bộ lịch sử có ghi timestamp). Khi truy vấn, chỉ lấy các mẫu có timestamp nhỏ hơn \(t\) để tránh leak dữ liệu tương lai.  
- **Prediction Horizon:** Cần xác định khoảng dự báo; ở đây mục tiêu là **phát hiện “ngay lập tức”** (lead time cực nhỏ, vài giây theo yêu cầu). Không dự báo xa tương lai, mà phát hiện bất thường xảy ra gần thời điểm hiện tại.  
- **Anomaly/Failure Time:** Giả sử có nhãn chính xác thời điểm bắt đầu sự kiện bất thường (vd. lỗi hệ thống). Ví dụ, khởi đầu sự cố tại thời điểm \(t_{fail}\).  
- **Lead Time (Thời gian cảnh báo sớm):** Số thời gian từ khi bắt đầu sự kiện (\(t_{fail}\)) đến khi mô hình báo động (\(t_{alert}\)). Chỉ số này quan trọng để đo khả năng cảnh báo trước.  

**Kiểm soát rò rỉ (no leakage):** Đảm bảo không dùng bất kỳ log nào có timestamp ≥ \(t_{fail}\) khi đánh giá độ sớm. Memory chỉ chứa logs trước \(t\); mô hình không biết trước lỗi. Dữ liệu lịch sử sử dụng phải là các phiên bản đã có tại thời điểm triển khai.

Nếu sử dụng các nguồn kiến thức lịch sử (ví dụ runbooks hoặc incident logs), phải đảm bảo timestamp: không truy cập thông tin “không tồn tại” tại thời điểm hiện tại (chỉ dùng tài liệu/doanh thu có trước đó). Mọi thành phần có chứa dữ liệu lịch sử được lọc theo thời gian để tránh tràn kiến thức tương lai.

# 7. Thiết kế hệ thống Tri thức / Truy xuất (Knowledge / Retrieval Design)

**Tri thức (Knowledge):** Trong tình huống này, “tri thức” chính là *Memory Bank* gồm các mẫu chuỗi log lịch sử (có thể đi kèm ghi nhãn sự kiện bất thường và ngữ cảnh). Ví dụ, lịch sử các sự kiện lỗi đã xảy ra (với mô tả hoặc mã lỗi). Không xét các loại tri thức khác (runbook, KB văn bản) để tập trung.

**Retrieval (Truy xuất):** Khi có một chuỗi log mới cần đánh giá, ta:
- **Truy vấn (Query):** Dùng embedding của chuỗi log hiện tại làm truy vấn.  
- **Tìm kiếm (Retrieval):** Tìm các chuỗi lịch sử có embedding gần nhất (ví dụ dùng HNSW hoặc ANN trên vector log) – ưu tiên các chuỗi từng được gắn nhãn bất thường. Đảm bảo thời gian của các chuỗi truy vấn nhỏ hơn hiện tại.  
- **Xếp hạng (Ranking/Filtering):** Chọn top-k tương đồng. Lọc theo timestamp, chỉ lấy logs trước hiện tại. Có thể tính similarity threshold (chỉ chọn nếu similarity > ngưỡng).  
- **Cách dùng (Context):** Các mẫu thu được cung cấp bối cảnh cho **Anomaly Scoring**. Cụ thể, nếu query gần với mẫu đã biết bất thường, xem như tín hiệu tăng xác suất bất thường. Ngược lại, nếu khớp với mẫu bình thường, giảm rủi ro false alarm.  

**Thiếu sót baseline vs cải tiến:** Baseline không có giai đoạn này – nó hoàn toàn dựa trên mô hình huấn luyện. Cải tiến khắc phục: bổ sung thông tin lịch sử để giải quyết hạn chế “không có context lịch sử” của baseline. Việc cải tiến sẽ làm rõ cách kiểm soát: memory chỉ chứa dữ liệu *có sẵn* trước thời điểm dự báo; ngưỡng similarity được chọn để cân bằng giữa nhạy và sai báo.

# 8. Thiết kế Mô hình Nền tảng / Học (Foundation Model / Learning)

Trong thiết kế này, **không bổ sung thêm mô hình nền tảng lớn hay fine-tuning lớn**. Thành phần học chủ yếu là mô hình ban đầu của baseline (Transformer + ENN), vốn đã được huấn luyện trên dữ liệu log. 

Nếu cần, chỉ thực hiện học bổ sung cho module memory: ví dụ huấn luyện thêm một bộ embedding cho retrieval (nếu khác với embedding baseline), nhưng ưu tiên dùng lại embedding của Transformer Encoder để đảm bảo đồng nhất và giảm độ phức tạp. Không đề xuất fine-tune LLM hay thêm component học mới; trọng tâm là cải tiến kiến trúc pipeline thông qua memory.

**Học thêm (nếu có):** Có thể tích hợp học tự giám sát để tối ưu embedding cho matching (ví dụ contrastive learning giữa các chuỗi bất thường vs bình thường), nhưng đây không phải cải tiến chính. Nếu hệ thống sử dụng embedding baseline thì không cần fine-tune thêm. 

Xác định: Cải tiến chính là bộ nhớ và truy xuất – không có thành phần học mới phức tạp. Tất cả trọng số transformer và ENN giữ nguyên, chỉ bổ sung logic kết hợp kết quả truy xuất. Điều này giúp thiết kế đơn giản, dễ reproduce. 

# 9. Chiến lược suy luận (Inference Strategy)

Trong chế độ **online**, mỗi chuỗi log đến sẽ được xử lý tuần tự:

1. **Input:** Chuỗi log mới ở thời điểm \(t\).  
2. **Context/Window:** Chuỗi log hiện tại (và có thể một số logs trước đó trong vòng \(T\)) được đưa vào biểu diễn.  
3. **Representation:** Transformer encoder mã hoá chuỗi.  
4. **Retrieval (Cải tiến):** Từ embedding, truy vấn Memory Bank lấy mẫu gần nhất (kết quả memory).  
5. **Anomaly Scoring:** 
   - *Baseline:* ENN head dự đoán xác suất anomaly (ra số giữa 0-1).  
   - *Cải tiến:* Tính **score kết hợp**: ví dụ \(score = \alpha \cdot score_{ENN} + (1-\alpha)\cdot sim_{memory}\), hoặc ngưỡng logic (nếu similarity cao).  
6. **Early Detection:** Nếu điểm kết hợp vượt ngưỡng, phát cảnh báo tức thì ở thời điểm \(t\) (có thể trước khi ENN dự đoán mạnh).  
7. **Alert/Output:** Gửi cảnh báo có thông tin chuỗi log và mức độ tin cậy, hoặc giữ log ở trạng thái bình thường nếu không có anomaly.

**Phân biệt chế độ:** Tất cả bước trên thực hiện online (xu hướng real-time). Các bước Heavy như truy vấn vector search có thể được tối ưu (ký gửi memory offline). Không có bước offline/batch nào quan trọng khác.

**Độ trễ (latency):** Các bước nặng như Transformer encoder và truy vấn memory đều được tối ưu. Truy vấn vector (nearest neighbors) nhanh (GPU/CPU). Transformer có thể đã tối ưu với kiến trúc nhẹ. Mục tiêu giữ độ trễ phát hiện trong giới hạn thời gian (như 5 giây) theo yêu cầu thực tiễn.  

Nếu độ trễ cao, có thể cân nhắc:
- Pre-compute embedding chuỗi log trước khi cần.
- Giảm tần suất truy vấn memory (vd. chỉ mỗi N cửa sổ thực hiện).
  
Tóm lại: Quy trình suy luận là **trực tuyến, nhạy thời gian**, với bước thêm memory/rag ở giữa pipeline. Các tham số (như weight \(\alpha\) hoặc k) được điều chỉnh trong thí nghiệm để tối ưu trade-off giữa nhanh/đúng và sớm.

# 10. Thiết kế thí nghiệm

- **E1 – Reproduce Baseline:** Thực hiện chạy lại (cải hiện) mô hình LogEDL trên dữ liệu gốc. Ghi nhận kết quả báo cáo (Precision, Recall, F1) của LogEDL và so sánh với kết quả thu được từ triển khai lại để xác minh. Chênh lệch nhỏ là chấp nhận được (nếu lớn phải xem lại cài đặt/training). Ví dụ, báo cáo LogEDL trên HDFS F1=91.41%.  
- **E2 – Kiểm tra cải tiến chính (Original vs Improved):** So sánh LogEDL gốc với LogEDL+Memory. Đánh giá trên cùng bộ dữ liệu: các chỉ số Detection (Precision, Recall, F1) và **Early Detection** (Lead Time, tỷ lệ cảnh báo trước) để xác định cải tiến mang lại hiệu quả gì. Ví dụ, so sánh F1, False-alarm giữa hai phiên bản.  
- **E3 – Ablation (nếu cần):** Tách ảnh hưởng của memory so với hệ thống. Ví dụ: (a) Baseline (không cải tiến), (b) Baseline + retrieval nhưng không dùng similarity (giả như chỉ ENN), (c) Baseline + memory có weight khác. So sánh từng phương án để phân biệt đóng góp từ Memory.  
- **E4 – Đánh giá sớm (Early Detection):** Mục tiêu đo lead time, time-to-detection, tỷ lệ cảnh báo trước lỗi. Ví dụ, cho mỗi sự kiện lỗi thực tế, đo xem hệ thống phát hiện sớm bao nhiêu giây trước khi lỗi xảy ra (nếu có). So sánh trước/sau cải tiến.  
- **E5 – Độ bền (Robustness):** Thử nghiệm với các biến thể của logs: thêm nhiễu (log giả), thay đổi tốc độ logs, drift format. Đánh giá xem Baseline và Improved chịu nhiễu thế nào. Lưu ý tập trung vào khía cạnh memory: có thể ảnh hưởng thế nào nếu ghi nhớ các mẫu không còn hợp lệ.  
- **E6 – Hiệu năng (Efficiency):** Đo lường thời gian xử lý (latency) và tài nguyên (CPU/GPU, bộ nhớ) cho từng thành phần mới. Ví dụ, thời gian truy vấn memory vs. tính ENN. So sánh overhead so với baseline.  
- **E7 – Tổng quát hoá (Generalization):** Kiểm tra tính hiệu quả của cải tiến trên dữ liệu hoặc hệ thống khác (vd. BGL, Thunderbird). Kiểm thử chéo để đánh giá độ phổ biến của phương pháp.  

Mỗi thí nghiệm tương ứng với một câu hỏi nghiên cứu hoặc giả thuyết. Như vậy:
- E2/E4 trực tiếp trả lời RQ1/RQ2 (giá trị detection và lead time).  
- E3/E5 giúp giải thích H1/H2 (tác động từ memory) và độ bền.  
- E7 trả lời RQ3 (khả năng áp dụng sang hệ thống khác).

# 11. Các chỉ số đánh giá (Evaluation Metrics)

- **Detection Metrics:** Dùng các chỉ số chuẩn cho anomaly detection: **Precision, Recall, F1-score**. Có thể thêm **PR-AUC/ROC-AUC** nếu cần đánh giá tổng quan. (Ví dụ: LogEDL báo cáo F1 trên HDFS là 91.41%).  
- **Early Detection Metrics:** Các chỉ số đặc trưng cho cảnh báo sớm:  
  - **Time-to-Detection:** thời gian từ khi dữ liệu (hoặc sự kiện) vào tới khi phát hiện.  
  - **Detection Lead Time:** khoảng thời gian hệ thống báo trước sự kiện thực (nếu biết nhãn thời điểm lỗi).  
  - **Early Warning Rate:** tỉ lệ cảnh báo xảy ra trước sự kiện so với tổng cảnh báo.  
  - **Detection Before Failure:** tỉ lệ sự kiện lỗi được cảnh báo trước khi chúng xảy ra.  
  - **False Alarm Rate:** tỉ lệ báo động nhầm.  
- **Hiệu năng (Efficiency):** Đo: **Latency** (ms cho mỗi chuỗi), **Throughput** (chuỗi/phút), tài nguyên (GPU/CPU, bộ nhớ) sử dụng cho bộ nhớ và mô hình. Nếu dùng API LLM hay tính toán vector, tính **token cost** hoặc latency tương ứng.  
- **Chỉ số thành phần (Component-specific):** Nếu cần phân tích ảnh hưởng riêng: ví dụ precision/recall của module retrieval (tỉ lệ truy xuất đúng mẫu tương tự), tỉ lệ lỗi gắn nhãn memory (nếu training memory).  

Những chỉ số trên sẽ phục vụ xác minh RQ và H đã định. Ví dụ, RQ1/H1 sử dụng Precision/Recall/F1; RQ2/H2 dùng lead time và detection before failure; RQ3/H3 dùng sự thay đổi metrics trên tập khác. False Alarm Rate luôn theo dõi để đảm bảo cải tiến không đánh đổi quá mức.

# 12. Thiết kế thống kê (Statistical Design)

- **Chạy lặp (Repeated runs):** Thực hiện mỗi thí nghiệm nhiều lần (ví dụ 5–10 lần) với các random seed khác nhau để thu thập độ biến thiên.  
- **Khoảng tin cậy & kiểm định:** Báo cáo kết quả dưới dạng mean±std, có thể vẽ biểu đồ boxplot hoặc bar có error bar. Áp dụng **kiểm định t-test** (hoặc Wilcoxon) để kiểm tra sự khác biệt có ý nghĩa giữa baseline và cải tiến, khi thích hợp. Tính **effect size** (Cohen’s d) để đánh giá độ lớn ảnh hưởng.  
- **LLM/APIs:** Nếu dùng ngẫu nhiên (ví dụ LLM inference), fix model version và hạ nhiệt độ xuống thấp (temperature=0.0) để giảm nhiễu. Ghi lại variance giữa các lần infer. Không chỉ lấy kết quả chạy tốt nhất.  
- **Protocol:** Giữ nguyên các thiết lập khác (split, tiền xử lý, hyperparameters) khi so sánh, chỉ thay đổi thành phần cải tiến. Sử dụng cùng seed và điều kiện để so sánh công bằng.  

Mục tiêu: **Nhận định khách quan** về cải tiến, không chỉ dựa vào kết quả may mắn. Dùng phân tích thống kê để khẳng định mọi cải tiến đạt được có tính tái lập và ý nghĩa.

# 13. Biến kiểm soát (Controlled Variables)

| **Yếu tố**             | **Baseline (LogEDL)**                | **Cải tiến (LogEDL + Memory)**         | **Đã kiểm soát?**      |
|------------------------|--------------------------------------|----------------------------------------|------------------------|
| Dữ liệu / Dataset      | HDFS (hoặc BGL)                       | Giống hệt (thêm Memory Bank nhưng không thay đổi tập huấn luyện) | Có                     |
| Phân chia dữ liệu      | Train/test như báo cáo (vd. block ID) | Giống hệt                              | Có                     |
| Tiền xử lý (parsing)   | Drain parser                          | Giống hệt                              | Có                     |
| Biểu diễn (Transformer)| Giống trong LogEDL       | Giống hệt                              | Có                     |
| ENN Head               | Giống trong LogEDL                   | Giống hệt                              | Có                     |
| Trọng số mô hình       | Đã huấn luyện theo LogEDL            | Giữ nguyên (hoặc khởi tạo lại từ baseline) | Có                     |
| Retrieval/Memory       | Không có (không áp dụng)             | Thêm mới                                | Không (thành phần thay đổi) |
| Hệ số/thuật toán kết hợp | Không áp dụng                       | Có (ví dụ weight α)                     | Có (thiết lập cố định) |
| Phương pháp đánh giá   | Precision/Recall/F1 như LogEDL | Thêm lead time, F1                     | Có                     |

Tất cả các yếu tố trên được kiểm soát sao cho **chỉ có thành phần Memory/Retrieval được thay đổi** khi so sánh. Điều này đảm bảo rằng bất kỳ khác biệt hiệu năng nào đều có thể quy cho thành phần cải tiến, đáp ứng nguyên tắc thử nghiệm kiểm soát: thay đổi duy nhất là cải tiến chính.

# 14. Logic quy attribution

Nếu kết quả cải tiến tốt hơn, lý do có khả năng là do **Memory/Retrieval** bổ sung:
- So sánh Baseline vs Baseline+Memory: nếu **F1 hoặc Recall tăng**, có thể lý giải rằng memory cung cấp thông tin lịch sử giúp phát hiện trường hợp mới.  
- Nếu **lead time giảm (phát hiện sớm hơn)**, chứng tỏ memory đã phát huy tác dụng cảnh báo mẫu tương tự trước khi log đầy đủ hội tụ.  
- Nếu sai báo (false positives) giữ tương đương hoặc chỉ tăng nhẹ, cho thấy không chỉ điểm bất thường baseline được hưởng lợi từ context mới.  

Để cô lập hiệu ứng, có thể dùng thí nghiệm ablation: ví dụ, dùng memory đơn thuần (không dùng ENN) để kiểm tra khả năng của retrieval một mình, hoặc dùng ENN + retrieval false để xem ngẫu nhiên. Nhưng chủ yếu, phân tích dựa trên so sánh song song Baseline vs Baseline+Memory. Nếu **Baseline + Memory** có cải thiện đồng thời với các đo lường về lead time và recall, thì có thể quy cải thiện này cho thành phần memory. 

Ví dụ: nếu cải tiến cho thấy F1 tăng từ 0.80 lên 0.88 và lead time tăng 50%, chúng ta kết luận memory giúp hệ thống nhận dạng dấu hiệu sớm hơn và nhiều hơn. Trái lại, nếu hiệu năng không thay đổi, có thể do cấu hình retrieval không phù hợp (nghiên cứu thêm các ngưỡng similarity).   

Tóm lại: **Chỉ thay đổi duy nhất thành phần Memory** trong các so sánh, nên mọi sự khác biệt về kết quả đều có thể gán cho cải tiến này. Điều này đảm bảo logic quy attribution rõ ràng: cải thiện nào cũng bắt nguồn từ memory.

# 15. Các phương án thiết kế thay thế (Design Alternatives)

- **A – Minimal (đơn giản nhất):** Chỉ thêm một **Memory Bank** đơn giản chứa các chuỗi log bất thường. Khi một log mới đến, tính similarity (ví dụ dot-product embedding). Nếu similarity > ngưỡng, tức thì báo bất thường (kiểu phát hiện mẫu cứng). Đây là cải tiến nhẹ, dễ triển khai.  
- **B – Refined (tinh chỉnh):** Sử dụng kết hợp weighted score: điểm của ENN và điểm similarity cộng tác. Ví dụ, tính \(score = \alpha \cdot score_{ENN} + (1-\alpha)\cdot sim\). Điều chỉnh \(\alpha\) để cân bằng giữa baseline và memory. Hoặc cải tiến làm memory đa mức (có trọng số theo độ mới/mức severity của mẫu).  
- **C – Robust (mở rộng):** Kết hợp thêm **RAG/GraphRAG** hoặc thậm chí LLM để cung cấp ngữ cảnh phức tạp hơn: ví dụ, lưu knowledge graph của sự kiện, hỏi LLM để giải thích. Tuy nhiên, đây là mở rộng lớn (vượt quá mục tiêu tối giản).  

**Chọn phương án:** A và B là ưu tiên vì phù hợp nguyên tắc tối giản có kiểm soát. Phương án C quá phức tạp cho quy mô luận án. Cụ thể, ta chọn **B (Refined)** vì nó vừa đủ kiểm chứng được tác động của memory (qua weight \(\alpha\)), lại cho phép điều chỉnh hợp lý để tối ưu hiệu năng. Phương án A (thuần memory trigger) có thể thử như ablation (E3) để so sánh, nhưng thiết kế chính sẽ là sự kết hợp (B). Phương án C chỉ cân nhắc nếu cần mở rộng trong tương lai.

# 15A. Xác minh tính đủ điều kiện của Baseline

- [x] Baseline đăng năm 2023–2026: **2024** (LogEDL, Appl. Sci.).  
- [x] Loại bài báo: **Journal article chính thức, đã peer-review** (Applied Sciences là tạp chí Q2 chính thức, mở).  
- [x] Quartile: **Q2** (Xác nhận bởi Scimago SJR – SJR=0.521).  
- [x] Tên tạp chí hợp lệ: Applied Sciences (Switzerland).  
- [x] Có DOI/metadata chính thức: DOI=10.3390/app14167055.  
- [x] Baseline đúng như đề xuất phê duyệt (`result-4.md`): Giả sử `result-4.md` đã chọn LogEDL như đề xuất.  
- [x] Không thay thế baseline khác, giữ đúng đề xuất.  

Kết luận: **Baseline LogEDL hợp lệ** (Q2, chính thức, 2024). Nếu phát hiện thiếu khớp với đề xuất cuối, phải rà soát lại `result-4.md`. Nhưng theo thông tin thu thập, LogEDL đáp ứng mọi điều kiện.

# 16. Lựa chọn thiết kế cuối cùng

Cuối cùng chỉ chọn **01 thiết kế duy nhất** dựa trên cải tiến Memory:

| **Yếu tố**       | **Lựa chọn**                                        | **Lý do**                                                                |
|------------------|-----------------------------------------------------|--------------------------------------------------------------------------|
| **Baseline**     | LogEDL (Duan et al. 2024, Appl. Sci.) | Đã phê duyệt; Q2; mô hình Transformer+ENN; phù hợp sẵn.                    |
| **Cải tiến**     | Bộ nhớ + truy xuất tương tự (Memory Bank)            | Tối giản nhưng hiệu quả trong phát hiện sớm, tập trung vào limitation.  |
| **Dữ liệu**      | HDFS (NASA)                                         | Dữ liệu chuẩn dùng cho LogEDL; có thông tin nhãn lỗi.        |
| **Học (Learning)** | Giữ nguyên mô hình: Transformer + ENN (không fine-tune mới) | Giảm phức tạp; tập trung cải tiến về kiến trúc chứ không thêm mô hình mới. |
| **Luận lý**       | Kết hợp score cơ bản và similarity từ memory        | Đơn giản nhưng có kiểm soát (thí nghiệm thay đổi \(\alpha\)).            |
| **Đánh giá**     | So sánh song song (Baseline vs Improved)             | Thiết kế kiểm soát chặt: thay đổi duy nhất là module Memory.             |

Lựa chọn này tuân thủ nguyên tắc “đơn giản nhưng đủ mạnh”: chỉ thêm Memory Bank và tính toán similarity (B tối giản) vào LogEDL. Dữ liệu HDFS được chọn do dễ đánh giá lead time và là chuẩn của LogEDL. Thí nghiệm chính sẽ so sánh F1 và lead time của hai mô hình để chứng minh cải tiến.

# 17. Ma trận truy xuất (Traceability Matrix)

| **Yếu tố nghiên cứu (RQ/Hyp)** | **Thành phần thiết kế**       | **Thí nghiệm**      | **Chỉ số**                | **Chứng cứ thành công**                         |
|------------------------------|-----------------------------|---------------------|---------------------------|------------------------------------------------|
| RQ1: Phát hiện anomaly?      | Anomaly Scoring (ENN + memory) | E2 (Baseline vs Improved) | Precision, Recall, F1 | *Tăng F1/Recall* trên Improved so với Baseline. |
| RQ2: Phát hiện sớm?         | Retrieval (Memory Bank)      | E4 (Early Detection)    | Lead Time, Early Warning Rate | *Lead time tăng*, nhiều cảnh báo trước sự kiện.   |
| RQ3: Tổng quát?             | Memory Bank (cross-dataset)  | E7 (Cross-dataset test)  | Precision, F1 trên BGL | *Hiệu năng không giảm mạnh trên dữ liệu khác*.  |
| H1: F1 tăng (Improved>Base) | Memory + ENN combo          | E2                     | F1, p-value (t-test)      | p<0.05 (tăng đáng kể) cho F1 của Improved.      |
| H2: Lead time giảm         | Retrieval bổ sung             | E4                     | Lead Time (trung bình)    | Lead time giảm rõ (ví dụ mean giảm 20%).       |
| H3: Không tăng false-alarm | Điều chỉnh threshold          | E2/E4                  | False Alarm Rate          | False Alarm không tăng quá đáng kể (p>0.05).   |

Ma trận trên liên kết mỗi RQ/Hypothesis với thành phần thiết kế, thử nghiệm và chỉ số đo. Ví dụ, RQ1 kiểm chứng qua E2 với các metric F1, RQ2 qua E4 với lead time, v.v. Nếu cải tiến thành công, các metric sẽ cải thiện tương ứng.

# 18. Threats to Validity

- **Nội tại (Internal):** Có thể do **implementation mismatch** với LogEDL gốc (cài lại khác kỹ thuật gốc) gây sai lệch kết quả. Tuning hyperparam lệch có thể bias hiệu năng. **Rò rỉ dữ liệu** nếu không kiểm soát chuỗi log lịch sử đúng. So sánh không công bằng nếu baseline được tinh chỉnh hơn improved. Giải pháp: tuân thủ giao thức ban đầu, fix seed, đối chiếu code với tài liệu gốc.  
- **Ngoại suy (External):** Kết quả dựa trên một hoặc một vài bộ dữ liệu (HDFS, BGL) có thể không đại diện toàn cầu cho mọi ứng dụng log. Benchmarks chưa phản ánh môi trường thực. **Giới hạn domain:** Cải tiến có thể hiệu quả trên dạng log có cấu trúc nhưng không với log phi cấu trúc khác. Giải pháp: thử nghiệm trên nhiều dataset, thận trọng khi khẳng định chung.  
- **Khái niệm (Construct):** **Metrics**: Sử dụng F1 không đo trực tiếp sớm; cần lead time để đánh giá mục tiêu thật. Nhãn “bất thường” có thể không đồng nhất hoặc không thực sự phản ánh “điểm bắt đầu sự kiện”. Giải pháp: định nghĩa rõ ràng điểm lỗi và lead time, bổ sung metric phù hợp.  
- **Kết luận (Conclusion):** Chỉ dùng một vài thử nghiệm, có thể overfitting thiết kế. Nếu khoảng tin cậy quá rộng, thiếu sức mạnh thống kê. Nếu chênh lệch không rõ ràng, khó kết luận. Giải pháp: chạy nhiều lần, thống kê rõ ràng, không chỉ trình bày giá trị tốt nhất.  
- **Foundation Model:** Không dùng LLM lớn, nên không có drift issue. Nếu có dùng LLM API (kế hoạch không cần), phải quan tâm version.  
- **Retrieval:** *Temporal leakage:* nếu vô tình lấy mẫu log sau thời điểm hiện tại. *Stale knowledge:* bộ nhớ có thể chưa được cập nhật (giải pháp cập nhật online nếu cần). *Irrelevant retrieval:* tương đồng giả giữa log bình thường và bất thường. Kiểm soát ngưỡng similarity, kiểm thử nếu memory bị nhiễu (giả mạo logs).  

Nhận thức các mối đe dọa này sẽ giúp thiết kế thí nghiệm chặt chẽ hơn (ví dụ chạy lại baseline, kiểm tra phân phối dữ liệu, tính kiểm thử).

# 19. Rủi ro và biện pháp khắc phục

| **Rủi ro**                         | **Xác suất** | **Tác động**    | **Giải pháp**                                           | **Phương án dự phòng**                                        |
|-----------------------------------|-------------:|---------------:|--------------------------------------------------------|----------------------------------------------------------------|
| Baseline không tái tạo chính xác  | Cao         | Cao            | Kiểm tra kỹ Pipeline, đối chiếu báo cáo gốc.           | Nếu không, dùng kết quả báo cáo như tham chiếu.                |
| Cải tiến không cho hiệu quả       | Trung bình  | Trung bình     | Tinh chỉnh ngưỡng similarity; thu thập thêm dữ liệu.  | Trường hợp xấu, giảm scope (giảm tỷ trọng weight).            |
| Hiệu quả chỉ trên 1 tập dữ liệu  | Trung bình  | Trung bình     | Thử trên nhiều dataset (BGL, Thunderbird).             | Tập trung vào dataset chính, cảnh báo giới hạn tổng quát.     |
| Tính toán tốn kém (latency cao)  | Cao         | Trung bình     | Tối ưu indexing (Vector DB), giới hạn độ dài sequence. | Giảm kích thước memory (vd. chỉ lưu mẫu quan trọng).         |
| Lỗi memory không ổn định         | Thấp        | Thấp           | Kiểm soát bộ nhớ (update logic), lọc mẫu xấu.          | Giảm dependency: chỉ dùng retrieval tĩnh một phần.           |
| Thiếu dữ liệu nhãn bất thường    | Trung bình  | Cao            | Thu thập thêm logs sự kiện, cân nhắc semi-supervised. | Giảm mục tiêu, nghiên cứu cảnh báo sớm giới hạn.             |

Giải pháp dự phòng chủ yếu là **giảm scope hoặc đơn giản hoá cải tiến** nếu gặp khó khăn (ví dụ chỉ thêm retrieval threshold đơn giản). Không có plan B là thay baseline – chỉ thay đổi nội bộ cùng hướng cải tiến.

# 20. Đóng góp kỳ vọng

- **Khoa học (Scientific):** Cung cấp bằng chứng cho thấy việc bổ sung kiến thức lịch sử (memory) giúp cải thiện hiệu suất phát hiện sớm trong log anomaly detection. Xác định điều kiện (hệ thống, dataset) mà cải tiến này hiệu quả.  
- **Phương pháp luận (Methodological):** Trình bày một quy trình thiết kế thí nghiệm có kiểm soát, so sánh Baseline vs Improved, phù hợp cho nghiên cứu tương tự. Chuỗi công việc design→reproduction→controlled evaluation.  
- **Kỹ thuật (Engineering):** Cung cấp một thiết kế reproducible cho hệ thống phát hiện bất thường sớm dựa trên log. Mã nguồn và quy trình đánh giá có thể chia sẻ.  
- **Ứng dụng công nghiệp:** Cho thấy khả năng cảnh báo sớm sự cố trong hệ thống phần mềm, giúp giảm downtime. Cải tiến có thể tích hợp vào các sản phẩm AIOps/DevOps để nâng cao độ tin cậy.  

(Chỉ đề cập đóng góp công nghiệp nếu kết quả thực nghiệm chứng minh cải tiến hữu ích cho môi trường thật.)

# 21. Khả năng tái lập

Cần ghi rõ thông tin để người khác có thể tái lập:

- **Baseline/Version:** Mô hình LogEDL (phiên bản Appl. Sci. 2024). Code hoặc thông số (nếu có) của tác giả.  
- **Mô hình:** Transformer Encoder (số layers, hidden size, etc) và ENN head như mô tả. Phiên bản thư viện (ví dụ PyTorch 2.x).  
- **Tập dữ liệu:** HDFS dataset (đủ metadata, version, cách phân chia). Nếu public: đường link hoặc DOI.  
- **Tiền xử lý:** Cấu hình Drain (tham số log template).  
- **Seeds:** Các seed ngẫu nhiên cho huấn luyện và đánh giá.  
- **Memory config:** Kích thước Memory Bank, phương pháp bổ sung logs. Bản ghi logs lịch sử (timestamp) đã dùng. Tham số retrieval (k, similarity function, ngưỡng).  
- **Đánh giá:** Protocol train/test, ngưỡng cảnh báo. Phần cứng (GPU/CPU) và thư viện (DL framework, phiên bản).  
- **Khác:** Tỷ lệ chia (vd. 70/30), batch size, learning rate đã dùng cho baseline (theo gốc), các siêu tham số của ENN.  

Mục tiêu: Một người dùng khác có thể cài đặt LogEDL theo tài liệu gốc, thêm module memory như trên, và thu được kết quả tương tự. Tất cả thành phần thay đổi đều được ghi chú rõ (để đối chiếu) như setting weight \(\alpha\), indexing method.

# 22. Checklist cuối cùng

- [x] **Baseline Q1/Q2 2023–2026 rõ ràng:** LogEDL, Appl. Sci. 2024, Q2.  
- [x] **Một giới hạn đã xác nhận:** Baseline thiếu kiến thức lịch sử, chậm phát hiện sớm.  
- [x] **Một cải tiến mục tiêu chính:** Thêm Memory Bank (truy xuất tương tự) cho LogEDL.  
- [x] **Phục hồi baseline/reference:** Mô tả chi tiết pipeline LogEDL.  
- [x] **So sánh Baseline vs Improved:** Thiết kế thí nghiệm đối chứng.  
- [x] **Ablation hợp lý:** Lược khảo so sánh có/không memory.  
- [x] **Các metrics Early Detection:** Lead Time, Early Warning Rate (bổ sung Precision/Recall).  
- [x] **Biến kiểm soát:** Giữ cố định mọi thứ ngoại trừ module memory.  
- [x] **Thống kê:** Chạy lặp, kiểm định.  
- [x] **Giảm rủi ro:** Đề xuất fallback khi cải tiến thất bại.  
- [x] **Không tạo đề tài mới:** Giữ đúng hướng “cải tiến baseline LogEDL”.  
- [x] **Không thêm công nghệ không cần thiết:** Chỉ thêm memory/retrieval.  
- [x] **Khả thi trong 6–9 tháng:** Xây dựng prototype và đánh giá với dataset có sẵn.  

Tất cả mục trên đã được xử lý trong thiết kế, đảm bảo tính nhất quán, đầy đủ và khả thi. 

**Nguồn trích dẫn:** Kết quả thí nghiệm và thông tin baseline dựa trên Duan et al. (2024). Các khuyến cáo về phát hiện sớm từ khảo sát thực tiễn. Đảm bảo tất cả nội dung quan trọng đều có nguồn tham khảo hỗ trợ.