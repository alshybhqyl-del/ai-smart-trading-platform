# AI SMART TRADING PLATFORM

نسخة أولية عملية قابلة للتشغيل محليًا عبر Docker Compose. الوضع الافتراضي Paper/Demo؛ لا تُرسل أوامر حقيقية إلى Binance.

## المكونات
- `backend/`: FastAPI، مؤشرات فنية، محرك إشارات، حواجز مخاطر، اتصال Binance للبيانات العامة.
- `frontend/`: واجهة Next.js بسيطة متجاوبة تعرض حالة النظام والإشارات.
- `docker-compose.yml`: PostgreSQL وRedis والواجهة والخلفية.
- `tests/`: اختبارات أساسية.

## تشغيل سريع
1. ثبّت Docker Desktop أو Docker Engine مع Compose.
2. انسخ `.env.example` إلى `.env`.
3. شغّل: `docker compose up --build`
4. افتح `http://localhost:3000` للواجهة و`http://localhost:8000/docs` لواجهة API.

## وضع التداول والأمان
- `TRADING_MODE=demo` هو الافتراضي.
- لا توجد أوامر تداول حقيقية في هذه النسخة؛ واجهة Binance الحالية للبيانات العامة فقط.
- لا تضع مفاتيح API في الواجهة أو ترسلها في المحادثات.
- عند إضافة مفاتيح مستقبلًا: استخدم مفتاحًا بلا صلاحية سحب، وقيّد IP، وخزّن السر في Secret Manager.
- لا تفعّل Futures أو التداول الآلي قبل اختبار مستقل، ومراجعة قانونية/تنظيمية مناسبة، واختبارات تكامل على Testnet.
- إشارات المؤشرات ليست توصية استثمارية ولا تضمن الربح.

## API
- `GET /health`
- `GET /api/market/klines?symbol=BTCUSDT&interval=15m&limit=200`
- `GET /api/signals?symbol=BTCUSDT&interval=15m`
- `POST /api/risk/position-size` مع `{ "equity": 1000, "risk_pct": 0.5, "entry": 60000, "stop": 58800 }`

## ما يلزم قبل النشر العام
إضافة تسجيل دخول ومصادقة ثنائية، تشفير أسرار بمفتاح KMS، migrations، مراقبة وتنبيهات، اختبارات أمنية، HTTPS وقيود شبكة، ثم ربط تداول Testnet ومراجعة التنفيذ. لا تعتبر هذه النسخة نظامًا إنتاجيًا أو روبوت تداول حقيقيًا.
