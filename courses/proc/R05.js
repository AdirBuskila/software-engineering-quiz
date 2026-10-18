/* Process course · level 5 - Scrum events: planning, daily, review (demo), retrospective, burn-down */
SE_LEVEL("proc", {
  id: "R05", order: 5, icon: "📅", title: "Scrum: ארבע הפגישות של הספרינט",
  goal: "לשייך כל פגישה (Planning, Daily, Review, Retrospective) למטרה, לזמן ולמה שנדון בה.",
  lesson: { html: `
<p>העבודה ב-Scrum מחולקת ל<b>ספרינטים</b>: איטרציות קצובות, לרוב שבועיים עד ארבעה. בכל ספרינט ארבע פגישות:</p>
<table>
<thead><tr><th>הפגישה</th><th>מתי</th><th>מה עושים בה</th></tr></thead>
<tbody>
<tr><td><b>Sprint Planning</b></td><td>בתחילת הספרינט</td><td><b>מתכננים את יעדי הספרינט הבא</b> (22S-A-Q6, 23B-A-Q7)</td></tr>
<tr><td><b>Daily Scrum</b></td><td>כל יום, <b>10 עד 20 דקות בתחילת היום</b>, בעמידה (24B-A-Q6, 23B-A-Q14)</td><td>סטטוס: מה נעשה ביום הקודם ומה מתוכנן להיום (22B-A-Q3)</td></tr>
<tr><td><b>Sprint Review</b></td><td>בסוף הספרינט</td><td>דנים בעבודה <b>שהושלמה</b> ומעדכנים את ה-Backlog (24B-A-Q2); מציגים Demo של <b>תוצרי הספרינט הנוכחי</b> (21-B-Q8)</td></tr>
<tr><td><b>Sprint Retrospective</b></td><td>בסוף הספרינט</td><td>דנים <b>מה עבד טוב ומה אפשר לשפר בתהליך העבודה</b> (24B-B-Q6)</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>השאלה "על מה מדברים":</strong> <b>קדימה</b> (יעדים) ← Planning. <b>היום</b> (סטטוס) ← Daily. <b>המוצר שהושלם</b> ← Review. <b>התהליך</b> ← Retrospective. כל ערבוב בין "המוצר" ל"התהליך" הוא המלכודת הנפוצה בין Review ל-Retrospective.</div>
<p><b>Sprint Burn-Down Chart</b> הוא גרף של סך השעות שעוד יש לבצע בספרינט (24B-B-Q3), והוא יורד ככל שהעבודה מתקדמת. אורך ה-Retrospective אינו "שעה בתחילת היום" או "10 עד 20 דקות בסוף היום": אלה מסיחים שמערבבים אותה עם Planning ו-Daily (26S-A-Q7).</p>
<div class="lesson-ex">דוגמה: בסוף ספרינט הצוות נפגש כדי לדון מה עבד טוב ומה אפשר לשפר בעבודה שלו. מדובר ב-<b>Retrospective</b> (26CL-Q8). ובישיבה שבה הלקוח רואה את הפיצ'רים שהושלמו מדובר ב-<b>Review</b>.</div>
<div class="lesson-trap">⚠️ <strong>Daily אינו דיון טכני.</strong> אם שני מפתחים פותחים דיון של חצי שעה, עוצרים אותו וממשיכים אחרי הפגישה עם המעורבים בלבד: הפגישה היא סנכרון קצר (כ-15 דקות), לא ביטול ולא הארכה (26CL-Q7).</div>
` },
  questions: [
    { id: "R05-Q1", question: "באיזו פגישת Scrum מתכננים את יעדי הספרינט הבא?",
      options: ["Sprint Planning", "Daily Scrum", "Sprint Review", "Sprint Retrospective"], answer: 0,
      recap: "תכנון יעדי הספרינט הבא = Sprint Planning",
      explanation: "**Sprint Planning** מתכננת את יעדי הספרינט הבא. Daily נותנת סטטוס, Review מציגה את העבודה שהושלמה, ו-Retrospective דנה בתהליך." },
    { id: "R05-Q2", question: "מה נכון לגבי ה-Daily Scrum?",
      options: ["נמשכת בין 10 ל-20 דקות בתחילת היום ומעדכנים בה על המשימות", "נמשכת כשעה בסוף היום ומתכננים בה את המחר", "מתקיימת פעם בשבועיים ומציגים בה מוצר ללקוח", "אין פגישה כזו ב-Scrum"], answer: 0,
      recap: "Daily: 10-20 דקות, בתחילת היום, סטטוס",
      explanation: "**Daily** קצרה (10 עד 20 דקות), **בתחילת היום**, ומיועדת לסטטוס. שעה בסוף היום, פעם בשבועיים והצגה ללקוח אינן Daily, ובוודאי שהפגישה קיימת." },
    { id: "R05-Q3", question: "בסוף הספרינט הלקוח צופה בהדגמה של הפיצ'רים שהושלמו בספרינט. איזו פגישה זו?",
      options: ["Sprint Review", "Sprint Planning", "Daily Scrum", "Sprint Retrospective"], answer: 0,
      recap: "הדגמת תוצרי הספרינט = Sprint Review",
      explanation: "הצגת **התוצרים שהושלמו** היא **Sprint Review**. Planning מתכננת את הספרינט הבא, Daily היא סטטוס יומי ו-Retrospective עוסקת בשיפור התהליך ולא בהצגת מוצר." },
    { ref: "24B-B-Q6", recap: "Retrospective: מה עבד טוב ומה אפשר לשפר בתהליך" },
    { ref: "24B-B-Q3", recap: "Burn-Down: סך השעות שנותרו לביצוע בספרינט" },
  ],
});
