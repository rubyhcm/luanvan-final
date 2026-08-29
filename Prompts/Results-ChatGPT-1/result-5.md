# 1. Kiểm tra nhất quán thiết kế nghiên cứu  

| **Element**        | **Từ result-4**                                   | **Giải thích thiết kế**                                               | **Thống nhất?** |
|--------------------|---------------------------------------------------|---------------------------------------------------------------------|---------------|
| **Baseline**       | Phát hiện bất thường trên log sử dụng LLM (LLM-based)    | Phương pháp cơ sở: sử dụng Mô hình Ngôn ngữ lớn (LLM, ví dụ GPT-4 hoặc Llama) dưới dạng huấn luyện-thuần (inference only) để phân loại bản ghi log (bình thường/bất thường). | Có            |
| **Giới hạn**       | Thiếu bối cảnh lịch sử và tri thức miền (domain)            | LLM mặc định không sử dụng tri thức lịch sử hoặc ngữ cảnh rộng, dẫn đến khả năng cảnh báo sớm thấp (delay trong phát hiện).         | Có            |
| **Cải tiến mục tiêu** | Thêm truy xuất tri thức lịch sử (RAG) hoặc bộ nhớ vào LLM | Cải tiến: tích hợp RAG/memory để truy vấn log lịch sử hoặc kiến thức miền (như runbooks) nhằm mở rộng ngữ cảnh phân tích.      | Có            |
| **Câu hỏi RQ**     | RQ1, RQ2, RQ3 (xem result-4)                    | RQ1: Cải tiến có cải thiện độ chính xác phát hiện? RQ2: Cải tiến có cho phép cảnh báo sớm hơn? RQ3: Cải tiến có tổng quát tốt? | Có            |
| **Giả thuyết H**   | H1, H2, H3 (xem result-4)                     | H1: Cải tiến tăng F1; H2: Cải tiến giảm thời gian phát hiện; H3: Cải tiến tăng khả năng tổng quát/độ bền.               | Có            |
| **Chỉ số chính**   | Precision/Recall/F1, Độ trễ phát hiện             | Các chỉ số đánh giá: độ chính xác (Precision), độ thu hồi (Recall), F1, thêm các chỉ số phát hiện sớm như lead time, false alarm.   | Có            |
| **Dataset chính**  | BGL (hệ thống) và/hoặc HDFS (big data)        | Dữ liệu: Bộ dữ liệu log hệ thống điển hình (ví dụ BGL **Blue Gene/L** hoặc HDFS).                      | Có            |

Phần này đối chiếu giữa các yếu tố trong tài liệu `result-4.md` (đề xuất đã phê duyệt) và cách chúng ta hiểu để áp dụng vào thiết kế. Chúng tôi giả định các mục Baseline, RQ, Hypotheses… như trên phù hợp với định hướng đề tài; nếu có mâu thuẫn với đề xuất gốc, ưu tiên giữ nội dung của proposal (đã phê duyệt) để đảm bảo tính nhất quán.  

# 2. Tái cấu trúc Baseline hiện tại  

**Pipeline tổng quát:** Log thô → Tiền xử lý/Phân tích (Parsing) → Mã biểu diễn/Context → Mô hình dự báo (LLM) → Phát hiện bất thường → Đầu ra (cảnh báo).  

- **Đầu vào (Raw Logs):** Dữ liệu log thô của hệ thống, bao gồm các thông điệp thời gian (timestamp), mức độ (INFO/WARN/ERROR), component, và nội dung log. Log được sắp theo thứ tự thời gian.  
- **Tiền xử lý/Parsing:** Sử dụng bộ phân tích log (ví dụ Drain hoặc Spell) để tách template và tham số của mỗi thông điệp log. Kết quả: mỗi bản ghi log được biểu diễn dưới dạng `TemplateID + Giá trị tham số`. Bước này giúp giảm số lượng kí tự và chuẩn hóa định dạng trước khi đưa vào LLM.  
- **Mã biểu diễn (Representation):** Chuyển đổi bản ghi (hoặc một cửa sổ log) thành dạng ngôn ngữ tự nhiên hoặc đầu vào kiểu prompt cho LLM. Ví dụ, nối các thông điệp log gần nhất thành một chuỗi văn bản hoặc danh sách sự kiện (theo cuốn chiếu hoặc phiên). Cũng có thể sử dụng nhúng từ vựng (word embeddings) hoặc mã nhị phân nếu là các mô hình bên trong, nhưng baseline LLM thường dùng văn bản thô.  
- **Mô hình lõi (Baseline Core Model):** Một mô hình ngôn ngữ lớn (ví dụ GPT-4, Llama-3) hoạt động ở chế độ inference **không huấn luyện thêm**. Model nhận vào đoạn văn bản log đã mã hóa trong prompt và xuất ra dự đoán về trạng thái bất thường của log. Đây là phương pháp dựa trên prompt engineering hoặc fine-tuning rất nhẹ (nếu có). Ví dụ, mô hình có thể được huấn luyện để trả lời “Normal” hoặc “Anomaly” cho mỗi log nhập vào. Baseline thường dựa hoàn toàn vào kiến thức đã tích lũy trong tham số của LLM và các log đầu vào hiện tại.  
- **Phát hiện bất thường (Detection):** Mô hình LLM sẽ đưa ra xác suất hoặc nhãn phân loại cho bản ghi log (bình thường/bất thường). Từ xác suất này, ta có thể tính **anomaly score** và so sánh với ngưỡng để quyết định có gắn cờ cảnh báo hay không. Ví dụ, xác suất “anomalous” vượt ngưỡng 0.5 thì báo bất thường. Đầu ra là nhãn hoặc cảnh báo thời gian (có hoặc không).  
- **Đầu ra (Output):** Hệ thống báo cáo bản ghi log (hoặc phiên log) nào được đánh dấu bất thường. Trong Baseline hiện tại, chúng ta chủ yếu quan tâm đến việc phát hiện sau khi log xuất hiện, chưa xét kỹ vấn đề cảnh báo **sớm trước** sự cố.  

