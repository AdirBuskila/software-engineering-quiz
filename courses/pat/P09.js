/* Design-patterns course · level 9 - boss: real exam questions on every pattern */
SE_LEVEL("pat", {
  id: "P09", order: 9, icon: "🏆", title: "מבחן גמר: תבניות עיצוב", boss: true,
  goal: "שש שאלות אמיתיות מהמבחנים על Singleton, Factory, Observer, Command ו-MVC.",
  lesson: { html: `
<p>זה מבחן הגמר של הקורס: שש שאלות אמיתיות מהמבחנים, ללא רמזים. לפני שמתחילים, הנה כל הקורס בטבלה אחת.</p>
<table>
<thead><tr><th>הצורך או המילה בתיאור</th><th>התבנית</th><th>הפרט שנבחן</th></tr></thead>
<tbody>
<tr><td>מופע אחד, משאב יחיד</td><td><b>Singleton</b></td><td>בנאי פרטי; מחלקה אחת בתרשים; מספר קבוע של מופעים נאכף ב-getInstance</td></tr>
<tr><td>סוג נקבע בזמן ריצה, בלי להכיר מחלקות קונקרטיות</td><td><b>Factory</b></td><td>המתודה מחזירה ממשק; הלקוח מנותק מהמחלקה הקונקרטית</td></tr>
<tr><td>משהו משתנה וכמה רכיבים מתעדכנים</td><td><b>Observer</b></td><td>Subject מחזיק Observers; הסינון ב-notify; Attach בכל Subject</td></tr>
<tr><td>כפתורים, תפריטים, שלט, מקליט, undo</td><td><b>Command</b></td><td>Invoker, Command, Receiver</td></tr>
<tr><td>הפרדה בין נתונים, הצגה ובקרה</td><td><b>MVC</b></td><td>Model: נתונים ולוגיקה · Controller: מעדכן Model · View: הצגה</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>שלושה צעדים לכל שאלה:</strong> (1) מנסחים את הצורך במשפט. (2) בוחרים את התבנית. (3) בודקים שהתפקידים שבתשובה נכונים, כי לעתים התבנית נכונה והתפקידים הפוכים.</div>
<div class="lesson-ex">דוגמה: "שירות התראות צריך לשלוח ב-SMS, בדוא״ל או ב-Push לפי בחירת המשתמש" ← סוג שנקבע בזמן ריצה ← Factory שמחזירה את הממשק <code>Notifier</code> (26CL-Q12, 26S-A-Q16).</div>
<div class="lesson-trap">⚠️ <strong>אל תתפתו לאפשרות ארוכה ומפורטת.</strong> לפעמים התשובה הנכונה היא הקצרה והמסיח מפרט משהו יפה אבל שגוי בתפקידים. קראו את התפקידים עד הסוף.</div>
` },
  questions: [
    { ref: "25S-A-Q10", recap: "מספר מופעים קבוע = Singleton שאוכפת את הכמות בפונקציית האחזור" },
    { ref: "25F0a-Q8", recap: "סוג שנבחר ע\"י הלקוח בזמן ריצה = Factory שמחזירה Products" },
    { ref: "26S-A-Q17", recap: "Ticket (שמשתנה) = Subject · הרכיבים שמתעדכנים = Observers" },
    { ref: "26B-A-Q19", recap: "שלט = Invoker · מכשירים = Receiver · Command מתווכת" },
    { ref: "24B-B-Q11", recap: "Model: נתונים ולוגיקה · Controller מעדכן Model · View: הצגה" },
    { ref: "24B-B-Q8", recap: "סינון עדכונים נעשה בפעולת notify של ה-Subject" },
  ],
});
