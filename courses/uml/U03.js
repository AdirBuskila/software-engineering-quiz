/* UML course · level 3 - class diagram: multiplicity and its code, which relations exist, which classes a system gets */
SE_LEVEL("uml", {
  id: "U03", order: 3, icon: "🔢", title: "תרשים מחלקות: ריבוי, קשרים ובחירת מחלקות",
  goal: "לתרגם ריבוי (1..*, 1..10) למבנה בקוד, לדעת אילו קשרים קיימים בתרשים מחלקות, ולבחור מחלקות מתיאור מערכת.",
  lesson: { html: `
<p><strong>ריבוי (multiplicity)</strong> כתוב ליד קצה הקשר ואומר כמה אובייקטים משתתפים בו: <code>1</code>, <code>0..1</code>, <code>1..*</code>, <code>1..10</code>. בקשר הכלה הריבוי קובע <b>איך המחלקה השלמה מחזיקה את החלקים</b> בקוד: כל החלקים <b>מוכלים במבנה נתונים בתוך המחלקה השלמה</b>, ולרוב מבנה דינמי כשאין חסם עליון (21S-B-Q1).</p>
<table>
<thead><tr><th>הריבוי</th><th>המבנה בקוד</th><th>למה</th></tr></thead>
<tbody>
<tr><td><code>1..*</code> או <code>*</code></td><td><b>רשימה</b> (List)</td><td>אין חסם עליון, הגודל משתנה (25S-A-Q16)</td></tr>
<tr><td><code>1..10</code>, <code>2..4</code></td><td><b>מערך</b> (array)</td><td>יש חסם עליון קבוע (25F0b-Q15)</td></tr>
<tr><td><code>1</code> או <code>0..1</code></td><td>שדה בודד</td><td>לכל היותר אחד</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>חסם עליון קבוע ← מערך. כוכבית ← רשימה.</strong> לא קובץ ולא מחרוזת, ו"לא ניתן לדעת" אינו התשובה: הריבוי נקבע בתרשים והוא קובע את המבנה.</div>
<h3>אילו קשרים קיימים בתרשים מחלקות</h3>
<p>ירושה, association, aggregation ו-composition. המילים <b>Include</b> ו-<b>Extend</b> שייכות ל-<b>Use Case</b>, ואין בתרשים מחלקות "Exclude" (25B-N-Q16).</p>
<h3>אילו מחלקות יש במערכת</h3>
<p>מתוך תיאור מערכת בוחרים <b>ישויות נתונים</b> (משתמש, קריאה, הזמנה) ו<b>רכיבי שירות או לוגיקה</b> (מחלקת ולידציה, מחלקה שמתחברת לשירות ענן, מחלקה ששומרת ל-DB). מסך, כפתור, מדפסת ומסד הנתונים עצמו הם לא מחלקות של לוגיקת המערכת (24S-A-Q12, 25F0a-Q11, 26B-A-Q12).</p>
<div class="lesson-ex">דוגמה: חנות שבה לקוחות מזמינים מוצרים, שרת מטפל בהזמנות ומשתמש בשירות תשלום חיצוני. מחלקות סבירות: <code>Customer</code>, <code>Order</code>, <code>OrderService</code>, <code>PaymentService</code>. "כפתור" ו"מסך" הם חלק מה-View, לא ממחלקות הלוגיקה.</div>
<div class="lesson-trap">⚠️ <strong>"הכלה" אינה "ירושה".</strong> ריבוי קיים על קשרי הכלה (aggregation ו-composition) וגם על association, ואין לו שום קשר לחץ ההורשה.</div>
` },
  questions: [
    { ref: "25S-A-Q16", recap: "ריבוי 1..* ממומש ברשימה" },
    { id: "U03-Q1", question: "בתרשים מחלקות, קשר הכלה בין Course ל-Lab מסומן בריבוי 2..4 ליד Lab. באיזה מבנה Course תחזיק את אובייקטי ה-Lab?",
      options: ["מערך בגודל חסום", "קובץ", "מחרוזת אחת", "אי אפשר לדעת, הריבוי אינו משפיע"], answer: 0,
      recap: "חסם עליון קבוע ← מערך",
      explanation: "הריבוי `2..4` נותן **חסם עליון קבוע** (4), ולכן מערך מתאים. כוכבית הייתה מובילה לרשימה. קובץ ומחרוזת אינם מבנה להחזקת אובייקטים, והריבוי כן קובע את מבנה האחסון." },
    { id: "U03-Q2", question: "איזו רשימה מכילה רק קשרים שקיימים בתרשים מחלקות?",
      options: ["ירושה, association, aggregation, composition", "Include, Extend, ירושה, association", "Exclude, Include, composition, aggregation", "Extend, Exclude, association, ירושה"], answer: 0,
      recap: "Include / Extend שייכים ל-Use Case, ואין Exclude",
      explanation: "בתרשים מחלקות יש **ירושה, association, aggregation ו-composition**. Include ו-Extend הם קשרים בין Use Cases, ואין בכלל קשר בשם Exclude. כל אחת משלוש הרשימות האחרות מכילה לפחות אחד מהם." },
    { id: "U03-Q3", question: "מערכת: לקוחות מזמינים מוצרים דרך האתר. שרת מקבל הזמנות, שומר אותן ומתחבר לשירות תשלום חיצוני. איזו קבוצה היא הבחירה הסבירה ביותר של מחלקות בתרשים המחלקות של השרת?",
      options: ["Customer, Order, OrderService, PaymentService", "Customer, Button, Screen, Printer", "Browser, Mouse, Keyboard, Order", "Database, Window, Menu, Customer"], answer: 0,
      recap: "מחלקות = ישויות נתונים + רכיבי שירות, לא מסכים או חומרה",
      explanation: "התרשים של השרת מכיל **ישויות** (`Customer`, `Order`) ו**רכיבי שירות** (`OrderService`, `PaymentService`). כפתור, מסך, מדפסת, עכבר, מקלדת וחלון הם חומרה או UI, ו-Database הוא מסד הנתונים עצמו ולא מחלקת לוגיקה." },
    { ref: "25F0b-Q15", recap: "ריבוי 1..10 ממומש במערך" },
  ],
});
