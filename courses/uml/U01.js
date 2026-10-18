/* UML course · level 1 - why several diagrams, and which model each diagram belongs to */
SE_LEVEL("uml", {
  id: "U01", order: 1, icon: "🗺️", title: "מפת התרשימים: לאיזה מודל שייך כל תרשים?",
  goal: "להסביר למה משתמשים בכמה תרשימי UML, ולשייך כל תרשים (מחלקות, רצף, Use Case, פעילות, מצבים) למודל שלו.",
  lesson: { html: `
<p><strong>UML</strong> היא שפת מידול גרפית. מערכת אחת מתוארת בה במספר <b>נקודות מבט (Perspectives)</b>, וכל תרשים מתמקד בהיבט אחר שלה. כך מבינים ומתכננים את המערכת במלואה (26S-A-Q13). אף תרשים לא מחליף את האחרים.</p>
<h3>ארבעה סוגי מודלים</h3>
<table>
<thead><tr><th>המודל</th><th>השאלה שהוא עונה עליה</th><th>התרשים</th></tr></thead>
<tbody>
<tr><td><b>Context</b> (הקשר)</td><td>איך התהליך או זרימת העבודה מתנהלים</td><td><b>Activity</b> (תרשים פעילות)</td></tr>
<tr><td><b>Interaction</b> (אינטראקציה)</td><td>מי מדבר עם המערכת ועם מי</td><td><b>Use Case</b> ו-<b>Sequence</b></td></tr>
<tr><td><b>Structure</b> (מבנה)</td><td>ממה המערכת בנויה</td><td><b>Class</b> (תרשים מחלקות)</td></tr>
<tr><td><b>Behavior</b> (התנהגות)</td><td>באילו מצבים המערכת יכולה להיות ואיך עוברים ביניהם</td><td><b>Statechart</b> (תרשים מצבים)</td></tr>
</tbody></table>
<p>תרשים המחלקות שייך גם לשלב ה-<b>Design &amp; Development</b> (20-A-Q2, SP-AMR-Q2), והוא תרשים <b>מבנה</b> ולא תרשים התנהגות (24B-A-Q13).</p>
<div class="lesson-rule">🔑 <strong>הדרך לזכור:</strong> <b>מחלקות</b> = מבנה. <b>Use Case</b> ו-<b>רצף</b> = אינטראקציה. <b>פעילות</b> = הקשר (תהליך). <b>מצבים</b> = התנהגות. שאלות "לאיזה מודל שייך תרשים X" מנוסחות כל פעם עם מסיחים אחרים, אבל הטבלה הזו לא משתנה (25B-N-Q17, 25F0a-Q15).</div>
<div class="lesson-ex">דוגמה: "לאיזה מודל שייך תרשים הרצף (sequence diagram)?" הוא מתאר הודעות בין משתתפים לאורך זמן ← <b>interaction model</b>. אם בין התשובות אין interaction, המשפט "כל התשובות האחרות שגויות" הוא הנכון (25F0b-Q16).</div>
<div class="lesson-trap">⚠️ <strong>"UML" אינו מודל.</strong> ב-SP-DGM-Q5 השאלה "לאיזה מודל שייך ה-UML" נענית ב"אף אחת מהתשובות": UML היא שפה שבה בונים תרשימים של כמה מודלים.</div>
` },
  questions: [
    { id: "U01-Q1", question: "לאיזה מודל שייך תרשים המחלקות (Class Diagram)?",
      options: ["Structure (מבנה)", "Interaction (אינטראקציה)", "Context (הקשר)", "Behavior (התנהגות)"], answer: 0,
      recap: "תרשים מחלקות = מודל מבנה",
      explanation: "תרשים מחלקות מתאר **ממה המערכת בנויה**: מחלקות, תכונות וקשרים, ולכן הוא **Structure**. Interaction הוא של Use Case ושל רצף, Context של תרשים פעילות ו-Behavior של תרשים מצבים." },
    { id: "U01-Q2", question: "לאיזה מודל שייך תרשים רצף (Sequence Diagram)?",
      options: ["Interaction (אינטראקציה)", "Structure (מבנה)", "Context (הקשר)", "Behavior (התנהגות)"], answer: 0,
      recap: "רצף ו-Use Case = מודל אינטראקציה",
      explanation: "תרשים רצף מתאר **הודעות בין משתתפים לאורך זמן**, וזה מודל **Interaction**. מבנה הוא תרשים המחלקות, הקשר הוא תרשים פעילות והתנהגות הוא תרשים מצבים." },
    { id: "U01-Q3", question: "לאיזה מודל שייך תרשים פעילות (Activity Diagram)?",
      options: ["Context (הקשר)", "Structure (מבנה)", "Interaction (אינטראקציה)", "Behavior (התנהגות)"], answer: 0,
      recap: "תרשים פעילות = מודל הקשר (זרימת תהליך)",
      explanation: "תרשים פעילות מתאר **זרימת עבודה או תהליך**, ובקורס הוא משויך למודל **Context**. בלבול נפוץ הוא עם Interaction (Use Case ורצף) ועם Behavior (תרשים מצבים)." },
    { id: "U01-Q4", question: "לאיזה מודל שייך תרשים מצבים (State Machine / Statechart)?",
      options: ["Behavior (התנהגות)", "Structure (מבנה)", "Context (הקשר)", "Interaction (אינטראקציה)"], answer: 0,
      recap: "תרשים מצבים = מודל התנהגות",
      explanation: "תרשים מצבים מתאר **באילו מצבים המערכת יכולה להיות ואיך עוברים בינם**, ולכן **Behavior**. Structure הוא תרשים המחלקות, Context תרשים פעילות ו-Interaction רצף ו-Use Case." },
    { ref: "26S-A-Q13", recap: "כמה Perspectives: אותה מערכת מנקודות מבט שונות, כל אחת מתמקדת בהיבט אחר" },
  ],
});