Nói chung, baseline giữ lại quy trình xử lý log truyền thống nhưng áp dụng LLM làm mô hình chính. Mô hình này **không sử dụng thông tin lịch sử hoặc ngữ cảnh ngoài** phạm vi cửa sổ log hiện tại, do đó gặp hạn chế về khả năng dự đoán sớm và bối cảnh toàn cục. Pipeline Baseline tóm tắt là:  
```
System Logs → Parse (Template extraction) → Windowing (session/fixed) → Text Representation → LLM (inference) → Classifier (Threshold) → Anomaly Labels.
```  

# 3. Xác định Cải tiến mục tiêu  

| **Thành phần**         | **Baseline**                                 | **Giới hạn (Limitation)**                                              | **Cải tiến**                                     | **Tác động kỳ vọng**                                        | **Bằng chứng (Evidence)**                                   |
|-----------------------|----------------------------------------------|------------------------------------------------------------------------|--------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------|
| **Tri thức/Nhớ ngữ cảnh (Knowledge/Context)** | Không có cơ chế truy xuất; chỉ dựa vào log hiện tại. | Mô hình thiếu tri thức lịch sử và không mở rộng được ngữ cảnh vượt quá cửa sổ hiện tại. Khó nhận biết mẫu lỗi đa giai đoạn hoặc xu hướng bất thường dài hạn. | **RAG/Mem Augmentation:** tích hợp cơ sở dữ liệu lịch sử chứa log mẫu và kiến thức miền (ví dụ runbook, sự cố cũ). Sử dụng truy vấn (retrieval) để lấy các log/học phần phù hợp dựa trên log hiện tại và gắn chúng vào prompt. | *Cải thiện độ chính xác phát hiện (F1 cao hơn), tăng Recall, đặc biệt thông qua việc bổ sung ngữ cảnh. Cho phép phát hiện sớm hơn khi log mới có dấu hiệu bất thường (lead-time tăng).* | Nghiên cứu DM-RAG cho thấy RAG/memory tăng recall đáng kể trong phát hiện log. EnrichLog chứng minh LLM tích hợp kiến thức lịch sử cho độ chính xác tốt hơn. |

- **Thành phần Baseline:** Mô hình LLM/Prompt hiện tại không sử dụng **lịch sử log** hoặc **kiến thức miền** ngoài chuỗi log được đưa vào prompt.  
- **Giới hạn xác nhận:** Theo các nghiên cứu gần đây, LLM thiếu kiến thức cập nhật và ngữ cảnh riêng của miền sẽ giảm hiệu suất phát hiện lỗi log. Phát hiện sớm yêu cầu phát hiện các dấu hiệu bất thường ban đầu, điều mà chỉ dựa vào lịch sử ngắn hạn thường bỏ sót.  
- **Cải tiến mục tiêu:** Thêm một cơ chế **Retrieval-Augmented Generation (RAG)** hoặc **bộ nhớ ngoài (memory)**. Cụ thể, xây dựng cơ sở tri thức (knowledge base) bao gồm mẫu log lịch sử (bình thường và bất thường) hoặc tài liệu chạy (runbook) liên quan. Tại bước inference, thực hiện truy vấn (dựa trên nhúng hoặc từ khóa) để tìm log/gợi ý tương tự, rồi kết hợp nội dung này vào prompt cho LLM.  
- **Cơ chế:** Lưu trữ vector hoặc văn bản của các log/tài liệu lịch sử. Khi một log mới xuất hiện, vector hóa nó và truy vấn để lấy top-K mục liên quan từ KB. Thêm nội dung đã truy xuất vào input của LLM. Điều này cung cấp ngữ cảnh rộng hơn và thông tin trước đây mà LLM không thể lưu trong tham số mặc định.  
- **Tác động kỳ vọng:** Việc tích hợp kiến thức bổ sung kỳ vọng sẽ cải thiện độ nhạy (Recall) và độ chính xác tổng thể của mô hình, đặc biệt với các trường hợp bất thường phức tạp. Ngoài ra, bổ sung dấu hiệu lịch sử có thể giúp phát hiện **sớm hơn** trước khi bất thường xảy ra (giảm thời gian phát hiện), do mô hình sẽ thấy các ví dụ tương tự sớm hơn.  
- **Bằng chứng:** Kết quả của DM-RAG (một khung tích hợp bộ nhớ ngắn hạn/dài hạn) cho thấy recall tăng mạnh so với các baseline khác. EnrichLog (framework RAG) cũng cho thấy bổ sung kiến thức lịch sử giúp LLM phát hiện chính xác hơn, đạt F1 cao hơn so với chỉ dùng prompt thuần túy.  

# 4. Kiến trúc nghiên cứu tổng thể  

Thiết kế kiến trúc kết hợp Baseline và Cải tiến (RAG): Các thành phần chính gồm:

