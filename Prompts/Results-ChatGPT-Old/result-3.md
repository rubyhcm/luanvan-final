# Tổng hợp thiếu hụt và cơ hội cải tiến

**1. Các khoảng trống (gaps) nghiên cứu đã xác định.** Các phân tích từ tài liệu chỉ ra một số hạn chế quan trọng của các phương pháp cơ bản (2025–2026) hiện có trong phát hiện bất thường log sớm:

- **Hạn chế gốc của phương pháp cơ bản (Baseline-specific).** Các phương pháp dựa trên mẫu (template-based), ví dụ như RAGLog hay LogRAG, chỉ thao tác trên chuỗi mẫu log đã tách, dẫn đến trường hợp “một mẫu có thể ứng với cả sự kiện bình thường và bất thường”. Kết quả là mất mát thông tin ngữ nghĩa và có thể gây nhầm lẫn (dương tính giả/âm tính giả) trong phát hiện. Tương tự, phương pháp LLM cơ bản (zero-shot) chỉ dựa vào kiến thức tiền huấn luyện nội bộ có xu hướng gán hầu hết các sự kiện là bất thường (đạt độ bao phủ recall rất cao nhưng sai nhiều trong precision). Hơn nữa, việc giới hạn độ dài ngữ cảnh (prompt) khiến các phương pháp dựa trên ví dụ (như LogPrompt) phải thêm nhiều tham chiếu lịch sử để cải thiện độ chính xác, làm tăng độ trễ và chi phí tính toán. Đồng thời, LLM tiền huấn luyện thường **thiếu tri thức chuyên ngành**, nghĩa là không “biết” nhiều về bối cảnh cụ thể của log (ví dụ lỗi hệ thống, mã số). Ngoài ra, giới hạn bộ nhớ ngữ cảnh của LLM là một vấn đề: LLM lớn vẫn không thể xử lý được lượng token quá lớn, gây nghẽn tài nguyên bộ nhớ. 

- **Hạn chế chung của nhóm phương pháp (Method-family).** Các phương pháp theo dõi phiên (session-based) không áp dụng được cho các trường hợp cần phát hiện trên từng sự kiện đơn lẻ, và ngược lại, phương pháp phân loại sự kiện riêng (entry-based) không tận dụng được ngữ cảnh đa-thời điểm (session) rộng hơn. Đa số đánh giá chỉ sử dụng các metric phân loại (Precision, Recall, F1) mà bỏ qua các tiêu chí về thời gian phát hiện sớm (lead time), làm giảm khả năng đánh giá mức độ cảnh báo **sớm** của phương pháp. 

- **Hạn chế liên quan dữ liệu/benchmark.** Hiện các benchmark log còn hạn chế về chỉ số đánh giá thời gian (như khoảng cách từ cảnh báo đến lỗi), và đôi khi thiếu đánh giá chéo trên tập dữ liệu mới. Ví dụ, phương pháp EnrichLog cho thấy hiệu suất rất cao trên một số dataset tiêu chuẩn, nhưng chưa rõ chất lượng tổng quát khi áp dụng vào hệ thống thực tế có log khác biệt.  

- **Hạn chế về đánh giá (Evaluation).** Mặc dù các công trình mới tập trung đạt F1 cao, rất ít nghiên cứu báo cáo kết quả cụ thể về thời gian dẫn cảnh báo (time-to-detect) hoặc khả năng dự đoán trước sự cố. Điều này tạo khoảng trống trong việc so sánh khả năng phát hiện thực sự sớm của các phương pháp. 

**Phân loại theo độ ưu tiên:** Các hạn chế cấp baseline được đánh giá ưu tiên cao (A), vì trực tiếp ảnh hưởng đến hiệu quả của phương pháp 2025–2026. Hạn chế cấp nhóm phương pháp chỉ xem xét khi nó có thể đóng góp cải tiến cụ thể cho baseline. Các hạn chế dataset/đánh giá chỉ xét khi ảnh hưởng rõ đến việc đánh giá phương pháp cơ bản. Hạn chế chung của ngành (chẳng hạn thiếu hệ thống AI sản xuất sẵn) ở mức rất rộng không nằm trong phạm vi đóng góp cụ thể cho phương pháp hiện có, nên không được ưu tiên. 

**Tóm lại,** các gap trọng yếu là: (i) phân tích log dựa trên mẫu làm mất ngữ cảnh (cần phân tích ngữ nghĩa sâu hơn); (ii) LLM không có tri thức chuyên ngành (cần bổ sung kiến thức); (iii) giới hạn bộ nhớ/độ dài ngữ cảnh (cần cơ chế lưu giữ/mở rộng ngữ cảnh); (iv) các phương pháp hiện nay chủ yếu tối ưu F1, thiếu mục tiêu thứ nguyên thời gian phát hiện sớm; (v) độ trễ khi prompt dài; v.v. Các thiếu hụt này đều có căn cứ từ kết luận chỉ ra trong tài liệu (ví dụ về nhầm lẫn mẫu log, hiện tượng LLM cơ bản luôn báo bất thường, và sự đánh đổi độ dài prompt – độ trễ).

## 2. Phân tích nguyên nhân gốc rễ theo baseline

