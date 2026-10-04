# إضافات المشروع النهائي

هذه الإضافات تعمل فوق مشروع الـMidterm الحالي، وتستخدم `orders_validated` كمصدر موثوق. لا تعيد بناء Raw Load ولا تنشئ مسار إدخال ثانيًا.

## 1. التثبيت

```powershell
python -m pip install -r requirements-final.txt
$env:PYTHONPATH = "$PWD\src"
```

شغّل MongoDB أولًا على `127.0.0.1:27017`.

## 2. فحص Schema قبل أول تشغيل

يجب التأكد أن بنية `orders_validated` هي البنية التي تستخدمها الإضافات:

```text
customer.address.city
customer.customer_id
items[].sku
items[].name
items[].qty
items[].total
order_date
status
```

قواعد المشروع الحالية تنشئ هذه البنية في `quality_rules.py`.

## 3. إنشاء الفهارس

```powershell
python -m final.cli indexes
```

ينشئ:

- Unique Index على `order_id`.
- Compound Index على `customer.address.city + order_date`.
- Compound Index على `customer.customer_id + order_date`.
- Compound Index على `orders_quarantine.run_id + error_codes`.
- Unique Index على `mv_processed_events.event_id`.

تُختار قيم المدينة والعميل ورقم الطلب المستخدمة في Explain من وثائق مجموعة التقييم نفسها، ولا تعتمد على قيم ثابتة من بيانات التدريب.

## 4. تشغيل التقارير الخمسة

```powershell
python -m final.cli report sales_by_city
python -m final.cli report top_products
python -m final.cli report sales_by_period
python -m final.cli report top_customers
python -m final.cli report orders_by_status
```

كل نتيجة تعرض اسم التقرير وعدد الصفوف والزمن والبيانات الفعلية.

## 5. بناء Materialized Views أول مرة

```powershell
python -m final.cli refresh-full
```

يُنشئ:

- `mv_sales_by_city`
- `mv_top_products`

## 6. التحديث التزايدي

يستخدم التحديث التزايدي `mv_updated_at` أو `processed_at` لتحديد التغييرات الأحدث من الـ Watermark. مسار منتصف الفصل ينتج `processed_at` تلقائيًا:

```text
processed_at: UTC datetime
```

ثم شغّل:

```powershell
python -m final.cli refresh-incremental
```

يستخدم النظام `mv_state` لحفظ لقطة آخر نسخة معالجة من كل طلب والـ Watermark، ثم يطرح أثر النسخة السابقة ويضيف أثر النسخة الحالية عند تعديل الطلب.

## 7. API

```powershell
python -m uvicorn final.api:app --app-dir src --host 127.0.0.1 --port 8000
```

افتح:

```text
http://127.0.0.1:8000/docs
```

المسارات:

```text
GET  /health
POST /ingest
POST /indexes
GET  /queries
GET  /queries/{name}
GET  /aggregations
GET  /aggregations/{name}
POST /refresh-mv?mode=full
POST /refresh-mv?mode=incremental
GET  /jobs
POST /jobs/{name}/run
```

`POST /ingest` يستقبل مسار ملف CSV محلياً على جهاز تشغيل الـ API، ثم يشغّل مشغل منتصف الفصل `../src/main.py --step all` باستخدام إعدادات MongoDB نفسها. لا ينشئ مسار إدخال بديلًا. يمكن تغيير مسار `main.py` عبر `MIDTERM_MAIN_SCRIPT` في `.env`.

## 8. المهام اليدوية

```powershell
curl -X POST http://127.0.0.1:8000/jobs/incremental/run
curl -X POST http://127.0.0.1:8000/jobs/full_refresh/run
```

كل تشغيل يُسجل في `job_runs` مع وقت البداية والنهاية والحالة والنتيجة أو الخطأ.

## 9. جدولة Windows Task Scheduler

أنشئ مهمتين تستدعيان PowerShell:

```powershell
python -m final.cli refresh-incremental
```

و:

```powershell
python -m final.cli report sales_by_city
```

يجب الاحتفاظ بسجل `job_runs` وإظهار آخر تشغيل يدويًا أثناء المناقشة.

## 10. شرح التصميم للدكتور

- `orders_validated` هو مصدر التحليل، وليس `orders_raw`.
- الـMaterialized View نتيجة محسوبة مسبقًا وليست نسخة خام.
- Full Refresh يستخدم عند الإنشاء الأول أو الإصلاح.
- Incremental Refresh يعالج الوثائق الجديدة أو المعدلة فقط.
- Contribution Model يحول الطلب إلى أثر على مجموع المدينة أو المنتج.
- Update للطلب يعني طرح الأثر القديم ثم إضافة الأثر الجديد.
- لقطة الوثيقة السابقة في `mv_state` تمنع إعادة تطبيق الأثر على الوثائق الأقدم.
- `watermark` يمنع إعادة قراءة التغييرات التي سبقت آخر تحديث ناجح.
- `job_runs` يثبت نجاح أو فشل المهمة.
