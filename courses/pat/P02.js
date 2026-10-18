/* Design-patterns course · level 2 - Singleton: one instance, three ingredients, when to use it, the bug that breaks it */
SE_LEVEL("pat", {
  id: "P02", order: 2, icon: "1️⃣", title: "Singleton: מופע אחד בלבד",
  goal: "לזהות מתי צריך Singleton, לכתוב את שלושת המרכיבים שלה, ולמצוא למה היא מייצרת כמה מופעים.",
  lesson: { html: `
<p><strong>Singleton</strong> היא תבנית יצירה (Creational) שמבטיחה שלמחלקה יהיה <b>מופע אחד בלבד</b> ושכל המערכת ניגשת אליו דרך נקודה אחת. היא שימושית כשהאובייקט שולט ב<b>משאב מצומצם</b> במערכת, למשל תור יחיד למספר מדפסות (19B-B-Q7, 24B-B-Q10).</p>
<h3>שלושה מרכיבים, ומחלקה אחת</h3>
<ul>
<li><b>בנאי פרטי</b> (<code>private</code>): אף אחד מבחוץ לא יכול לכתוב <code>new</code>.</li>
<li><b>שדה סטטי</b> שמחזיק את המופע היחיד.</li>
<li><b>מתודה סטטית ציבורית</b> <code>getInstance()</code> שיוצרת את המופע בקריאה הראשונה ומחזירה את אותו מופע בכל קריאה.</li>
</ul>
<pre class="lesson-code" dir="ltr"><code>public class Config {
  private static Config instance;
  private Config() { }
  public static Config getInstance() {
    if (instance == null) instance = new Config();
    return instance;
  }
}</code></pre>
<p>בתרשים מחלקות של Singleton יש <b>מחלקה אחת</b>, שמחזיקה שדה מהטיפוס של עצמה (24B-A-Q15).</p>
<div class="lesson-rule">🔑 <strong>אם יש יותר ממופע אחד, חפשו את הבנאי.</strong> אם הוא לא <code>private</code>, כל קוד יכול לכתוב <code>new</code> וליצור עוד מופע, ו-<code>getInstance</code> כבר לא עוזרת. זו הסיבה ב-24B-B-Q12 וב-26CL-Q16.</div>
<div class="lesson-ex">דוגמה: <code>Config a = Config.getInstance();</code> ואחריה <code>Config b = Config.getInstance();</code>. בקריאה הראשונה <code>instance</code> הוא <code>null</code>, אז נוצר מופע. בשנייה כבר יש מופע, ולכן מוחזר אותו אחד. התוצאה: <code>a == b</code> הוא <code>true</code>.</div>
<div class="lesson-trap">⚠️ <strong>מה Singleton לא עושה.</strong> היא לא עונה על "מערכת אחת ללקוח אחד", על דרישות אמינות וזמינות גבוהות או על מערכות מוזיקליות: אלה מסיחים מ-19B-B-Q7. וגם אם צריך <b>שני</b> מופעים בלבד (25S-A-Q10), הרעיון נשאר Singleton: אוכפים את המספר בפונקציית האחזור, לא בקוד שקורא <code>new</code> פעמיים.</div>
` },
  questions: [
    { id: "P02-Q1", question: "במחלקה הבאה רוצים להבטיח מופע יחיד, אבל מצליחים ליצור כמה מופעים. מה צריך לתקן?",
      code: "public class Logger {\n  private static Logger instance;\n  public Logger() { }\n  public static Logger getInstance() {\n    if (instance == null) instance = new Logger();\n    return instance;\n  }\n}",
      options: ["להפוך את הבנאי ל-private", "להפוך את getInstance למתודה לא סטטית", "להפוך את המחלקה ל-abstract", "להוסיף בנאי ציבורי שני עם פרמטר"], answer: 0,
      recap: "בנאי ציבורי = אפשר לעקוף את getInstance עם new",
      explanation: "הבעיה היא ה**בנאי הציבורי**: קוד מבחוץ כותב `new Logger()` ויוצר מופע נוסף. הפיכתו ל-`private` סוגרת את הדרך. אם `getInstance` הייתה לא סטטית, אי אפשר היה בכלל לקרוא לה בלי מופע. מחלקה abstract אי אפשר להפעיל, ובנאי ציבורי נוסף רק מחמיר." },
    { id: "P02-Q2", question: "איזה תיאור מתאים למבנה של התבנית Singleton?",
      options: ["מחלקה אחת עם בנאי פרטי, שדה סטטי מהטיפוס שלה ומתודה סטטית שמחזירה אותו", "ממשק אחד ושתי מחלקות קונקרטיות שמממשות אותו", "מחלקה Subject שמחזיקה רשימה של מחלקות Observer", "שלוש שכבות: Model, View ו-Controller"], answer: 0,
      recap: "Singleton = מחלקה אחת: בנאי private + שדה static + getInstance",
      explanation: "Singleton היא **מחלקה אחת** עם שלושה מרכיבים: בנאי פרטי, שדה סטטי ו-`getInstance`. התיאור עם Subject ו-Observer הוא Observer, השכבות הן MVC, והממשק עם שתי מחלקות מממשות מתאים למשל ל-Factory." },
    { id: "P02-Q3", question: "באיזה מהמקרים הבאים מתאים להשתמש ב-Singleton?",
      options: ["תור הדפסה אחד שמשרת את כל המדפסות במשרד", "אובייקט נפרד לכל לקוח של בנק", "הצגה של אותו מחיר במסכים רבים שמתעדכנים אוטומטית", "יצירת סוגי דוחות שונים לפי בחירת המשתמש"], answer: 0,
      recap: "משאב משותף שחייב להיות אחד = Singleton",
      explanation: "תור הדפסה יחיד הוא **משאב משותף שחייב להיות אחד**, וזה המקרה הקלאסי של Singleton (כמו ב-24B-B-Q10). אובייקט לכל לקוח הוא ההפך ממופע יחיד, עדכון מסכים הוא Observer, ובחירת סוג דוח בזמן ריצה היא Factory." },
    { id: "P02-Q4", question: "נתון קוד שמשתמש ב-Singleton שנכתב נכון (בנאי פרטי, שדה סטטי ו-getInstance כמו בשיעור):\n`Config a = Config.getInstance();`\n`Config b = Config.getInstance();`\n`System.out.println(a == b);`\nמה יודפס?",
      options: ["true", "false", "שגיאת קומפילציה", "NullPointerException"], answer: 0,
      recap: "שתי קריאות ל-getInstance מחזירות את אותו אובייקט",
      explanation: "הקריאה הראשונה יוצרת את המופע, והשנייה מחזירה **את אותו מופע**. אופרטור `==` משווה הפניות, ושתיהן מצביעות לאותו אובייקט, לכן `true`. בלי Singleton, שתי קריאות ל-`new` היו נותנות `false`." },
    { ref: "26CL-Q16", recap: "מופעים מרובים ב-Singleton = הבנאי לא private" },
  ],
});
