2026-05-27 12:09
Status: #ideas
Tag: [[Lập trình cơ bản]]
Linking Notes: [[Jeff Dean và Sanjay Ghemawat - Tình bạn đưa google đến vĩ đại]], [[Hadoop]]

## Bối cảnh đầu những năm 2000

Đầu những năm 2000, Internet bùng nổ, kích thước mạng World Wide Web tăng theo cấp số nhân qua từng năm. Các kỹ sư hàng đầu tại những công ty công nghệ đối mặt với thách thức rất lớn về việc scale-up hệ thống lên một mức độ chưa từng có trước đây.

Google lúc này là một startup kỳ lân đã chuyển lên văn phòng chính thức tại Mountain View, chứ không còn hoạt động trong phòng ký túc xá của Larry Page nữa; công cụ tìm kiếm của họ đã có hàng trăm triệu lượt tìm kiếm mỗi ngày. Khi ta search the web, ta không thực sự làm động tác Ctrl+F trên toàn hệ thống World Wide Web mà chỉ đơn giản là tìm kiếm trên một tấm bản đồ mà Google đã lập sẵn.

<div class="obs-callout obs-callout-quote" markdown="1">
<div class="obs-callout-title">Quote</div>

Khi Google còn tên BackRub (1996), bản đồ ấy nhỏ đến mức để vừa trong dàn máy đặt trong phòng ký túc xá của Page. Đến tháng Ba 2000, không có siêu máy tính nào đủ lớn để xử lý nó. Cách duy nhất để theo kịp là mua nhiều máy phổ thông rồi nối thành một hạm đội.

Vì gần nửa chi phí của các máy này nằm ở những linh kiện chẳng có mấy giá trị với Google như vỏ kim loại hay ổ đĩa, công ty đặt mua bo mạch chủ và ổ cứng rời rồi tự ráp chúng lại với nhau. Họ xếp được khoảng 1.500 thiết bị như vậy thành các cột cao gần 2 mét trong một tòa nhà ở Santa Clara, California; nhưng do lỗi phần cứng, chỉ khoảng 1.200 máy hoạt động. Các lỗi xuất hiện tưởng như ngẫu nhiên liên tục làm hệ thống đứt gãy. Muốn sống sót, Google phải hợp nhất đám máy đó thành một thể thống nhất, đàn hồi và chịu lỗi.

Jeff và Sanjay sát cánh phụ trách nỗ lực này. Wayne Rosing, từng làm ở Apple thời tiền Macintosh, gia nhập Google tháng 11/2000 để lãnh đạo đội kỹ thuật 100 người. “Họ mới là những người dẫn đường,” ông nói.

Làm việc 90 giờ mỗi tuần, họ viết mã để một ổ cứng hỏng cũng không kéo sập cả hệ thống. Họ thêm checkpoint vào quá trình crawl để có thể khởi động lại giữa chừng. Bằng cách phát triển sơ đồ mã hóa và nén mới, họ gần như nhân đôi sức chứa hệ thống.  

Trích: **The Friendship That Made Google Huge** _(xuất bản ngày 3 tháng 12, 2018 trên The New Yorker)_
</div>

Jeff và Sanjay được nhắc đến trong đoạn phía trên là Jeff Dean và Sanjay Ghemawat - hai kỹ sư huyền thoại của Google, hai kỹ sư cấp 11 duy nhất và nắm danh hiệu Google Senior Fellow cao quý cho tới thời điểm hiện tại. Vào đầu những năm 2000, đôi bạn thân này dính với nhau như hình với bóng, thậm chí nổi tiếng vì luôn code chung với nhau trên cùng một máy tính.

Tiếp tục làm việc cùng nhau và liên tục hoàn thiện các thuật toán tối ưu cho tính toán phân tán trên một cụm nhiều máy tính nối lại với nhau, năm 2003 và 2004, Jeff và Sanjay lần lượt cho ra hai paper có tính đột phá:
- [The Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf): Giải pháp lưu trữ phân tán
- [MapReduce: Simplified Data Processing on Large Clusters](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf): Giải pháp tính toán song song trên nhiều phần cứng rẻ tiền
## The Google File System