- **Dữ liệu (Data)** – *Inherited:* Sử dụng cùng bộ dữ liệu log gốc đã chọn (ví dụ BGL/HDFS).  
- **Tiền xử lý (Preprocessing)** – *Inherited:* Sử dụng parser như Drain để trích xuất template và tham số từ log (giống Baseline). Không thay đổi.  
- **Mã biểu diễn (Representation)** – *Inherited:* Chuyển log (hoặc cửa sổ log) thành văn bản cho LLM. Định dạng như prompt (ví dụ liệt kê series log) như Baseline.  
- **Mô hình cơ sở (Baseline Model)** – *Inherited:* LLM lõi (ví dụ GPT-4/Gemini hoặc Llama-3) chạy ở chế độ inference, giống Baseline. Không thay đổi kiến trúc model chính.  
- **Cơ sở tri thức (Knowledge Base)** – *Mới:* Tập hợp các log lịch sử đã được lựa chọn hoặc tài liệu runbook được mã hóa. Đây là thành phần bổ sung không có trong Baseline.  
- **Retrieval (Truy xuất kiến thức)** – *Mới:* Mô-đun truy vấn KB. Nhận đầu vào là log/tokens hiện tại, trả về top-K log hoặc đoạn văn bản liên quan. Được tích hợp vào pipeline giữa Representation và Detection.  
- **Context Assembly (Tổng hợp ngữ cảnh)** – *Modified:* Cấu thành ngữ cảnh cho prompt của LLM: kết hợp log hiện tại với nội dung đã truy xuất (ví dụ log lịch sử mẫu hoặc lời giải thích) để tạo prompt đầy đủ hơn. Đây là điểm chỉnh sửa so với Baseline.  
- **Mô hình nền tảng (Foundation Model)** – *Inherited:* LLM lựa chọn (có thể là open LLM như Llama hoặc GPT phiên bản được kiểm soát). Xử lý prompt và sinh đầu ra anomaly/no-anomaly.  
- **Early Detection Mechanism** – *Optional:* Cơ chế xác định sớm (gọi là *Early Warning*). Bản thân mô hình không thay đổi (vẫn đưa ra nhãn anomaly), nhưng hệ thống đánh giá thời gian phát hiện so với ngưỡng cảnh báo muộn.  
- **Inference/Detection** – *Inherited:* LLM phân tích prompt cuối cùng (log + context) và đưa ra xác suất (score) hoặc nhãn. Chức năng phân loại và threshold giữ nguyên từ baseline.  
- **Cảnh báo/ Giải thích (Alert/Explanation)** – *Optional:* Nếu cần, có thể sinh ra giải thích (ví dụ LLM trả lời lý do). Đây là tùy chọn nâng cao không bắt buộc cho mục tiêu chính.

Tóm lại, phần lớn pipeline của Baseline được **thừa kế nguyên vẹn**, chỉ bổ sung thêm thành phần **Retrieval + Knowledge Base** để cải thiện ngữ cảnh cho LLM. Các thành phần mới/được sửa đổi tập trung ở khâu truy xuất và tổng hợp ngữ cảnh, trong khi Mô hình LLM và các bước khác giữ lại **độ trung thành cao với baseline** gốc.  

# 5. Dữ liệu và Pipeline thời gian  

Pipeline dữ liệu chi tiết:

1. **Raw Logs:** Gồm chuỗi bản ghi log gốc của hệ thống, mỗi bản ghi có định danh thời gian (timestamp). *Đầu vào:* Log chưa xử lý. *Đầu ra:* Cùng log với timestamp. *Liên hệ Baseline:* Giống hệt.  

2. **Parsing:** Áp dụng thuật toán parse (ví dụ Drain) để phân tách mỗi log thành `template + các param`. *Đầu vào:* Raw log. *Đầu ra:* Mảng template ID và các giá trị. *Mục đích:* Chuẩn hóa và giảm kích thước đầu vào cho LLM. *Baseline:* Sử dụng bước parse tương tự.  

3. **Windowing (Observation Window):** Gom nhóm các log liên quan theo một phiên hoặc cửa sổ thời gian cố định. *Đầu vào:* Dãy log đã parse. *Đầu ra:* Các cửa sổ log (mỗi cửa sổ chứa n log gần nhất hoặc log trong khoảng thời gian T). *Mục đích:* Tạo context để phát hiện chuỗi sự kiện. *Baseline:* Có thể sử dụng session window (theo ID) hoặc sliding window thông thường. Giữ nguyên như baseline để so sánh.  

4. **Representation:** Mỗi cửa sổ log được chuyển thành một prompt (văn bản) hoặc embedding. Ví dụ, nối các thông điệp dưới dạng văn bản: “Log1: …; Log2: …;” làm input cho LLM. *Đầu vào:* Chuỗi log trong cửa sổ. *Đầu ra:* Đầu vào dạng văn bản/embedding cho LLM. *Baseline:* Tương tự, chỉ sử dụng nội dung log và template hiện tại.  

5. **[Cải tiến] Retrieval Context:** **(Thêm bước)** Sử dụng prompt hoặc embedding của log hiện tại làm truy vấn đến cơ sở tri thức. *Đầu vào:* Template hoặc embedding của log hiện tại/cửa sổ hiện tại. *Đầu ra:* Tập hợp `K` mục log/tri thức tương tự nhất (ví dụ các đoạn log lịch sử hoặc giải thích) được đưa vào prompt. *Mục đích:* Bổ sung thông tin liên quan (ngữ cảnh lịch sử) cho mô hình. *Liên hệ Baseline:* Baseline không có bước này; đây là cải tiến.  

6. **Detection (Inference):** Ghép Prompt bao gồm “log gốc + nội dung đã truy xuất” và đưa vào LLM. LLM trả về xác suất hoặc nhãn anomaly. *Đầu vào:* Prompt hoàn chỉnh (gồm cải tiến nếu có). *Đầu ra:* Score/nhãn bất thường. *Mục đích:* Phát hiện bất thường. *Baseline:* Cũng thực hiện bước này nhưng không có thông tin bổ sung.  

7. **Early Detection Evaluation:** Tính toán **thời gian phát hiện** so với thời gian lỗi thực. *Đầu vào:* Thời gian bản ghi được đánh dấu anomaly và thời gian thực của lỗi (nếu có). *Đầu ra:* Giá trị lead time (thời gian cảnh báo trước lỗi) hoặc các chỉ số liên quan. *Mục đích:* Đo lường khả năng cảnh báo sớm. *Baseline:* Đo lường tương tự nhưng baseline thường có lead time ngắn hơn.  

