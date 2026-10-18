/* Process course · level 4 - Scrum roles: Product Owner, Scrum Master, the team */
SE_LEVEL("proc", {
  id: "R04", order: 4, icon: "🧑‍🤝‍🧑", title: "Scrum: Product Owner, Scrum Master והצוות",
  goal: "לדעת מה תפקידו של Product Owner ומה של Scrum Master, ולשייך כל משימה בתיאור לבעל התפקיד הנכון.",
  lesson: { html: `
<p><strong>Scrum</strong> היא מסגרת לניהול פיתוח אג'ילי. התפקידים העיקריים בה הם <b>Scrum Master</b> ו-<b>Product Owner</b> (24B-B-Q2), ולצד אלה צוות הפיתוח. הצוות האופטימלי הוא של <b>5 עד 10 משתתפים</b> (24B-B-Q1).</p>
<table>
<thead><tr><th>תפקיד</th><th>אחריות</th></tr></thead>
<tbody>
<tr><td><b>Product Owner</b> (PO)</td><td><b>מגדיר את חזון המוצר ומנהל את ה-Backlog</b> (24B-A-Q4); קובע <b>עדיפויות סופיות</b> למימוש (19B-C-Q5); מכריע בין בעלי עניין חלוקים בשאלה מה חשוב קודם (26CL-Q6)</td></tr>
<tr><td><b>Scrum Master</b> (SM)</td><td><b>מנהל את תהליך ה-Scrum</b> (24B-A-Q3); <b>מסיר חסמים</b> שמציף הצוות, למשל תלות בצוות תשתיות (26B-A-Q9)</td></tr>
<tr><td><b>צוות הפיתוח</b></td><td>מבצע את העבודה; צוות רב-תחומי שבו כל בעלי התפקידים הדרושים</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>"מה" ו"באיזה סדר" ← PO. "איך התהליך" ו"מה חוסם" ← SM.</strong> לכן קביעת סדר העדיפויות היא של ה-PO, והסרת חסם היא של ה-SM. ה-SM אינו מנהל פרויקט קלאסי: הוא לא מקצה משימות, לא שומר על התקציב ולא מגדיר את חזון המוצר (24B-B-Q4).</div>
<div class="lesson-ex">דוגמה: בפרויקט Scrum, מנהל המכירות ומנהלת התפעול חלוקים מה לממש קודם. <b>ה-Product Owner</b> מכריע. באותו פרויקט מפתח אומר ב-Daily שהוא תקוע כי צוות התשתיות לא סיפק סביבה. <b>ה-Scrum Master</b> עוזר להסיר את החסם.</div>
<div class="lesson-trap">⚠️ <strong>אין "Team Leader", "Project Manager" או "DevOps Owner" ב-Scrum</strong> (26B-A-Q9). וגם לא "Scrum Owner" או "Product Master": שמות התפקידים מדויקים, ומסיחים מערבבים ביניהם.</div>
` },
  questions: [
    { id: "R04-Q1", question: "בפרויקט Scrum, מנהל המכירות ומנהלת התפעול חלוקים לגבי איזו יכולת לממש קודם. מי מכריע?",
      options: ["Product Owner", "Scrum Master", "צוות הפיתוח, בהצבעת רוב", "Project Manager"], answer: 0,
      recap: "סדר עדיפויות = Product Owner",
      explanation: "קביעת **סדר העדיפויות** והכרעה בין בעלי עניין היא של ה-**Product Owner**. ה-Scrum Master מנהל את התהליך, הצוות מבצע ולא מכריע על עדיפויות עסקיות, ואין תפקיד Project Manager ב-Scrum." },
    { id: "R04-Q2", question: "ב-Daily Scrum מפתח אומר שהוא לא יכול להתקדם כי צוות אחר לא סיפק לו סביבת בדיקות. מי אמור לסייע בהסרת החסם?",
      options: ["Scrum Master", "Product Owner", "Team Leader", "כל חבר צוות אחר לפי תור"], answer: 0,
      recap: "הסרת חסמים (impediments) = Scrum Master",
      explanation: "**Scrum Master** אחראי להסיר חסמים ולנהל את תהליך ה-Scrum. ה-PO עוסק בחזון וב-Backlog, ואין תפקיד Team Leader ב-Scrum." },
    { id: "R04-Q3", question: "איזו מהמשימות הבאות אינה תפקידו של Scrum Master אלא של Product Owner?",
      options: ["להגדיר את חזון המוצר ולנהל את ה-Backlog", "להסיר חסמים של הצוות", "לדאוג שהצוות מבין ומקיים את תהליך ה-Scrum", "לנהל את תהליך ה-Scrum"], answer: 0,
      recap: "חזון ו-Backlog = PO · תהליך וחסמים = SM",
      explanation: "**חזון המוצר וניהול ה-Backlog** שייכים ל-Product Owner. שלוש האחרות הן תפקידי ה-Scrum Master: הסרת חסמים, וידוא שהצוות מקיים את התהליך וניהול התהליך." },
    { ref: "24B-B-Q1", recap: "גודל צוות אופטימלי ב-Scrum: 5 עד 10 משתתפים" },
    { ref: "19B-C-Q5", recap: "Product Owner קובע עדיפויות סופיות למימוש מתוך מלאי המוצר" },
  ],
});