| **Baseline 2025–2026**      | **Thành phần**        | **Hạn chế**                                               | **Nguyên nhân gốc rễ**                        | **Bằng chứng**                         | **Tác động**                                            |
|-----------------------------|----------------------|-----------------------------------------------------------|-----------------------------------------------|----------------------------------------|--------------------------------------------------------|
| **LLM không huấn luyện (Zero-shot)** | Mô hình (tri thức nội sinh) | Dịch cao recall nhưng precision rất thấp: gán hầu hết sự kiện là bất thường | Dựa quá mức vào kiến thức pre-trained, thiếu huấn luyện/điều chỉnh với dữ liệu bình thường | Báo cáo EnrichLog: “LLMs không có kiến thức ngoài luôn đạt recall cao nhưng precision rất thấp” | Nhiều cảnh báo giả (False Positive) → kém tin cậy cho cảnh báo sớm |
| **LogPrompt (LLM theo ngữ cảnh tĩnh)** | Prompt (ví dụ lịch sử) | Hiệu quả chỉ tăng khi bổ sung nhiều ví dụ, làm tăng độ trễ và tài nguyên | Giới hạn của bộ nhớ ngữ cảnh LLM; chọn ngẫu nhiên bộ mẫu (100 logs) trong prompt | “Cải thiện độ chính xác thường đòi hỏi prompt dài hơn, tăng độ trễ và công suất tính toán” | Độ trễ cao, không đảm bảo cung cấp ngữ cảnh đầy đủ; có thể bỏ sót manh mối quan trọng |
| **RAGLog / LogRAG (truy vấn theo mẫu)** | Quá trình truy vấn (retrieval) | Mất ngữ nghĩa của bản ghi gốc: “một mẫu ứng với cả bình thường & bất thường” | Dựa trên template log được trích xuất bởi parser; tách biệt mẫu thông báo và nội dung | Giới thiệu EnrichLog: “phương pháp template vẫn kế thừa hạn chế của pipeline theo mẫu. Tức là một mẫu có thể ứng với cả sự kiện bình thường và bất thường” | Có thể bỏ lỡ tín hiệu cảnh báo thực trong văn bản thô, dẫn đến nhầm lẫn và giảm F1 |
| **LLM + tri thức nâng cao (EnrichLog)** | Kết hợp kiến thức (knowledge) | Cần tài liệu/dữ liệu mô tả hệ thống (corpus-specific) và ví dụ lịch sử (sample-specific) cho mỗi ngữ cảnh; nếu thiếu, hiệu quả giảm | Dù giải quyết được mẫu, vẫn phụ thuộc vào chất lượng tài liệu và khả năng truy vấn kiến thức | Kết quả EnrichLog cho thấy nếu có ngữ cảnh phong phú (EnrichLog*) thì F1 ≫ baseline; nhưng thiếu nguồn thì chỉ marginal | Giải pháp mạnh nhưng phụ thuộc vào sẵn có tri thức. Nếu không đủ tri thức, hiệu suất có thể giảm (Ví dụ: corpus-only chỉ cải thiện ít) |
| **Session-based Methods (MidLog, PLELog…)** | Tập hợp log theo phiên | Không dùng được cho từng sự kiện riêng (phát hiện sớm), chỉ áp dụng khi có chuỗi dài | Thiết kế cho phát hiện trên các phiên log (session) nên không phù hợp với kịch bản xem xét từng entry đơn lẻ | Các công trình EnrichLog chú ý “MidLog, PLELog, LLMeLog yêu cầu chuỗi nhiều log để phát hiện, nên bỏ qua khi chỉ có entry đơn” | Không thể áp dụng trực tiếp cho phát hiện bất thường theo entry; bỏ lỡ thông tin nếu dùng cho phát hiện sớm |

Mỗi dòng nêu rõ ràng **baseline, hạn chế, nguyên nhân** và **bằng chứng** trích từ tài liệu. Ví dụ, việc **LLM không huấn luyện** luôn đánh dấu sự kiện bất thường mặc dù rất nhiều sự kiện bình thường là dấu hiệu của việc mô hình chỉ dựa vào nội dung trong tham số mà không được hiệu chỉnh phù hợp. Tương tự, phương pháp **dựa trên mẫu** (LogPrompt, RAGLog) làm mất thông tin văn bản gốc dẫn đến tình trạng một template đại diện cho hai trạng thái khác nhau. Đây là nguyên nhân gốc rễ (log parsing thô) cho hạn chế về precision/recall thấp. Các hạn chế và nguyên nhân liên quan đến kiến thức tri thức (EnrichLog) hay bộ nhớ (memory) cũng được xác định tương ứng.

## 3. Định nghĩa cơ hội cải thiện

Dựa trên phân tích trên, ta đề xuất các cơ hội cải thiện được định dạng như sau:

- **Cải thiện mô hình LLM cơ bản bằng cách điều chỉnh ngưỡng/phân loại** – Xử lý hạn chế rằng LLM tiền huấn luyện mặc định đánh dấu mọi sự kiện là bất thường. Ví dụ, có thể bổ sung bước hiệu chỉnh xác suất (calibration) hoặc huấn luyện nhẹ (fine-tune) với dữ liệu chỉ chứa trạng thái bình thường để giảm bias và tăng precision. Bằng chứng từ kết quả EnrichLog cho thấy sử dụng 2 bước giúp “giữ recall cao trong khi giảm dương tính giả”. Dự kiến cải thiện: tăng precision mà vẫn giữ recall, cải thiện độ F1 chung. Có thể đánh giá bằng so sánh precision/recall giữa LLM gốc và LLM sau điều chỉnh, và đo changes trong false positive rate.

- **Nâng cấp cơ chế truy vấn cho LogPrompt bằng trích xuất thông minh hoặc bộ nhớ động** – Xử lý hạn chế về giới hạn bối cảnh tĩnh và độ trễ. Thay vì chọn ngẫu nhiên 100 dòng cũ, có thể áp dụng **retrieval động**: chọn lọc các log liên quan nhất (theo embedding) hoặc lưu giữ mẫu lịch sử qua một “thẻ nhớ” (memory) để bổ sung ngữ cảnh cho prompt. Ví dụ: dùng thuật toán embedding để tìm 10 dòng cũ liên quan nhất thay vì chọn ngẫu nhiên, hoặc dùng LLM có khả năng tiếp tục trước các entry đã xử lý. Kỳ vọng cải thiện: tăng recall/precision nhờ có ngữ cảnh phù hợp hơn, giảm độ trễ bởi chỉ truy xuất thông tin cần thiết. Thí nghiệm: so sánh F1 và độ trễ giữa LogPrompt cơ bản và phiên bản có retrieval; thực nghiệm loại bỏ từng thành phần (ablation).

- **Mở rộng phương pháp truy vấn RAG bằng cả ngữ nghĩa của log thô** – Xử lý vấn đề của RAGLog/LogRAG (template-based) bằng cách tích hợp thông tin ngữ nghĩa sâu từ văn bản log gốc. Cụ thể, bên cạnh lưu template, lưu cả embedding của toàn bộ thông điệp log trong cơ sở dữ liệu RAG. Khi truy vấn, hệ thống vừa so sánh template, vừa so sánh nội dung ký tự. Bằng chứng: mô hình phải “trực tiếp phân tích văn bản log thô để giữ lại thông tin ngữ nghĩa”. Kỳ vọng: nâng cao khả năng phân biệt các sự kiện khác thường mà mẫu template không phân biệt được. Đánh giá: so sánh hiệu suất (F1) của RAGLog/LogRAG có và không có embedding log, trên cùng tập dữ liệu; kết hợp đo thêm hiện tượng giảm nhầm lẫn.

