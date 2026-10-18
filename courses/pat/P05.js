/* Design-patterns course · level 5 - Observer in practice: roles in a scenario, class diagram, many subjects, filtering */
SE_LEVEL("pat", {
  id: "P05", order: 5, icon: "📡", title: "Observer בתרגיל: תפקידים, תרשים וסינון",
  goal: "לשבץ רכיבים בתפקידי Subject ו-Observer בתיאור מערכת, לקרוא את תרשים המחלקות, ולדעת איפה מסננים עדכונים.",
  lesson: { html: `
<p>בתרגיל, השלב הראשון הוא לשבץ את הרכיבים בתפקידים. <b>ה-Subject</b> הוא האובייקט ש<b>משתנה</b>, וה-<b>Observers</b> הם אלה שצריכים <b>להגיב</b> לשינוי. בשאלות המבחן: <code>StockPriceTracker</code> הוא ה-Subject, ו-<code>TraderDashboard</code> ו-<code>AutomatedTradingBot</code> הם ה-Observers (25F0a-Q10); אובייקט Ticket שמשנה סטטוס הוא ה-Subject, והדשבורד, מערכת ה-Analytics ושירות ההתראות הם ה-Observers (26S-A-Q17).</p>
<div class="lesson-rule">🔑 <strong>מי משתנה ומי מגיב?</strong> המשתנה הוא Subject. אלה שצריכים לדעת על השינוי הם Observers. הכיוון הפוך הוא המסיח הקבוע ("Ticket הוא Observer וכל שלושת הרכיבים הם Subject").</div>
<h3>תרשים המחלקות</h3>
<p>בתרשים של Observer יש <b>שתי רמות</b> של מחלקות: מופשטות (abstract) וקונקרטיות (concrete). חץ ההורשה מופיע <b>בין מחלקת Observer מופשטת למחלקת Observer קונקרטית</b> (24B-B-Q7, 24B-A-Q14). הקשר בין Subject ל-Observer הוא הכלה, לא הורשה.</p>
<pre class="lesson-code" dir="ltr"><code>Subject  o------&gt;  Observer (abstract)
                         ^
                         |  inheritance
                  ConcreteObserver</code></pre>
<h3>שלוש וריאציות שנשאלו</h3>
<ul>
<li><b>Observer אחד, כמה Subjects:</b> קוראים ל-<code>Attach</code> בכל Subject ומרשימים את אותו Observer (25F0b-Q10).</li>
<li><b>רק חלק מה-Observers מקבלים חלק מהנתונים:</b> ההחלטה את מי לעדכן מתקבלת ב-<code>notify</code> של ה-Subject (24B-B-Q8, 25B-N-Q11), לא אצל ה-Observers.</li>
<li><b>עדיפות:</b> ב-<code>Attach</code> ה-Subject מוסיף את ה-Observer לתור לפי עדיפות (24S-A-Q7).</li>
</ul>
<div class="lesson-ex">דוגמה: תחנת מזג אוויר <code>WeatherStation</code> משתנה, ושני מסכים (<code>PhoneScreen</code>, <code>WebWidget</code>) מציגים את הטמפרטורה. ה-Subject הוא <code>WeatherStation</code>; ה-Observers הם שני המסכים. להוסיף מסך שלישי = Attach אחד, בלי לשנות את התחנה.</div>
<div class="lesson-trap">⚠️ <strong>Mediator דומה ל-Observer במבנה.</strong> שתיהן נראות כמעט אותו דבר בתרשים מחלקות (23-EX-Q7). בשאלות על תרחיש, "כשדבר אחד משתנה וכמה רכיבים מתעדכנים" הוא Observer.</div>
` },
  questions: [
    { id: "P05-Q1", question: "באפליקציית מזג אוויר, האובייקט WeatherStation מעדכן טמפרטורה, והאובייקטים PhoneScreen ו-WebWidget מציגים אותה וצריכים להתעדכן בכל שינוי. מהם התפקידים בתבנית Observer?",
      options: ["WeatherStation הוא Subject, ו-PhoneScreen ו-WebWidget הם Observers", "WeatherStation הוא Observer, ו-PhoneScreen ו-WebWidget הם Subjects", "WeatherStation הוא Invoker, ו-PhoneScreen ו-WebWidget הם Receivers", "WeatherStation הוא Factory, ו-PhoneScreen ו-WebWidget הם Products"], answer: 0,
      recap: "מי שמשתנה = Subject · מי שמגיב = Observer",
      explanation: "התחנה היא זו ש**משתנה**, ולכן **Subject**; שני המסכים **מגיבים** לשינוי, ולכן **Observers**. החלפת התפקידים היא המסיח הקבוע. Invoker ו-Receiver שייכים ל-Command, ו-Factory ו-Product ל-Factory." },
    { id: "P05-Q2", question: "מסך ניטור אחד (Dashboard) צריך לקבל עדכונים משתי תחנות שונות, StationA ו-StationB. כיצד נרשמים?",
      options: ["קוראים ל-Attach בכל אחת מהתחנות ומרשימים את אותו Dashboard", "אי אפשר: Observer יכול להיות רשום רק ב-Subject אחד", "קוראים ל-update בכל תחנה ומעבירים לה את ה-Dashboard", "מגדירים את ה-Dashboard כ-Subject ואת שתי התחנות כ-Observers שלו"], answer: 0,
      recap: "Observer אחד ב-Subjects רבים = Attach בכל Subject",
      explanation: "ההרשמה היא פעולה על ה-**Subject**, ולכן קוראים ל-`Attach` **בכל תחנה** ומעבירים את אותו Dashboard. אין מגבלה של Subject אחד, `update` היא הפעולה שה-Observer מקבל ולא פעולת הרשמה, והתחנות הן אלה שמשתנות ולכן הן ה-Subjects." },
    { id: "P05-Q3", question: "במערכת התראות, רק חלק מה-Observers צריכים לקבל עדכון על טמפרטורה קריטית, והשאר לא. איפה מתקבלת ההחלטה את מי לעדכן?",
      options: ["בפעולת notify של ה-Subject, שמסננת למי לשלוח", "בפעולת Attach של כל Observer, שמסננת את ה-Subjects", "בפעולת Detach, שמסירה את כל מי שלא צריך", "בתרשים המחלקות, לפני שהקוד נכתב"], answer: 0,
      recap: "סינון עדכונים נעשה ב-notify של ה-Subject",
      explanation: "ה-Subject הוא שמחזיק את הרשימה וקורא ל-`notify`, ולכן שם נעשה **הסינון**: למי לשלוח ואיזה מידע. Attach ו-Detach מנהלות את הרשימה ולא מחליטות לגבי כל עדכון, ותרשים המחלקות מתאר מבנה ולא החלטות בזמן ריצה." },
    { ref: "24B-B-Q7", recap: "חץ הורשה ב-Observer: בין Observer מופשט ל-Observer קונקרטי" },
    { ref: "25F0a-Q10", recap: "StockPriceTracker = Subject, הרכיבים שמגיבים = Observers" },
  ],
});