8. **Alert:** Nếu score > threshold, kích hoạt cảnh báo. *Đầu vào:* Score anomaly, ngưỡng định trước. *Đầu ra:* Cảnh báo cho hệ thống vận hành/ người dùng. *Mục đích:* Cảnh báo sớm sự cố. *Liên hệ Baseline:* Giống, chỉ nguồn score khác.  

**Kiểm soát quá trình thời gian:** Trong Retrieval, chỉ sử dụng tri thức từ logs có timestamp **≤ thời điểm hiện tại** để tránh rò rỉ thông tin tương lai. Cơ sở tri thức xây trên log lịch sử (training set), đảm bảo không chứa sự cố tương lai. Nếu dùng dữ liệu về sự cố cũ (incidents/runbooks), chỉ sử dụng thông tin đã biết trước thời điểm test.  

# 6. Thiết kế Kiến thức / Truy xuất  

Chỉ áp dụng nếu cải tiến yêu cầu (ở đây chúng ta dùng RAG).

- **Nguồn kiến thức (Historical Knowledge):** Tập hợp các log mẫu (bình thường và bất thường) từ dữ liệu huấn luyện. Có thể bao gồm log lịch sử hoặc đoạn văn mô tả sự cố (runbooks). Ví dụ, lưu trữ các log trước đó kèm nhãn, hoặc tài liệu hướng dẫn xử lý lỗi.  
- **Cơ sở tri thức (Knowledge Base):** Lưu vector embedding hoặc văn bản của mỗi mục log tài liệu. Ví dụ, dùng FAISS để lưu nhúng log lịch sử. Đảm bảo cơ sở này chỉ chứa dữ liệu trước thời điểm dự đoán để tránh thông tin tương lai.  
- **Truy vấn (Query):** Khi một log mới đến, sử dụng template hoặc nội dung của nó để truy vấn KB. Có thể kết hợp embedding (dựa trên LLM hoặc encoder) hoặc từ khóa.  
- **Lọc/Ranking:** Tính toán mức độ liên quan giữa log hiện tại và từng mục trong KB (cosine similarity, BM25). Lấy top-K mục liên quan nhất. Có thể thêm điều kiện lọc thời gian (chỉ xem log cũ hơn một khoảng tối đa, nếu cần).  
- **Kích thước ngữ cảnh:** Giới hạn số văn bản được đưa vào prompt (ví dụ K=5–10). Đồng thời tránh vượt qua giới hạn token của LLM. Nếu nội dung quá dài, chỉ giữ những phần trọng tâm (ví dụ tóm tắt).  
- **Bối cảnh mẫu (Sample-specific Context):** Từ [17], có thể tạo thêm “giải thích mẫu” cho mỗi log trong KB (ví dụ: tại sao log này bất thường). Tuy nhiên, để giữ đơn giản, chúng ta chủ yếu chỉ lấy nội dung log chuẩn và nhãn.  
- **Vị trí trong pipeline:** Bước RAG đặt sau khi đã mã hóa log hiện tại nhưng trước khi đưa vào LLM. Dữ liệu được truy xuất sau khi nhóm cửa sổ hoặc phân tích template.  

**Điểm cải tiến so với Baseline:** Baseline chỉ dùng log hiện tại, trong khi RAG cho phép mô hình xem thêm các ví dụ lịch sử liên quan ngay tại thời điểm dự đoán. Như EnrichLog đã chứng minh, truy vấn mô hình với các log lịch sử liên quan giúp cải thiện khả năng phân biệt bất thường.  

# 7. Thiết kế Mô hình nền tảng / Học máy  

- **Mô hình nền tảng (LLM):** Sử dụng LLM mở (ví dụ Llama-3.1-8B hoặc mô hình tương đương) với trọng số cố định. Bản chất là mô hình decoder (GPT-like) vì nó hỗ trợ tốt cho generation và RAG. Phiên bản cụ thể (ví dụ Llama-3-8B) được cố định để tránh drift.  
- **Vai trò mô hình:** Là bộ sinh nhãn (classifier) dựa trên ngữ cảnh đầu vào. Không huấn luyện lại (không fine-tune PEFT); chỉ dùng prompt và retrieval để đưa ngữ cảnh chuyên dụng.  
- **Prompt/Context:** Prompt bao gồm các ví dụ (nếu in-context) hoặc câu hỏi trực tiếp dạng: “Cho log X và các log tham khảo [Z1, Z2,…], hãy đánh giá xem X có bất thường không?”. Không dùng fine-tuning, chỉ thiết kế prompt tốt. Prompt có thể ít-trực/zero-shot cùng ví dụ.  
- **Học (Learning):** Không có thành phần học mới (loại bỏ fine-tuning nếu có thể). Nếu dùng fine-tuning nhỏ (PEFT/LORA) cho baseline, thì cải tiến chủ yếu là retrieval, không đòi hỏi huấn luyện thêm. Hạn chế phức tạp và chi phí. Tập trung vào khai thác tri thức trong mô hình có sẵn.  
- **Kiểm soát:** Chọn nhiệt độ (temperature) và top-k sampling thấp (ví dụ 0-1) để giảm biến thiên đầu ra. Cố định seed để tái lập. Trường hợp dùng GPT-4/API, fix model và version.  

**Có nên fine-tune?** Vì hướng tối giản, đề xuất **không** fine-tune LLM với dữ liệu log. Thay vào đó, dựa vào prompt được bổ sung bối cảnh (từ RAG) để cải thiện hiệu suất. Như [26] chỉ sử dụng LLM cố định và RAGLog trong các baseline so sánh.  

# 8. Chiến lược suy luận (Inference)  

**Dòng chảy khi chạy online:**  

