// End-to-end tests for Interview Prep BD (run: node e2e.mjs)
import { chromium } from 'playwright';
import fs from 'node:fs';

const APP = 'file:///home/claude/interview-prep/app/index.html';
const AXE = fs.readFileSync('/tmp/claude-0/e2e/node_modules/axe-core/axe.min.js', 'utf8');
const results = [];
let failures = 0;
function check(name, cond, detail) {
  results.push({ name, ok: !!cond, detail: detail == null ? '' : String(detail) });
  if (!cond) failures++;
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail != null ? '  — ' + detail : ''));
}

const browser = await chromium.launch();
async function newPage(opts = {}) {
  const ctx = await browser.newContext({ viewport: opts.viewport || { width: 1366, height: 900 }, reducedMotion: opts.reducedMotion || 'reduce', acceptDownloads: true });
  const page = await ctx.newPage();
  page._errors = [];
  page.on('pageerror', (e) => page._errors.push('pageerror: ' + e.message));
  page.on('console', (m) => { if ((m.type() === 'error') && !/ERR_TUNNEL|fonts\.g|net::ERR/.test(m.text())) page._errors.push('console: ' + m.text()); });
  return { ctx, page };
}
const hash = async (page, h) => { await page.evaluate((x) => { location.hash = x; }, h); await page.waitForTimeout(120); };
const state = (page) => page.evaluate(() => window.InterviewPrep.getState());
const bank = (page) => page.evaluate(() => window.QBANK.map((q) => ({ id: q.id, technology: q.technology, difficulty: q.difficulty, type: q.type, market: q.market })));

