# دليل بناء لوحة تحكم Power BI احترافية (Superstore Business Intelligence)

يُوثق هذا الدليل طريقة تصميم ونمذجة البيانات وكتابة صيغ DAX لبناء لوحة تحكم تفاعلية للمشروع. يهدف هذا الملف إلى إظهار مهاراتك في **ذكاء الأعمال (BI)** ونمذجة البيانات أمام مسؤولي التوظيف.

---

## 1. نمذجة البيانات (Data Modeling - Star Schema)
لأفضل أداء في Power BI، يفضل تقسيم الجدول المفرد إلى **نموذج النجمة (Star Schema)**، والذي يتكون من جدول حقائق (Fact Table) وجداول أبعاد (Dimension Tables):

- **جدول الحقائق: `Fact_Orders`**
  - يحتوي على المقاييس الرقمية والمفاتيح: `Row_ID`, `Order_ID`, `Order_Date_Key`, `Customer_ID`, `Product_ID`, `Postal_Code`, `Sales`, `Quantity`, `Discount`, `Profit`.
  
- **جداول الأبعاد (Dimensions):**
  - **`Dim_Customers`**: يحتوي على `Customer_ID`, `Customer_Name`, `Segment`.
  - **`Dim_Products`**: يحتوي على `Product_ID`, `Product_Name`, `Category`, `Sub-Category`.
  - **`Dim_Geography`**: يحتوي على `Postal_Code`, `City`, `State`, `Country`, `Region`.
  - **`Dim_Calendar`**: جدول التواريخ (مهم جداً لتحليلات الوقت Time Intelligence): يحتوي على `Date`, `Year`, `Quarter`, `Month`, `Month_Name`, `Week_Number`.

### العلاقات (Relationships):
- `Fact_Orders [Customer_ID]  -->  Dim_Customers [Customer_ID]` (Many-to-One `* : 1`)
- `Fact_Orders [Product_ID]   -->  Dim_Products [Product_ID]` (Many-to-One `* : 1`)
- `Fact_Orders [Postal_Code]  -->  Dim_Geography [Postal_Code]` (Many-to-One `* : 1`)
- `Fact_Orders [Order_Date]   -->  Dim_Calendar [Date]` (Many-to-One `* : 1`)

---

## 2. صيغ ومقاييس DAX المتقدمة (Key Measures)

قم بإنشاء جدول مقاييس منفصل في Power BI باسم `_Measures` واكتب الصيغ التالية:

### المقاييس الأساسية (Core Metrics):
- **إجمالي المبيعات (Total Sales):**
  ```dax
  Total Sales = SUM(Fact_Orders[Sales])
  ```
- **إجمالي الأرباح (Total Profit):**
  ```dax
  Total Profit = SUM(Fact_Orders[Profit])
  ```
- **هامش الربح (Profit Margin %):**
  ```dax
  Profit Margin = DIVIDE([Total Profit], [Total Sales], 0)
  ```
- **عدد الطلبات الفريدة (Total Orders):**
  ```dax
  Total Orders = DISTINCTCOUNT(Fact_Orders[Order_ID])
  ```
- **متوسط نسبة الخصم (Average Discount):**
  ```dax
  Average Discount = AVERAGE(Fact_Orders[Discount])
  ```

### تحليلات الوقت التراكمية (Time Intelligence):
- **المبيعات منذ بداية السنة المالية (YTD Sales):**
  ```dax
  YTD Sales = TOTALYTD([Total Sales], 'Dim_Calendar'[Date])
  ```
- **الأرباح منذ بداية السنة المالية (YTD Profit):**
  ```dax
  YTD Profit = TOTALYTD([Total Profit], 'Dim_Calendar'[Date])
  ```
- **مبيعات العام الماضي نفس الفترة (Prior Year Sales - PY Sales):**
  ```dax
  PY Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Dim_Calendar'[Date]))
  ```
- **معدل نمو المبيعات السنوي (YoY Sales Growth %):**
  ```dax
  YoY Sales Growth = DIVIDE([Total Sales] - [PY Sales], [PY Sales], 0)
  ```

---

## 3. التصميم البصري للداشبورد (Visual Layout & UX)

للحصول على تصميم **Premium** ومبهر، اتبع هذه التوجيهات في Power BI Desktop:

### لوحة الألوان المقترحة (Sleek Dark / Light Theme):
- **الخلفية الأساسية**: رمادي فاتح جداً `#F8FAFC` أو كحلي داكن `#0F172A` (للـ Dark Mode).
- **لون المبيعات الرئيسي**: الأزرق `#2563EB` أو `#3B82F6`.
- **لون الأرباح (إيجابي)**: الأخضر الزمردي `#10B981`.
- **لون الخسائر (سلبي)**: الأحمر المرجاني `#EF4444`.

### توزيع العناصر في الصفحة (Dashboard Layout):
1. **القسم العلوي (Header & KPIs)**:
   - ضع بطاقات المؤشرات (Multi-row Card or Single Cards) في الأعلى لعرض: `Total Sales` و `Total Profit` و `Profit Margin` و `Total Orders`.
   - أضف مقسمات التاريخ (Slicers) مثل `Year` و `Region` في الجانب العلوي الأيسر لتسهيل الفلترة.
2. **القسم الأوسط (Trends & Geography)**:
   - **رسم بياني خطي (Line Chart)**: يعرض `Total Sales` و `Total Profit` على المحور الصادي (Y-axis) و `Month-Year` على المحور السيني (X-axis) لمراقبة الأداء الشهري.
   - **خريطة تفاعلية (Filled Map / Bubble Map)**: تعرض حجم المبيعات والأرباح حسب الولايات أو المدن.
3. **القسم السفلي (Categories & Products)**:
   - **رسم بياني شريطي متراكم (Stacked Bar Chart)**: يوضح المبيعات والأرباح لكل فئة (`Category`) وفئة فرعية (`Sub-Category`).
   - **جدول التفاصيل (Top Products Matrix)**: مصفوفة تعرض المنتجات الأكثر ربحية باستخدام شرط التنسيق الشرطي (Conditional Formatting) لتظليل المنتجات الخاسرة بالأحمر.

---

## 4. كيفية استيراد البيانات النظيفة في Power BI
1. افتح **Power BI Desktop**.
2. اضغط على **Get Data** ثم اختر **Text/CSV**.
3. حدد الملف النظيف الذي تم إنشاؤه بواسطة كود البايثون:
   `data/processed/superstore_clean.csv`
4. اضغط على **Transform Data** لفتح محرر Power Query والتأكد من تحديد أنواع البيانات تلقائياً بشكل صحيح (التواريخ كـ Date، والأرقام كـ Decimal Number).
5. اضغط على **Close & Apply** وابدأ في تصميم لوحة التحكم وفقاً لهذا الدليل!