- **Bổ sung tri thức chuyên ngành bằng cách tăng cường dữ liệu ngữ cảnh (knowledge augmentation)** – Hạn chế hiện tại của các phương pháp LLM là thiếu tri thức ngành. Ví dụ cải thiện: tích hợp một **cơ sở tri thức ngoại tuyến** gồm định nghĩa lỗi, nguyên nhân, hoặc mạng kiến thức hoạt động của hệ thống, và cung cấp cho LLM dưới dạng prompt hoặc qua RAG. EnrichLog đã chỉ ra rằng đưa “kiến thức cụ thể về tập dữ liệu” và “ví dụ mẫu” vào prompt giúp cải thiện rất nhiều. Kỳ vọng: cải thiện độ chính xác và giải thích được cao hơn nhờ LLM hiểu ngữ cảnh sâu của hệ thống; đánh giá qua sự thay đổi F1 và confidence khi có/không có tri thức bổ sung. 

- **Sử dụng mô hình LLM có bộ nhớ/bối cảnh dài hoặc các cơ chế lưu trữ (Memory) cho bối cảnh dài** – Khắc phục giới hạn ngữ cảnh và bộ nhớ của LLM. Ví dụ: dùng LLM kiến trúc mới có context window lớn hơn (hoặc phân mảnh input thành các khối có attention dài) để xử lý cả một luồng log dài hơn, thay vì cắt gọt. Hoặc dùng LLM có khả năng truy xuất (“openAI Retrieval Memory”) ghi nhớ các sự kiện quan trọng đã học. Dựa trên nhận xét của LogLLM rằng **LLM gặp khó khi input liên tục cả chuỗi log dài** và sử dụng BERT để tóm tắt mỗi bản tin, ta có thể sử dụng giải thuật tóm tắt tích hợp hoặc mô hình LLM có bộ nhớ dài (thí dụ Longformer). Kỳ vọng: giữ được thông tin xuyên suốt nhiều mục log, nâng cao khả năng phát hiện bất thường xuất hiện ở phần sau của luồng sự kiện. Đánh giá: so sánh hiệu năng trên các luồng dài cho mô hình gốc vs mô hình tăng dung lượng/ngữ cảnh.

Mỗi cơ hội trên đều được hình thành từ các hạn chế đã xác nhận, có chứng cứ hỗ trợ từ kết quả nghiên cứu và có tiềm năng được đánh giá thực nghiệm. Chẳng hạn, cơ hội thêm ngữ nghĩa log gốc dựa trên lời nhận xét “template pipeline giới hạn khả năng, cần xử lý văn bản thô”. Cơ hội bổ sung tri thức tận dụng kết quả cho thấy RAG và LogPrompt cùng fail trên một số bộ dữ liệu (BGL, Thunderbird), gợi ý cần cách tiếp cận mạnh hơn về tri thức. 

## 4. Đánh giá cơ hội cải tiến

Đối với mỗi cơ hội trên, chúng tôi đánh giá các khía cạnh chính (trên thang 1–10, càng cao càng tích cực) như sau:

| **Cơ hội**                                                         | **Baseline**          | **Hạn chế**                            | **Bằng chứng**           | **Evidence Strength** | **Giá trị Khoa học** | **Giá trị Kỹ thuật** | **Khả năng Thực thi** | **Phù hợp Luận văn** | **Cơ hội Công bố** | **Giá trị Công nghiệp** | **Đánh giá tổng quan** |
|-------------------------------------------------------------------|-----------------------|----------------------------------------|-------------------------|----------------------:|--------------------:|--------------------:|----------------------:|--------------------:|-------------------:|-----------------------:|-----------------------:|
| **1. Hiệu chỉnh mô hình LLM (calibration)**                        | LLM zero-shot         | Dương tính giả cao (low precision) | EnrichLog (EnrichLog*) | 8                   | 7                  | 7                  | 9                    | 9                  | 6                 | 8                     | 8.0                   |
| **2. Truy xuất ngữ cảnh cho LogPrompt (retrieval/memory)**        | LogPrompt (static)    | Giới hạn bối cảnh, độ trễ       | Prompt-based tradeoff | 7                   | 7                  | 6                  | 6                    | 7                  | 7                 | 6                     | 6.3                   |
| **3. Tích hợp ngữ nghĩa log gốc vào RAG (semantic retrieval)**     | RAGLog/LogRAG        | Mất thông tin gốc (template bias) | RAG vs EnrichLog    | 8                   | 8                  | 8                  | 6                    | 7                  | 8                 | 8                     | 7.5                   |
| **4. Bổ sung kiến thức chuyên ngành (Knowledge-augmented)**       | LLM/RAG              | Thiếu tri thức hệ thống         | EnrichLog corpus/samples | 7                   | 8                  | 7                  | 5                    | 5                  | 8                 | 7                     | 6.8                   |
| **5. LLM có bộ nhớ/ngữ cảnh dài (Memory-Augmented)**              | LLM large-context     | Giới hạn dài ngữ cảnh, OOM    | LogLLM summarization | 8                   | 8                  | 8                  | 6                    | 7                  | 7                 | 8                     | 7.6                   |

- **Evidence Strength:** độ mạnh của bằng chứng hỗ trợ ý tưởng (có dẫn chứng thí nghiệm). Ví dụ, O1 (LLM calibration) có chứng cứ [33†L770-L779] (EnrichLog*) cho thấy cải thiện rõ tình trạng false positive. O3 (ngữ nghĩa log gốc) có chứng cứ từ [19†L124-L127][21†L262-L266] mạnh về hạn chế template. Điểm thấp có ở cơ hội 2 vì chỉ dựa trên báo cáo trade-off prompt.
- **Giá trị Khoa học:** mức độ đóng góp mới, giải quyết hạn chế rõ. O3, O4 cao do xử lý vấn đề chủ chốt; O1, O5 vừa phải (điều chỉnh, kỹ thuật); O2 trung bình.
- **Giá trị Kỹ thuật:** kỳ vọng cải thiện hiệu năng/dộ chính xác. O3, O5 được đánh giá cao vì trực tiếp nâng cao khả năng nhận diện; O1 trung bình cao (trực tiếp ảnh hưởng precision); O4 tốt (cải thiện sematic); O2 có thể không cải thiện quá nhiều do độ trễ.
- **Khả năng Thực thi:** độ khó triển khai (1 khó – 10 dễ). O1 đơn giản (bộ ngưỡng, tinh chỉnh prompt) nên cao; O2, O3, O5 cần triển khai thu thập/vận hành retrieval hơi phức tạp hơn; O4 khó nhất (tổ chức cơ sở tri thức).
- **Phù hợp Luận văn:** tính hoàn thành trong 6–9 tháng, khả thi cho luận văn. Tương tự Khả năng Thực thi.
- **Cơ hội Công bố:** tiềm năng đăng bài: O3, O4 có tính mới cao; O1, O5 hơi thông dụng nhưng vẫn quan trọng; O2 vừa tầm.
- **Giá trị Công nghiệp:** mức độ hữu ích cho sản phẩm: O1, O3, O5 cao (nâng chất lượng cảnh báo); O4 trung bình-cao (phụ thuộc domain); O2 thấp hơn (chủ yếu hạ tầng).

