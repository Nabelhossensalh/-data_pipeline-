# مشروع البيانات الضخمة (Big Data - Phase 2)
## إضافات المشروع النهائي - دليل التشغيل والتقييم الشامل

يعمل هذا المشروع كإضافة مستقلة (Standalone Extension) معتمدة على قاعدة بيانات MongoDB `ecommerce_store` ومجموعة `orders_validated` كمصدر موثوق للبيانات المعالجة، دون إعادة بناء الـ Raw Load ودون تكرار مسار الإدخال.

---

## 📋 المحتويات
1. [التثبيت والإعداد السريع](#1-التثبيت-والإعداد-السريع)
2. [واجهة API الموحدة (FastAPI) والـ Swagger](#2-واجهة-api-الموحدة-fastapi-والـ-swagger)
3. [الاستعلامات والفهارس (Queries & Indexes)](#3-الاستعلامات-والفهارس-queries--indexes)
4. [تحليل explain("executionStats") قبل وبعد الفهارس](#4-تحليل-explainexecutionstats-قبل-وبعد-الفهارس)
5. [تقارير التجميعات الخمسة (Aggregation Reports)](#5-تقارير-التجميعات-الخمسة-aggregation-reports)
6. [العروض المادية والتحديث التزايدي (Materialized Views)](#6-العروض-المادية-والتحديث-التزايدي-materialized-views)
7. [المهام المجدولة واليدوية (Scheduled & Manual Jobs)](#7-المهام-المجدولة-واليدوية-scheduled--manual-jobs)
8. [أوامر واجهة السطر البرمجي (CLI)](#8-أوامر-واجهة-السطر-البرمجي-cli)
9. [ملاحظات معمارية للمناقشة](#9-ملاحظات-معمارية-للمناقشة)

---

## 1. التثبيت والإعداد السريع

### المتطلبات
- **Python**: 3.10 أو أحدث.
- **MongoDB**: يعمل محلياً على `127.0.0.1:27017`.
- هذا المجلد موجود داخل مستودع المشروع النصفي، ويستخدم `../src/main.py` كمدخل للـ Pipeline.

### خطوات التثبيت
```powershell
# 1. الانتقال إلى مجلد المشروع
cd final_extension

# 2. تثبيت الحزم المطلوبة
python -m pip install -r requirements.txt

# 3. إعداد متغير البيئة لمسار الأكواد
$env:PYTHONPATH = "$PWD\src"

# 4. إعداد ملف البيئة (اختياري، القيم الافتراضية تعمل مباشرة)
Copy-Item .env.example .env
```

---

## 2. واجهة API الموحدة (FastAPI) والـ Swagger

لتشغيل السيرفر الموحد للاختبار والتقييم:

```powershell
python -m uvicorn final.api:app --app-dir src --host 127.0.0.1 --port 8000
```
أو عبر سكريبت التشغيل السريع:
```powershell
.\run_final_api.ps1
```

- **رابط التوثيق التفاعلي (Swagger UI):** `http://127.0.0.1:8000/docs`
- **رابط التوثيق البديل (ReDoc):** `http://127.0.0.1:8000/redoc`

يتطلب `POST /ingest` مسار ملف محلياً يقبله مشغل منتصف الفصل على جهاز تشغيل الـ API، ويشغّل
`../src/main.py --step all` باستخدام إعدادات MongoDB نفسها:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/ingest `
   -ContentType 'application/json' `
   -Body '{"source_file":"C:\\data\\orders.csv"}'
```

### جدول المسارات المطلوبة (End-Points):

| المسار (Method + Path) | الوصف | طريقة الاستجابة |
|---|---|---|
| `GET /health` | فحص اتصال قاعدة البيانات وحالة النظام | JSON يوضح حالة الاتصال وحالة المجدول |
| `POST /ingest` | تشغيل بوابة منتصف الفصل على ملف CSV محلي | نتيجة مراحل Pipeline الفعلية أو خطأ التشغيل |
| `POST /indexes` | بناء الفهارس المطلوبة في MongoDB | JSON بأسماء الفهارس المنشأة |
| `GET /queries` | قائمة الاستعلامات العملية الخمسة | أسماء وتفاصيل الاستعلامات المتاحة |
| `GET /queries/{name}` | تنفيذ استعلام عملي محدد بالاسم مع حد اختياري `limit` | نتائج الاستعلام من البيانات الفعلية |
| `GET /aggregations` | قائمة تقارير التجميعات الخمسة | أسماء وشرح التقارير التجميعية |
| `GET /aggregations/{name}` | تشغيل تقرير تجميعي محدد واسترجاع البيانات الفعلية | مخرجات التقرير، عدد الصفوف والزمن المستغرق |
| `POST /refresh-mv?mode=full` أو `incremental` | تحديث العروض المادية (كلي أو تزايدي) | تفاصيل التحديث وعدد الوثائق والـ Watermark |
| `GET /jobs` | عرض سجل تشغيل المهام وحالة الجدولة | آخر 50 تشغيل مسجل في `job_runs` |
| `POST /jobs/{name}/run` | تشغيل مهمة يدوياً (`incremental`, `full_refresh`, `reports`) | تسجيل النتيجة الفورية وحالتها في `job_runs` |
| `GET /explain` | تنفيذ فحص Explain لـ 3 استعلامات قبل وبعد الفهارس | أرقام `executionStats` والمقارنة العلمية |

---

## 3. الاستعلامات والفهارس (Queries & Indexes)

### الفهارس المنشأة في MongoDB:
1. **Unique Index:** على حقل `order_id` (يمنع تكرار الطلب ويسرّع البحث الفردي).
2. **Compound Index 1:** على `("customer.address.city", 1) + ("order_date", -1)` (يخدم استعلامات الطلبات الجغرافية والفرز الزمني).
3. **Compound Index 2:** على `("customer.customer_id", 1) + ("order_date", -1)` (يخدم استعلامات سجل طلبات العميل).
4. **Compound Index 3:** على `("run_id", 1) + ("error_codes", 1)` في `orders_quarantine` لمتابعة جودة التشغيلات.
5. **Unique Index:** على `mv_processed_events.event_id` لضمان مبدأ عدم التكرار (Idempotency).

### الاستعلامات العملية الخمسة:
- `orders_by_city`: توزيع الطلبات حسب المدينة.
- `quarantine_by_error`: توزيع أخطاء العزل حسب كود الخطأ.
- `corrected_orders`: الطلبات التي طُبقت عليها قواعد تصحيح جودة البيانات.
- `customer_orders`: عدد طلبات كل عميل مرتبة تنازلياً.
- `recent_orders`: أحدث الطلبات المعالجة في النظام زمنياً.

---

## 4. تحليل explain("executionStats") قبل وبعد الفهارس

تم فحص 3 استعلامات حيوية قبل إنشاء الفهارس (مسح شامل `COLLSCAN`) وبعد إنشاء الفهارس (`IXSCAN`):

| الاستعلام | الفهرس المطبق | سبب اختيار الفهرس | الأثر الفعلي (Before vs After) |
|---|---|---|---|
| **1. استعلام المدينة والتاريخ**<br>`customer.address.city + order_date` | Compound Index:<br>`ix_city_order_date` | استعلام أساسي في لوجستيات التوزيع لعرض أحدث الشحنات في مدينة مختارة من البيانات. | **قبل:** `COLLSCAN` مع الفرز المطلوب.<br>**بعد:** يستخدم الفهرس المركب عند اختيار الخطة له؛ أرقام الوثائق والمفاتيح والزمن تُقرأ من `executionStats` للبيانات الحالية. |
| **2. سجل طلبات العميل**<br>`customer.customer_id + order_date` | Compound Index:<br>`ix_customer_order_date` | عرض سجل مشتريات عميل موجود في المجموعة مرتباً زمنياً. | **قبل:** `COLLSCAN` للبحث عن العميل.<br>**بعد:** يستفيد من بادئة العميل ثم ترتيب التاريخ، وتختلف الأرقام حسب مجموعة التقييم. |
| **3. البحث المباشر بالطلب**<br>`order_id` | Unique Index:<br>`ux_order_id` | تتبع طلب موجود باستخدام المعرف الفريد. | **قبل:** `COLLSCAN`.<br>**بعد:** بحث باستخدام الفهرس الفريد؛ تُعرض إحصاءات التنفيذ الفعلية دون افتراض أعداد ثابتة. |

لتشغيل فحص الـ Explain مباشرة:
```powershell
python -m final.cli explain
```
أو عبر المتصفح: `http://127.0.0.1:8000/explain`

---

## 5. تقارير التجميعات الخمسة (Aggregation Reports)

التقارير الخمسة مبنية وفق متطلبات الوثيقة وتعمل بصورة مستقلة:

1. **`sales_by_city`**: إجمالي المبيعات وعدد الطلبات لكل مدينة (مع ترتيب تنازلي).
2. **`top_products`**: أعلى المنتجات مبيعاً من حيث الإيرادات والكميات (مع استخدام `$unwind` وتحويل المبالغ).
3. **`sales_by_period`**: المبيعات الشهرية المجمعة عبر السنوات لتحليل النمو.
4. **`top_customers`**: أكثر 20 عميلاً إنفاقاً في المتجر لدعم برامج الولاء.
5. **`orders_by_status`**: توزيع الطلبات وإجمالي المبالغ حسب الحالة (تم التسليم، ملغي، بانتظار الدفع، ...).

التشغيل عبر السطر البرمجي:
```powershell
python -m final.cli report sales_by_city
python -m final.cli report top_products
python -m final.cli report sales_by_period
python -m final.cli report top_customers
python -m final.cli report orders_by_status
```

---

## 6. العروض المادية والتحديث التزايدي (Materialized Views)

تم بناء العروض المادية المطلوبة:
- **`daily_sales_summary`** (وكذلك `mv_sales_by_city`)
- **`top_products_summary`** (وكذلك `mv_top_products`)

### آلية التحديث التزايدي (Incremental Refresh):
1. **نقطة التوقف (Watermark):** يحفظ النظام آخر تاريخ تعديل ناجح `last_watermark` في مجموعة `mv_state`.
2. **قراءة الفروقات فقط (Delta Load):** يقرأ النظام الوثائق التي يكون `mv_updated_at` أو `processed_at` فيها أحدث من `last_watermark`. يستخدم `processed_at` الذي تنتجه بوابة منتصف الفصل.
3. **نموذج الأثر التفاضلي (Contribution Model):**
   - عند تعديل طلب: يتم طرح أثره القديم (Sign = -1) ثم إضافة أثره الجديد (Sign = +1).
   - عند إضافة طلب جديد: يتم إضافة أثره (Sign = +1).
   - عند إلغاء طلب: يتم إلغاء مساهمته من مجاميع المدينة والمنتج.
4. **منع إعادة الاحتساب:** تحفظ المجموعة `mv_state` لقطة آخر نسخة معالجة لكل طلب، ويُحدّث الـ Watermark بعد تطبيق التغييرات؛ لذلك لا يعاد احتساب الوثائق الأقدم في التشغيل التالي.

التشغيل:
```powershell
# بناء أولي كامل:
python -m final.cli refresh-full

# تحديث تزايدي ذكي:
python -m final.cli refresh-incremental
```

---

## 7. المهام المجدولة واليدوية (Scheduled & Manual Jobs)

يعتمد النظام على `BackgroundScheduler` يعمل تلقائياً عند إطلاق الـ API:

1. **المهمة الأولى (Incremental MV Refresh):** تعمل كل 5 دقائق لتحديث العروض المادية من الطلبات الجديدة.
2. **المهمة الثانية (Aggregation Reports Refresh):** تعمل كل 60 دقيقة لتوليد وتحديث التقارير التجميعية الدورية.

### التشغيل اليدوي للاختبار والمناقشة:
يمكن تشغيل أي مهمة يدوياً وتوثيق نتائجها فوراً في سجل `job_runs`:
```powershell
curl -X POST http://127.0.0.1:8000/jobs/incremental/run
curl -X POST http://127.0.0.1:8000/jobs/full_refresh/run
curl -X POST http://127.0.0.1:8000/jobs/reports/run
```
كل عملية تسجل: `job_name`, `started_at`, `finished_at`, `status` ("success" أو "failed") و تفاصيل `result` أو `error`.

---

## 8. أوامر واجهة السطر البرمجي (CLI)

```powershell
# إنشاء كافة الفهارس:
python -m final.cli indexes

# استعراض مقارنة Explain بالأرقام:
python -m final.cli explain

# تشغيل أي تقرير تجميعي:
python -m final.cli report sales_by_city
python -m final.cli report top_products
python -m final.cli report sales_by_period
python -m final.cli report top_customers
python -m final.cli report orders_by_status

# تحديث العروض المادية:
python -m final.cli refresh-full
python -m final.cli refresh-incremental
```

---

## 9. ملاحظات معمارية للمناقشة
- **استقلالية البيانات:** يعتمد التحليل النهائي على `orders_validated` كطبقة بيانات نقية خالية من أخطاء الـ Raw.
- **التوافق التلقائي للأنواع:** تم استخدام `$convert` في خطوط أنابيب MongoDB للتعامل الآمن مع الحقول النصية أو الرقمية لـ `total_amount` و `items`.
- **قابلية التوسع:** خطوط التجميع التزايدي تمنع الحاجة لمعالجة ملايين السجلات في كل مرة، وتكتفي بمعالجة السجلات الجديدة فقط في أجزاء من الثانية.