Ý tưởng chính của GFS là chặt 1 file khổng lồ (Petabyte ~ triệu GB) ra thành nhiều khúc nhỏ và lưu ở nhiều máy chủ nhỏ. Các máy chủ nhỏ này, được gọi là **Chunkserver**, báo cáo cho một máy chủ **Master**. 
Hãy tưởng tượng hệ thống GFS như một nhà kho: 
- **Master** là ông quản lý kho nắm hết vị trí của từng loại mặt hàng (sách kệ 1, đồ ăn kệ 2, tivi kệ 3,…)
- **Chunkserver** là các kệ thực sự chứa hàng
- Những cục hàng nhỏ để trên kệ được gọi là **chunk**

Vậy câu hỏi đặt ra là: khi ta cắt nhỏ dữ liệu và lưu trữ ở nhiều nơi như vậy, nếu chẳng may một node bị lỗi thì làm sao? Phần cứng máy tính tương đối ổn định và hiếm khi gặp lỗi... cho tới khi bạn có đủ nhiều. Quản lý một hạm đội hàng nghìn bộ xử lý nối lại với nhau bằng dây rợ loằng ngoằng thật không phải một công việc đơn giản. Các vấn đề như đứt dây, chập điện, thậm chí là random byte flip vì bức xạ vi sóng vũ trụ xảy ra như cơm bữa. Sẽ là thảm họa nếu file dữ liệu khổng lồ của bạn tự nhiên mất đi vài mảnh chỉ vì một cái dây điện đột nhiên sút ra.

Các nhà khoa học tại Google đã tính đến cả cơ chế chịu lỗi cho việc này trong thuật toán của mình. 
- Cách giải quyết là mỗi block dữ liệu nhỏ sẽ được nhân bản thành 3 bản sao và lưu ở 3 máy chủ khác nhau. Nếu một máy fail thì có thể lấy từ máy khác sang backup. Đây là lý do GFS được quảng cáo với khả năng chịu lỗi cao.
- rack awareness: **Master** sẽ quyết định 3 bản ghi trên được lưu ở node nào thông qua một thuật toán gọi là rack awareness (ưu tiên 2 bản cùng 1 rack để đọc, ghi nhanh bản thứ 3 ở rack khác để phòng hư máy, mất điện)