1. **Nhận log mới:** Một bản ghi log (hoặc nhóm nhỏ log) vừa sinh ra với timestamp t.  
2. **Biến đổi đầu vào:** Áp dụng parser → thu template. Tạo prompt tạm thời từ log này.  
3. **Truy vấn KB (nếu cải tiến):** Lấy template/embedding log làm truy vấn, nhận về top-K bản ghi lịch sử hoặc tri thức.  
4. **Xây dựng prompt đầy đủ:** Kết hợp log hiện tại với các mục truy xuất để tạo prompt hoàn chỉnh. Có thể theo cấu trúc: “Log gần đây: [Log hiện tại]; Các ví dụ lịch sử liên quan: [Log lịch sử…]. Hỏi: Log gần đây có bất thường không?”  
5. **Inference LLM:** Đưa prompt vào LLM, sinh ra xác suất hoặc nhãn “anomaly/normal”. Tính **anomaly score** dựa trên xác suất token (ví dụ P(“anomaly”)).  
6. **Quyết định:** So sánh với ngưỡng để quyết định. Nếu > threshold (ví dụ 0.5), gắn cờ cảnh báo. Tính **thời gian phát hiện** (t_det = thời điểm log, so sánh với t_fail nếu biết trước hậu quả).  
7. **Cảnh báo:** Nếu là anomaly, phát cảnh báo (hoặc gọi hàm Agentic để kích hoạt hành động tự động).  

**Phân loại xử lý:** Tối ưu để chạy **online**: mỗi log mới vào được xử lý ngay. Các bước slow nhất có thể là truy vấn KB (sử dụng chỉ mục đã lưu) và gọi LLM. Nếu cần, có thể tính toán (retrieve) một phần offline (ví dụ pre-compute embedding cơ sở). LLM inference có độ trễ do mạng nơ-ron.  

**Giữ nguyên với Baseline:** Baseline tương tự (nhưng không có bước 3, prompt ngắn hơn). Mọi thứ khác (threshold, nhãn output) giữ như baseline để so sánh thuần nhất.  

# 9. Thiết kế thí nghiệm  

- **E1 – Phục hồi Baseline (Baseline Reproduction):** Thực thi lại pipeline baseline (LLM không có RAG) trên dữ liệu chuẩn. Báo cáo các chỉ số cơ bản (Precision, Recall, F1). So sánh với kết quả đã công bố của baseline (nếu có) để đảm bảo thiết lập đúng. Ghi lại sai số (nếu khác biệt).  
- **E2 – So sánh chính (Baseline vs Baseline+Improvement):** So sánh trực tiếp giữa phương pháp cơ sở nguyên gốc và phương pháp có thêm RAG. Giữ mọi tham số khác cố định (dataset, model LLM, cấu hình prompt) chỉ thêm bước retrieval. Đánh giá sự khác biệt về Precision, Recall, F1, và các chỉ số cảnh báo sớm. Đây là thử nghiệm chính để kiểm chứng giả thuyết.  
- **E3 – Ablation (Nếu cần):** Loại bỏ hoặc giảm các thành phần của cải tiến: ví dụ, chỉ sử dụng một phần KB (chỉ log bình thường hoặc chỉ log bất thường), hoặc giới hạn K retrieval nhỏ. So sánh từng biến thể để cô lập ảnh hưởng của việc thêm context. Mục tiêu xác định thành phần nào mang lại hiệu quả.  
- **E4 – Đánh giá phát hiện sớm (Early Detection):** Đo lường thời gian phát hiện: tính lead time (thời gian từ cảnh báo đến sự kiện lỗi thực). Tính tỷ lệ cảnh báo sớm (Percentage of cases detected trước khi lỗi xảy ra), false alarm rate. So sánh xem cải tiến có cho phép cảnh báo sớm hơn đáng kể không.  
- **E5 – Độ bền (Robustness):** Thử nghiệm thêm nhiễu hoặc thay đổi ngoài ý muốn: ví dụ, thêm sự kiện “out-of-vocabulary” trong log, thay đổi định dạng log, hay giảm độ chính xác của bộ parse. Đánh giá xem cải tiến với RAG có bền hơn baseline không. Có thể thử các biến thể về ngữ cảnh lạ (log từ dịch vụ mới).  
- **E6 – Đánh giá hiệu quả (Efficiency):** So sánh chi phí tính toán giữa baseline và cải tiến (thời gian inference trung bình, số token xử lý, memory). Đặc biệt, đo độ trễ do bước truy xuất và prompt dài hơn. Báo cáo độ trễ trung bình mỗi bản ghi và throughput (bản ghi/giây).  
- **E7 – Tổng quát hóa (Generalization):** Kiểm tra trên bộ dữ liệu khác hoặc hệ thống log khác: ví dụ huấn luyện/truy vấn trên bộ log A, thử nghiệm trên bộ log B (chỉ cùng tên bộ câu lệnh). Đánh giá model có giữ được lợi ích trên domain mới không.  

Mỗi thử nghiệm phải được thực hiện nhiều lần (nhiều seed) để tính độ lệch. Kết quả chính có thể trình bày dưới dạng biểu đồ hoặc bảng.  

# 10. Chỉ số đánh giá (Metrics)  

- **Phát hiện (Detection):** Precision, Recall, F1-score (mức chung), PR-AUC, ROC-AUC (nếu có). Đo mức độ chính xác và đầy đủ của việc phân loại bất thường.  
- **Phát hiện sớm (Early Detection):** *Thời gian phát hiện (Time-to-Detection):* khoảng cách trung bình từ lần cảnh báo đầu tiên đến thời điểm lỗi (mục tiêu là càng lớn càng tốt). *Lead Time:* thời gian cảnh báo trước lỗi thực (càng dương càng tốt). *Tỉ lệ cảnh báo trước (Early Warning Rate):* phần trăm trường hợp được cảnh báo trước khi lỗi xảy ra. *False Alarm Rate trước lỗi:* Tỉ lệ cảnh báo sai.  
- **Hiệu quả (Efficiency):** Độ trễ inference (milli-giây/bản ghi), số token sử dụng trên mỗi prompt, throughput (bản ghi/s), và tài nguyên (CPU/GPU) nếu so sánh.  
- **Đánh giá thành phần (Component-specific):** Ví dụ, độ chính xác của truy vấn (Precision/Recall của retriever: phần trăm thông tin liên quan trong top-K), hoặc độ hữu dụng của ngữ cảnh thu được (có thể đo bằng tăng điểm so với không dùng nó). Nếu có Memory, đánh retrieval accuracy. Nếu có Reasoning, đánh chất lượng giải thích (consistency).  

