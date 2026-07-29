const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');

// Extract script text
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/i);
if (scriptMatch) {
    try {
        new Function(scriptMatch[1]);
        console.log("Script compilation SUCCESSFUL!");
    } catch (e) {
        console.error("Script SYNTAX ERROR:", e);
    }
}
