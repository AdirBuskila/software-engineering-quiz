/* Course registry for the guided "צריך עזרה?" sections.
   Each level file (courses/<course>/<ID>.js) calls SE_LEVEL("<course>", {...}); levels are kept
   sorted by `order`. course-ui.js renders them; tools/course_check.js lints them. */
window.COURSES = window.COURSES || {};
window.SE_LEVEL = function(courseId, level){
  const c = window.COURSES[courseId] || (window.COURSES[courseId] = { levels: [] });
  c.levels.push(level);
  c.levels.sort((a, b) => a.order - b.order);
};
