"use client";
import {useEffect, useState} from "react";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
export default function Home(){
 const [health,setHealth]=useState(null), [sig,setSig]=useState(null), [err,setErr]=useState("");
 const [symbol,setSymbol]=useState("BTCUSDT"), [interval,setInterval]=useState("15m");
 async function refresh(){
  try{
   const [h,s]=await Promise.all([fetch(API+"/health"),fetch(`${API}/api/signals?symbol=${symbol}&interval=${interval}`)]);
   if(!h.ok||!s.ok) throw new Error("تعذر جلب البيانات");
   setHealth(await h.json()); setSig(await s.json()); setErr("");
  }catch(e){setErr(e.message+" — تحقق من تشغيل الخادم والاتصال بالإنترنت.");}
 }
 useEffect(()=>{refresh(); const t=setInterval(refresh,30000); return ()=>clearInterval(t)},[]);
 return <main>
  <header><div><small>AI POWERED MARKET ANALYTICS</small><h1>AI SMART TRADING PLATFORM</h1><p>منصة تحليل السوق وإدارة المخاطر</p></div><span className="pill">● وضع تجريبي DEMO</span></header>
  <section className="warning">هذه النسخة للتحليل والمحاكاة فقط. لا تنفّذ صفقات حقيقية ولا تضمن الأرباح.</section>
  <section className="grid">
   <article><label>حالة النظام</label><h2>{health?.status==="ok"?"متصل":"غير متصل"}</h2><p>تنفيذ التداول الحقيقي: معطّل</p></article>
   <article><label>الأصل المالي</label><select value={symbol} onChange={e=>setSymbol(e.target.value)}><option>BTCUSDT</option><option>ETHUSDT</option><option>BNBUSDT</option><option>SOLUSDT</option></select><p>بيانات Binance العامة</p></article>
   <article><label>الإطار الزمني</label><select value={interval} onChange={e=>setInterval(e.target.value)}>{["1m","5m","15m","1h","4h","1d"].map(x=><option key={x}>{x}</option>)}</select><p>تحديث كل 30 ثانية</p></article>
  </section>
  <section className="panel"><div className="row"><h2>إشارة الذكاء الاصطناعي</h2><button onClick={refresh}>تحديث التحليل</button></div>
   {err&&<p className="error">{err}</p>}
   {!sig&&!err&&<p>جارٍ تحميل البيانات...</p>}
   {sig&&<><div className="signal"><strong>{sig.action}</strong><span>درجة التوافق: {sig.confidence}/100</span></div>
    <div className="grid metrics"><div><label>سعر الدخول المرجعي</label><b>{sig.entry??"—"}</b></div><div><label>وقف الخسارة النظري</label><b>{sig.stop_loss??"—"}</b></div><div><label>هدف الربح النظري</label><b>{sig.take_profit??"—"}</b></div></div>
    <p>{sig.reason}</p><p className="muted">المؤشرات: {sig.indicators?`RSI ${sig.indicators.rsi} · EMA20 ${Number(sig.indicators.ema20).toFixed(2)} · EMA50 ${Number(sig.indicators.ema50).toFixed(2)}`:"بيانات غير كافية"}</p>
   </>}
  </section>
  <section className="panel"><h2>حواجز الأمان</h2><ul><li>الوضع الافتراضي DEMO.</li><li>لا توجد صلاحية تداول أو سحب متصلة.</li><li>لا يتم إرسال أوامر إلى Binance.</li><li>لا تستخدم الإشارة وحدها لاتخاذ قرار مالي.</li></ul></section>
  <footer>الإصدار 0.1.0 · بيانات السوق من Binance Public API · للاختبار والتطوير</footer>
 </main>
}
