/* Design-patterns course · level 8 - Chain of Responsibility, Flyweight, Mediator: the three "other" patterns */
SE_LEVEL("pat", {
  id: "P08", order: 8, icon: "🔗", title: "Chain, Flyweight ו-Mediator",
  goal: "לזהות לפי תיאור קצר מתי מדובר ב-Chain of Responsibility, ב-Flyweight או ב-Mediator, ומה משותף להן ולתבניות שכבר למדת.",
  lesson: { html: `
<p>שלוש תבניות שנשאלו רק במבחני התרגול של המרצה, בשאלות קצרות של "מה משותף ומה שונה". לא צריך לדעת מימוש, רק את הרעיון ואת ההשוואה.</p>
<table>
<thead><tr><th>תבנית</th><th>משפחה</th><th>הרעיון במשפט</th></tr></thead>
<tbody>
<tr><td><b>Chain of Responsibility</b> (שרשרת)</td><td>התנהגות</td><td>בקשה עוברת בשרשרת מטפלים (handlers); <b>המטפל הראשון שיכול לטפל, מבצע</b> (25-EX-Q5, 23-EX-Q10)</td></tr>
<tr><td><b>Flyweight</b></td><td>מבנה</td><td>משתפים אובייקטים זהים במקום ליצור אלפי עותקים, כדי לחסוך זיכרון</td></tr>
<tr><td><b>Mediator</b> (מתווך)</td><td>התנהגות</td><td>אובייקט מרכזי שדרכו מדברים הרכיבים, במקום שכל אחד ידבר עם כולם</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>שלוש השוואות שחוזרות:</strong> (1) <b>Singleton ו-Flyweight:</b> בשתיהן הבנאי פועל רק אם עצמים מסוימים <b>טרם נבנו</b>, כי בשתיהן משתמשים שוב באובייקט קיים (23-EX-Q6). (2) <b>Mediator ו-Observer:</b> דמיון רב במבנה של <b>תרשים המחלקות</b> שלהם (23-EX-Q7). (3) <b>Chain:</b> לא כל המטפלים מבצעים, רק הראשון שמסוגל.</div>
<div class="lesson-ex">דוגמה: פנייה לתמיכה עוברת מנציג רמה 1 לרמה 2 ולמנהל. כל אחד בודק "אני יכול לטפל?" ואם כן, הוא מטפל והשרשרת נעצרת. זו <b>Chain of Responsibility</b>. לעומת זאת, אלפי עצים זהים במשחק שמשתפים נתוני תמונה אחד הם <b>Flyweight</b>, וחדר צ'אט שבו כל הודעה עוברת דרך אובייקט מרכזי הוא <b>Mediator</b>.</div>
<div class="lesson-trap">⚠️ <strong>"כל המטפלים מבצעים" שגוי.</strong> אין כאן pipeline שבו כל מטפל מסיים ומעביר הלאה לכולם. אחרי שמטפל מסוגל מבצע את הפעולה, זה המטפל הרלוונטי (25-EX-Q5).</div>
` },
  questions: [
    { id: "P08-Q1", question: "פנייה של לקוח עוברת קודם לנציג רמה 1. אם הוא לא מסוגל לטפל בה, היא עוברת לנציג רמה 2, ואחר כך למנהל, ומי שמסוגל מטפל בה. באיזו תבנית מדובר?",
      options: ["Chain of Responsibility", "Flyweight", "Singleton", "Abstract Factory"], answer: 0,
      recap: "בקשה שעוברת בשרשרת עד שמישהו מסוגל לטפל = Chain of Responsibility",
      explanation: "הבקשה עוברת בשרשרת מטפלים עד שהראשון שיכול לטפל מבצע, וזו **Chain of Responsibility**. Flyweight חוסכת זיכרון בשיתוף אובייקטים, Singleton מבטיחה מופע יחיד ו-Abstract Factory יוצרת משפחות אובייקטים." },
    { id: "P08-Q2", question: "במשחק יש 50,000 עצים, ולרובם אותה תמונה ואותם נתונים משותפים. הזיכרון נגמר. איזו תבנית עונה על הבעיה?",
      options: ["Flyweight: משתפים אובייקט משותף במקום לשכפל אותו", "Command: כל עץ הוא פקודה שאפשר לבטל", "Observer: כל עץ נרשם כצופה במשחק", "Mediator: העצים מדברים זה עם זה דרך אובייקט מרכזי"], answer: 0,
      recap: "מספר עצום של אובייקטים דומים + בעיית זיכרון = Flyweight",
      explanation: "הבעיה היא **זיכרון** בגלל אובייקטים רבים כמעט זהים, ו-**Flyweight** פותרת אותה בשיתוף. Command, Observer ו-Mediator עוסקות בהפעלה, בעדכון ובתקשורת, ולא בחיסכון בזיכרון." },
    { id: "P08-Q3", question: "בחדר צ'אט, כל משתתף שולח הודעות לאובייקט ChatRoom מרכזי, וזה מעביר אותן לשאר, כך שהמשתתפים לא מכירים זה את זה. באיזו תבנית מדובר?",
      options: ["Mediator", "Singleton", "Factory", "Chain of Responsibility"], answer: 0,
      recap: "תקשורת בין רכיבים דרך אובייקט מרכזי = Mediator",
      explanation: "כשהרכיבים מדברים דרך **אובייקט מרכזי** ולא ישירות, זו **Mediator**. אין כאן יצירת אובייקטים (Factory), מופע יחיד כדרישה (Singleton), או שרשרת שבה רק הראשון שמסוגל מטפל." },
    { ref: "23-EX-Q6", recap: "Singleton ו-Flyweight: הבנאי פועל רק אם עצמים מסוימים טרם נבנו" },
    { ref: "23-EX-Q7", recap: "Mediator ו-Observer דומות במבנה תרשים המחלקות" },
    { ref: "25-EX-Q5", recap: "ב-Chain המטפל הראשון שיכול לטפל מבצע את פעולתו" },
  ],
});