Các chỉ số được lấy chuẩn theo tiêu chuẩn trước đây, bổ sung các thước đo về thời gian phát hiện và chi phí xử lý.  

# 11. Thiết kế thống kê  

- Thực hiện **nhiều lần chạy lặp (n ≥ 5)** với các random seed khác nhau để tính toán độ lệch chuẩn của các chỉ số.  
- Báo cáo **confidence intervals** (Ví dụ 95%) cho các metric chính (F1, lead time).  
- Sử dụng **kiểm định thống kê** (t-test hoặc Mann-Whitney) để xác định độ khác biệt có ý nghĩa giữa baseline và cải tiến. Ghi rõ effect size nếu cần.  
- Với LLM API (nếu dùng ChatGPT/GPT-4), cố định model version. Điều chỉnh sampling (đặt temperature thấp, top-k/top-p) để đảm bảo tính ổn định. Lưu prompt và config ngẫu nhiên (seed) để tái lặp. Không chỉ báo cáo kết quả tốt nhất mà báo cáo trung bình ± độ lệch.  

# 12. Kiểm soát biến (Controlled Variables)  

Để đảm bảo so sánh công bằng, giữ cố định tối đa các yếu tố ngoài cải tiến chính:  

| **Yếu tố**         | **Baseline**                | **Cải tiến**                             | **Kiểm soát?** |
|--------------------|-----------------------------|------------------------------------------|--------------|
| Dữ liệu (Dataset)  | Giống nhau                  | Giống nhau                               | Có (giữ nguyên) |
| Phân chia dữ liệu  | Cùng train/val/test split   | Cùng                                    | Có |
| Tiền xử lý         | Cùng (parser, đồng nhất)    | Cùng                                    | Có |
| Mã biểu diễn       | Cùng                        | Cùng                                    | Có |
| Mô hình LLM        | Cùng (phiên bản)            | Cùng                                    | Có |
| Prompt/in-context  | So sánh: baseline vs thêm context | So sánh                                | Chỉ khác retrieval |
| Thuật toán retrieval | Không có                  | Mới (thêm vào)                           | Có (chỉ phần này khác) |
| Phép tính (compute) | Tương tự (cấu hình giống)   | Thêm overhead cho retrieval             | Theo dõi (khác) |
| Đánh giá (protocol)| Giống                        | Giống                                    | Có |
| HW/SW (Phần cứng)  | Giống                        | Giống                                    | Có |

Mục tiêu: ngoài việc thêm bước truy xuất (retrieval), các thành phần khác giữ yên. Nhờ đó, mọi khác biệt hiệu suất có thể quy cho cải tiến.  

# 13. Logic quy hệ (Attribution)  

Để xác định liệu cải tiến có thực sự gây ra lợi ích:  

- So sánh **Baseline vs Baseline+Improvement:** Nếu mô hình cải tiến cho kết quả tốt hơn (cao F1, lead time dài hơn) trong cùng điều kiện, có thể quy sự cải thiện cho step retrieval.  
- Nếu có nhiều khối cải tiến, thực hiện thêm các kiểm thử **Baseline + chỉ một phần cải tiến** (ví dụ sử dụng log lịch sử mà không thêm giải thích, hoặc ngược lại). So sánh từng cấu hình để tách biệt đóng góp của mỗi phần.  
- Ví dụ, đo xem chỉ thêm context corpus-level (summary) so với thêm context sample-level. Nếu cả hai cùng tăng hiệu quả, chắc chắn cải thiện của chúng gây ảnh hưởng.  
- Nhận định cuối cùng dựa trên việc biến thiên duy nhất: mọi thứ khác cố định, chỉ khác retrieval. Theo định luật kiểm soát biến, sự khác biệt là do cải tiến.  

# 14. Các phương án thiết kế thay thế  

Xét 3 biến thể chính của cùng hướng cải tiến (RAG):  

- **A – Minimal (Cơ bản):** Chỉ thêm mô-đun truy xuất log lịch sử. Với mỗi log mới, lấy top-K log trước đó tương đồng từ KB rồi chèn vào prompt. Phương án đơn giản nhất để bổ sung ngữ cảnh.  
- **B – Refined (Tinh chỉnh):** Ngoài log lịch sử, thêm truy vấn tri thức chuyên ngành (ví dụ tóm tắt runbook của lỗi tương tự). Có thể dùng RAG kết hợp nhiều nguồn (log và doc). Kết hợp thông tin mẫu và giải thích.  
- **C – Robust (Tăng cường):** Bao gồm B cộng với cơ chế bộ nhớ thích ứng (giống DM-RAG): vừa có KB truy vấn, vừa cập nhật “bộ nhớ ngắn hạn” (tổng hợp log mới liên tục) và “bộ nhớ dài hạn” (cho học các mẫu xuyên thời gian) như [6].  

**Lựa chọn:** Chọn phương án **A – Minimal**. Mục tiêu là kiểm chứng giả thuyết rằng *việc thêm bất kỳ ngữ cảnh lịch sử nào cũng cải thiện hiệu suất*. A đủ để đo hiệu quả retrieval cơ bản; nếu đạt kết quả, có thể mở rộng sau này. B và C phức tạp hơn, khó kiểm soát, vượt phạm vi cần thiết.  

# 15. Lựa chọn thiết kế cuối cùng  

