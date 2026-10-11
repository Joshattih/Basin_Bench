// Build the running Basin Bench deck: slides/basin_bench.pptx. Re-run after every milestone.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "Joshua Attih";
pres.title = "Basin Bench";

const NAVY = "0B2A4A", TEAL = "1C7293", WHITE = "FFFFFF", INK = "1A1A1A", MIST = "E6EFF5", ICE = "9FD3E8";
const F = "Arial";
const num = (s, n, color) => s.addText(String(n), { x: 12.3, y: 6.9, w: 0.8, h: 0.4, fontSize: 18, color, fontFace: F, align: "right", margin: 0, isTextBox: true });

// Slide 1: the question
let s = pres.addSlide();
s.background = { color: NAVY };
s.addText("BASIN BENCH", { x: 0.8, y: 0.9, w: 11.7, h: 1.0, fontSize: 40, bold: true, color: ICE, fontFace: F, margin: 0, isTextBox: true });
s.addText("Does physics make a machine learning model better at predicting rivers?",
  { x: 0.8, y: 2.2, w: 11.7, h: 3.0, fontSize: 60, bold: true, color: WHITE, fontFace: F, margin: 0, valign: "top", isTextBox: true });
s.addText("671 US rivers.   Three models.   One fair test.", { x: 0.8, y: 5.6, w: 11.7, h: 0.8, fontSize: 32, color: ICE, fontFace: F, margin: 0, isTextBox: true });
num(s, 1, ICE);
s.addNotes("Read the question slowly. Pause. Rivers are hard to predict. We ask one thing: when a learning model is handed what a physics model knows, does it predict better.");

// Slide 2: three models, same rivers, one score each
s = pres.addSlide();
s.background = { color: WHITE };
s.addText("Three models. The same rivers. One score each.", { x: 0.8, y: 0.6, w: 11.7, h: 1.4, fontSize: 48, bold: true, color: NAVY, fontFace: F, margin: 0, isTextBox: true });
const cards = [["PHYSICS", "GR4J", "Keeps account of water in the soil"],
               ["LEARNER", "XGBoost", "Finds patterns in past weather"],
               ["BOTH", "Hybrid", "The learner, handed the physics account"]];
const x0 = 0.8, cw = 3.7, gap = 0.3;
cards.forEach(([kind, name, line], i) => {
  const x = x0 + i * (cw + gap), dark = i === 2, c = dark ? WHITE : NAVY;
  s.addShape(pres.ShapeType.roundRect, { x, y: 2.3, w: cw, h: 3.2, fill: { color: dark ? TEAL : MIST }, line: { color: dark ? TEAL : MIST }, rectRadius: 0.2 });
  s.addText(kind, { x: x + 0.3, y: 2.55, w: cw - 0.6, h: 0.5, fontSize: 20, bold: true, color: c, fontFace: F, margin: 0, isTextBox: true });
  s.addText(name, { x: x + 0.3, y: 3.05, w: cw - 0.6, h: 1.0, fontSize: 44, bold: true, color: c, fontFace: F, margin: 0, isTextBox: true });
  s.addText(line, { x: x + 0.3, y: 4.2, w: cw - 0.6, h: 1.2, fontSize: 22, color: c, fontFace: F, margin: 0, valign: "top", isTextBox: true });
});
s.addText("Every river gives every model one score. We compare the scores river by river.",
  { x: 0.8, y: 5.9, w: 11.7, h: 0.9, fontSize: 28, bold: true, color: TEAL, fontFace: F, margin: 0, isTextBox: true });
num(s, 2, NAVY);
s.addNotes("Three contestants. The physics model keeps a running account of soil water. The learner only sees patterns. The hybrid is the learner handed the physics account. Same rivers, same years, one score each. Pause. The comparison is river by river, which is what makes it fair.");

pres.writeFile({ fileName: "slides/basin_bench.pptx" }).then(f => console.log("saved", f));