Căn cứ vào tổng thể các tiêu chí, **cơ hội 1, 3, 5** có điểm cộng đồng cao nhất (7–8) nhờ bằng chứng rõ, tác động lớn và khả thi. Các cơ hội 2, 4 có tiềm năng nhưng điểm thực thi hoặc công bố kém hơn. 

## 5. Phân tích công nghệ Foundation Model

Nhìn từ góc độ công nghệ **Foundation Models** và các thành phần AI:

- **LLM và reasoning:** Phù hợp với các cải tiến liên quan đến hiểu ngữ nghĩa sâu và suy luận phức tạp. Ví dụ, “nâng cấp tri thức chuyên ngành” sử dụng LLM để diễn giải tài liệu hệ thống, hoặc “bổ sung bộ nhớ” sử dụng LLM có attention dài. O1 (hiệu chỉnh LLM) chủ yếu liên quan tới mô hình LLM nội sinh và prompt engineering.  
- **Retrieval/RAG:** Định hướng các cải thiện có chứa cơ sở tri thức bên ngoài. Cơ hội 2 (truy xuất ngữ cảnh cho prompt) và 3 (truy xuất thông tin ngữ nghĩa từ log) nằm ở mảng này. Chúng đề xuất dùng kho tri thức (như vector embedding) để hỗ trợ LLM. Phải đánh giá kỹ về chất lượng và tính kịp thời của dữ liệu truy vấn (như embedding log, cơ sở tri thức tài liệu) bởi chúng quyết định hiệu quả phát hiện.  
- **Knowledge-Augmented AI:** Tập trung vào tích hợp tri thức bên ngoài như ontologies hay knowledge graph. Cơ hội 4 (tăng cường tri thức chuyên ngành) thuộc nhóm này. Nó liên quan đến việc mã hóa các nghiệp vụ hệ thống, mã lỗi, hoặc tài liệu vận hành vào mô hình. Mặc dù tiềm năng giúp LLM hiểu sâu hơn, cần lưu ý độ lớn của kiến thức (có thể vượt ngưỡng ngữ cảnh) và rủi ro LLM “hoang tưởng”.  
- **Memory/Bộ nhớ dài:** Đề cập đến các mô hình có lưu trữ thông tin lịch sử. Cơ hội 2 (dạng memory cho prompt) và 5 (LLM context dài) liên quan. O5 có thể tận dụng LLM mới (như transformer có context window dài) hoặc kết hợp với bộ nhớ bên ngoài (vector store lưu lịch sử log quan trọng).  
- **Reasoning (Logic, causal):** Mặc dù quan trọng trong một số hệ thống, các cơ hội trên không tập trung vào reasoning cao cấp (chẳng hạn chain-of-thought) vì vấn đề ở đây chủ yếu là dữ liệu và bối cảnh đầu vào. LLM có reasoning chỉ giúp ở bước hậu (giải thích), không phải cốt lõi.
- **Agentic AI:** Liên quan đến tự động hóa nhiều bước và sử dụng nhiều mô hình/đại lý (agents). Trong bối cảnh này, khó thấy cần agent. Vd. không cần một agent tuần tự tra cứu nhiều nguồn cho từng log. Agent có thể tăng độ phức tạp (độ trễ, chi phí) mà không rõ mang lại lợi ích cụ thể.

## 6. Ưu tiên phát hiện sớm

Các cải tiến được đề xuất chủ yếu cải thiện độ chính xác và chất lượng nhãn chứ chưa trực tiếp tối ưu hóa “phát hiện sớm” (lead time). Ví dụ:

- **O1 (calibration)**: tăng độ chính xác nhãn bất thường nhưng không kéo ngắn thời gian cảnh báo. 
- **O2 (retrieval prompt)**: có thể tăng độ nhạy do thêm ngữ cảnh, nhưng độ trễ tăng có thể cản trở cảnh báo sớm. 
- **O3 (semantic retrieval)**: cải thiện phân loại nhưng không ảnh hưởng trực tiếp lead time.
- **O4 (bổ sung tri thức)**: cũng chủ yếu nâng độ tin cậy nhãn, không nhắm trực tiếp đến phát hiện sớm.
- **O5 (memory)**: có thể hỗ trợ bằng cách lưu giữ thông tin qua thời gian, nhưng chưa rõ nó cho phép đưa ra cảnh báo trước khi sự kiện hoàn thành.

Tóm lại, các cải tiến trên tập trung nâng cao độ chính xác phân loại (Precision/F1). Để ưu tiên phát hiện sớm, cần bổ sung đánh giá như *Time-to-Detect* (khoảng thời gian từ khởi phát bất thường đến khi cảnh báo) hoặc *Early Warning Horizon*. Nếu nghiên cứu mở rộng vào mục tiêu này, có thể xem xét những giải pháp chuyên biệt như mô hình dự báo thời gian hoặc chú trọng cảnh báo sớm trong tập huấn luyện (ví dụ, đa nhãn sớm). Tuy nhiên, trong phạm vi cải thiện nhỏ của baseline, những điểm này cần được ghi nhận là mục tiêu đánh giá bổ sung, thay vì mục tiêu thiết kế trực tiếp.

## 7. Bản đồ Baseline → Hạn chế → Cải thiện

