/* Design-patterns course · level 4 - Observer: Subject, Observer and the four operations attach / detach / notify / update */
SE_LEVEL("pat", {
  id: "P04", order: 4, icon: "👀", title: "Observer: Subject, Observer ופעולות Attach ו-Notify",
  goal: "לדעת מי מחזיק את מי ב-Observer, מה עושה כל אחת מהפעולות, ולעקוב אחרי מי מקבל עדכון.",
  lesson: { html: `
<p><strong>Observer</strong> היא תבנית התנהגות. יש <b>Subject</b> (הנושא, האובייקט שמשתנה) ו<b>Observers</b> (הצופים, אובייקטים שרוצים לדעת כשהנושא משתנה). כשה-Subject משתנה, <b>כל ה-Observers שרשומים אצלו</b> משתנים בהתאם (24B-A-Q9) ומקבלים הודעת עדכון (24B-A-Q11).</p>
<h3>ארבע פעולות</h3>
<table>
<thead><tr><th>פעולה</th><th>מי מפעיל</th><th>מה היא עושה</th></tr></thead>
<tbody>
<tr><td><b>Attach</b></td><td>על ה-Subject</td><td>מחברת Observer מסוים אל ה-Subject (24B-B-Q9)</td></tr>
<tr><td><b>Detach</b></td><td>על ה-Subject</td><td>מנתקת Observer מסוים מה-Subject (24B-A-Q10)</td></tr>
<tr><td><b>notify</b></td><td>ה-Subject</td><td>עוברת על כל ה-Observers הרשומים ושולחת לכל אחד update</td></tr>
<tr><td><b>update</b></td><td>על ה-Observer</td><td>הפעולה שבה ה-Observer מקבל את העדכון</td></tr>
</tbody></table>
<p>ה-Subject <b>מחזיק</b> אוסף של Observers (קשר של הכלה, 25S-A-Q8). הוא לא יודע מי הם בפרטים, רק שיש להם <code>update</code>, ולכן אפשר להוסיף Observers חדשים בלי לשנות אותו.</p>
<div class="lesson-rule">🔑 <strong>כיוון הפעולות:</strong> Attach ו-Detach הן על ה-Subject ("את מי להוסיף או להסיר"), ו-update היא על ה-Observer ("קיבלתי עדכון"). השמות לא מתחלפים: אף פעם לא "מנתקים Subject מ-Observer".</div>
<div class="lesson-ex">דוגמה: <code>s.attach(a); s.attach(b); s.attach(c); s.detach(b);</code> ואז ה-Subject משתנה ומפעיל <code>notify</code>. הרשימה אחרי כל הפעולות היא a, c, ולכן <b>a ו-c מקבלים update, ו-b לא</b>.</div>
<div class="lesson-trap">⚠️ <strong>אין בדיקת מסד נתונים משותף.</strong> ה-Observers לא "שואלים" את ה-Subject כל כמה זמן ולא קוראים מאותו מסד נתונים: הם מקבלים <b>הודעה</b> כשיש שינוי. זו התשובה ב-24B-A-Q11, והמסיחים שם בנויים מהבלבול הזה.</div>
` },
  questions: [
    { ref: "24B-B-Q9", recap: "Attach = חיבור Observer מסוים אל ה-Subject" },
    { id: "P04-Q1", question: "בתבנית Observer, מי מחזיק רשימה של מי?",
      options: ["ה-Subject מחזיק את רשימת ה-Observers הרשומים אצלו", "כל Observer מחזיק את רשימת כל ה-Subjects בעולם", "אף אחד מהם לא מחזיק רשימה, והעדכון מתבצע דרך מסד נתונים משותף", "ה-Observers מחזיקים רשימה של Observers אחרים"], answer: 0,
      recap: "ה-Subject מחזיק אוסף Observers (הכלה)",
      explanation: "ה-**Subject מחזיק** אוסף של Observers, ולכן `notify` יודעת למי לשלוח. Observer לא מחזיק רשימת Subjects בכל העולם, ואין מסד נתונים משותף: העדכון מגיע בהודעה." },
    { id: "P04-Q2", question: "מתבצעים הצעדים הבאים לפי הסדר, ואז ה-Subject משתנה ומפעיל notify:\n`s.attach(a)`, `s.attach(b)`, `s.attach(c)`, `s.detach(b)`\nמי מקבל update?",
      options: ["a ו-c", "a, b ו-c", "b בלבד", "אף אחד, כי Detach מוחקת את כל הרשימה"], answer: 0,
      recap: "Detach מסירה Observer אחד מהרשימה, לא את כולם",
      explanation: "אחרי שלוש הוספות הרשימה היא a, b, c; `detach(b)` מסירה **רק את b**; ולכן `notify` שולחת update ל-**a ו-c**. b כבר לא רשום, ו-Detach לא מוחקת את שאר הרשימה." },
    { id: "P04-Q3", question: "מה קורה כאשר ה-Subject משנה את המצב שלו?",
      options: ["ה-Subject מפעיל notify, ובה נשלח update לכל Observer רשום", "כל Observer מפעיל attach על עצמו כדי לברר מה השתנה", "ה-Subject מפעיל detach על כל ה-Observers כדי לאפס אותם", "ה-Observers משנים את ה-Subject בהתאם למצב שלהם"], answer: 0,
      recap: "שינוי ב-Subject ← notify ← update לכל Observer רשום",
      explanation: "הזרימה היא: שינוי מצב ← `notify` ← `update` לכל Observer שברשימה. Attach ו-Detach עוסקות ברשימה עצמה ולא בעדכון. והכיוון הוא מה-Subject אל ה-Observers (24B-A-Q9), לא להפך." },
    { id: "P04-Q4", question: "איזו פעולה נקראת על ה-Observer עצמו, ובה הוא מקבל את העדכון מה-Subject?",
      options: ["update", "attach", "detach", "notify"], answer: 0,
      recap: "update = על ה-Observer · attach/detach/notify = ניהול ושליחה אצל ה-Subject",
      explanation: "**update** היא הפעולה של ה-Observer שמקבלת את העדכון. Attach ו-Detach מתבצעות על ה-Subject כדי לנהל את הרשימה, ו-notify היא הפעולה של ה-Subject ששולחת את העדכונים." },
    { ref: "24B-A-Q11", recap: "Observers מקבלים הודעת עדכון כשה-Subject משתנה" },
  ],
});
