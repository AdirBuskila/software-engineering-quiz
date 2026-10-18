/* Design-patterns course · level 3 - Factory Method: who decides the concrete class, what the client sees, Abstract Factory */
SE_LEVEL("pat", {
  id: "P03", order: 3, icon: "🏭", title: "Factory: מי יוצר את האובייקט?",
  goal: "לזהות מתי Factory מתאימה, להסביר מה הקוד הקורא רואה, ולהבדיל בין Factory ל-Abstract Factory.",
  lesson: { html: `
<p><strong>Factory (בית חרושת)</strong> היא מחלקה שיוצרת אובייקט של מחלקה אחרת (25-EX-Q4). בתבנית <b>Factory Method</b> יש מתודה אחת שמקבלת בקשה (בדרך כלל פרמטר) ומחזירה את <b>המופע המתאים</b> (19B-C-Q8).</p>
<p>הטריק: חתימת המתודה מחזירה <b>ממשק (interface)</b> או מחלקת-על, ומחלקות קונקרטיות יורשות ממנו או מממשות אותו. הקוד הקורא מכיר רק את הממשק (21-A-Q9, 24B-B-Q13).</p>
<pre class="lesson-code" dir="ltr"><code>interface Notifier { void send(String msg); }
class Sms implements Notifier { ... }
class Email implements Notifier { ... }

class NotifierFactory {
  static Notifier create(String channel) {
    if (channel.equals("sms")) return new Sms();
    return new Email();
  }
}
Notifier n = NotifierFactory.create(userChoice);</code></pre>
<h3>למה זה טוב</h3>
<ul>
<li><b>הפרדה</b> בין הקוד שיוצר את האובייקטים לקוד שמשתמש בהם (22B-A-Q11).</li>
<li>הלקוח <b>מנותק מהמחלקה הקונקרטית</b>, ולכן אפשר להוסיף סוג חדש (למשל WhatsApp) בלי לגעת בקוד הקורא (24S-A-Q8).</li>
<li>הסוג נקבע <b>בזמן ריצה</b>, על ידי הלקוח באמצעות פרמטר (24S-A-Q10).</li>
</ul>
<div class="lesson-rule">🔑 <strong>מתי Factory ולא <code>new</code> ישיר?</strong> כשסוג האובייקט המדויק <b>לא ידוע עד זמן הריצה</b>, או כשהקוד הקורא לא צריך להכיר מחלקות קונקרטיות (25S-A-Q9).</div>
<h3>Abstract Factory</h3>
<p>גרסה גדולה יותר: בית חרושת שיוצר <b>משפחה</b> של אובייקטים קשורים שמתאימים זה לזה. הדוגמה מהמבחן: מערכת החלונות במערכות הפעלה שונות (23-EX-Q9). בית חרושת אחד ל-Windows יוצר כפתור וחלון בסגנון Windows, ובית חרושת אחר ל-Mac יוצר את אותם רכיבים בסגנון Mac.</p>
<div class="lesson-ex">דוגמה: מערכת שמנתחת קבצים בפורמטים JSON, XML ו-CSV, והפורמט ידוע רק כשהמשתמש מעלה קובץ. הצורך: <b>סוג האובייקט נקבע בזמן ריצה</b> ← Factory שמקבלת את הפורמט ומחזירה <code>Parser</code> (ממשק), וכל מנתח הוא מחלקה קונקרטית (25F0a-Q8).</div>
<div class="lesson-trap">⚠️ <strong>Factory לא מבטיחה מופע יחיד.</strong> "יש רק מופע אחד" היא Singleton. בשאלות על התראות מסוג Email, SMS ו-Push (26S-A-Q16) המסיח Singleton נשמע הגיוני, אבל הצורך שם הוא יצירה לפי סוג.</div>
` },
  questions: [
    { ref: "25S-A-Q9", recap: "Factory על פני new כשהסוג המדויק לא ידוע עד זמן הריצה" },
    { id: "P03-Q1", question: "נתון הקוד `Notifier n = NotifierFactory.create(userChoice);` כאשר Notifier הוא ממשק ו-Sms ו-Email מממשות אותו. איזו טענה נכונה?",
      options: ["הקוד הקורא לא תלוי במחלקות Sms ו-Email", "הקוד הקורא חייב לכתוב `new Sms()` בעצמו", "ייווצר תמיד מופע אחד בלבד לאורך כל חיי התוכנית", "המחלקה Email חייבת לרשת מהמחלקה Sms"], answer: 0,
      recap: "הלקוח מכיר רק את הממשק, לא את המחלקות הקונקרטיות",
      explanation: "הלקוח מחזיק משתנה מטיפוס **הממשק** ומקבל מה-Factory מופע מתאים, ולכן הוא לא תלוי במחלקות הקונקרטיות. מי שכותב `new` הוא ה-Factory, לא הלקוח. מופע יחיד הוא Singleton, ואין שום צורך שמחלקה אחת תירש מהשנייה." },
    { id: "P03-Q2", question: "מערכת תשלומים תומכת באשראי, PayPal והעברה בנקאית. השיטה נבחרת בזמן ריצה, ובעתיד יתווספו שיטות. באיזו תבנית תשתמשו ואיך?",
      options: ["Factory: מתודה שמקבלת את סוג התשלום ומחזירה אובייקט מהממשק PaymentMethod", "Singleton: מחלקה אחת עם בנאי פרטי שמכילה את כל שיטות התשלום בתוך if ארוך", "Observer: כל שיטת תשלום נרשמת כ-Observer ומקבלת כל תשלום", "Command: שיטת התשלום משמשת כ-Invoker והלקוח כ-Receiver"], answer: 0,
      recap: "סוג שנקבע בזמן ריצה + צפי להרחבה = Factory שמחזירה ממשק",
      explanation: "הצורך הוא **בחירת סוג בזמן ריצה** עם אפשרות להוסיף סוגים: Factory שמחזירה `PaymentMethod`. Singleton עם if ארוך הוא ההפך מהרחבה קלה, Observer מיועדת לעדכון רכיבים כשמשהו משתנה, ו-Command לעטיפת פעולות כאובייקטים." },
    { id: "P03-Q3", question: "איזה מהבאים הוא יתרון של שימוש ב-Factory?",
      options: ["ניתוק הלקוח מהמחלקות הקונקרטיות", "הבטחה שיהיה רק מופע אחד של כל מחלקה", "ביטול הצורך בממשקים ובירושה", "אפשרות לבטל פעולה שכבר בוצעה"], answer: 0,
      recap: "יתרון Factory: הלקוח לא תלוי במחלקה הקונקרטית",
      explanation: "היתרון הוא **ניתוק הלקוח מהמחלקה הקונקרטית**, כך שאפשר להחליף או להוסיף סוגים בלי לשנות אותו. מופע יחיד הוא Singleton, ביטול פעולות הוא Command, ובפועל Factory מסתמכת על ממשקים וירושה ולא מבטלת אותם." },
    { id: "P03-Q4", question: "איזו דוגמה מתאימה ל-Abstract Factory (ולא ל-Factory Method פשוטה)?",
      options: ["בית חרושת שיוצר כפתור, תיבת סימון וחלון בסגנון Windows, ובית חרושת אחר שיוצר אותם בסגנון Mac", "מתודה שמקבלת את המחרוזת \"csv\" ומחזירה מנתח קבצים אחד", "מחלקה עם בנאי פרטי שמחזירה תמיד את אותו אובייקט", "אובייקט שמקבל הודעה בכל פעם שמחיר המניה משתנה"], answer: 0,
      recap: "Abstract Factory = יצירת משפחה של אובייקטים שמתאימים זה לזה",
      explanation: "Abstract Factory יוצרת **משפחה** של אובייקטים קשורים (כפתור + תיבה + חלון באותו סגנון), כמו מערכת החלונות ב-23-EX-Q9. מתודה שמחזירה מנתח אחד היא Factory Method, מחלקה שמחזירה תמיד אותו אובייקט היא Singleton, וקבלת הודעות היא Observer." },
    { ref: "21-A-Q9", recap: "Factory Method מחזירה interface שממנו יורשים ה-Concrete Classes" },
  ],
});
