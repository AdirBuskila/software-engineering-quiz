/* Testing course · level 8 - boss: real exam questions on testing */
SE_LEVEL("tst", {
  id: "T08", order: 8, icon: "🏆", title: "מבחן גמר: בדיקות תוכנה", boss: true,
  goal: "שש שאלות אמיתיות מהמבחנים על JUnit, Mock, ערכי גבול, מודל V וסדר הבדיקות.",
  lesson: { html: `
<p>מבחן הגמר: שש שאלות אמיתיות מהמבחנים בלי רמזים. הנה הקורס בטבלה אחת.</p>
<table>
<thead><tr><th>הנושא</th><th>מה חייבים לזכור</th></tr></thead>
<tbody>
<tr><td>רמות בדיקה</td><td>Inspection ראשונה (בלי הרצה) · Unit · Integration · System · Acceptance</td></tr>
<tr><td>מודל V</td><td>מתכננים לפי שלב, מבצעים אחרי קידוד · קבלה מתוכננת ראשונה ומבוצעת אחרונה · יחידה מבוצעת ראשונה</td></tr>
<tr><td>JUnit</td><td>הכנה ב-setup · פעולה ב-@Test · ניקוי ב-tearDown · assertEquals(expected, actual)</td></tr>
<tr><td>Mock</td><td>מחליף את התלות, לא את היחידה הנבדקת</td></tr>
<tr><td>תכנון בדיקות</td><td>ערכי גבול משני צדי כל סף</td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>לפני שעונים:</strong> שואלים "מה גודל הנבדק?" (יחידה, שילוב, מערכת) ו"מי מוכן ראשון?" (תכנון מול ביצוע). רוב השאלות נסגרות על ארבע השאלות האלה.</div>
<div class="lesson-ex">דוגמה: "אילו בדיקות, ברוב המקרים, יבוצעו קודם מבחינת ציר הזמן של הפיתוח?" ← קודם כל סקירה (Inspection), כי היא לא צריכה קוד שרץ, ואחריה בדיקות יחידה. ומאותה סיבה JUnit, שמריצה קוד, לא מתאימה ל-Inspection (21-B-Q7).</div>
<div class="lesson-trap">⚠️ <strong>"נכון לגבי ביצוע" מול "נכון לגבי תכנון".</strong> בשאלות על מודל V שימו לב לשאלה מה מתבקש: מתי הבדיקה <b>מתוכננת</b> ומתי היא <b>מבוצעת</b>.</div>
` },
  questions: [
    { ref: "24B-A-Q23", recap: "קודם כל Inspection (בלי הרצה), אחר כך שאר הבדיקות" },
    { ref: "25S-A-Q5", recap: "מודל V: קבלה מתוכננת ראשונה ומבוצעת אחרונה" },
    { ref: "25F0a-Q6", recap: "במודל V בדיקות היחידה מבוצעות ראשונות" },
    { ref: "23B-A-Q5", recap: "חיבור לשרת ב-setup, חישובים ב-@Test, סגירה ב-tearDown" },
    { ref: "26S-A-Q20", recap: "Mock של התלות (AIService) ולא של היחידה הנבדקת" },
    { ref: "26CL-Q19", recap: "ערכי גבול: סמוכים לסף משני צדיו" },
  ],
});
