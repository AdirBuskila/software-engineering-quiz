/* Design-patterns course · level 7 - MVC: Model, View, Controller, who talks to whom */
SE_LEVEL("pat", {
  id: "P07", order: 7, icon: "🖥️", title: "MVC: Model, View ו-Controller",
  goal: "לשבץ מחלקות בשלוש השכבות של MVC, לדעת איך המידע זורם ביניהן, ולהסביר למה קל להחליף תצוגה.",
  lesson: { html: `
<p><strong>MVC</strong> מפרידה אפליקציה לשלוש שכבות. היא שימושית בעיקר למערכות עם <b>ממשק משתמש מורכב</b> (19B-B-Q8).</p>
<table>
<thead><tr><th>שכבה</th><th>אחריות</th><th>דוגמה</th></tr></thead>
<tbody>
<tr><td><b>Model</b></td><td>הנתונים והלוגיקה העסקית (24B-B-Q11)</td><td>האובייקט <code>Ticket</code>, עגלת הקניות</td></tr>
<tr><td><b>View</b></td><td>הצגת הנתונים למשתמש, בלי לוגיקה עסקית</td><td>מסך "פתיחת תקלה"</td></tr>
<tr><td><b>Controller</b></td><td>מקבל פעולות משתמש ו<b>מעדכן את ה-Model</b></td><td><code>TicketController</code></td></tr>
</tbody></table>
<div class="lesson-rule">🔑 <strong>הזרימה:</strong> המשתמש פועל על ה-View ← ה-View מעביר ל-Controller ← ה-Controller מעדכן את ה-Model ← ה-Model מחזיר דרך ה-Controller להצגה. ה-View וה-Model <b>לא מדברים ישירות</b> (SP-DGM-Q15: <code>view ⟷ controller ⟷ model</code>).</div>
<p><b>היתרון:</b> הפרדת השכבות מאפשרת <b>להחליף את ה-View בקלות</b> (מסך מובייל במקום אתר) בלי לגעת בלוגיקה (25F0a-Q13). אבל השכבות עדיין קשורות זו לזו, ולכן צריך לתכנן כל אחת בקפידה. כשצריך להציג שינוי בנתונים על כמה תצוגות, משלבים MVC עם Observer: התצוגות נרשמות כ-Observers של ה-Model (25B-N-Q10).</p>
<div class="lesson-ex">דוגמה: משתמש פותח קריאת שירות בטופס. <b>הטופס (<code>TicketForm</code>) = View</b>, הוא מעביר לחיצה על "שלח" ל-<b><code>TicketController</code></b>, ש<b>בודק את הנתונים ויוצר <code>Ticket</code> = Model</b> ושומר אותו (26B-A-Q14).</div>
<div class="lesson-trap">⚠️ <strong>לא מערבבים.</strong> "ה-View אחראי על הלוגיקה העסקית" ו"ה-Controller היא שכבה עצמאית שלא מתקשרת עם האחרות" שגויים: הלוגיקה והנתונים ב-Model, וה-Controller הוא החוליה בין השכבות.</div>
` },
  questions: [
    { id: "P07-Q1", question: "באפליקציית חנות: מסך \"עגלת הקניות\" (CartScreen), המחלקה CartController שמטפלת בלחיצה על \"הוסף\", והמחלקה Cart שמחזיקה את הפריטים והחישוב של הסכום. מה החלוקה ל-MVC?",
      options: ["View: CartScreen · Controller: CartController · Model: Cart", "View: Cart · Controller: CartScreen · Model: CartController", "View: CartController · Controller: Cart · Model: CartScreen", "View: Cart · Controller: CartController · Model: CartScreen"], answer: 0,
      recap: "מסך = View · מטפל בפעולות משתמש = Controller · נתונים ולוגיקה = Model",
      explanation: "המסך מציג ← **View**; `CartController` מקבל את הלחיצה ומעדכן ← **Controller**; `Cart` מחזיקה את הפריטים ואת חישוב הסכום ← **Model**. שאר האפשרויות מחליפות תפקידים." },
    { id: "P07-Q2", question: "המשתמש לוחץ על כפתור \"הוסף לעגלה\". לפי MVC, מי מקבל את הלחיצה ומעדכן את הנתונים?",
      options: ["ה-Controller מקבל את הפעולה ומעדכן את ה-Model", "ה-View מעדכן ישירות את ה-Model", "ה-Model מעדכן את ה-Controller ואז את עצמו", "ה-Factory יוצר Controller חדש לכל לחיצה"], answer: 0,
      recap: "View ← Controller ← עדכון Model: ה-View לא מעדכן את ה-Model ישירות",
      explanation: "זרימת MVC: פעולה ב-View ← **Controller** ← **עדכון ה-Model**. ה-View לא מדבר ישירות עם ה-Model (SP-DGM-Q15). ה-Model לא יוזם את העדכון הזה, ו-Factory אינה חלק מהתבנית." },
    { id: "P07-Q3", question: "מפתחים אפליקציית רשימת משימות עם מסך ווב, וכעת רוצים להוסיף מסך לנייד. למה MVC מקלה על כך?",
      options: ["כי הפרדת השכבות מאפשרת להחליף או להוסיף View בלי לשנות את ה-Model", "כי ה-Model וה-View הם אותה מחלקה, ולכן שינוי אחד משנה את השניים", "כי ה-Controller הוא Singleton ולכן כל התצוגות משתמשות בו", "כי MVC מבטיחה שלא ייווצר אף באג בשכבת התצוגה"], answer: 0,
      recap: "הפרדת שכבות = קל להחליף את ה-View",
      explanation: "היתרון הוא ה**הפרדה**: הנתונים והלוגיקה ב-Model, ולכן אפשר להוסיף View חדש בלי לשנות אותו (25F0a-Q13). ה-Model וה-View בנפרד, ה-Controller אינו Singleton בהגדרה, ושום תבנית לא מבטיחה היעדר באגים." },
    { ref: "19B-B-Q8", recap: "MVC שימושית בעיקר למערכות עם ממשק משתמש מורכב" },
    { ref: "SP-DGM-Q15", recap: "זרימה: view ⟷ controller ⟷ model" },
  ],
});