| **Baseline (2025–2026)**      | **Hạn chế đã xác nhận**                        | **Strength Chứng cứ** | **Nguyên nhân gốc**      | **Hướng cải thiện**                                            | **Tác động mong đợi**                              | **Đánh giá**                                                 | **Rủi ro chính**                        |
|-------------------------------|----------------------------------------------|----------------------|--------------------------|-----------------------------------------------------------------|----------------------------------------------------|-------------------------------------------------------------|------------------------------------------|
| **LLM tiền huấn luyện (zero-shot)**    | Chạy quá mức (100% recall, precision thấp) | 8                    | Dựa hoàn toàn kiến thức nội sinh, lệch về dương tính giả | Bổ sung điều chỉnh (threshold/fine-tune) để giảm dương tính giả | Tăng precision, giữ recall cao                       | So sánh precision/recall với & không điều chỉnh; đo giảm FP/FN | Quá ít dữ liệu “bình thường” để hiệu chỉnh    |
| **LogPrompt (prompt tĩnh)**   | Cần prompt dài để đạt chính xác, làm tăng độ trễ    | 7                    | Bộ nhớ ngữ cảnh hạn chế, chọn mẫu ngẫu nhiên    | Dùng truy vấn chọn lọc (embedding retrieval) hoặc memory       | Cải thiện recall/precision với ít ví dụ hơn; giảm độ trễ | Thử nghiệm với số lượng và cách chọn ví dụ khác nhau        | Độ trễ vẫn tăng nếu tìm kiếm nhiều; lạc hướng nếu chọn nhầm ví dụ |
| **RAGLog / LogRAG (template)**   | Mất ngữ nghĩa; cùng template biểu thị cả bình thường và bất thường | 8                    | Dựa vào parser tạo template thô         | Tăng cường truy vấn bằng embedding log gốc (kết hợp ký tự)   | Phát hiện đúng thêm các bất thường ẩn dưới mẫu giống nhau        | So sánh F1 với/không dùng embedding log; đánh giá false negative   | Chi phí tính toán (embedding); risk nhiễu nếu truy xuất sai mẫu     |
| **LLM + tri thức (EnrichLog)** | Phụ thuộc dữ liệu chuyên ngành; corpus-only cải thiện rất ít | 7                    | Cần tài liệu chi tiết, nếu thiếu không tận dụng được | Hoàn thiện corpus-specific và sample-specific knowledge, hoặc dùng knowledge graph | Tăng độ tin cậy và giảm false positives khi có tri thức đúng    | Đánh giá F1 với/không có tri thức; metrics confidence               | Dữ liệu tri thức khó có, nguy cơ “bay màu” nếu LLM hiểu sai      |
| **Session-based (MidLog)**    | Không áp dụng cho từng sự kiện (phát hiện sớm) | 5                    | Thiết kế dựa vào chuỗi dài            | Tích hợp mô hình hiện tại với thông tin đa-thời điểm (nếu cần) | Mở rộng khả năng phát hiện tổng hợp nhưng phức tạp | (Nếu cần) Đánh giá kết hợp với trình phát hiện entry-based         | Không khả thi trong scope luận văn                |

Mỗi dòng thể hiện mối liên kết từ **Baseline → Hạn chế → Nguyên nhân → Cải thiện**. Ví dụ, **LLM tiền huấn luyện** gặp tình trạng bias nêu trên (high recall, low precision) do thiếu huấn luyện mục tiêu; cải tiến đề xuất là **hiệu chỉnh threshold hoặc tinh chỉnh nhẹ** để giảm tỷ lệ cảnh báo giả, kỳ vọng tăng precision mà vẫn giữ recall cao. **LogPrompt** được cải thiện bằng truy vấn thông minh thay vì chọn ngẫu nhiên các log lịch sử, nhằm bổ sung bối cảnh cần thiết mà không tăng độ trễ quá nhiều. 

## 8. Phạm vi cải tiến

Phân loại mức độ cải tiến theo quy mô thay đổi:

- **Mức 1 – Sửa đổi tối thiểu:** Thay đổi một thành phần. Ví dụ, O1 (calibration LLM) và O2 (cải thiện selection prompt) chỉ can thiệp vào thành phần đầu ra hoặc retrieval hiện có. Đây là ưu tiên cao vì tính khả thi cao và ít rủi ro.
- **Mức 2 – Mở rộng vừa phải:** Bổ sung một số thành phần liên quan. Ví dụ O3 (tích hợp embedding log) yêu cầu thêm thành phần embedder và so sánh, O5 (LLM memory) cần thay thế mô hình LLM hoặc thêm hệ thống bộ nhớ. Mức độ phức tạp cao hơn nhưng nếu khả thi thì có thể thử.
- **Mức 3 – Tái kiến trúc lớn:** Thay đổi nhiều thành phần hoặc khung tổng thể mới. O4 (tri thức chuyên ngành) có thể đòi hỏi bổ sung cơ sở tri thức lớn và thiết kế pipeline mới, ít khả thi trong thời gian giới hạn.

Ưu tiên được đặt vào **Mức 1 – 2** (thay đổi nhỏ đến vừa), nhằm đảm bảo có thể hoàn thành thử nghiệm thực nghiệm rõ ràng trong thời gian luận văn. 

## 9. Tính khả thi thực nghiệm

Mỗi cơ hội cải tiến có thể kiểm chứng qua các bước:

- **Baseline:** Phương pháp gốc của năm 2025–2026 (ví dụ LLM không sửa đổi, LogPrompt gốc, RAGLog gốc, v.v.) được tái triển khai.
- **Bản cải tiến:** Thêm thành phần cải thiện (ví dụ, LLM sau hiệu chỉnh; LogPrompt với retrieval; RAGLog với embedding mới).
- **Ablation:** Nếu cần, thử nghiệm loại bỏ từng yếu tố mới để đánh giá tác dụng riêng. Ví dụ, khi dùng truy xuất, ablation có thể là chỉ dùng một phần tri thức.
- **Metrics:** Ngoài Precision, Recall, F1 truyền thống, ưu tiên đo thêm các chỉ số về tính “sớm” như *Time-to-Detect*, *Mean Time to Detect (MTTD)* hoặc *Lead Time*. Ví dụ: trong ngữ cảnh phát hiện sớm, ta có thể đánh giá xem cải tiến giúp cảnh báo bao nhiêu giây/phút trước sự cố so với baseline. Các chỉ số phụ như latency, throughput cũng cần đo nếu thay đổi retrieval (O2) hoặc mô hình (O5). Robustness và generalization (chéo dataset) cũng nên xem xét nếu có thể.
- **Thiết kế thí nghiệm:** Với mỗi cơ hội, xây dựng các thí nghiệm đối chứng. Ví dụ: đối với O1, so sánh hiệu suất LLM trước và sau calibration trên cùng tập log; đối với O3, so sánh RAGLog có/không có sử dụng embedding; v.v.

Nếu một cơ hội không xác định được cách kiểm chứng (ví dụ rất khó đo lead time), đó là dấu hiệu giảm ưu tiên. Các cơ hội trên đều có thể kiểm chứng bằng cách thêm thành phần và đo lường các metric nêu trên.

