/* Testing course · level 1 - test levels: inspection, unit, integration (subsystem), and why "zero bugs" is never promised */
SE_LEVEL("tst", {
  id: "T01", order: 1, icon: "🧱", title: "רמות בדיקה: יחידה, שילוב, מערכת וסקירה",
  goal: "להבדיל בין בדיקת יחידה, שילוב, מערכת, קבלה וסקירה (Inspection), ולהסביר למה בדיקות לא מבטיחות אפס שגיאות.",
  lesson: { html: `
<p><strong>בדיקות תוכנה</strong> מחפשות שגיאות בשלבים שונים של הפיתוח. כל רמה בודקת גודל אחר של המערכת:</p>
<table>
<thead><tr><th>הרמה</th><th>מה בודקים</th><th>מי כותב או מריץ</th></tr></thead>
<tbody>
<tr><td><b>Inspection</b> (סקירה)</td><td>קוד או מסמכים <b>בלי להריץ</b></td><td>בני אדם; אוטומציה כמעט לא קיימת כאן (21-A-Q5)</td></tr>
<tr><td><b>Unit test</b></td><td><b>יחידת תוכנה קטנה</b>: מחלקה או מתודה (24B-A-Q20)</td><td>מפתחים, עם ספריית JUnit</td></tr>
<tr><td><b>Integration / Subsystem</b></td><td>שילוב של יחידות שכבר נבדקו כל אחת לחוד (24S-A-Q19)</td><td>מפתחים או צוות בדיקות</td></tr>
<tr><td><b>System test</b></td><td>המערכת השלמה</td><td>צוות בדיקות</td></tr>
<tr><td><b>Acceptance test</b></td><td>האם המערכת עונה על דרישות הלקוח</td><td>הלקוח או נציגו</td></tr>
</tbody></table>
<p>בדיקות תת-מערכת נקראות גם <b>בדיקות אינטגרציה</b> כי תת-מערכת בנויה מיותר מיחידה אחת (25F0a-Q19).</p>
<div class="lesson-rule">🔑 <strong>גודל הנבדק קובע את שם הבדיקה:</strong> יחידה אחת = Unit. כמה יחידות ביחד = Integration. הכל = System. מול הלקוח = Acceptance. בלי להריץ = Inspection, ולכן JUnit לא מתאימה לה (21-B-Q7).</div>
<div class="lesson-ex">דוגמה: <code>OrderService</code> ו-<code>PaymentService</code> נבדקו כל אחת לחוד (Unit). עכשיו כותבים בדיקה שמריצה את שתיהן יחד: הזמנה שעוברת דרך התשלום. זו בדיקת <b>Integration</b>.</div>
<div class="lesson-trap">⚠️ <strong>"אין אף פעם הבטחה של אפס שגיאות"</strong> (24B-A-Q21). גם אחרי בדיקות שילוב אפשר למצוא שגיאה (24B-B-Q25). משתדלים לכסות את כל השגיאות האפשריות, אבל אין הבטחה מלאה, ולא "רק למערכות חומרה" יש אפס שגיאות.</div>
` },
  questions: [
    { id: "T01-Q1", question: "איזו בדיקה נעשית על קוד או מסמך בלי להריץ אותם?",
      options: ["Inspection (סקירה)", "Unit test", "Integration test", "System test"], answer: 0,
      recap: "בלי הרצה = Inspection (בדיקה סטטית)",
      explanation: "**Inspection** היא סקירה סטטית: קוראים את הקוד או המסמך **בלי להריץ**. כל השאר (Unit, Integration, System) מריצות את התוכנה." },
    { id: "T01-Q2", question: "כל אחת מהמחלקות OrderService ו-PaymentService נבדקה בנפרד ועברה. כעת כותבים בדיקה שמזמינה מוצר ומעבירה אותו דרך שתי המחלקות יחד. איזו בדיקה זו?",
      options: ["Integration test", "Unit test", "Acceptance test", "Inspection"], answer: 0,
      recap: "שילוב של יחידות שנבדקו בנפרד = Integration",
      explanation: "שילוב **שתי יחידות שכבר נבדקו** הוא **Integration**. Unit בודקת יחידה אחת בבידוד, Acceptance נעשית מול הלקוח ו-Inspection לא מריצה קוד." },
    { id: "T01-Q3", question: "כל הבדיקות של מערכת עברו בהצלחה, כולל בדיקות שילוב. האם אפשר להבטיח שאין בה אף שגיאה?",
      options: ["לא, אין הבטחה מלאה של אפס שגיאות", "כן, בדיקות שילוב מבטיחות אפס שגיאות", "כן, אבל רק במערכות תוכנה ולא בחומרה", "תלוי אם הבדיקות נכתבו ב-JUnit"], answer: 0,
      recap: "בדיקות מצמצמות שגיאות ולא מבטיחות אפס",
      explanation: "בדיקות **מוצאות שגיאות אבל לא מוכיחות שאין**: אין הבטחה מלאה של אפס שגיאות. השימוש ב-JUnit או סוג המערכת לא משנים זאת." },
    { ref: "25F0a-Q19", recap: "בדיקות תת-מערכת = בדיקות אינטגרציה, כי תת-מערכת בנויה מיותר מיחידה אחת" },
    { ref: "21-A-Q5", recap: "בדיקות אוטומטיות ברוב המקרים אינן חלק מ-Inspection" },
  ],
});
