/* UML course · level 9 - boss: real exam questions on every diagram */
SE_LEVEL("uml", {
  id: "U09", order: 9, icon: "🏆", title: "מבחן גמר: UML ומידול", boss: true,
  goal: "שש שאלות אמיתיות מהמבחנים על מודלים, תרשים מחלקות, רצף, Use Case ותרשים מצבים.",
  lesson: { html: `
<p>מבחן הגמר: שש שאלות אמיתיות מהמבחנים בלי רמזים. הנה כל הקורס בטבלה אחת, לפני שמתחילים.</p>
<table>
<thead><tr><th>התרשים</th><th>המודל</th><th>מה חייבים לזכור</th></tr></thead>
<tbody>
<tr><td><b>Class</b></td><td>Structure</td><td>משולש = ירושה · מעוין מלא = composition · 1..* רשימה · 1..10 מערך</td></tr>
<tr><td><b>Sequence</b></td><td>Interaction</td><td>קו חיים · סרגל הפעלה · חץ מקווקו = תשובה · X = הריסה · Actor מתחיל</td></tr>
<tr><td><b>Use Case</b></td><td>Interaction</td><td>include = חובה · extend = אופציונלי · אין ציר זמן</td></tr>
<tr><td><b>Activity</b></td><td>Context</td><td>solid bar: כולם חייבים להסתיים</td></tr>
<tr><td><b>Statechart</b></td><td>Behavior</td><td>XOR = אחד בכל רגע · AND = במקביל · אין מסרים</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>שאלת "לאיזה מודל":</strong> מחפשים את התרשים בטבלה ואז בודקים אם התשובה הנכונה מופיעה. אם לא, התשובה היא "כל התשובות האחרות שגויות" (25F0b-Q16).</div>
<div class="lesson-ex">דוגמה: "לאיזה מודל שייך תרשים המצבים?" ← באילו מצבים המערכת יכולה להיות ← <b>behavior model</b>. אם בין התשובות אין behavior, התשובה היא "כל התשובות האחרות שגויות" (26CL-Q9).</div>
<div class="lesson-trap">⚠️ <strong>קשרים לא עוברים בין תרשימים.</strong> Include ו-Extend הם של Use Case, ירושה והכלה של תרשים מחלקות, ובתרשים רצף יש רק הודעות.</div>
` },
  questions: [
    { ref: "25F0a-Q15", recap: "תרשים פעילות שייך למודל context" },
    { ref: "24B-A-Q18", recap: "סרגל הפעלה = הזמן שבו משתתף מבצע ומחכה לתשובה" },
    { ref: "26CL-Q11", recap: "Composition = מעוין מלא בצד השלם (DoctorCalendar)" },
    { ref: "24B-B-Q16", recap: "AND בתרשים מצבים = מצבים בלתי תלויים שמתקיימים במקביל" },
    { ref: "25B-N-Q17", recap: "Use Case שייך למודל interaction" },
    { ref: "24S-A-Q12", recap: "מחלקות לוגיקה בצד הלקוח: שחקן, נשק ומחלקה שפונה לשרת" },
  ],
});
