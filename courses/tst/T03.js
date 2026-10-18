/* Testing course · level 3 - JUnit: @BeforeEach, @Test, @AfterEach, asserts, and where each step belongs */
SE_LEVEL("tst", {
  id: "T03", order: 3, icon: "🧰", title: "JUnit: setup, test ו-tearDown",
  goal: "לדעת מתי רצה כל אנוטציה של JUnit, מה הפרמטרים של assertEquals, ולשבץ את שלבי הבדיקה במקום הנכון.",
  lesson: { html: `
<p><strong>JUnit</strong> היא ספרייה לבדיקות יחידה ב-Java. מחלקת בדיקה מכילה מתודות עם אנוטציות:</p>
<table>
<thead><tr><th>אנוטציה</th><th>מתי היא רצה</th><th>למה משמשת</th></tr></thead>
<tbody>
<tr><td><code>@Test</code></td><td>מריצה את המתודה כ-test case (SP-DGM-Q4)</td><td>הבדיקה עצמה</td></tr>
<tr><td><code>@BeforeEach</code> (או <code>@Before</code>)</td><td><b>פעם אחת לפני כל טסט</b> (20-B-Q4)</td><td>setup: יצירת נתונים, פתיחת חיבור</td></tr>
<tr><td><code>@AfterEach</code> (או <code>@After</code>)</td><td><b>פעם אחת אחרי כל טסט</b> (19B-B-Q10)</td><td>tearDown: סגירה וניקוי</td></tr>
</tbody></table>
<p>בתוך הטסט מוסיפים בדיקות <b>assert</b>. ב-<code>assertEquals</code> מועברים <b>הערך המצופה (expected) ואז הערך האמיתי (actual)</b> (24B-B-Q22). <code>assertTrue</code> בודקת שמשתנה בוליאני הוא אמת (24B-A-Q19).</p>
<pre class="lesson-code" dir="ltr"><code>@BeforeEach void setUp()   { calc = new Calc(); }
@Test       void adds()    { assertEquals(5, calc.add(2, 3)); }
@AfterEach  void tearDown(){ calc = null; }</code></pre>
<div class="lesson-rule">🔑 <strong>איפה כל שלב?</strong> מה שצריך <b>לפני</b> הבדיקה (יצירת מידע, פתיחת חיבור או קובץ) ב-setup. מה שמבצעים ובודקים ב-<code>@Test</code>. מה ש<b>סוגרים אחרי</b> (קובץ, חיבור) ב-tearDown. כך כל טסט מתחיל מאותו מצב נקי, ותמיד מנקים אחריו (22S-A-Q2, 24S-A-Q17).</div>
<div class="lesson-ex">דוגמה: בדיקת פונקציה שמשתמשת בקובץ. פותחים וקוראים את הקובץ ב-<code>@BeforeEach</code>, מפעילים את הפונקציה ב-<code>@Test</code>, וסוגרים את הקובץ ב-<code>@AfterEach</code>. אם יש שלוש מתודות <code>@Test</code> במחלקה, ה-setup וה-tearDown ירוצו <b>שלוש פעמים כל אחד</b>.</div>
<div class="lesson-trap">⚠️ <strong>אנוטציות "לפני הכל" ו"אחרי הכל".</strong> <code>@BeforeEach</code> ו-<code>@AfterEach</code> רצות סביב <b>כל</b> טסט. המסיחים "פעם אחת לפני הרצת כל הטסטים" מתארים אנוטציות אחרות (<code>@BeforeAll</code>), לא את מה שנשאל.</div>
` },
  questions: [
    { id: "T03-Q1", question: "במחלקת בדיקה יש מתודת `@BeforeEach` אחת, מתודת `@AfterEach` אחת ושלוש מתודות `@Test`. כמה פעמים תרוץ מתודת ה-`@BeforeEach` בהרצת כל המחלקה?",
      options: ["3", "1", "4", "0"], answer: 0,
      recap: "@BeforeEach רצה פעם אחת לפני כל טסט",
      explanation: "`@BeforeEach` רצה **לפני כל טסט**, ולכן שלוש פעמים לשלושה טסטים (וכך גם `@AfterEach`). הערך 1 מתאים ל-`@BeforeAll`, ו-4 או 0 אינם נובעים מהכלל." },
    { id: "T03-Q2", question: "בבדיקת מחלקה Cart צריך: ליצור עגלה עם שני פריטים, להפעיל את total() ולוודא את הסכום, ולנקות קובץ זמני שנוצר. מה השימוש הנכון בספריית הבדיקות?",
      options: ["יוצרים את העגלה ב-setup, מפעילים total() ובודקים ב-@Test, ומנקים את הקובץ ב-tearDown", "מפעילים total() ב-setup, יוצרים את העגלה ב-@Test, ומנקים את הקובץ ב-tearDown", "יוצרים את העגלה ב-tearDown, מפעילים total() ב-@Test, ומנקים את הקובץ ב-setup", "יוצרים את העגלה ב-@Test, מנקים את הקובץ ב-setup, ומפעילים total() ב-tearDown"], answer: 0,
      recap: "הכנה ב-setup · פעולה ובדיקה ב-@Test · ניקוי ב-tearDown",
      explanation: "הכנה (יצירת העגלה) ב-**setup**, פעולה ובדיקה ב-**@Test**, וניקוי (הקובץ) ב-**tearDown**. כל סדר אחר מפעיל את `total()` לפני שנוצרה עגלה, או מנקה לפני שהשתמשו." },
    { id: "T03-Q3", question: "נכתבה הבדיקה `assertEquals(7, calc.add(2, 3));` כאשר `add` מחזירה את סכום הפרמטרים. מה תהיה התוצאה?",
      options: ["הבדיקה נכשלת: הערך המצופה 7 שונה מהערך האמיתי 5", "הבדיקה עוברת, כי 2 ועוד 3 קרוב ל-7", "הבדיקה נכשלת בקומפילציה כי חסר פרמטר שלישי", "הבדיקה עוברת, כי assertEquals בודקת רק אם הערך שונה מאפס"], answer: 0,
      recap: "assertEquals(expected, actual): נכשלת כשהערכים שונים",
      explanation: "הפרמטר הראשון הוא **המצופה (7)** והשני **האמיתי (5)**. הם שונים ← **הבדיקה נכשלת**. אין קירוב ואין פרמטר שלישי חובה, ו-`assertEquals` משווה ערכים ולא בודקת שונות מאפס." },
    { ref: "20-B-Q4", recap: "@BeforeEach / @Before רצה פעם אחת לפני כל טסט" },
    { ref: "24B-A-Q19", recap: "assertTrue בודקת שמשתנה בוליאני הוא אמת" },
  ],
});