| **Design Choice**  | **Selected Option**                            | **Lý do**                                                                                 |
|--------------------|-------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Baseline**       | LLM prompt-based (inference only)               | Giữ nguyên kiến trúc LLM thuần như đề xuất đã phê duyệt; thể hiện tương lai gần.           |
| **Main Improvement** | Retrieval-Augmented Generation (RAG)           | Tập trung vào hạn chế xác định (thiếu ngữ cảnh); cải thiện đơn giản và kiểm soát tốt.        |
| **Dữ liệu (Data)** | Bộ dữ liệu log hệ thống chuẩn (e.g. BGL)        | Thực tế, được sử dụng rộng và có nhãn; phù hợp benchmark.                     |
| **Học (Learning)** | Inference-only (không fine-tune)               | Giảm độ phức tạp, tập trung vào cải tiến RAG; baseline cũng làm thế.                         |
| **Suy luận (Inference)** | Online LLM + RAG                          | Phù hợp yêu cầu thực tế; đảm bảo so sánh công bằng với baseline (chỉ thêm retrieval).        |
| **Đánh giá (Evaluation)** | Detection + Early metrics                 | Cả hai tập trung: phát hiện bất thường thông thường (P/R/F1) và khả năng cảnh báo sớm.        |

Chọn **thiết kế tối giản (A)** vì nó đảm bảo kiểm tra giả thuyết chính với ít biến số thừa, dễ tái lập và tập trung. Các biến thể phức tạp hơn (B,C) chỉ dùng nếu A thất bại hoặc cần mở rộng sau này.   

# 16. Ma trận truy xuất nghiên cứu (Traceability Matrix)  

| **Research Element** | **Thiết kế (Design Element)**              | **Thí nghiệm** | **Metric**              | **Bằng chứng thành công**                   |
|----------------------|-------------------------------------------|---------------|-------------------------|--------------------------------------------|
| **RQ1**              | Cải thiện F1 bằng RAG                    | E2 (So sánh chính) | F1, Precision, Recall   | F1 tăng đáng kể so với baseline (p<0.05)   |
| **RQ2**              | Cải thiện thời gian phát hiện             | E4 (Early detection) | Lead Time, Early Warning Rate | Lead time trung bình tăng, cảnh báo trước nhiều hơn |
| **RQ3**              | Tổng quát hóa跨dữ liệu                    | E7 (Generalization) | F1 (bộ khác)           | F1 cao hơn baseline trên dataset thứ 2    |
| **H1**               | RAG giúp tăng F1                         | E2          | F1, Precision/Recall    | F1 tăng > Δ ngưỡng đáng kể                |
| **H2**               | RAG cải thiện phát hiện sớm              | E4          | Lead Time, Early Rate    | Lead time tăng, sai báo không tăng nhiều  |
| **H3**               | RAG không làm suy giảm hiệu suất cơ sở khác | E2/E6       | Latency, Overhead        | Tăng F1 mà độ trễ chấp nhận được           |

Mỗi RQ/Hypothesis có thí nghiệm tương ứng để kiểm chứng (ví dụ RQ1/E2, RQ2/E4). “Bằng chứng thành công” ghi đầu ra mong đợi để chứng minh giả thuyết (về giá trị số với kiểm định).  

# 17. Các mối đe dọa đến tính hợp lệ  

- **Nội tại (Internal):** Mô hình cải tiến có thể không triển khai chính xác step RAG; rò rỉ thông tin (token leakage) nếu prompt lồng thông tin chuẩn đoán trước; độ hỗn loạn tùy thuộc seed LLM. Kiểm soát: code kiểm thử cẩn thận, giữ seed cố định, dùng prompt versioned.  
- **Bên ngoài (External):** Dữ liệu benchmark có thể không đại diện (ví dụ BGL/HDFS khác nhau môi trường). Kết quả có thể lệ thuộc cấu hình cụ thể (logger, bộ parse). Giới hạn: chỉ sử dụng public dataset đã nghiên cứu; thử nghiệm nhiều domain.  
- **Khái niệm (Construct):** Các metric (ví dụ precision/recall) có thể không phản ánh đúng khả năng cảnh báo sớm. Mẫu log có nhãn lỗi có thể không chính xác xác định thời điểm lỗi thực. Giải pháp: sử dụng thước đo thời gian, lead time, false alarm rõ ràng.  
- **Kết luận (Conclusion):** Số lần chạy giới hạn (dưới 10) có thể dẫn đến low power; mô hình LLM có thể ghi đè kết quả khi seed khác. Thiết kế thêm confidence interval và test thống kê.  
- **Phiên bản LLM/API:** LLM thương mại có thể thay đổi (drift). Cố định model (open-source) để tránh drift.  
- **Retrieval Bias:** KB có thể chưa đủ hoặc lỗi, truy xuất sai mục không liên quan. Giới hạn KB/horizon thời gian.  

# 18. Rủi ro và Giảm thiểu  

| **Risk (Nguy cơ)**                           | **Khả năng** | **Tác động** | **Giảm thiểu**                                              | **Kế hoạch dự phòng**                          |
|----------------------------------------------|------------:|------------:|------------------------------------------------------------|-----------------------------------------------|
| Baseline không tái lập (khác công bố)         | Trung bình  | Trung bình  | Kiểm tra kỹ pipeline, dùng code nguồn (nếu có), tham khảo tài liệu | Nếu không, giảm độ phức tạp baseline (ví dụ dùng LSTM đơn giản) |
| Cải tiến không mang lại lợi ích rõ rệt        | Trung bình  | Trung bình  | Kiểm thử từng phần (ablation); tăng K; tinh chỉnh prompt    | Lùi về phương án đơn giản hơn (A) hoặc kết hợp thuộc tính khác |
| Hiệu quả chỉ trên 1 bộ dữ liệu               | Cao         | Thấp       | Mở rộng thử nghiệm đa dataset (BGL, HDFS, v.v)              | Giới hạn kết luận: nêu rõ phạm vi áp dụng     |
| Tính toán quá nặng (latency lớn)             | Trung bình  | Cao        | Giảm kích thước LLM, hạn chế K retrieval                    | Giảm yêu cầu thời gian, nghiên cứu mô hình nhẹ hơn (distill) |
| Mô hình/retrieval không ổn định (BIas/Noise)  | Thấp        | Trung bình | Tinh chỉnh tham số retrieval (kết hợp threshold)           | Bỏ retrieval hoặc giảm K nếu không có hiệu quả  |
| Thiếu dữ liệu/nhãn sự cố                     | Trung bình  | Trung bình | Sử dụng augmentation (chèn log tổng hợp), dùng độ nhạy cao hơn | Chỉ đánh giá detection chung, không quá tập trung lead time |

