const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');

const dom = new JSDOM(html, {
    runScripts: "dangerously",
    resources: "usable"
});

const win = dom.window;
const doc = win.document;

// Trigger DOMContentLoaded
const event = new win.Event('DOMContentLoaded');
doc.dispatchEvent(event);

setTimeout(() => {
    const container = doc.getElementById('quizCardsContainer');
    console.log("=== QUIZ CARDS CONTAINER INNER HTML ===");
    console.log(container ? container.innerHTML : "CONTAINER IS NULL!");
    console.log("=========================================");
    console.log("activeQuizzesList length:", win.activeQuizzesList ? win.activeQuizzesList.length : "UNDEFINED");
}, 500);