## 10. Phù hợp luận văn

| **Cơ hội**                    | **Thời gian** | **Tính toán** | **Dữ liệu** | **Độ phức tạp** | **Tái lập** | **Rủi ro** | **Thích hợp luận văn** |
|-------------------------------|-------------:|-------------:|-----------:|---------------:|------------:|-----------:|----------------------:|
| **1. Calibration LLM**        | 2–3 tuần     | Thấp         | Có sẵn (log normal) | Thấp           | Cao        | Thấp       | 9/10                |
| **2. Retrieval cho Prompt**   | 1–2 tháng    | Trung bình   | Log lịch sử (có sẵn)  | Trung bình      | Trung bình | Trung bình | 7/10                |
| **3. Semantic Retrieval**     | 2–3 tháng    | Cao (embedding) | Cần tạo embedding log  | Trung bình      | Trung bình | Trung bình | 7/10                |
| **4. Knowledge-Augmented**    | 4–6 tháng    | Cao (tri thức)  | Cần thu thập tài liệu | Cao            | Thấp       | Cao        | 4/10                |
| **5. Memory-Augmented LLM**   | 2–3 tháng    | Cao (LLM mới)   | Sử dụng tập dữ liệu tương tự | Trung bình      | Trung bình | Trung bình | 7/10                |

Đánh giá cho thấy: **Cơ hội 1, 2, 3, 5** khả thi trong 6–9 tháng với tài nguyên tính toán vừa phải (chủ yếu GPU phổ thông) và dữ liệu sẵn có. Trong khi đó, **Cơ hội 4** tốn nhiều thời gian và phụ thuộc dữ liệu tri thức khó có, độ phức tạp cao nên ít phù hợp cho luận văn (điểm thấp).

## 11. Phân tích rủi ro

| **Cơ hội**                    | **Rủi ro chính**                            | **Xác suất** | **Tác động** | **Giải pháp giảm nhẹ**                        | **Rủi ro còn lại** |
|-------------------------------|--------------------------------------------|------------:|------------:|----------------------------------------------|-------------------|
| **1. Calibration LLM**        | Thiếu dữ liệu “bình thường” để calibrate   | Trung bình  | Trung bình  | Thu thập thêm log bình thường, sử dụng kỹ thuật oversample | Vẫn có thể giảm recall |
| **2. Retrieval Prompt**       | Lựa chọn ngữ cảnh sai (noisy)              | Thấp        | Trung bình  | Dùng embedding chất lượng, tuning tham số   | Tăng độ trễ nếu chọn nhiều ví dụ |
| **3. Semantic Retrieval**     | Chi phí tính toán cao; truy xuất sai        | Trung bình  | Cao        | Tối ưu hóa embedding, giới hạn kích thước bộ nhớ | Ít cải thiện nếu dữ liệu văn bản không đồng nhất |
| **4. Knowledge-Augmented**    | Tri thức sai/hư cấu (hallucination)         | Cao         | Cao        | Lọc/biên tập dữ liệu tri thức, kiểm tra đa nguồn | Kết quả vẫn lệ thuộc dữ liệu chuẩn |
| **5. Memory-Augmented LLM**   | LLM mới thất bại/không cải thiện (Out-of-memory) | Trung bình  | Trung bình  | Dùng mô hình tăng dần, thử nghiệm trên tập nhỏ  | Latency cao nếu context quá dài |

Các rủi ro chủ yếu liên quan tới **dữ liệu không đủ/chất lượng kém** (Cơ hội 1, 4) và **tăng độ trễ tính toán** (Cơ hội 2, 5). Chúng ta có thể giảm thiểu bằng các biện pháp như kỹ thuật oversampling, chuẩn hóa tri thức, chọn lựa mô hình/thông số phù hợp. Rủi ro tồn dư sẽ được cân nhắc trong thiết kế thí nghiệm và luận văn (ví dụ, đề cập khả năng recall giảm khi calibrate quá mức).

## 12. Xếp hạng cơ hội cải tiến

| **Hạng** | **Cơ hội**                           | **Baseline**        | **Hạn chế chính**                                 | **Bằng chứng**            | **Ảnh hưởng**                        | **Khả thi** | **Rủi ro** | **Tổng** |
|--------:|-------------------------------------|--------------------|-------------------------------------------------|---------------------------|-------------------------------------|-----------|-----------|--------:|
| 1        | Semantic Retrieval (Cơ hội 3)      | RAGLog/LogRAG      | Mất thông tin gốc (template)      | Template limit | Cải thiện mạnh F1                | 6/10      | Vừa phải   | ≈7.5   |
| 2        | Calibration LLM (Cơ hội 1)         | LLM tiền huấn luyện | Dương tính giả cao                | Baseline bias  | Tăng precision, giảm FP         | 9/10      | Thấp       | ≈8.0   |
| 3        | Memory-Augmented (Cơ hội 5)        | LLM large-context  | Giới hạn ngữ cảnh                | OOM issues   | Xử lý tốt hơn các log dài      | 6/10      | Vừa phải   | ≈7.6   |
| 4        | Retrieval cho Prompt (Cơ hội 2)    | LogPrompt          | Giới hạn bối cảnh, độ trễ         | Prompt tradeoff | Tăng precision/recall với ít data | 6/10      | Trung bình | ≈6.3   |
| 5        | Knowledge-Augmented (Cơ hội 4)    | LLM/RAG            | Thiếu tri thức hệ thống          | EnrichLog knowledge | Xử lý bất thường tốt hơn | 5/10      | Cao        | ≈6.8   |

Ưu tiên các cơ hội có **bằng chứng mạnh, tác động lớn, khả thi cao**. Đứng đầu là Ứng dụng **truy xuất ngữ nghĩa cho RAG (Cơ hội 3)** – xử lý trực tiếp hạn chế mẫu log đã được chứng minh (強 evidence), tiếp theo là **calibration LLM (Cơ hội 1)** – đơn giản nhưng hiệu quả (Cao khả thi). Hạng ba là **bộ nhớ/ngữ cảnh dài (Cơ hội 5)** do tiềm năng cải thiện với các log dài. **Retrieval cho prompt** và **tăng cường tri thức** (Cơ hội 2 và 4) ít ưu tiên hơn vì độ khả thi hoặc rủi ro thấp hơn, tuy vẫn có giá trị nếu có thời gian.

## 13. Cơ hội cải tiến hàng đầu