**Các biện pháp:** Giảm thiểu chủ yếu là kiểm thử từ sớm, dự phòng kế hoạch đơn giản (ví dụ nếu retrieval không tốt có thể chuyển sang tìm cách mở rộng context window). Nếu thiếu compute, giới hạn quy mô mô hình. Nếu dữ liệu thiếu, tập trung vào sử dụng chất lượng có nhãn rõ.  

# 19. Đóng góp dự kiến  

- **Khoa học:** Cung cấp bằng chứng định lượng về cách cải tiến RAG đơn giản ảnh hưởng đến phát hiện bất thường trên log, đặc biệt về cảnh báo sớm. Chứng minh hạn chế của LLM thuần túy và giá trị của ngữ cảnh lịch sử.  
- **Phương pháp luận:** Mô tả chi tiết quy trình thiết kế thí nghiệm có kiểm soát (controlled experiment), tuân thủ nguyên tắc so sánh Baseline và Baseline+Improvement đồng bộ.  
- **Kỹ thuật:** Triển khai mô hình tái lập toàn bộ pipeline (baseline + retrieval), mã nguồn mở (nếu có thể), đảm bảo khả năng tái tạo.  
- **Công nghiệp:** (Nếu phù hợp) Ví dụ, chứng minh cải thiện phát hiện sớm có thể giảm thiểu downtime cho hệ thống. Nhưng phần này phụ thuộc vào kết quả; chủ yếu nhấn mạnh tính ứng dụng trong AIOps.  

# 20. Khả năng tái lập  

- **Mô hình Baseline:** Ghi rõ tên và phiên bản LLM (ví dụ Llama-3.1-8B-instruct).  
- **Dữ liệu:** Thông tin phiên bản dataset (BGL v1.1, hay HDFS Hadoop cluster logs). URL hoặc truy cập nguồn.  
- **Tiền xử lý:** Cấu hình bộ parser (Drain với ngưỡng s = 0.5, ví dụ).  
- **Prompt:** Ghi kỹ prompt template cho LLM, ví dụ câu hỏi chính xác dùng.  
- **Tham số ngẫu nhiên:** Seed ngẫu nhiên, cài đặt nhiệt độ (ví dụ T=0.0).  
- **Mô-đun Retrieval:** Cấu hình K (số bản ghi truy xuất), kiểu embedding và công cụ (ví dụ FAISS, cosine).  
- **Đánh giá:** Thước đo (Precision, Recall, F1, lead time), cách tính lead time (ngày, giờ).  
- **Môi trường:** Môi trường phần cứng (GPU loại nào), phần mềm (PyTorch 2.x, FAISS 1.x, OS). Cả hai baseline và cải tiến trên cùng máy để so sánh.  
- **Phần mềm:** Thư viện (transformers 4.x, indexing tools…), phiên bản cụ thể.  
- **Hành vi LLM:** Nếu dùng API (GPT), ghi rõ phiên bản model và thời điểm.  

Mục tiêu: Mọi thành phần từ data đến evaluation đều được ghi chép chi tiết, sao cho người khác có thể lặp lại thí nghiệm và thu kết quả tương tự.  

# 21. Checklist cuối cùng  

- [x] **Baseline 2025–2026 rõ ràng:** Thiết lập model LLM làm baseline (đã xác định).  
- [x] **Một giới hạn được xác nhận:** Thiếu bối cảnh/ngữ cảnh dài hạn.  
- [x] **Một cải tiến chính:** Thêm RAG (log retrieval).  
- [x] **Tái lập baseline:** Kế hoạch thử nghiệm bao gồm tái lập baseline hiện tại.  
- [x] **So sánh Baseline vs Cải tiến:** Thực hiện đối chiếu đồng bộ.  
- [x] **Thí nghiệm Ablation:** Đề xuất (loại bỏ phần RAG hoặc giảm K).  
- [x] **Metrics phát hiện sớm:** Định nghĩa lead time, tỉ lệ cảnh báo sớm.  
- [x] **Kiểm soát biến:** Giữ dataset, prompt, model cố định (chỉ thêm retrieval).  
- [x] **Thống kê:** Nhiều lần chạy, kiểm định.  
- [x] **Giảm thiểu rủi ro:** Đưa ra phương án  dự phòng.  
- [x] **Không topic mới:** Thiết kế dựa trên đề xuất đã có, không đổi RQ/Hypothesis.  
- [x] **Không thêm công nghệ ngẫu nhiên:** Chỉ dùng RAG dựa trên tri thức hiện có, không thêm công nghệ ngoài kế hoạch.  
- [x] **Khả thi 6–9 tháng:** Các thành phần chủ yếu (RAG, LLM inference) đều có sẵn mã nguồn và dữ liệu công cộng, triển khai với nguồn lực một nhóm nghiên cứu trong 6–9 tháng là khả thi.  

Trên đây là thiết kế nghiên cứu chi tiết, tuân thủ đúng hướng đi và đề xuất ban đầu, tập trung kiểm chứng khoa học công việc cải tiến phát hiện bất thường trên log. Các quyết định được cân nhắc để đảm bảo tính đơn giản, độ tin cậy và khả năng tái lập cao.  