/* 1. Opens without a build step, no JS errors, all navigation works */
{
  const { ctx, page } = await newPage();
  await page.goto(APP);
  await page.waitForSelector('.hero');
  check('App opens from file:// and renders the dashboard', await page.locator('.hero h1').isVisible());
  const total = await page.evaluate(() => window.QBANK.length);
  check('Question bank loaded', total === 584, total + ' questions');
  const v = await page.evaluate(() => window.InterviewPrep.validate());
  check('Runtime validator reports no errors/warnings', v.errors.length === 0 && v.warnings.length === 0, v.errors.length + ' errors, ' + v.warnings.length + ' warnings');
  const statTotal = await page.locator('.stat', { hasText: 'Total questions' }).locator('.stat__value').textContent();
  check('Dashboard total comes from data', statTotal.trim() === String(total), statTotal);
  const answered = await page.locator('.stat', { hasText: 'Answered' }).first().locator('.stat__value').textContent();
  check('New user starts at zero progress', answered.trim() === '0');
  check('Getting-started state shown for new user', await page.locator('text=Getting started').isVisible());
  const navHrefs = await page.$$eval('#nav a', (as) => as.map((a) => a.getAttribute('href')));
  let navOk = 0;
  for (const href of navHrefs) {
    await page.click(`#nav a[href="${href}"]`);
    await page.waitForTimeout(100);
    const cur = await page.getAttribute(`#nav a[href="${href}"]`, 'aria-current');
    const h1 = await page.locator('#main h1, #main .empty h3').first().textContent().catch(() => '');
    if (cur === 'page' && h1 && h1.length > 1) navOk++;
  }
  check('Every sidebar navigation link works and shows the active state', navOk === navHrefs.length, navOk + '/' + navHrefs.length + ' links');
  const techLinks = await page.$$eval('#sidebarTechs a', (as) => as.length);
  check('Sidebar lists all 18 technology categories', techLinks === 18, techLinks);
  check('No JavaScript errors during navigation', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 2. Technology explorer, search (EN + BN), filters, counts, empty state */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/technologies');
  await page.waitForSelector('.tech-card');
  const data = await bank(page);
  const cards = await page.locator('.tech-card').count();
  check('Technology explorer shows 18 cards', cards === 18, cards);
  const jsCard = page.locator('.tech-card', { hasText: 'JavaScript' });
  const jsTotal = await jsCard.locator('.row strong').first().textContent();
  check('Technology card counts come from data', jsTotal.trim() === String(data.filter((q) => q.technology === 'javascript').length), 'JavaScript card: ' + jsTotal);
  await page.fill('input[type=search]', 'docker');
  await page.waitForTimeout(250);
  check('Technology search filters cards', (await page.locator('.tech-card').count()) === 1);
  await page.fill('input[type=search]', '');
  await page.waitForTimeout(250);
  await page.click('.tech-card:has-text("React") >> text=Start learning');
  await page.waitForTimeout(150);
  const countText = await page.locator('.results-count strong').first().textContent();
  check('Card "Start learning" opens that technology in the explorer', countText.trim() === String(data.filter((q) => q.technology === 'react').length) && page.url().includes('tech=react'), countText);

  await hash(page, '#/questions');
  await page.selectOption('#f-tech', '');
  await page.waitForTimeout(150);
  const count = async () => parseInt((await page.locator('.results-count strong').first().textContent()).trim(), 10);
  check('Explorer shows all questions with no filters', (await count()) === 584);
  await page.fill('#f-q', 'closure');
  await page.waitForTimeout(400);
  const en = await count();
  check('English search works', en > 0, '"closure" → ' + en);
  await page.fill('#f-q', 'পার্থক্য');
  await page.waitForTimeout(400);
  const bn = await count();
  check('Bangla search works', bn > 0, '"পার্থক্য" → ' + bn);
  await page.fill('#f-q', 'connection pool');
  await page.waitForTimeout(400);
  check('Multi-word search works', (await count()) > 0, '"connection pool" → ' + (await count()));
  await page.fill('#f-q', 'zzqxv-no-such-term');
  await page.waitForTimeout(400);
  check('Useful empty state when nothing matches', await page.locator('.empty', { hasText: 'No questions match' }).isVisible());
  await page.fill('#f-q', '');
  await page.waitForTimeout(400);
  await page.selectOption('#f-tech', 'javascript');
  await page.selectOption('#f-diff', 'hard');
  await page.waitForTimeout(200);
  const exp1 = data.filter((q) => q.technology === 'javascript' && q.difficulty === 'hard').length;
  check('Technology + difficulty filters combine', (await count()) === exp1, (await count()) + ' vs expected ' + exp1);
  await page.selectOption('#f-diff', '');
  await page.selectOption('#f-type', 'mcq');
  await page.waitForTimeout(200);
  const exp2 = data.filter((q) => q.technology === 'javascript' && q.type === 'mcq').length;
  check('Type filter combines with technology', (await count()) === exp2, (await count()) + ' vs ' + exp2);
  await page.selectOption('#f-tech', '');
  await page.selectOption('#f-type', '');
  await page.selectOption('#f-market', 'bangladesh');
  await page.waitForTimeout(200);
  const exp3 = data.filter((q) => q.market === 'bangladesh').length;
  check('Market filter works', (await count()) === exp3, (await count()) + ' vs ' + exp3);
  await page.click('text=Clear all filters');
  await page.waitForTimeout(200);
  check('Clear all filters resets the count', (await count()) === 584);
  await page.selectOption('#f-sort', 'diffDesc');
  await page.waitForTimeout(200);
  const firstDiff = await page.locator('.q-item').first().locator('.badge--extreme').count();
  check('Sort by difficulty (extreme first) works', firstDiff === 1);
  check('Pagination keeps the DOM small', (await page.locator('.q-item').count()) === 20);
  check('No JavaScript errors in explorer', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 3. Question detail: modes, reveal, bookmark/learned/review persistence, MCQ single scoring, language */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/q/js-010');
  await page.waitForSelector('.q-title');
  // Learning mode shows the answer immediately
  check('Learning mode shows the reference answer immediately', await page.locator('.answer-panel').isVisible());
  await page.click('.seg button:has-text("Interview")');
  await page.waitForTimeout(150);
  check('Interview mode hides the answer until revealed', (await page.locator('.answer-panel').count()) === 0 && await page.locator('text=Reveal answer').isVisible());
  await page.click('text=Reveal answer');
  await page.waitForTimeout(150);
  check('Reveal answer works without any delay', await page.locator('.answer-panel').isVisible());
  check('Version info, docs link and follow-ups render', await page.locator('text=Version information').isVisible() && (await page.locator('.ref-list a').count()) > 0);
  await page.click('.q-detail__aside button:has-text("Bookmark")');
  await page.click('.q-detail__aside button:has-text("Mark as learned")');
  await page.click('.q-detail__aside button:has-text("Flag for review")');
  await page.waitForTimeout(150);
  await page.click('.assess-btn--partial');
  await page.waitForTimeout(150);
  await page.click('.assess-btn--correct'); // re-assessing in the same view replaces, not duplicates
  await page.waitForTimeout(150);
  let st = await state(page);
  check('Bookmark, learned and review flags are independent', st.bookmarks.includes('js-010') && st.learnedQuestions.includes('js-010') && st.reviewQuestions.includes('js-010'));
  check('Re-assessing in one view does not double count', st.questionProgress['js-010'].history.length === 1 && st.questionProgress['js-010'].history[0].r === 'correct');
  await page.reload();
  await page.waitForSelector('.q-title');
  st = await state(page);
  check('Bookmarks/learned/assessment persist after reload', st.bookmarks.includes('js-010') && st.learnedQuestions.includes('js-010') && st.questionProgress['js-010'].history.length === 1);
  check('Interview-mode preference persists', st.preferences.mode === 'interview');
  await hash(page, '#/bookmarks');
  check('Bookmarks page lists the bookmarked question', (await page.locator('.q-item').count()) === 1);
  // Opening a question does not auto-mark it learned
  await hash(page, '#/q/css-001');
  st = await state(page);
  check('Opening a question does not mark it as learned', !st.learnedQuestions.includes('css-001'));
  // MCQ in detail view
  const mcqId = await page.evaluate(() => window.QBANK.find((q) => q.type === 'mcq' && q.technology === 'sql').id);
  await hash(page, '#/q/' + mcqId);
  await page.locator('.mcq-option').nth(0).click();
  await page.click('text=Submit answer');
  await page.waitForTimeout(150);
  check('MCQ is graded automatically and locked', (await page.locator('.mcq-option:disabled').count()) === 4 && (await page.locator('.mcq-option.is-correct').count()) === 1);
  // Switching language re-renders but must not allow re-scoring
  await page.locator('.topbar .seg button').nth(1).click();
  await page.waitForTimeout(150);
  st = await state(page);
  check('MCQ cannot be scored twice (language switch keeps the lock)', (await page.locator('.mcq-option:disabled').count()) === 4 && st.questionProgress[mcqId].history.length === 1);
  check('Bangla mode translates navigation and content', (await page.locator('#nav a[href="#/practice"]').textContent()).includes('প্র্যাকটিস') && /[ঀ-৿]/.test(await page.locator('.q-title').first().textContent()));
  await page.locator('.topbar .seg button').nth(2).click();
  await page.waitForTimeout(150);
  check('Both mode shows English and Bangla together', (await page.locator('.bi-label', { hasText: 'English' }).count()) > 0 && (await page.locator('.bi-label', { hasText: 'বাংলা' }).count()) > 0);
  await page.reload();
  await page.waitForSelector('.q-title');
  st = await state(page);
  check('Language preference persists', st.preferences.lang === 'both');
  check('No JavaScript errors in question detail', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 4. Practice session: scoring, skip, persistence across reload & language switch, results */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/practice');
  await page.waitForSelector('text=Start session');
  await page.click('button:has-text("Custom Practice")');
  await page.fill('#p-count', '4');
  await page.locator('.chip', { hasText: 'HTML' }).click();
  await page.locator('.chip', { hasText: 'Easy' }).click();
  await page.locator('.chip', { hasText: 'Conceptual' }).click();
  await page.waitForTimeout(150);
  const pool = await page.evaluate(() => window.QBANK.filter((q) => q.technology === 'html' && q.difficulty === 'easy' && q.type === 'conceptual').length);
  await page.click('button:has-text("Start session")');
  if (pool < 4) { await page.click('.modal .btn--primary'); }
  await page.waitForSelector('.session-top');
  let st = await state(page);
  const ids = st.activeSession.ids;
  check('Session uses only questions matching the configuration, without duplicates', ids.length === Math.min(4, pool) && new Set(ids).size === ids.length, ids.join(','));
  // Q1 correct
  await page.click('text=Reveal answer');
  await page.click('.assess-btn--correct');
  await page.waitForSelector('text=Question 2 of');
  // Reload mid-session → state preserved
  await page.reload();
  await page.waitForSelector('.session-top');
  check('Unfinished session survives a page reload', (await page.locator('text=Question 2 of').count()) === 1);
  // Language switch mid-session preserves position
  await page.locator('.topbar .seg button').nth(1).click();
  await page.waitForTimeout(150);
  st = await state(page);
  check('Language switch preserves the session position and answers', st.activeSession.index === 1 && st.activeSession.answers[ids[0]].result === 'correct');
  await page.locator('.topbar .seg button').nth(0).click();
  await page.waitForTimeout(150);
  // Q2 partial (keyboard: Space reveals, 2 = partial)
  await page.locator('#main').click({ position: { x: 5, y: 5 } }).catch(() => {});
  await page.keyboard.press('Space');
  await page.waitForTimeout(120);
  await page.keyboard.press('2');
  await page.waitForSelector('text=Question 3 of');
  check('Keyboard shortcuts reveal and assess', true);
  // Q3 incorrect
  await page.click('text=Reveal answer');
  await page.click('.assess-btn--incorrect');
  await page.waitForSelector('text=Question 4 of');
  // Q4 skip (without revealing)
  await page.click('.reveal button:has-text("Skip")');
  await page.waitForSelector('text=See results');
  await page.click('text=See results');
  await page.waitForSelector('.score-ring');
  st = await state(page);
  const s = st.sessions[st.sessions.length - 1];
  const sm = s.summary;
  check('Weighted score = earned ÷ available (easy=1: 1 + 0.5 + 0 + 0 of 4)', sm.earned === 1.5 && sm.possible === 4, sm.earned + '/' + sm.possible);
  check('Accuracy = correct ÷ answered, skips excluded (1/3)', Math.abs(sm.accuracy - 1 / 3) < 1e-9, sm.accuracy);
  check('Counts: correct 1, partial 1, incorrect 1, skipped 1', sm.correct === 1 && sm.partial === 1 && sm.incorrect === 1 && sm.skipped === 1);
  const ringText = await page.locator('.score-ring__label b').textContent();
  check('Results screen shows the weighted percentage', ringText.trim() === '38%', ringText);
  const accText = await page.locator('.stat', { hasText: 'Accuracy' }).locator('.stat__value').textContent();
  check('Results screen shows simple accuracy separately', accText.trim() === '33%', accText);
  check('Skipped answer recorded in progress history', st.questionProgress[ids[3]].history.slice(-1)[0].r === 'skipped');
  check('Session saved to history and active session cleared', st.sessions.length === 1 && st.activeSession === null);
  check('Results list questions to review (3 non-correct)', (await page.locator('.q-item').count()) === 3);
  check('Review Mistakes enabled when there are mistakes', await page.locator('button:has-text("Review mistakes")').isEnabled());
  // Incorrect + review pages reflect the session
  await hash(page, '#/incorrect');
  check('Incorrect Answers page lists the incorrect question', (await page.locator('.q-item').count()) === 1);
  await hash(page, '#/review');
  check('Spaced-review schedule queued the incorrect/partial answers', st.questionProgress[ids[2]].due != null && st.questionProgress[ids[1]].due != null && st.questionProgress[ids[0]].due == null);
  await hash(page, '#/dashboard');
  const accDash = await page.locator('.stat', { hasText: 'Accuracy' }).locator('.stat__value').textContent();
  check('Dashboard statistics update from recorded progress', accDash.trim() === '33%', accDash);
  await hash(page, '#/history');
  check('Study History lists the session', (await page.locator('table.table tbody tr').count()) === 1);
  check('No JavaScript errors in practice flow', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 5. MCQ session: no double scoring, Enter advances, fewer-than-requested handling */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/practice');
  await page.waitForSelector('text=Start session');
  await page.locator('.chip', { hasText: 'MCQ' }).click();
  await page.locator('.chip', { hasText: 'Docker' }).click();
  await page.locator('.chip', { hasText: 'Extreme' }).click(); // no extreme docker MCQs exist → zero match
  await page.waitForTimeout(150);
  check('Configuration with no matches is blocked with an explanation', await page.locator('text=No questions match this configuration').isVisible());
  await page.locator('.chip', { hasText: 'Extreme' }).click();
  await page.click('button:has-text("Deep Practice")'); // 30 requested
  await page.click('button:has-text("Start session")');
  await page.waitForSelector('.modal');
  check('Fewer-than-requested matches → offers the available number', await page.locator('.modal', { hasText: 'Only' }).isVisible());
  await page.click('.modal .btn--primary');
  await page.waitForSelector('.session-top');
  let st = await state(page);
  const id0 = st.activeSession.ids[0];
  await page.locator('.mcq-option').nth(1).click();
  await page.click('text=Submit answer');
  await page.waitForTimeout(150);
  await page.locator('.mcq-option').nth(2).click({ force: true }).catch(() => {});
  await page.keyboard.press('3');
  st = await state(page);
  check('MCQ in session scored exactly once', st.questionProgress[id0].history.length === 1 && st.activeSession.answers[id0].mcqChoice === 1);
  await page.keyboard.press('Enter');
  await page.waitForSelector('text=Question 2 of');
  await page.click('button:has-text("Previous")');
  await page.waitForSelector('text=Question 1 of');
  st = await state(page);
  check('Returning to an answered MCQ keeps it locked', (await page.locator('.mcq-option:disabled').count()) === 4 && st.questionProgress[id0].history.length === 1);
  // Finish early: unanswered count as skipped in the session summary only
  await page.click('button:has-text("End")');
  await page.waitForSelector('.modal');
  await page.click('.modal .btn--primary');
  await page.waitForSelector('.score-ring');
  st = await state(page);
  const sm = st.sessions[0].summary;
  check('Ending early counts unanswered questions as skipped', sm.skipped === sm.total - 1, sm.skipped + ' of ' + sm.total);
  check('No JavaScript errors in MCQ session', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 6. Timed session auto-submits; interview simulation; daily challenge; flashcards */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/interview');
  await page.waitForSelector('text=Start mock interview');
  await page.click('button:has-text("Start mock interview")');
  await page.waitForSelector('.session-top');
  let st = await state(page);
  check('Interview simulation starts with answers hidden and a time limit', (await page.locator('.answer-panel').count()) === 0 && st.activeSession.deadline != null && st.activeSession.kind === 'interview');
  const diffs = await page.evaluate((ids) => ids.map((id) => window.QBANK.find((q) => q.id === id).difficulty), st.activeSession.ids);
  const order = ['easy', 'medium', 'hard', 'extreme'];
  check('Interview questions progress from easier to harder', diffs.every((d, i) => i === 0 || order.indexOf(d) >= order.indexOf(diffs[i - 1])), diffs.join(','));
  check('Interview excludes MCQs by default', (await page.evaluate((ids) => ids.filter((id) => window.QBANK.find((q) => q.id === id).type === 'mcq').length, st.activeSession.ids)) === 0);
  await page.click('text=Reveal answer');
  await page.click('.assess-btn--correct');
  await page.waitForTimeout(200);
  // Simulate the time limit expiring
  await page.evaluate(() => { const k = 'ipbd:state'; const d = JSON.parse(localStorage.getItem(k)); d.activeSession.deadline = Date.now() - 1000; localStorage.setItem(k, JSON.stringify(d)); });
  await page.reload();
  await page.waitForSelector('.score-ring', { timeout: 5000 });
  st = await state(page);
  check('Timed session auto-submits when time runs out', st.activeSession === null && st.sessions.length === 1 && st.sessions[0].kind === 'interview');

  await hash(page, '#/daily');
  const dailyIds = await page.evaluate(() => { const d = new Date(); return d.toDateString(); });
  await page.click('button:has-text("Start challenge")');
  await page.waitForSelector('.session-top');
  st = await state(page);
  const n = st.activeSession.ids.length;
  check('Daily challenge has 3 questions', n === 3, n);
  for (let i = 0; i < n; i++) {
    if (await page.locator('.mcq-option').count()) { await page.locator('.mcq-option').nth(0).click(); await page.click('text=Submit answer'); await page.waitForTimeout(100); if (i < n - 1) await page.keyboard.press('Enter'); }
    else { await page.click('text=Reveal answer'); await page.click('.assess-btn--correct'); }
    await page.waitForTimeout(250);
  }
  await page.click('text=See results');
  await page.waitForSelector('.score-ring');
  st = await state(page);
  const key = Object.keys(st.daily)[0];
  check('Daily challenge completion stored by local date', !!key && /^\d{4}-\d{2}-\d{2}$/.test(key));
  // Daily set deterministic: reload page, same ids
  await hash(page, '#/daily');
  const sameIds = await page.evaluate(() => window.InterviewPrep.getState().sessions.slice(-1)[0].ids.join(','));
  await page.reload(); await page.waitForTimeout(200);
  check('Daily challenge view shows completed state', await page.locator('text=View results').isVisible());

  await hash(page, '#/flashcards');
  await page.waitForSelector('.flashcard');
  await page.click('.flashcard');
  check('Flashcard flips on click', (await page.getAttribute('.flashcard', 'aria-pressed')) === 'true');
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(150);
  check('Flashcard keyboard navigation', (await page.locator('text=Card 2 of').count()) === 1);
  check('No JavaScript errors in interview/daily/flashcards', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 7. Storage robustness: corrupted & incompatible data, export, import validation, reset confirmation */
{
  const { ctx, page } = await newPage();
  await page.goto(APP);
  await page.waitForSelector('.hero');
  await page.evaluate(() => localStorage.setItem('ipbd:state', '{"version":1, "bookmarks": [oops'));
  await page.reload();
  await page.waitForSelector('.hero');
  const backupKeys = await page.evaluate(() => Object.keys(localStorage).filter((k) => k.startsWith('ipbd:state:corrupt')));
  check('Corrupted storage does not crash; a backup copy is kept', backupKeys.length === 1 && page._errors.length === 0);
  check('User is told about the corrupted data', await page.locator('.callout', { hasText: 'unreadable' }).isVisible());
  await page.evaluate(() => localStorage.setItem('ipbd:state', JSON.stringify({ version: 99, bookmarks: ['x'] })));
  await page.reload();
  await page.waitForSelector('.hero');
  check('Incompatible future version handled without crashing', (await page.locator('.callout', { hasText: 'incompatible' }).count()) === 1);
  await page.evaluate(() => localStorage.setItem('ipbd:state', JSON.stringify({ bookmarks: ['js-001', 'html-001', 123, null], learned: ['css-002'], progress: { 'js-001': { history: [{ r: 'correct', at: Date.now() }, { r: 'bogus', at: 1 }] } } })));
  await page.reload();
  await page.waitForSelector('.hero');
  let st = await state(page);
  check('Unversioned data is migrated and sanitised', st.version === 1 && st.bookmarks.length === 2 && st.learnedQuestions[0] === 'css-002' && st.questionProgress['js-001'].history.length === 1);

  await hash(page, '#/settings');
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('button:has-text("Export JSON")')]);
  const exported = JSON.parse(fs.readFileSync(await dl.path(), 'utf8'));
  check('Export downloads a valid JSON backup', exported.app === 'interview-prep-bd' && exported.data.bookmarks.length === 2);
  // Invalid imports
  await page.setInputFiles('#importFile', { name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from('{not json') });
  await page.waitForTimeout(300);
  check('Malformed JSON import is rejected', await page.locator('.toast', { hasText: 'not valid JSON' }).isVisible());
  await page.setInputFiles('#importFile', { name: 'other.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify({ hello: 'world' })) });
  await page.waitForTimeout(300);
  check('Foreign JSON import is rejected', await page.locator('.toast', { hasText: 'not an Interview Prep BD backup' }).isVisible());
  st = await state(page);
  check('Rejected imports leave data unchanged', st.bookmarks.length === 2);
  // Valid import with confirmation
  const bk = JSON.parse(JSON.stringify(exported));
  bk.data.bookmarks = ['react-001', 'react-002', 'react-003', '<img src=x onerror=alert(1)>'];
  await page.setInputFiles('#importFile', { name: 'ok.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(bk)) });
  await page.waitForSelector('.modal[open]');
  check('Valid import asks for confirmation first', await page.locator('.modal', { hasText: 'Replace your data' }).isVisible());
  await page.click('.modal .btn--danger');
  await page.waitForTimeout(300);
  st = await state(page);
  check('Confirmed import replaces data', st.bookmarks.includes('react-003'));
  check('Imported strings are never rendered as HTML', (await page.evaluate(() => document.querySelectorAll('img[src="x"]').length)) === 0);
  // Reset requires confirmation
  await page.click('button:has-text("Reset progress")');
  await page.waitForSelector('.modal[open]');
  const disabled = await page.locator('.modal .btn--danger').isDisabled();
  check('Reset needs typed confirmation (button disabled until RESET typed)', disabled);
  await page.click('.modal button:has-text("Cancel")');
  await page.waitForTimeout(200);
  st = await state(page);
  check('Cancelling reset keeps data', st.bookmarks.length === 4);
  await page.click('button:has-text("Reset progress")');
  await page.waitForSelector('.modal[open]');
  await page.fill('.modal input', 'RESET');
  await page.click('.modal .btn--danger');
  await page.waitForTimeout(300);
  st = await state(page);
  check('Confirmed reset clears progress but keeps preferences', st.bookmarks.length === 0 && Object.keys(st.questionProgress).length === 0 && st.preferences.lang === 'en');
  check('No uncaught errors in storage tests', page._errors.length === 0, page._errors.join(' | '));
  await ctx.close();
}

/* 8. Planner, weak topics, theme, responsive layouts, mobile drawer */
{
  const { ctx, page } = await newPage();
  await page.goto(APP + '#/planner');
  await page.waitForSelector('#pl-target');
  await page.fill('#pl-target', '15');
  await page.click('button:has-text("Save")');
  await page.waitForTimeout(150);
  let st = await state(page);
  check('Study planner saves the daily target', st.planner.dailyTarget === 15);
  await page.fill('#pl-target', '0');
  await page.click('button:has-text("Save")');
  await page.waitForTimeout(150);
  st = await state(page);
  check('Invalid daily target rejected', st.planner.dailyTarget === 15);
  // Weak topics from recorded results
  await page.evaluate(() => {
    const k = 'ipbd:state'; const d = JSON.parse(localStorage.getItem(k));
    const ids = window.QBANK.filter((q) => q.technology === 'redis').slice(0, 2).map((q) => q.id);
    const sub = window.QBANK.find((q) => q.id === ids[0]).subtopic;
    const same = window.QBANK.filter((q) => q.technology === 'redis' && q.subtopic === sub).map((q) => q.id);
    same.forEach((id) => { d.questionProgress[id] = { history: [{ r: 'incorrect', at: Date.now() - 5000 }, { r: 'partial', at: Date.now() }], box: 1, due: Date.now() }; });
    localStorage.setItem(k, JSON.stringify(d));
  });
  await page.reload();
  await page.waitForTimeout(200);
  check('Weak topics are detected from recorded performance', (await page.locator('section.card', { hasText: 'Weak topics' }).locator('.badge--bad').count()) >= 1);
  await page.click('.topbar button[aria-label*="light theme"]');
  await page.waitForTimeout(100);
  st = await state(page);
  check('Theme toggle works and persists', st.preferences.theme === 'light' && (await page.getAttribute('html', 'data-theme')) === 'light');
  await ctx.close();

  // Responsive: no horizontal overflow on phone/tablet in EN, BN and Both
  for (const vp of [{ width: 390, height: 844 }, { width: 768, height: 1024 }]) {
    const { ctx: c2, page: p2 } = await newPage({ viewport: vp });
    await p2.goto(APP);
    await p2.waitForSelector('.hero');
    const routes = ['#/dashboard', '#/technologies', '#/questions', '#/q/sql-012', '#/q/docker-015', '#/practice', '#/interview', '#/bookmarks', '#/incorrect', '#/review', '#/history', '#/planner', '#/settings', '#/flashcards', '#/daily', '#/sources'];
    let worst = 0, worstRoute = '';
    for (const lang of ['EN', 'বাংলা', 'Both']) {
      await p2.locator('.topbar .seg button').nth(['EN', 'বাংলা', 'Both'].indexOf(lang)).click();
      for (const r of routes) {
        await hash(p2, r);
        const ov = await p2.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
        if (ov > worst) { worst = ov; worstRoute = lang + ' ' + r; }
      }
    }
    check(`No horizontal page overflow at ${vp.width}px (EN/BN/Both, 16 routes)`, worst <= 0, worst ? worst + 'px on ' + worstRoute : 'none');
    if (vp.width === 390) {
      await hash(p2, '#/dashboard');
      await p2.click('#menuBtn');
      await p2.waitForTimeout(300);
      const visible = await p2.evaluate(() => document.getElementById('app').classList.contains('is-nav-open'));
      await p2.keyboard.press('Escape');
      await p2.waitForTimeout(200);
      const closed = await p2.evaluate(() => !document.getElementById('app').classList.contains('is-nav-open'));
      check('Mobile navigation drawer opens and closes with Escape', visible && closed);
      const small = await p2.$$eval('.btn, .icon-btn, .chip', (els) => els.filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 30; }).length);
      check('Touch targets are at least ~30px tall on mobile', small === 0, small + ' small controls');
    }
    check(`No JavaScript errors at ${vp.width}px`, p2._errors.length === 0, p2._errors.join(' | '));
    await c2.close();
  }
}

/* 9. Accessibility audit (axe-core) and reduced motion */
{
  const { ctx, page } = await newPage({ reducedMotion: 'reduce' });
  await page.goto(APP);
  await page.waitForSelector('.hero');
  const dur = await page.evaluate(() => getComputedStyle(document.querySelector('.hero')).animationDuration + '|' + getComputedStyle(document.querySelector('.btn')).transitionDuration);
  check('prefers-reduced-motion disables animations', dur.split('|').every((x) => parseFloat(x) < 0.01), dur);
  const routes = ['#/dashboard', '#/technologies', '#/questions', '#/q/js-005', '#/q/sql-012', '#/practice', '#/settings', '#/sources'];
  const all = {};
  for (const r of routes) {
    await hash(page, r);
    await page.addScriptTag({ content: AXE }).catch(() => {});
    const res = await page.evaluate(async () => {
      const out = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] }, resultTypes: ['violations'] });
      return out.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, sample: v.nodes[0] && v.nodes[0].target.join(' ') }));
    });
    for (const v of res) { const k = v.id; all[k] = all[k] || { impact: v.impact, n: 0, routes: [], sample: v.sample }; all[k].n += v.n; all[k].routes.push(r); }
  }
  // Same audit in the light theme (reload so the preference applies)
  await page.evaluate(() => { const k = 'ipbd:state'; const d = JSON.parse(localStorage.getItem(k) || '{}'); d.version = 1; d.preferences = Object.assign({}, d.preferences, { theme: 'light', lang: 'both' }); localStorage.setItem(k, JSON.stringify(d)); });
  for (const r of routes) {
    await page.goto(APP + r); await page.waitForTimeout(150);
    await page.addScriptTag({ content: AXE }).catch(() => {});
    const res = await page.evaluate(async () => {
      const out = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] }, resultTypes: ['violations'] });
      return out.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, sample: v.nodes[0] && v.nodes[0].target.join(' ') }));
    });
    for (const v of res) { const k = 'light:' + v.id; all[k] = all[k] || { impact: v.impact, n: 0, routes: [], sample: v.sample }; all[k].n += v.n; all[k].routes.push(r); }
  }
  const serious = Object.entries(all).filter(([, v]) => v.impact === 'critical' || v.impact === 'serious');
  check('axe-core: no critical/serious WCAG 2 A/AA violations (8 screens × dark + light, Both-language mode)', serious.length === 0, JSON.stringify(serious));
  if (Object.keys(all).length) console.log('   axe (all impacts):', JSON.stringify(all));
  await ctx.close();
}

await browser.close();
fs.writeFileSync('/tmp/claude-0/e2e/results.json', JSON.stringify(results, null, 2));
console.log(`\n${results.length - failures}/${results.length} checks passed`);
process.exit(failures ? 1 : 0);
