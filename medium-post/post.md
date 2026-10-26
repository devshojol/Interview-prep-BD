# I Built a Free Interview Prep App for Developers in Bangladesh, in English and বাংলা

**Subtitle:** 834 questions across 19 technologies, with a quick answer for revision, a deep answer for the follow-ups, and spaced review for what you got wrong. Free, no account.

**Tags (Medium allows 5):** Interview Preparation · JavaScript · React Native · Web Development · Bangladesh

---

[IMAGE 01-cover.png]

A few weeks before an interview, most of us do the same thing. We open a folder of PDFs someone shared in a Facebook group ("Top 50 React Interview Questions", "JS notes"), read the answers, nod, and feel ready.

Then the interviewer asks a follow-up.

*"Okay, `useEffect` runs after render. Why did your effect run twice?"*
*"You said `WHERE` filters rows. So why can't you use `COUNT(*)` in it?"*

A one-line answer you memorised doesn't survive that second question. And if you think through technical ideas half in Bangla and half in English, like most developers here do, an English-only explanation is one more thing to translate in your head under pressure.

So I built **Interview Prep BD**: a free, bilingual practice app that helps you *say* the answer, not just read it.

👉 **Try it:** [devshojol.github.io/Interview-prep-BD](https://devshojol.github.io/Interview-prep-BD/)
👉 **Source code:** [github.com/devshojol/Interview-prep-BD](https://github.com/devshojol/Interview-prep-BD)

## What's inside

- **834 questions across 19 technologies:** HTML, CSS, JavaScript, React, Next.js, **React Native (with Expo and SQLite)**, Node.js, Express, NestJS, MongoDB, Mongoose, PostgreSQL, SQL, Drizzle ORM, Redis, Vector Databases, Docker, NGINX and AWS.
- **A behavioural & projects section:** "Tell me about yourself", "Walk me through your project", "What's the hardest bug you've fixed?", and more.
- **Every question in English, বাংলা, or both side by side.**
- **Four levels:** Easy, Medium, Hard and Extreme, from viva-style fundamentals to senior system design.
- **A voice interviewer** that reads questions aloud in English, so practice sounds like the real thing.

## 1. A quick answer first, the deep answer below

Every question has two layers.

The **quick answer** is 1–3 plain sentences: the thing you'd say first in an interview. It's perfect for revising the night before.

The **full answer** below it explains *why* it works, with code, common mistakes, an interview tip and the follow-up questions an interviewer is likely to ask next. That's the part that gets you through the second and third question.

[IMAGE 02-quick-and-full-answer-bilingual.png]
*Caption: The quick answer on top, the full answer below, here in English and Bangla side by side.*

## 2. Real Bangla, not machine translation

The Bangla is written the way developers here actually talk. Technical terms stay in English (`closure`, `event loop`, `index`), and the explanation around them is natural Bangla. You can switch between English, বাংলা and Both at any time, on desktop or phone.

[IMAGE 03-bangla-on-mobile.png]
*Caption: A quick-recall SQL question in Bangla on a phone.*

## 3. Quick recall for written tests and viva rounds

Many interviews here start with an MCQ test or a "viva", rapid fundamental questions. For that, each technology has **10 quick-recall questions** with short, plain answers and a tiny code example:

- What is hoisting, and how do `var`, `let` and `const` differ?
- `call` vs `apply` vs `bind`?
- `WHERE` vs `HAVING`?
- `app.use()` vs `app.get()` in Express?
- `find()` vs `findOne()` vs `findById()` in Mongoose?
- What is Metro, and what is Hermes, in React Native?

There's a dedicated flashcard deck for them too. Shuffle and flip through 190 cards on the bus.

## 4. Practise like it's the real interview

Reading answers feels productive, but it isn't practice. The app is built around one habit: **answer out loud first, then check.**

- **Interview mode** hides the answer until you reveal it.
- You **grade yourself honestly**: correct, partially correct or incorrect.
- **MCQs are graded automatically.**
- **Practice sessions** (10, 20 or 30 questions) and a **timed interview simulation** that goes from easy to hard.
- A **daily challenge** of three questions.

[IMAGE 04-dashboard.png]
*Caption: The dashboard shows your accuracy, weighted score, streak and what's due for review.*

## 5. An interviewer that actually speaks

Reading a question on a screen is not the same as hearing it from a person across the table. In the **Interview Simulation** and the **Daily Challenge**, an English voice now reads each question aloud ("Question 3…"), then hands over to you: *"Your turn: answer out loud."*

- Replay a question any time, or press **V**.
- **Listen** buttons on every question page, in practice sessions and on flashcards. Flashcards can read the question, then the quick answer when you flip.
- Pick the voice and speed in Settings, and choose where questions are read automatically.
- It uses your browser's built-in voices, so there's nothing to install. Chrome and Edge usually have the most natural-sounding ones.

[IMAGE 08-voice-interviewer.png]
*Caption: The interviewer reads the question aloud, then it's your turn to answer out loud.*

## 6. Your mistakes come back on a schedule

Anything you get wrong or only half right comes back for review after 1 day, then 3, 7, 14 and 30 days. The app also spots **weak topics** (for example, React "Effects and Cleanup") so you know what to study next. No more re-reading things you already know.

## 7. Behavioural and project questions

Technical rounds get the attention, but the first and last questions are often non-technical. The behavioural section tells you **what the interviewer is checking**, gives you a **structure** (like STAR), and a **sample answer** with blanks you fill in with your own story. No fake statistics, no copy-paste scripts.

[IMAGE 05-behavioural-question.png]
*Caption: "Walk me through a project you built": how to answer, a sample answer, common mistakes and likely follow-ups.*

## 8. React Native, including Expo and SQLite

As a React Native developer myself, I wanted this section to cover what you actually do at work, not just "what is a component". It includes:

- Core components, Flexbox, safe areas and the keyboard
- FlatList and FlashList performance
- Expo Router navigation and deep links
- Choosing between AsyncStorage, SecureStore, MMKV and **expo-sqlite**
- SQLite migrations with `SQLiteProvider`, transactions, prepared statements and SQL injection
- Offline-first sync
- EAS Build and OTA updates (including what happens when an OTA update breaks native compatibility)
- The New Architecture

[IMAGE 07-react-native-storage.png]
*Caption: "Where should each piece of data go?": AsyncStorage vs SecureStore vs MMKV vs SQLite.*

## Up to date, and checked

Interview answers go stale fast. A 2022 answer about Next.js caching is simply wrong today. The content targets current versions (React 19.3, Next.js 16, Node.js 26 LTS, Express 5, React Native 0.88 with Expo SDK 58), labels legacy APIs as legacy, and links to the official docs for every answer.

Wherever it was possible, the code examples were actually **run**: JavaScript and Node.js snippets in Node, SQL queries in SQLite. The question bank also went through a full review pass for technical accuracy. There's a **Versions & Sources** page in the app that lists what each answer is based on.

If you spot a mistake, please open an issue on GitHub. That's the whole point of making it open source.

[IMAGE 06-technologies.png]
*Caption: Pick a technology, or filter by area: frontend, mobile, backend, databases, DevOps & cloud, AI & search, career skills.*

## A simple two-week plan

If you have an interview coming up, here's how I'd use it:

1. **Days 1–3:** Flip through the quick-recall flashcards for your stack. Mark anything you can't explain.
2. **Days 4–10:** One 20-question practice session a day in Interview mode. Answer out loud, then grade yourself honestly. Turn on the voice so you *hear* each question first.
3. **Every day:** Clear your review queue first. Those are your weak spots.
4. **Days 11–13:** Run the timed interview simulation, and practise the behavioural questions out loud.
5. **Day 14:** Read only the quick answers for your weak topics. Sleep.

## Free, private, no account

It's a plain HTML, CSS and JavaScript app with no backend and no login. Your progress stays in your browser, and you can export it as a backup. Want it offline? Download the repo and open `index.html`; it runs straight from your computer.

---

I'd love to hear what you think: which topics are missing, which answers helped, and what tripped you up in your last interview. Leave a comment, star the repo, or open an issue.

**Good luck with your next interview. শুভকামনা!** 🚀

👉 [devshojol.github.io/Interview-prep-BD](https://devshojol.github.io/Interview-prep-BD/)
