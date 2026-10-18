/* Design-patterns course · level 6 - Command: Command, Invoker, Receiver; decoupling and undo */
SE_LEVEL("pat", {
  id: "P06", order: 6, icon: "🎛️", title: "Command: Invoker, Command ו-Receiver",
  goal: "לשבץ רכיבים בתפקידי Invoker, Command ו-Receiver, ולהסביר איך Command מנתקת את המפעיל מהמבצע ומאפשרת undo.",
  lesson: { html: `
<p><strong>Command</strong> היא תבנית התנהגות שעוטפת <b>בקשה לפעולה כאובייקט</b>. כך אפשר לשמור פעולה, להעביר אותה, לתזמן אותה ולבטל אותה. העיקרון שהיא מממשת הוא <b>ניתוק (loose decoupling)</b> בין מי שמפעיל לבין מי שמבצע (SP-AMR-Q7).</p>
<h3>שלושה תפקידים</h3>
<table>
<thead><tr><th>תפקיד</th><th>מי זה</th><th>דוגמה</th></tr></thead>
<tbody>
<tr><td><b>Invoker</b> (מפעיל)</td><td>זה שמפעיל פקודה ומחזיק אותה</td><td>כפתורים ותפריטים (24B-A-Q7), שלט רחוק, מקליט פעולות</td></tr>
<tr><td><b>Command</b> (פקודה)</td><td>אובייקט שעוטף את הפעולה, עם <code>execute()</code></td><td>"הוספת טקסט", "הדלקת אור"</td></tr>
<tr><td><b>Receiver</b> (מקבל)</td><td>האובייקט שהפעולה <b>מבוצעת עליו</b> כשהפקודה נקראת (24S-A-Q9)</td><td>המסמך שעובדים עליו (24B-A-Q8), הנורה, עורך הטקסט</td></tr>
</tbody></table>
<p>ה-Invoker <b>מכיל</b> את ה-Command (קשר הכלה, 25F0b-Q8) ומכיר רק את הממשק שלו. הוא לא יודע מה בדיוק הפקודה עושה ועל מי. את העבודה עושה ה-Command מול ה-Receiver.</p>
<div class="lesson-rule">🔑 <strong>שאלת שלוש המילים:</strong> מי <b>מפעיל</b> (לוחץ, מחזיק, מקליט) = Invoker. מה <b>הפעולה</b> כאובייקט = Command. על מה <b>הפעולה קורית</b> = Receiver. כך נפתרת שאלת המקליט ב-25S-A-Q11: מקליט = Invoker, "הוספת טקסט" = Command, עורך הטקסט = Receiver.</div>
<div class="lesson-ex">דוגמה: שלט רחוק ובית חכם. <code>Remote</code> לוחץ על כפתור ומפעיל <code>command.execute()</code>. <code>LightOnCommand</code> קורא ל-<code>light.turnOn()</code>. התפקידים: <b>Remote = Invoker</b>, <b>LightOnCommand = Command</b>, <b>Light = Receiver</b>. אפשר להוסיף מכשיר חדש בלי לשנות את השלט.</div>
<div class="lesson-trap">⚠️ <strong>Undo.</strong> כדי לבטל פעולות, כל Command מקבלת גם <code>undo()</code>, וה-Invoker שומר את הפקודות שבוצעו (למשל במחסנית) ומפעיל <code>undo()</code> על האחרונה (26CL-Q17). לא שומרים עותק מלא של כל המצבים ב-Singleton, ולא יוצרים מחדש את הכל.</div>
` },
  questions: [
    { id: "P06-Q1", question: "בבית חכם, שלט רחוק (Remote) מפעיל מנורה (Light) דרך האובייקט TurnOnCommand שקורא ל-light.turnOn(). מהם התפקידים בתבנית Command?",
      options: ["Remote הוא Invoker, TurnOnCommand הוא Command ו-Light הוא Receiver", "Remote הוא Receiver, TurnOnCommand הוא Invoker ו-Light הוא Command", "Remote הוא Command, TurnOnCommand הוא Receiver ו-Light הוא Invoker", "Remote הוא Subject, TurnOnCommand הוא Observer ו-Light הוא Product"], answer: 0,
      recap: "מפעיל = Invoker · הפעולה = Command · מי שמבצעים עליו = Receiver",
      explanation: "השלט **מפעיל** ← Invoker; `TurnOnCommand` הוא **הפעולה כאובייקט** ← Command; המנורה היא זו ש**הפעולה מתבצעת עליה** ← Receiver. שאר הסידורים מחליפים תפקידים, והאחרון משתמש במושגים של Observer ו-Factory." },
    { id: "P06-Q2", question: "מה ה-Invoker יודע על הפעולה שהוא מפעיל?",
      options: ["רק את הממשק של ה-Command (למשל execute), לא מה בדיוק היא עושה ועל מי", "את המחלקה הקונקרטית של ה-Receiver ואת כל הפונקציות שלו", "שום דבר, כולל זה שיש לו פקודה להפעיל", "את הרשימה המלאה של כל ה-Observers שרשומים אצלו"], answer: 0,
      recap: "Invoker מכיר רק את ממשק ה-Command (ניתוק)",
      explanation: "זה העיקרון של התבנית: ה-Invoker **מחזיק Command ומכיר רק את הממשק** שלה, ולכן אפשר להחליף או להוסיף פקודות בלי לשנות אותו. אם הוא היה מכיר את ה-Receiver הקונקרטי, לא היה ניתוק. רשימת Observers שייכת לתבנית אחרת." },
    { id: "P06-Q3", question: "בעורך גרפי נדרש ביטול (undo) של הפעולות האחרונות. איפה ובאיזה מבנה נשמרות הפעולות שבוצעו, בתבנית Command?",
      options: ["ה-Invoker שומר את הפקודות שבוצעו במחסנית ומפעיל undo() על האחרונה", "ה-Receiver שומר עותק מלא של כל מצביו הקודמים כמשתנה גלובלי", "כל פקודה מחזיקה מצביע ל-Subject שמעדכן אותה בכל ביטול", "ה-Factory יוצר מחדש את כל הצורות מאפס בכל ביטול"], answer: 0,
      recap: "undo: ה-Invoker שומר פקודות במחסנית ומפעיל undo() על האחרונה",
      explanation: "בתבנית Command כל פעולה היא אובייקט עם `execute()` ו-`undo()`, וה-**Invoker שומר את הפקודות שבוצעו במחסנית** כדי לבטל מהאחרונה אל הראשונה. עותק גלובלי של כל המצבים וסריקה מחדש הם לא פתרון Command, ו-Subject אינו קשור כאן." },
    { ref: "25S-A-Q11", recap: "מקליט פעולות = Invoker · פעולת טקסט = Command · עורך = Receiver" },
    { ref: "24B-A-Q8", recap: "Receiver = המסמך שעובדים עליו" },
  ],
});