1. **Cơ hội 1 – Calibration Mô hình LLM cơ bản:**  
   - **Baseline:** LLM tiền huấn luyện (không có fine-tune).  
   - **Hạn chế:** Luôn gán hầu hết các sự kiện là bất thường (recall≈100%, precision thấp).  
   - **Bằng chứng:** Thí nghiệm EnrichLog cho thấy mẫu gốc (Base) đạt recall 100% nhưng precision chỉ ~7–21% (tại BGL). Kết quả nhấn mạnh bias hệ thống của LLM không cân bằng.  
   - **Hướng cải thiện:** Giới thiệu cơ chế hiệu chỉnh: ví dụ đặt ngưỡng xác suất (threshold) sao cho chỉ những câu trả lời có confidence vượt mức mới gán bất thường, hoặc huấn luyện nhẹ LLM với dữ liệu thuần “bình thường” để hiệu chỉnh bias.  
   - **Tác động:** Giảm mạnh số cảnh báo giả, tăng precision mà không đánh đổi nhiều recall; cải thiện F1 tổng thể. Có thể làm tăng tính tin cậy của hệ thống cảnh báo.  
   - **Đánh giá:** So sánh độ chính xác và recall trước/sau điều chỉnh trên các tập log. Dự kiến precision tăng đáng kể (từ ~30% lên >80% ở một số trường hợp).  
   - **Rủi ro:** Có thể giảm nhẹ recall nếu threshold quá cao; khả năng không đủ mẫu normal để calibrate. Mitigation: sử dụng kỹ thuật oversampling, thử nhiều giá trị threshold.  
   - **Phù hợp luận văn:** Rất phù hợp (thuần kỹ thuật, thời gian ngắn). Không cần dữ liệu mới lớn, dễ tái lập.  

2. **Cơ hội 2 – Thêm tìm kiếm ngữ cảnh cho Prompt:**  
   - **Baseline:** Phương pháp LogPrompt tiêu chuẩn với prompt tĩnh gồm 100 dòng ngẫu nhiên.  
   - **Hạn chế:** Hiệu quả phụ thuộc vào số lượng dòng tham chiếu; hiện tượng trade-off prompt dài – độ trễ cao.  
   - **Bằng chứng:** Ngưỡng bổ sung tham chiếu dẫn tới latency tăng. EnrichLog và RAGLog cho thấy kết quả tốt hơn khi tìm những log phù hợp thay vì ngẫu nhiên.  
   - **Hướng cải thiện:** Thay cho chọn ngẫu nhiên, áp dụng **truy xuất ngữ nghĩa**: sử dụng embedding (ví dụ BERT) để tìm K log cũ liên quan nhất đến log mới, hoặc dùng module memory để ghi nhớ các mẫu bất thường điển hình. Prompt nhập vào sẽ là các log liên quan nhất, không phải ngẫu nhiên.  
   - **Tác động:** Tăng khả năng phát hiện (cả precision và recall) nhờ có ví dụ phù hợp; giảm kích thước prompt cần dùng; giảm độ trễ vì chỉ đưa thông tin liên quan vào.  
   - **Đánh giá:** Thử nghiệm tăng F1 so với chọn ngẫu nhiên. Nên đo thêm thời gian thực thi. Có thể thấy một số dataset mà trước đó LogPrompt chỉ F1 ~36–54% (BGL) có thể tăng lên ~74% (theo EnrichLog).  
   - **Rủi ro:** Cần tuning embedding và K; nếu nhầm log, vẫn bị lỗi. Bù: thử nghiệm đa tham số, kiểm định kết quả với dữ liệu đã gắn nhãn.  
   - **Phù hợp luận văn:** Khá phù hợp; cần lập trình thêm retrieval nhưng vẫn nằm trong khả năng luận văn.

3. **Cơ hội 3 – Truy xuất ngữ nghĩa log gốc (Semantic Retrieval cho RAG):**  
   - **Baseline:** RAGLog hoặc LogRAG hiện nay chỉ dùng template log.  
   - **Hạn chế:** Vẫn “một mẫu có thể ứng với cả bình thường và bất thường”, tức cơ chế template không tách được hai trường hợp.  
   - **Bằng chứng:** Giới hạn của pipeline template được nhấn mạnh trong EnrichLog. Kết quả thử nghiệm cho thấy đưa thêm thông tin ngữ cảnh (corpus, sample) giúp vượt qua hạn chế này.  
   - **Hướng cải thiện:** Lưu trữ và truy vấn song song cả template lẫn nội dung văn bản (token) của log. Khi tìm kiếm, thực hiện tìm kiếm song song trong database template và database embedding văn bản. Sau đó kết hợp kết quả để đưa vào prompt LLM.  
   - **Tác động:** Kỳ vọng tăng đáng kể hiệu quả trên những trường hợp mà mẫu không đủ phân biệt. Ví dụ, các sự kiện có cùng template nhưng khác ở phần thông điệp (thông tin lỗi chi tiết) sẽ được xử lý chính xác hơn.  
   - **Đánh giá:** So sánh F1 trên bộ dữ liệu BGL/Spirit/... với RAG gốc. Đo thêm false negative reduction.  
   - **Rủi ro:** Tính toán embedding bổ sung, có thể tốn tài nguyên; nếu embedding không đủ tốt, cải thiện thấp. Giải pháp: sử dụng embedding chất lượng (như LM contextual), hạn chế chiều sau embedding.  
   - **Phù hợp luận văn:** Tốt. Cần thực thi thêm pipeline embedding, nhưng có sẵn code và dữ liệu, tập trung vào tích hợp và thử nghiệm.

4. **Cơ hội 4 – Tích hợp tri thức chuyên ngành (Knowledge-Augmented):**  
   - **Baseline:** Mọi phương pháp LLM/RAG hiện có mà không thêm tri thức đặc trưng.  
   - **Hạn chế:** LLM không biết đặc trưng hệ thống, còn corpus-only (chỉ tóm tắt log) cho cải thiện rất ít.  
   - **Bằng chứng:** EnrichLog chỉ marginal khi chỉ có tóm tắt corpus; chỉ khi thêm sample-level knowledge thì mới hiệu quả mạnh.  
   - **Hướng cải thiện:** Tạo bộ tri thức bao gồm quy tắc, lỗi hệ thống, kiến thức miền (có thể dạng knowledge graph hoặc bảng) và cung cấp cho LLM qua prompt hoặc tìm kiếm RAG. Ví dụ, tạo file tài liệu (các định nghĩa sự cố) và gửi vào prompt. Hoặc xây dựng mô-đun chuyên biệt để bổ sung thông tin này.  
   - **Tác động:** Nếu thực hiện tốt, có thể cải thiện lớn độ chính xác (nhất là với các trường hợp phức tạp), và giải thích được dự đoán. LLM sẽ hiểu ngữ cảnh kỹ thuật sâu hơn.  
   - **Đánh giá:** So sánh mô hình với/không có kiến thức ấy. Đo confidence prediction (theo EnrichLog cải thiện confidence).  
   - **Rủi ro:** Thu thập và biên soạn kiến thức là khó khăn; LLM có thể “sai lạc” nếu tri thức nhập sai. Phòng tránh: giám sát kết quả kỹ lưỡng, chỉ thêm tri thức thực sự cần thiết.  
   - **Phù hợp luận văn:** Ít phù hợp do khối lượng công việc lớn, rủi ro cao. Có thể là hướng phụ hoặc nghiên cứu dài hạn.