Tuy nhiên, **GFS** cũng có một số hạn chế. Đổi lại sự bá đạo về dung lượng, GFS chấp nhận đánh đổi. Nó sinh ra chỉ để phục vụ cho việc **đọc/ghi dữ liệu lớn một cách tuần tự** (quét từ đầu đến cuối file để làm index công cụ tìm kiếm). GFS sẽ cực kỳ phế và chậm chạp nếu bạn dùng nó cho các tác vụ đòi hỏi chỉnh sửa, ghi đè liên tục hoặc nhảy cóc để đọc một phần nhỏ ở giữa file (Random Access).
- [Tìm Hiểu Về Hadoop, HDFS, Hadoop MapReduce - Viblo](https://viblo.asia/p/tim-hieu-ve-hadoop-hdfs-hadoop-mapreduce-ly-thuyet-5pPLkjNZJRZ#_hdfs-hadoop-distributes-file-system-2)

## Map & Reduce

<div class="obs-callout obs-callout-quote" markdown="1">
<div class="obs-callout-title">Quote</div>

Trong vài năm đầu của thập niên 2000, hai tác giả cùng nhiều nhà nghiên cứu khác tại Google đã thử rất nhiều cách khác nhau để xử lý một lượng lớn dữ liệu thô, chẳng hạn: file crawled về từ web, web requests logs,... để tính toán nhiều loại dữ liệu thứ cấp khác nhau, chẳng hạn như chỉ mục đảo ngược, cấu trúc đồ thị của tài liệu web, số lượng trang được cào về trên mỗi máy chủ, tập hợp các truy vấn phổ biến nhất theo từng ngày, v.v. 

Hầu hết các tính toán phía trên đều khá đơn giản về mặt khái niệm, tuy nhiên lại khó khăn trong khâu thực hành vì lượng dữ liệu đầu vào quá lớn và các phép tính phải được phân phối trên hàng trăm hoặc hàng nghìn máy để hoàn thành trong một khoảng thời gian hợp lý. Các vấn đề về tính toán song song, phân phối dữ liệu và xử lý lỗi đòi hỏi một lượng code lớn và phức tạp để giải quyết, vì thế thường đẩy nhà nghiên cứu xa khỏi việc hoàn thành các bài toán ban đầu.

*Theo Jeff & Sanjay - 2004*
[static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf)
</div>

Để giải quyết sự phức tạp này, hai nhà khoa học đã thiết kế một framework tính toán mới, tự động hóa các setup phức tạp của việc song song hóa code, kiểm soát lỗi phần cứng, phân phối dữ liệu giữa nhiều bộ xử lý khác nhau. Mô hình tính toán này được lấy cảm hứng từ các hàm cơ bản `map` và `reduce` trong các functional programming languages như Lisp.

Về cơ bản có thể tóm gọn: 
- **Map:** Các máy đồng loạt xử lý phần dữ liệu mình đang giữ để cho ra kết quả trung gian.
- **Reduce:** Gộp các kết quả trung gian đó lại thành kết quả cuối cùng.
Ví dụ:
- Bài toán của bạn là đếm số lần xuất hiện của từ “hạnh phúc” trong toàn bộ sách trong kho.
- Có 2 cách để làm bài này:
	1. Thuê một ông kế toán trưởng đếm nhanh, cộng giỏi đi đến từng kệ, giở sách ra đếm từ đầu đến cuối.
	2. Thuê 1000 công nhân đứng sẵn ở từng kệ, đếm 1000 kệ một lúc rồi ông kế toán trưởng đi lấy số cộng lại thôi.
- Cách (2) là cách của MapReduce, trong đó câu lệnh Map & Reduce sẽ như sau:
	- Map: Hãy đếm cho tôi số lần xuất hiện của từ "hạnh phúc" trên kệ của bạn, ghi kết quả ra giấy với cú pháp như sau: `[mã_kệ, kết_quả_đếm]`
	- Reduce: Collect toàn bộ kết quả từ các kệ & tính tổng `kết_quả_đếm`. 
### Sự bùng nổ tại Google

Hai kỹ sư huyền thoại Jeff & Sanjay đã bắt tay viết những dòng code đầu tiên cho thư viện MapReduce vào tháng 2/2003. Chỉ 6 tháng sau, đến tháng 8/2003, họ tiếp tục tung ra các bản nâng cấp lớn, đưa vào những cơ chế then chốt như ưu tiên xử lý dữ liệu tại chỗ (locality optimization) và cân bằng tải động (dynamic load balancing) giữa các máy worker.

Nhưng điều thú vị là, khi công bố paper vào năm 2004, chính Jeff và Sanjay cũng thừa nhận họ đã vô cùng bất ngờ trước độ "đa năng" của hệ thống do chính tay mình tạo ra. MapReduce nhanh chóng vượt ra khỏi bài toán Indexing ban đầu và lan rộng ra mọi ngóc ngách dự án tại Google. Khắp các phòng ban, người ta dùng nó để giải quyết đủ thứ chuyện:

- Các bài toán Machine Learning quy mô khổng lồ.
- Phân cụm dữ liệu (clustering) để vận hành Google News và Froogle.
- Khai thác dữ liệu để chạy các báo cáo xu hướng tìm kiếm toàn cầu (như Google Zeitgeist).
- Bóc tách thuộc tính từ hàng triệu trang web (chẳng hạn trích xuất thông tin địa lý để tối ưu cho hệ thống local search).
- Xử lý các phép toán đồ thị (graph computations) cực lớn.

Sự bùng nổ này thể hiện rất rõ qua các con số trong kho lưu trữ mã nguồn của Google lúc bấy giờ. Từ con số 0 tròn trĩnh vào đầu năm 2003, lượng chương trình dùng MapReduce được đẩy (check-in) lên hệ thống đã vọt lên gần 900 chương trình độc lập chỉ trong vòng 1 năm rưỡi (tính đến tháng 9/2004).

[laurel.datsi.fi.upm.es/\_media/docencia/asignaturas/ppd/mapreduce-osdi04slides.pdf](https://laurel.datsi.fi.upm.es/_media/docencia/asignaturas/ppd/mapreduce-osdi04slides.pdf)
![Pasted image 20260528163614](../assets/media/Pasted%20image%2020260528163614.png)

Tại sao MapReduce lại có sức lan tỏa khủng khiếp đến vậy? Câu trả lời nằm ở sự tối giản. Nó cho phép một kỹ sư viết ra một đoạn code đơn giản và chạy trơn tru trên cả nghìn máy chủ chỉ trong chưa đầy 30 phút, đẩy tốc độ làm bản mẫu (prototyping) lên mức không tưởng ở thời điểm đó.

Đột phá lớn nhất của hệ thống này là tính trừu tượng hóa: Nó trao sức mạnh siêu máy tính cho cả những lập trình viên **chưa từng có một ngày kinh nghiệm** làm việc với hệ thống phân tán hay tính toán song song. Họ không cần đau đầu vì lỗi phần cứng hay đứt mạng, họ chỉ việc viết logic, mọi sự phức tạp của hạ tầng đã có MapReduce lo.
### Tại sao MapReduce lại là một cuộc cách mạng?

1. **Mang tính toán đến với dữ liệu thay vì mang dữ liệu về nơi tính toán:** sách (dữ liệu) nằm im trên kệ, thứ duy nhất di chuyển là thuật toán `map` (siêu nhẹ) được gửi đến cho các công nhân. 
2. **Sức mạnh của đám đông:** Điều này hiển nhiên, ông kế toán trưởng dù có đếm nhanh cộng giỏi cỡ nào cũng không lại 1000 công nhân đếm cùng một lúc. Nếu giả sử có tìm được ông đếm nhanh gấp 1000 lần người thường thì giá chắc chắn sẽ đắt hơn 1000 người bình thường cộng lại.
3. **Khả năng chịu lỗi:** Đang đếm nửa chừng, ông công nhân ở Kệ 5 bị ngất (Node bị sập). Ông quản lý kho lập tức chạy sang Kệ 8 (nơi đang chứa bản sao - sao chép dự phòng của Kệ 5 nhờ cơ chế nhân bản của HDFS) và bảo ông công nhân ở đó: _"Đếm hộ tao đống sách của Kệ 5 luôn cái"_. Hệ thống vẫn vận hành mượt mà, không phải chạy lại từ đầu.
### Hạn chế của MapReduce

MapReduce là một framework rất mạnh nhưng nó không phải là siêu thuật toán giải quyết được mọi vấn đề. MapReduce phù hợp nếu vấn đề của bạn có 2 thuộc tính sau đây:
- Bộ dữ liệu cực lớn.
- Phép toán có tính chất giao hoán và kết hợp, chẳng hạn phép cộng trong bài toán đếm bên trên.

Nhưng đối với các bài toán phức tạp hơn, chẳng hạn tính trung bình (average), trung vị (median), hay các bài toán machine learning như k-means, gradient descent, kiến trúc MapReduce sẽ gặp 2 vấn đề chính như sau:
- Trải nghiệm của developer tồi tệ: với mỗi vấn đề phía trên, developer phải vắt óc ra một bộ hàm `map` và `reduce` mới:
	- Ví dụ với Average giá sách toàn kho: 
		- map: cần trả về `[mã_kệ, (giá_TB, số_sách_trên_kệ)]`
		- reduce: tính trung bình có trọng số của `giá_TB` & `số_sách_trên_kệ`
	- Các bộ `map` và `reduce` này sẽ càng trở nên phức tạp khi bài toán phức tạp hơn -> trải nghiệm viết code và maintain tồi tệ.
- Xử lý bài toán có tính lặp: hầu hết các bài toán của machine learning đều có tính lặp, tức là thực hiện 1 phép tính nhiều lần, output của vòng lặp trước sẽ là input của vòng sau và lặp lại cho tới khi đạt một điều kiện dừng nhất định.
	- MapReduce được thiết kế để sau mỗi vòng lặp tính toán, kết quả được ghi xuống ổ đĩa cứng rồi đọc lại ở vòng tiếp theo. Điều này dẫn tới hàng trăm lần đọc/ghi xuống ổ đĩa cứng khi giải bài toán có tính lặp, và đây là nút cổ chai chí mạng khiến MapReduce hụt hơi trước những bài toán hiện đại hơn.

Nhìn ra được các điểm yếu của MapReduce ở đây, ta sẽ có cơ sở để hiểu cách mà các hệ thống sau này giải quyết những vấn đề này trong các phần tiếp theo của bài viết.
## Con voi vàng Hadoop, một bản viết lại dân chủ hóa

[![YouTube video ebgXN7VaIZA](https://img.youtube.com/vi/ebgXN7VaIZA/hqdefault.jpg)](https://www.youtube.com/watch?v=ebgXN7VaIZA)

### 1. Hành trình từ Nutch đến Yahoo

Năm 2004, trong một góc của San Francisco có một lập trình viên khoảng đầu 40, cao gầy, khỏe khoắn, tóc hơi vàng, đôi mắt xanh và nụ cười thường trực nở trên môi mang tên Doug Cutting. Đồng sự của anh là Mike Cafarella, 30 tuổi, một nghiên cứu sinh trẻ đang theo học Thạc sĩ Khoa học Máy tính tại Đại học Washington. Hai người đang cùng nhau xây dựng Nutch, một công cụ tìm kiếm mã nguồn mở với mục tiêu đầy tham vọng là lập chỉ mục hàng tỷ trang web. Tuy nhiên, họ nhanh chóng va phải "bức tường" về khả năng mở rộng khi kiến trúc cũ không thể xử lý khối lượng dữ liệu khổng lồ này trên một vài máy tính đơn lẻ.

Cùng thời điểm này, cặp đôi Jeff & Sanjay tại Google cũng đã làm việc với nhau được vài năm và cho ra 2 paper mang tính đột phá mà ta đã cùng lướt qua ở phần trên:
- **Google File System (GFS - 2003):** Giải pháp lưu trữ phân tán.
- **MapReduce (2004):** Mô hình tính toán song song.

Như buồn ngủ gặp chiếu manh, Cutting và Cafarella đã tự mình tái tạo các hệ thống này trong dự án Nutch dưới dạng **NDFS** (Nutch Distributed File System) và một bộ thực thi MapReduce sơ khai. Khi Jeff và Sanjay viết ra MapReduce tại Google, họ share phần ý tưởng với cả thế giới, giữ lại phần code cho riêng Google sử dụng. Doug và Mike lấy cảm hứng từ ý tưởng này để viết lại một bản mã nguồn mở và chia sẻ cho cả cộng đồng cùng xài chung.

Đến tháng 1 năm 2006, Doug Cutting gia nhập Yahoo!, một công ty đang khao khát giải pháp cho các vấn đề dữ liệu tìm kiếm của chính mình. Một tháng sau, Hadoop chính thức được tách ra khỏi Nutch để trở thành một dự án độc lập, với cái tên được đặt theo *con voi đồ chơi của con trai Doug* [(accorsi.net/docs/hadoop.pdf - page 10)](https://accorsi.net/docs/hadoop.pdf). 

*(Doug Cutting cùng con voi đồ chơi & Mike Cafarella)*
![Pasted image 20260528172841](../assets/media/Pasted%20image%2020260528172841.png)

### 2. Sự phát triển tại Yahoo! và chiến thắng trước Google

<div class="obs-callout obs-callout-note" markdown="1">
<div class="obs-callout-title">Note</div>

Tham khảo: 
- [Official Google Blog: Sorting 1PB with MapReduce](https://googleblog.blogspot.com/2008/11/sorting-1pb-with-mapreduce.html)
- [Winning a 60 Second Dash with a Yellow Elephant - 2009](https://sortbenchmark.org/Yahoo2009.pdf)
- [TeraByte Sort on Apache Hadoop - 2008](https://sortbenchmark.org/YahooHadoop.pdf)

Có thể thấy là cả 2 papers của Yahoo đều cite Google GFS & MapReduce

> Apache Hadoop is a open source software framework that dramatically simplifies writing distributed data intensive applications. It provides a distributed file system, which is modelled after the Google File System[2], and a map/reduce[1] implementation that manages distributed computation. Since the primary primitive of map/reduce is a distributed sort, most of the custom code is glue to get the desired behavior.
</div>

Yahoo! đóng vai trò là vườn ươm khổng lồ, cung cấp nguồn lực mà không một cá nhân nào có được: hàng trăm kỹ sư (dẫn đầu bởi **Owen O'Malley** và **Arun Murthy**) và các cụm máy chủ lên tới hàng ngàn nút.

Để chứng minh sức mạnh của Hadoop, Yahoo! đã tham gia các cuộc thi sắp xếp dữ liệu (sort benchmark) thế giới và liên tục lập kỷ lục:
#### Sort 1TB (~1000GB)


- **Năm 2008:**
	- Hadoop trở thành hệ thống nhanh nhất sắp xếp 1 TB dữ liệu (209s trên 910 nút), đánh bại các siêu máy tính đắt tiền.
	- Cuối năm đó Google tập trung vào tuning và cho ra kỷ lục sort 1 TB trong 68s với 1000 nút.
- **Tháng 4 năm 2009:**
	- Đội ngũ Yahoo! đã sử dụng Hadoop để sắp xếp **1 TB chỉ trong 62 giây**, chính thức vượt qua kỷ lục 68 giây do Google thiết lập vào tháng 11 năm trước đó.
#### Sort 1PB (~1 triệu GB)

- **Google (Tháng 11/2008):** Sort 1PB trong 6 tiếng 2 phút / 48.000 nút $\rightarrow$ Tốc độ đạt **2.76 TB/phút**.
- **Yahoo (Tháng 5/2009):** Sort 1PB trong 16 tiếng 15 phút / 3658 nút $\rightarrow$ Tốc độ đạt **1.03 TB/phút**.

Nếu chỉ nhìn tốc độ thuần, Google thắng. Nhưng Yahoo lại giật giải **GraySort chính thức của năm 2009** vì đơn giản Google chỉ viết blog khoe chứ không nộp bài. Kết quả của Google được team nhà tự setup và tự đo kết quả. Trong khi đó Yahoo đem toàn bộ tài liệu kỹ thuật, minh bạch hóa cấu hình trước ban giám khảo của Sort Benchmark 2009. Thêm nữa, hãy nhớ Google đã sử dụng một bộ phần cứng khủng hơn hẳn so với Yahoo cho các vụ sort 1PB đó, chỉ xét riêng về số lượng nút.

> Xem thêm: [Sort Benchmark Home Page](https://sortbenchmark.org/)

## Kết

MapReduce và Hadoop đã hoàn thành xuất sắc sứ mệnh lịch sử của mình: dân chủ hóa năng lực xử lý dữ liệu phân tán ở quy mô lớn, biến những cụm máy phổ thông thành một cỗ máy tính toán khổng lồ mà doanh nghiệp và cộng đồng đều có thể tiếp cận. Nhưng cũng chính vì được thiết kế cho bối cảnh kỹ thuật đầu những năm 2000, chúng mang theo những giới hạn cố hữu về mô hình lập trình và hiệu năng, đặc biệt ở các bài toán lặp và phân tích tương tác hiện đại. Khi nhu cầu dữ liệu tiếp tục phình to và đòi hỏi tốc độ phản hồi cao hơn, những tay chơi mới tất yếu sẽ xuất hiện. Trong bài tiếp theo, chúng ta sẽ nghiên cứu một đại diện tiêu biểu của data platform hiện đại: **Apache Spark**.

