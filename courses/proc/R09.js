/* Process course · level 9 - boss: real exam questions on process models, Scrum and requirements */
SE_LEVEL("proc", {
  id: "R09", order: 9, icon: "🏆", title: "מבחן גמר: תהליכים, Agile ודרישות", boss: true,
  goal: "שש שאלות אמיתיות מהמבחנים על בחירת מתודולוגיה, תפקידי Scrum, פגישות, שינויים באמצע ספרינט ודרישות.",
  lesson: { html: `
<p>מבחן הגמר: שש שאלות אמיתיות מהמבחנים בלי רמזים. הנה הקורס בטבלה אחת.</p>
<table>
<thead><tr><th>הנושא</th><th>מה חייבים לזכור</th></tr></thead>
<tbody>
<tr><td>בחירת מודל</td><td>דרישות ידועות ויציבות ובקרה ← Waterfall / Plan Driven · דרישות משתנות ← Agile · POC ← Build and Fix</td></tr>
<tr><td>תפקידים</td><td>PO: חזון, Backlog ועדיפויות · SM: תהליך והסרת חסמים</td></tr>
<tr><td>פגישות</td><td>Planning: יעדים · Daily: סטטוס · Review: מה הושלם · Retrospective: איך משפרים</td></tr>
<tr><td>באמצע ספרינט</td><td>דרישה חדשה ← Product Backlog · משימה גדולה מההערכה ← מתאימים את העבודה ליעד</td></tr>
<tr><td>דרישות</td><td>פעולה = פונקציונלית · איכות ואילוץ = לא פונקציונלית · עמום או "איך" = דרישה גרועה</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>תהליך פתרון:</strong> מזהים את הנושא (מודל, תפקיד, פגישה, דרישה), מוצאים את השורה בטבלה, ורק אז מסננים את התשובות.</div>
<div class="lesson-ex">דוגמה: "חברה בונה מערכת לגוף ממשלתי, עם דרישות ולוחות זמנים מוגדרים מראש" ← דרישות ידועות ובקרה ← Plan Driven. המסיח "אג'ייל כי הוא תמיד מהיר יותר" נפסל כי אין שיטה שתמיד מהירה יותר (SP-AMR-Q5).</div>
<div class="lesson-trap">⚠️ <strong>שימו לב למילה "לא" ו"אינה".</strong> בשאלות של "איזה משפט לא נכון" או "איזו דרישה אינה פונקציונלית" הופכים את השאלה בראש לפני שקוראים את התשובות.</div>
` },
  questions: [
    { ref: "26S-A-Q8", recap: "דרישות מפורטות מראש + בקרה = Plan Driven" },
    { ref: "24B-A-Q4", recap: "Product Owner: חזון המוצר וניהול ה-Backlog" },
    { ref: "24B-A-Q2", recap: "Sprint Review: לדון בעבודה שהושלמה ולעדכן את ה-Backlog" },
    { ref: "26S-A-Q6", recap: "משימה גדולה מההערכה ← מתאימים את העבודה ליעד הספרינט" },
    { ref: "26S-A-Q4", recap: "העברה בנקאית = פונקציונלית · 5,000 בדקה = לא פונקציונלית" },
    { ref: "23S-A-Q4", recap: "דרישה שמכתיבה תבניות תיכון מתייחסת למימוש ואינה דרישת משתמש טובה" },
  ],
});