5. **Cơ hội 5 – Dùng LLM có bộ nhớ/dài hạn (Memory-Augmented LLM):**  
   - **Baseline:** LLM có window ngắn, hoặc pipeline hiện tại không lưu giữ thông tin vượt quá giới hạn.  
   - **Hạn chế:** LLM thiếu khả năng tiếp cận thông tin dài hạn, dễ rơi vào OOM khi chuỗi log dài.  
   - **Bằng chứng:** LogLLM đã chứng minh nếu input liên tục mọi log sẽ “OOM và làm LLM khó tập trung”. EnrichLog dùng 2 bước (EnrichLog*) để giảm false positive trong corpus lớn cũng gợi ý cần chia nhỏ tác vụ.  
   - **Hướng cải thiện:** Sử dụng LLM hỗ trợ context window dài (ví dụ GPT-4o, Longformer) hoặc chia log thành các phần tóm tắt qua BERT như LogLLM. Hoặc áp dụng mô-đun bộ nhớ ngoài: lưu trữ thông tin then chốt và cho phép LLM truy xuất khi cần.  
   - **Tác động:** Cho phép mô hình xem xét dãy sự kiện dài hơn, nâng cao khả năng phát hiện các bất thường xuất hiện ở phần sau của luồng log. Cải thiện dự đoán khi cần bối cảnh dài.  
   - **Đánh giá:** So sánh LLM gốc với phiên bản có context window mở rộng. Đo F1 trên các log dài (như BGL sessions). Đo thêm độ ổn định (không bị OOM).  
   - **Rủi ro:** Cần GPU mạnh; có thể latency tăng. Nếu chọn wrong architecture, không cải thiện. Giải pháp: thử nghiệm trên bộ dữ liệu mẫu, điều chỉnh kích thước block.  
   - **Phù hợp luận văn:** Khá cao. Cần làm quen với mô hình LLM mới hoặc kỹ thuật summarization, vẫn khả thi trong 6–9 tháng.

## 14. Khuyến nghị cuối cùng

- **Ưu tiên chính (Primary):** *Kết hợp ngữ nghĩa log gốc vào RAG (Cơ hội 3).* Đây là cải tiến trực tiếp xử lý hạn chế căn bản nhất (template bias) với bằng chứng vững chắc. Cải tiến này tuy cần thêm công cụ embedding nhưng hoàn toàn khả thi và dự kiến nâng cao F1 đáng kể mà vẫn kiểm soát được độ phức tạp. Là ưu tiên hàng đầu nhờ tác động lớn và tiềm năng phổ biến.  
- **Dự phòng (Backup):** *Hiệu chỉnh mô hình LLM (Cơ hội 1).* Đây là giải pháp đơn giản, ít rủi ro với khả năng thực hiện nhanh, giúp tăng precision ngay. Mặc dù ít tính mới, nhưng theo evidence từ EnrichLog, cho kết quả rõ ràng trong việc giảm false positive. Đề xuất làm song song nếu các cải tiến khác trì hoãn.  
- **Lựa chọn thay thế (Alternative):** *Sử dụng LLM có bộ nhớ/ngữ cảnh dài (Cơ hội 5).* Nếu nhóm nghiên cứu tiếp cận được các mô hình LLM hiện đại hỗ trợ context dài hoặc áp dụng cơ chế memory, đây có thể là hướng bổ sung để xử lý trường hợp log dài và dữ liệu khổng lồ. Dù phải đầu tư vào tài nguyên, nhưng cải thiện tiềm năng về khả năng phân tích chuỗi dài của hệ thống.

Mỗi hướng đều dựa trên **baseline-giới hạn** cụ thể và có bằng chứng hỗ trợ (ví dụ về tình trạng mặc định dự đoán hay mất ngữ nghĩa mẫu). Các đề xuất này đều tập trung vào **targeted improvement** (chứ không xây dựng framework mới hoàn toàn), dễ kiểm chứng thực nghiệm (so sánh metric) và gắn sát giới hạn đã xác nhận.

## 15. Định vị nghiên cứu cuối cùng

Qua đánh giá tổng hợp, các cải tiến này đều thuộc **Level 2 – Cải tiến nhắm mục tiêu** (Targeted Improvement) so với baseline 2025–2026. Chúng không tạo ra khung hoặc kiến trúc hoàn toàn mới mà mở rộng/bổ sung các thành phần để nâng chất. Kết quả cho thấy đủ cơ sở để dự án luận văn tập trung vào **mức cải tiến (improvement)** trên nền tảng phương pháp hiện có, chứ không phải reimplementation hay phát triển framework mới. Các cơ hội đã có chứng cứ tương đối rõ (ít nhất là do các nghiên cứu 2025 chỉ ra), và khả năng thí nghiệm cao. Nếu cần đưa ra ý kiến, đề tài này sẽ được định vị ở cấp “nâng cao phương pháp hiện tại” của năm 2025–2026, với mục tiêu cải thiện chi tiết và kiểm chứng thực nghiệm. 

**Tóm lại:** Theo phân tích, hướng nghiên cứu nên ưu tiên **cải tiến nhỏ nhưng có bằng chứng mạnh** (ví dụ, tích hợp ngữ nghĩa, calibrate LLM) thay vì ý tưởng lớn thiếu minh chứng. Trung tâm vẫn là “Baseline → Hạn chế → Giải pháp cụ thể → Đo lường lợi ích”. Kết luận chung: đề tài có cơ sở nằm ở **mức cải tiến mục tiêu (targeted improvement)**, với các bằng chứng và thí nghiệm hỗ trợ. 

