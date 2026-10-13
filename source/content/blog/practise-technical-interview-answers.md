---
title: "How to practise technical interview questions: answer aloud, grade honestly, review on a schedule"
seoTitle: How to practise technical interview questions
description: A practice routine for technical interviews that builds recall rather than recognition, with a rubric for grading your own answers and a simple spaced-review schedule.
publishedAt: 2026-10-13
category: Technical Interview Preparation
tags: [interview preparation, study method, spaced repetition, self-assessment]
---

Reading interview questions and their answers feels productive, but it mostly trains recognition: you see an answer and agree with it. In an interview there is nothing to recognise. You have to produce an explanation from memory, in order, out loud, while someone listens. This article describes a routine that practises that skill directly. It has three parts: answer before you look, grade yourself against a clear rubric, and come back to weak questions on a schedule.

It is written for developers preparing for technical interviews, whether for a local company or a remote role. The method is general. Where it mentions Interview Prep BD, that is simply where the routine is built in.

## Answer before you look

The single most useful change is to **commit to an answer before you see the reference**. Read the question, then answer it as you would in the interview: say it out loud, or write the key points if you are somewhere you cannot talk. Only then reveal the reference answer.

Retrieving an answer is harder than rereading one, and that difficulty is the point. It shows you exactly which parts you can produce on demand and which parts you only recognise. Rereading hides that difference.

Two practical rules make this work:

- **Give yourself a time box.** A few minutes for a conceptual question is realistic. If you have nothing after that, stop, reveal the answer and grade it as incorrect. Staring at a blank page for twenty minutes trains nothing.
- **Say it in the language of the interview.** If your interview will be in English, practise the spoken answer in English, even if you first think it through in Bangla. Explaining a concept fluently is a separate skill from understanding it, and it improves with repetition.

In the app, each question has an Interview mode that hides the answer until you reveal it, and the timed [interview simulation](app:#/interview) also shows how long you spent thinking. Learning mode shows the answer immediately, which is useful the first time you meet a topic but should not be your default once you are preparing.

## A structure for spoken answers

Interviewers listen for whether you understand how something works, not whether you can recite a definition. A reliable shape for conceptual answers is:

1. **What it is**, in one sentence.
2. **How it works**: the mechanism, in two or three steps.
3. **An example**: a short piece of code, a query or a concrete scenario.
4. **A trade-off or pitfall**: when it is the wrong choice, or the mistake people make with it.

For example, asked "what is event delegation?", a complete answer defines it (one listener on a parent handles events from many children), explains the mechanism (events bubble up, so the parent sees them and checks `event.target`), gives an example (a list where items are added dynamically), and names a pitfall (some events, such as `focus`, do not bubble, and `event.target` may be a nested element, so you check with `closest()`). That shape fits most conceptual questions, and step 4 is usually what separates a good answer from an adequate one.

For output-prediction and query questions, the structure is different: write down your prediction first, then explain each step. The articles on [predicting JavaScript output](post:javascript-event-loop-output-questions) and [SQL join and aggregate traps](post:sql-joins-where-having-null) show what that step-by-step reasoning looks like.

## Grade yourself with a rubric

Self-assessment only helps if it is honest and consistent. Decide in advance what each grade means:

| Grade | Meaning |
|---|---|
| Correct | You covered the core idea and the mechanism, and nothing you said was wrong. Missing a minor detail is fine. |
| Partial | The direction was right, but you missed a key part (often the mechanism or the main pitfall), or you said something inaccurate that you would need to correct. |
| Incorrect | You could not answer, or the core of your answer was wrong. |
| Skipped | You chose not to attempt it. This is not a failure, but it is not practice either. |

Two habits keep the grading honest. First, compare against the reference **point by point**, not by overall impression: list the two or three ideas the reference treats as essential and check whether you said each one. Second, grade what you said, not what you meant. "I knew that" is the recognition trap again.

Multiple-choice questions remove the judgement, which is why the app grades MCQs automatically and locks the result once it is scored. Everything else is self-assessed, because free-form answers cannot be graded reliably by a program.

## Review weak questions on a schedule

Getting a question right once, immediately after reading the answer, does not mean you will get it right in a week. Spaced review fixes this by bringing each weak question back after a gap, and widening the gap each time you answer correctly.

A simple schedule is enough. This is the one Interview Prep BD uses:

- An **incorrect** answer comes back the next day.
- A **partial** answer comes back in three days.
- Each **correct** answer on a question that is due moves it to the next interval in the sequence 1, 3, 7, 14 and 30 days. After the 30-day review it leaves the queue.

The schedule is deliberately transparent rather than adaptive, so you can always see why a question is due. The [Review Questions](app:#/review) screen lists what is due today and over the next week, and [flashcards](app:#/flashcards) are a quick way through a due deck when you only have a few minutes.

What matters more than the exact intervals is the commitment to do the due reviews before starting new material. New questions feel like progress. Due reviews are where the progress is kept.

## Mix difficulty and topics

When you practise one topic in a block (twenty React questions in a row), each answer is primed by the previous one. Interviews do not work that way: a question about closures can be followed by one about database indexes. Once you have covered a topic once, mix it with others:

- Use **mixed sessions** across several technologies rather than single-topic blocks. The [Practice setup](app:#/practice) lets you choose several technologies and difficulties together.
- **Include harder questions before you feel ready.** Easy questions build confidence, but medium and hard questions are where the trade-off discussions happen. Extreme questions are senior-level material and are not a requirement for junior roles.
- **Keep a short daily habit.** The [daily challenge](app:#/daily) picks three questions from your local date: one MCQ, one medium and one hard. It is a small, fixed amount that is easy to keep up on busy days.

## Run a timed mock before the real thing

A week or two before an interview, run timed mock sessions with answers hidden and questions ordered from easier to harder. The interview simulation does this and submits automatically when the time runs out. The goal is to practise pacing and to recover from a question you cannot answer, which is a skill in itself: say what you do know, reason out loud towards the rest, and move on rather than freezing.

After each mock, the results show which questions were partial or incorrect. Those go straight into the review queue, and they tell you what to study next more reliably than a general feeling of which topics are weak.

## Summary

- Answer before you look, out loud and in the interview's language.
- Use a fixed structure: what it is, how it works, an example, a trade-off.
- Grade against a rubric, point by point, and grade what you actually said.
- Do due reviews first, and let correct answers push questions further out.
- Mix topics and difficulties, and rehearse under time pressure before the real interview.

You can start with any technology from the [technology list](app:#/technologies), or open [all questions](app:#/questions) and filter by what you need.
