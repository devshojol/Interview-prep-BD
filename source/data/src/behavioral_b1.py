# Behavioural & project questions — beh-001 … beh-020 (see AUTHORING §8a)
# a_* = what the interviewer checks + how to structure; ex_* = short first-person sample answer
# for a junior/fresher with [placeholders]. No statistics, salaries or company facts.
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

STAR = ("Wikipedia — Situation, task, action, result (STAR)", "https://en.wikipedia.org/wiki/Situation,_task,_action,_result")
CODE_REVIEW = ("Wikipedia — Code review", "https://en.wikipedia.org/wiki/Code_review")
C = dict(type="behavioral", market="both", ver="Version-independent (behavioural)", vs=False, status="stable")

QUESTIONS = [
    # ------------------------------------------------------------------ beh-001
    Q(
        id="beh-001", sub="Introduction", diff="easy", prio="high", mins=2, **C,
        tags=["introduction", "self-pitch", "first-impression"],
        q_en=r"""Tell me about yourself.""",
        q_bn=r"""তোমার নিজের সম্পর্কে বলো।""",
        a_en=r"""The interviewer wants a short, relevant summary and a first sense of whether you fit the role. Use **present → past → future**: who you are now, one or two things you've built or learned that match this job, and why you're here. Keep it to about 60–90 seconds.""",
        a_bn=r"""Interviewer একটা ছোট, প্রাসঙ্গিক summary শুনতে চান, আর বুঝতে চান তুমি role-টার সাথে মেলো কিনা। **Present → past → future** ক্রমে বলো: এখন তুমি কে, এই job-এর সাথে মেলে এমন এক-দুইটা জিনিস যা তুমি বানিয়েছ বা শিখেছ, আর কেন এখানে apply করেছ। সময় রাখো মোটামুটি 60–90 second।""",
        ex_en=r"""
"I'm [your name], a [fresher / junior] [MERN / backend] developer. I finished my [degree] at [university] in [year], and since then I've been building [type of apps] with [main stack]. The project I'm proudest of is [project], where I [one concrete thing you built, e.g. built the JWT login and role-based access]. Lately I've been learning [skill relevant to this job]. I applied here because [specific reason linked to the role], and I'd like to grow into [direction]." """,
        ex_bn=r"""
"আমি [তোমার নাম], একজন [fresher / junior] [MERN / backend] developer। [Year]-এ [university] থেকে [degree] শেষ করেছি, তারপর থেকে [main stack] দিয়ে [কোন ধরনের app] বানাচ্ছি। যে project নিয়ে আমি সবচেয়ে গর্বিত সেটা [project], যেখানে আমি [একটা নির্দিষ্ট কাজ, যেমন JWT login আর role-based access বানিয়েছি]। ইদানীং [এই job-এর সাথে প্রাসঙ্গিক skill] শিখছি। এখানে apply করেছি কারণ [role-এর সাথে যুক্ত নির্দিষ্ট কারণ], আর আমি [কোন দিকে] grow করতে চাই।" """,
        mist_en=r"""- Reciting the whole CV or life story (hometown, school, hobbies first).
- Talking for three or four minutes.
- Listing technologies without saying what you built with them.
- A memorised script delivered like a robot.""",
        mist_bn=r"""- পুরো CV বা জীবনের গল্প বলা (আগে বাড়ি, school, hobby)।
- তিন-চার মিনিট ধরে বলে যাওয়া।
- শুধু technology-র নাম বলা, সেগুলো দিয়ে কী বানিয়েছ তা না বলা।
- মুখস্থ script robot-এর মতো বলা।""",
        tip_en=r"""Practise a 60–90 second version out loud, and change only the last line for each company.""",
        tip_bn=r"""60–90 second-এর একটা version জোরে জোরে practice করো, আর প্রতিটা company-র জন্য শুধু শেষ লাইনটা বদলাও।""",
        follow=[("Which of those projects should we talk about first?", "ওই project-গুলোর মধ্যে কোনটা নিয়ে আগে কথা বলব?"),
                ("Why did you choose that stack?", "ওই stack কেন বেছে নিলে?")],
        related=["beh-002", "beh-011"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-002
    Q(
        id="beh-002", sub="Projects", diff="medium", prio="high", mins=4, **C,
        tags=["project", "architecture", "tech-choices", "ownership"],
        q_en=r"""Walk me through a project you built. What is its architecture, and why did you choose that tech stack?""",
        q_bn=r"""তোমার বানানো একটা project আমাকে বুঝিয়ে বলো। এর architecture কী, আর ওই tech stack কেন বেছে নিয়েছিলে?""",
        a_en=r"""They're checking that you really built it and understand it: the problem, your part, how the pieces fit, and the reasons behind your choices. Go **problem → users → architecture** (frontend, API, database, hosting) **→ your part → one hard decision and its trade-off → result and what you'd change**.""",
        a_bn=r"""Interviewer দেখতে চান project-টা সত্যিই তুমি বানিয়েছ আর বোঝো কিনা: সমস্যাটা কী, তোমার অংশ কোনটা, অংশগুলো কীভাবে জোড়া লাগে, আর প্রতিটা সিদ্ধান্তের কারণ কী। এই ক্রমে বলো: **সমস্যা → কারা ব্যবহার করে → architecture** (frontend, API, database, hosting) **→ তোমার অংশ → একটা কঠিন সিদ্ধান্ত আর তার trade-off → ফলাফল আর কী বদলাতে চাও**।""",
        ex_en=r"""
"[Project] is a [what it does] for [who uses it]. It has a [React / Next.js] frontend that calls a [Express / NestJS] REST API, with [PostgreSQL / MongoDB] for data and [Redis / S3 / other] for [purpose], deployed on [where]. I built [your parts]. I chose [database] because [reason tied to the data, e.g. orders and payments are relational, so I wanted transactions and foreign keys]. The trickiest part was [problem], which I solved by [approach]. If I rebuilt it, I'd [improvement, e.g. write tests earlier or add pagination from day one]." """,
        ex_bn=r"""
"[Project] হলো [কারা ব্যবহার করে]-এর জন্য একটা [কী করে]। এর [React / Next.js] frontend একটা [Express / NestJS] REST API call করে, data থাকে [PostgreSQL / MongoDB]-তে, আর [উদ্দেশ্য]-এর জন্য [Redis / S3 / অন্য কিছু], deploy করা [কোথায়]। আমি বানিয়েছি [তোমার অংশ]। [Database] বেছে নিয়েছিলাম কারণ [data-র সাথে যুক্ত কারণ, যেমন order আর payment relational, তাই transaction আর foreign key চেয়েছিলাম]। সবচেয়ে কঠিন অংশ ছিল [সমস্যা], সমাধান করেছি [পদ্ধতি] দিয়ে। আবার বানালে আমি [উন্নতি, যেমন আগে থেকেই test লিখতাম বা শুরু থেকেই pagination দিতাম]।" """,
        mist_en=r"""- Saying "we" the whole time, so the interviewer can't tell what *you* did.
- Justifying a choice with "it's popular" or "the tutorial used it".
- Not knowing the details of a part you claim (auth, deployment, database design).
- Claiming users, traffic or results you can't back up.""",
        mist_bn=r"""- পুরো সময় "আমরা" বলা, ফলে interviewer বুঝতে পারেন না *তুমি* কী করেছ।
- কোনো choice-এর কারণ হিসেবে "এটা popular" বা "tutorial-এ এটা ছিল" বলা।
- যে অংশ তুমি করেছ বলছ (auth, deployment, database design), তার detail না জানা।
- এমন user, traffic বা ফলাফল দাবি করা যা প্রমাণ করতে পারবে না।""",
        tip_en=r"""Sketch a quick box diagram if you can, and be ready to go deep on any box you mention.""",
        tip_bn=r"""সম্ভব হলে একটা ছোট box diagram এঁকে দেখাও, আর যে box-এর কথা বলবে সেটা নিয়ে গভীরে যাওয়ার জন্য তৈরি থাকো।""",
        follow=[("How does authentication work in that project?", "ওই project-এ authentication কীভাবে কাজ করে?"),
                ("What would break first if traffic grew ten times?", "Traffic দশ গুণ হলে আগে কী ভাঙবে?")],
        related=["beh-001", "beh-003"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-003
    Q(
        id="beh-003", sub="Problem Solving", diff="medium", prio="high", mins=3, **C,
        tags=["debugging", "star", "root-cause"],
        q_en=r"""Tell me about the hardest bug you've fixed.""",
        q_bn=r"""তোমার fix করা সবচেয়ে কঠিন bug-টার কথা বলো।""",
        a_en=r"""They're checking your debugging process: reproduce, narrow it down, test hypotheses, fix, and prevent it from coming back. Use **STAR** (situation, task, action, result), spend most of the time on the action, and finish with the root cause and what you changed so it won't happen again.""",
        a_bn=r"""Interviewer তোমার debugging process দেখতে চান: bug reproduce করা, জায়গাটা ছোট করে আনা, hypothesis test করা, fix করা, আর যেন আবার না হয় তার ব্যবস্থা করা। **STAR** (situation, task, action, result) ব্যবহার করো, সবচেয়ে বেশি সময় দাও action-এ, আর শেষে root cause আর আবার না হওয়ার জন্য কী বদলেছ সেটা বলো।""",
        ex_en=r"""
"In [project], [symptom, e.g. some users were randomly logged out]. I couldn't reproduce it locally, so I [what you did: added logs, checked the Network tab, looked for a pattern]. That showed [clue]. My first guess was [wrong hypothesis], but [how you ruled it out]. The real cause was [root cause, e.g. two tabs refreshing the token at the same time]. I fixed it by [fix], added [a test / a log / an alert] so it can't silently come back, and [wrote it up for the team]." """,
        ex_bn=r"""
"[Project]-এ [লক্ষণ, যেমন কিছু user হঠাৎ হঠাৎ logout হয়ে যাচ্ছিল]। Local-এ reproduce করতে পারছিলাম না, তাই আমি [কী করেছ: log যোগ করেছি, Network tab দেখেছি, pattern খুঁজেছি]। তাতে [clue] পেলাম। প্রথমে ভেবেছিলাম [ভুল hypothesis], কিন্তু [কীভাবে বাদ দিলে]। আসল কারণ ছিল [root cause, যেমন দুটো tab একই সময়ে token refresh করছিল]। আমি [fix] দিয়ে ঠিক করেছি, [test / log / alert] যোগ করেছি যাতে চুপচাপ আবার না ফেরে, আর [team-এর জন্য লিখে রেখেছি]।" """,
        mist_en=r"""- Picking a trivial bug (a typo) or one you can't explain technically.
- Jumping straight to the fix without showing how you found it.
- Blaming a teammate or the framework.
- Not knowing the root cause ("it just started working").""",
        mist_bn=r"""- ছোটখাটো bug (typo) বা এমন bug বেছে নেওয়া যেটা technically ব্যাখ্যা করতে পারো না।
- কীভাবে খুঁজে পেলে তা না দেখিয়ে সরাসরি fix-এ চলে যাওয়া।
- Teammate বা framework-কে দোষ দেওয়া।
- Root cause না জানা ("এমনিই ঠিক হয়ে গেল")।""",
        tip_en=r"""Pick a bug where your reasoning shows, and name the tools you used (debugger, logs, DevTools, `git bisect`).""",
        tip_bn=r"""এমন bug বেছে নাও যেখানে তোমার চিন্তার ধারা বোঝা যায়, আর যে tool ব্যবহার করেছ সেগুলোর নাম বলো (debugger, log, DevTools, `git bisect`)।""",
        follow=[("How would you catch that bug earlier next time?", "পরের বার ওই bug আরও আগে কীভাবে ধরবে?"),
                ("Which tools do you reach for first when debugging?", "Debug করার সময় প্রথমে কোন tool ব্যবহার করো?")],
        related=["beh-002", "beh-004"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-004
    Q(
        id="beh-004", sub="Growth & Learning", diff="medium", prio="high", mins=3, **C,
        tags=["mistake", "failure", "ownership", "star"],
        q_en=r"""Tell me about a mistake you made or a time you failed.""",
        q_bn=r"""তোমার করা একটা ভুল বা ব্যর্থ হওয়ার একটা ঘটনা বলো।""",
        a_en=r"""They're checking honesty, ownership and learning, not perfection. Pick a real but moderate mistake, own it in a sentence or two, then spend most of the answer on how you limited the damage and the habit you changed afterwards.""",
        a_bn=r"""Interviewer সততা, দায় নেওয়া আর শেখার ক্ষমতা দেখতে চান, নিখুঁত হওয়া না। একটা সত্যিকারের কিন্তু মাঝারি ভুল বেছে নাও, এক-দুই বাক্যে দায় স্বীকার করো, তারপর উত্তরের বেশিরভাগ সময় দাও ক্ষতি কীভাবে সামলালে আর পরে কোন অভ্যাস বদলালে সেখানে।""",
        ex_en=r"""
"During [project / internship], I [mistake, e.g. ran a database migration on staging without testing it on a copy of the data], and [impact, e.g. staging was broken for part of the day]. I told my [lead / team] right away and [how you fixed it, e.g. rolled back and corrected the migration]. Since then I [concrete habit, e.g. test migrations on a copy first and always keep a rollback step]." """,
        ex_bn=r"""
"[Project / internship]-এর সময় আমি [ভুল, যেমন data-র copy-তে test না করেই staging-এ database migration চালিয়েছিলাম], ফলে [প্রভাব, যেমন দিনের কিছু সময় staging ভাঙা ছিল]। আমি সাথে সাথে [lead / team]-কে জানিয়েছি আর [কীভাবে ঠিক করলে, যেমন rollback করে migration ঠিক করেছি]। তারপর থেকে আমি [নির্দিষ্ট অভ্যাস, যেমন আগে copy-তে migration test করি আর সবসময় rollback-এর ব্যবস্থা রাখি]।" """,
        mist_en=r"""- Fake mistakes like "I work too hard".
- A story that raises red flags, such as hiding a problem from your team.
- Blaming others for your part.
- A vague lesson ("I learned to be careful").""",
        mist_bn=r"""- "আমি খুব বেশি কাজ করি"-র মতো নকল ভুল বলা।
- এমন গল্প যেটা সন্দেহ জাগায়, যেমন team-এর কাছ থেকে সমস্যা লুকানো।
- নিজের অংশের দায় অন্যের ঘাড়ে চাপানো।
- অস্পষ্ট শিক্ষা ("সাবধান হতে শিখেছি")।""",
        tip_en=r"""Keep the mistake short and the learning long, and end on the habit you follow today.""",
        tip_bn=r"""ভুলের অংশ ছোট রাখো, শেখার অংশ বড় করো, আর শেষ করো এখন যে অভ্যাস মেনে চলো সেটা দিয়ে।""",
        follow=[("How did your team react?", "তোমার team কীভাবে react করেছিল?"),
                ("Has that habit helped you since?", "সেই অভ্যাস পরে কোনো কাজে লেগেছে?")],
        related=["beh-003", "beh-008"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-005
    Q(
        id="beh-005", sub="Teamwork", diff="medium", prio="high", mins=3, **C,
        tags=["conflict", "teamwork", "communication", "star"],
        q_en=r"""Tell me about a conflict or disagreement you had with a teammate. How did you handle it?""",
        q_bn=r"""কোনো teammate-এর সাথে তোমার মতবিরোধ বা conflict-এর একটা ঘটনা বলো। কীভাবে সামলেছিলে?""",
        a_en=r"""They're checking whether you can disagree respectfully and focus on the outcome. Use **STAR**: a disagreement about the work (not personalities), how you listened and brought facts, how the decision was made, and how the working relationship was afterwards.""",
        a_bn=r"""Interviewer দেখতে চান তুমি সম্মান রেখে দ্বিমত করতে পারো কিনা আর ফলাফলের দিকে মন দাও কিনা। **STAR** ব্যবহার করো: কাজ নিয়ে মতবিরোধ (ব্যক্তিগত না), তুমি কীভাবে শুনেছ আর তথ্য এনেছ, সিদ্ধান্ত কীভাবে হলো, আর পরে একসাথে কাজের সম্পর্ক কেমন ছিল।""",
        ex_en=r"""
"In our [final-year project / team at company], a teammate and I disagreed on [e.g. MongoDB vs PostgreSQL]. First I asked why they preferred [their option] and learned they were worried about [concern]. I suggested we list the requirements and build a small prototype with each. [Outcome: we picked X because Y / we went with their idea and I backed it fully.] We kept working well together, and I learned to [lesson, e.g. ask about the concern behind an opinion]." """,
        ex_bn=r"""
"আমাদের [final-year project / company-র team]-এ একজন teammate আর আমার মধ্যে [যেমন MongoDB না PostgreSQL] নিয়ে দ্বিমত হয়েছিল। প্রথমে জিজ্ঞেস করেছি কেন সে [তার option] চায়, তখন বুঝলাম তার চিন্তা ছিল [concern]। আমি বললাম requirement-গুলো লিখে দুটো দিয়েই ছোট prototype বানাই। [ফলাফল: Y কারণে X নিলাম / তার idea নিলাম আর আমি পুরোপুরি support করলাম।] আমরা পরেও ভালোভাবে একসাথে কাজ করেছি, আর আমি শিখেছি [শিক্ষা, যেমন কোনো মতের পেছনের চিন্তাটা জিজ্ঞেস করা]।" """,
        mist_en=r"""- Saying "I've never had a conflict".
- Making the other person the villain.
- A story where you "won" by going over their head to the manager.
- Personal or emotional conflicts unrelated to the work.""",
        mist_bn=r"""- "আমার কখনো কারও সাথে conflict হয়নি" বলা।
- অন্যজনকে খলনায়ক বানানো।
- এমন গল্প যেখানে তাকে টপকে manager-এর কাছে গিয়ে "জিতেছ"।
- কাজের সাথে সম্পর্কহীন ব্যক্তিগত বা আবেগের conflict।""",
        tip_en=r"""Show "disagree and commit": once the team decides, you support the decision fully.""",
        tip_bn=r""""Disagree and commit" দেখাও: team সিদ্ধান্ত নিলে তুমি সেটা পুরোপুরি support করো।""",
        follow=[("What would you do if your lead made a decision you strongly disagreed with?", "তোমার lead এমন সিদ্ধান্ত নিলে যেটার সাথে তুমি একদম একমত না, তখন কী করবে?"),
                ("How do you handle a teammate who keeps missing deadlines?", "যে teammate বারবার deadline miss করে, তাকে কীভাবে সামলাবে?")],
        related=["beh-008", "beh-015"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-006
    Q(
        id="beh-006", sub="Work Style", diff="medium", prio="high", mins=3, **C,
        tags=["deadline", "prioritisation", "pressure", "star"],
        q_en=r"""Tell me about a time you worked under tight deadline pressure.""",
        q_bn=r"""এমন একটা সময়ের কথা বলো যখন কঠিন deadline-এর চাপে কাজ করেছ।""",
        a_en=r"""They're checking how you prioritise and communicate under pressure. Explain how you broke the work down, agreed on what mattered most, cut or postponed the rest, raised risks early, and what you delivered.""",
        a_bn=r"""Interviewer দেখতে চান চাপের মধ্যে তুমি কীভাবে priority ঠিক করো আর যোগাযোগ রাখো। বলো কীভাবে কাজ ভাগ করেছ, কোনটা সবচেয়ে জরুরি তা নিয়ে একমত হয়েছ, বাকিগুলো বাদ দিয়েছ বা পিছিয়েছ, ঝুঁকির কথা আগেভাগে জানিয়েছ, আর শেষে কী deliver করেছ।""",
        ex_en=r"""
"Before our [demo / release / submission], we had [time left] and [remaining work]. I listed the tasks and agreed with [lead / client / team] which features were must-haves. I focused on [core feature], postponed [nice-to-have], and told [them] early that [risk]. We delivered [what] on time and finished [postponed item] in the next [week / sprint]. Next time I'd [lesson, e.g. raise the risk earlier]." """,
        ex_bn=r"""
"আমাদের [demo / release / submission]-এর আগে হাতে ছিল [সময়], আর বাকি ছিল [কাজ]। আমি task-গুলোর list করে [lead / client / team]-এর সাথে ঠিক করলাম কোন feature না হলেই নয়। আমি [মূল feature]-এ মন দিলাম, [nice-to-have] পিছিয়ে দিলাম, আর আগেই [তাদের] জানালাম যে [ঝুঁকি]। আমরা সময়মতো [কী] deliver করেছি, আর পিছানো [কাজ] পরের [week / sprint]-এ শেষ করেছি। পরের বার আমি [শিক্ষা, যেমন ঝুঁকির কথা আরও আগে বলব]।" """,
        mist_en=r"""- Presenting all-nighters as your method.
- Claiming you never feel pressure.
- Skipping testing to make the deadline without mentioning the risk.
- Staying silent until the deadline is already missed.""",
        mist_bn=r"""- সারা রাত জেগে কাজ করাকেই পদ্ধতি হিসেবে দেখানো।
- বলা যে তুমি কখনো চাপ অনুভব করো না।
- Deadline ধরতে testing বাদ দেওয়া, কিন্তু ঝুঁকির কথা না বলা।
- Deadline পার হয়ে যাওয়া পর্যন্ত চুপ থাকা।""",
        tip_en=r"""Highlight the moment you communicated the trade-off; that matters more than heroics.""",
        tip_bn=r"""যে মুহূর্তে তুমি trade-off-টা জানিয়েছ সেটা জোর দিয়ে বলো; বীরত্বের গল্পের চেয়ে এটাই বেশি গুরুত্বপূর্ণ।""",
        follow=[("What do you do when you realise you'll miss a deadline?", "যখন বুঝবে deadline miss হবে, তখন কী করো?"),
                ("How do you estimate a task?", "একটা task-এর সময় কীভাবে estimate করো?")],
        related=["beh-014", "beh-017"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-007
    Q(
        id="beh-007", sub="Growth & Learning", diff="easy", prio="high", mins=2, **C,
        tags=["learning", "new-technology", "self-learning"],
        q_en=r"""Tell me about a time you had to learn a new technology quickly.""",
        q_bn=r"""এমন একটা সময়ের কথা বলো যখন তোমাকে দ্রুত একটা নতুন technology শিখতে হয়েছিল।""",
        a_en=r"""They're checking how you learn on your own: official docs, small experiments, building something real, and asking for help at the right time. Give one concrete example with the timeline and what you shipped at the end.""",
        a_bn=r"""Interviewer দেখতে চান তুমি নিজে নিজে কীভাবে শেখো: official docs, ছোট experiment, সত্যিকারের কিছু বানানো, আর ঠিক সময়ে সাহায্য চাওয়া। একটা নির্দিষ্ট উদাহরণ দাও, কত সময় লেগেছে আর শেষে কী বানিয়েছ সেটা সহ।""",
        ex_en=r"""
"For [project / task], I had to use [technology, e.g. Docker], which I'd never used. I started with the official getting-started guide, then built a tiny example: I [e.g. containerised my own Express API]. When I got stuck on [problem], I read the error carefully, searched the docs and issues, and then asked [a senior] with what I'd already tried. Within [time], I [result, e.g. had our app running with Docker Compose for the whole team]." """,
        ex_bn=r"""
"[Project / task]-এর জন্য আমাকে [technology, যেমন Docker] ব্যবহার করতে হয়েছিল, যেটা আগে কখনো ব্যবহার করিনি। আমি official getting-started guide দিয়ে শুরু করি, তারপর একটা ছোট example বানাই: [যেমন নিজের Express API containerise করেছি]। [সমস্যা]-তে আটকে গেলে আগে error ভালো করে পড়েছি, docs আর issue-তে খুঁজেছি, তারপর আমি কী কী চেষ্টা করেছি সেটা বলে [একজন senior]-কে জিজ্ঞেস করেছি। [সময়]-এর মধ্যে আমি [ফলাফল, যেমন পুরো team-এর জন্য Docker Compose দিয়ে app চালু করে দিয়েছি]।" """,
        mist_en=r"""- "I just watch YouTube tutorials" as the whole process.
- No concrete result at the end.
- Claiming expertise after a few days.
- Never mentioning official documentation.""",
        mist_bn=r"""- পুরো process হিসেবে শুধু "YouTube tutorial দেখি" বলা।
- শেষে কোনো নির্দিষ্ট ফলাফল না থাকা।
- কয়েক দিন শিখেই expert দাবি করা।
- Official documentation-এর কথা একবারও না বলা।""",
        tip_en=r"""Mention how you check your understanding: building something, explaining it to someone, or writing short notes.""",
        tip_bn=r"""বলো কীভাবে নিজের বোঝাটা যাচাই করো: কিছু বানিয়ে, কাউকে বুঝিয়ে, বা ছোট note লিখে।""",
        follow=[("What are you learning right now?", "এখন কী শিখছ?"),
                ("How do you decide when to stop and ask for help?", "কখন থেমে সাহায্য চাইবে, সেটা কীভাবে ঠিক করো?")],
        related=["beh-016"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-008
    Q(
        id="beh-008", sub="Teamwork", diff="easy", prio="high", mins=2, **C,
        tags=["code-review", "feedback", "growth"],
        q_en=r"""How do you handle feedback on your code in a code review? Give an example.""",
        q_bn=r"""Code review-তে তোমার code নিয়ে feedback এলে কীভাবে সামলাও? একটা উদাহরণ দাও।""",
        a_en=r"""They're checking whether you take feedback without ego and actually learn from it. Describe one specific comment, how you made sure you understood it, what you changed, and what you now do by default; add that you can disagree politely with reasons.""",
        a_bn=r"""Interviewer দেখতে চান তুমি ego ছাড়া feedback নিতে পারো কিনা আর সত্যিই তা থেকে শেখো কিনা। একটা নির্দিষ্ট comment-এর কথা বলো, কীভাবে নিশ্চিত হয়েছ যে বুঝেছ, কী বদলেছ, আর এখন default-ভাবে কী করো; সাথে বলো যে কারণ দেখিয়ে ভদ্রভাবে দ্বিমতও করতে পারো।""",
        ex_en=r"""
"On one of my early PRs in [company / project], the reviewer pointed out that I [feedback, e.g. had business logic inside the route handler and no error handling]. I asked why it mattered, and they explained [reason, e.g. it's hard to test and errors would crash the request]. I moved it into [a service / middleware], and now I [habit, e.g. review my own diff and check error paths before asking for review]. When I disagree with a comment, I explain my reasoning and we decide together." """,
        ex_bn=r"""
"[Company / project]-এ আমার শুরুর দিকের একটা PR-এ reviewer দেখালেন যে আমি [feedback, যেমন route handler-এর ভেতরে business logic রেখেছি আর error handling নেই]। আমি জিজ্ঞেস করলাম কেন এটা সমস্যা, উনি বোঝালেন [কারণ, যেমন test করা কঠিন আর error হলে request crash করবে]। আমি সেটা [service / middleware]-এ সরিয়েছি, আর এখন [অভ্যাস, যেমন review চাওয়ার আগে নিজের diff নিজে দেখি আর error path check করি]। কোনো comment-এর সাথে একমত না হলে কারণ বুঝিয়ে বলি, তারপর একসাথে সিদ্ধান্ত নিই।" """,
        mist_en=r"""- Getting defensive or treating review comments as personal criticism.
- "I've never received any feedback."
- Changing everything blindly without understanding why.
- No concrete example.""",
        mist_bn=r"""- Defensive হয়ে যাওয়া বা review comment-কে ব্যক্তিগত সমালোচনা ভাবা।
- "আমি কখনো কোনো feedback পাইনি" বলা।
- কেন তা না বুঝে অন্ধভাবে সব বদলে ফেলা।
- কোনো নির্দিষ্ট উদাহরণ না থাকা।""",
        tip_en=r"""Show both sides: you welcome good feedback, and you can push back politely with reasons.""",
        tip_bn=r"""দুই দিকই দেখাও: ভালো feedback খুশি মনে নাও, আবার কারণ দেখিয়ে ভদ্রভাবে দ্বিমতও করতে পারো।""",
        follow=[("How do you give feedback on someone else's code?", "অন্যের code-এ তুমি কীভাবে feedback দাও?"),
                ("What do you check before opening a pull request?", "Pull request খোলার আগে কী কী check করো?")],
        related=["beh-004", "beh-005"],
        refs=[CODE_REVIEW],
    ),
    # ------------------------------------------------------------------ beh-009
    Q(
        id="beh-009", sub="Career Goals", diff="easy", prio="high", mins=2, **C,
        tags=["motivation", "company-research", "why-us"],
        q_en=r"""Why do you want to work at our company, and why this role?""",
        q_bn=r"""আমাদের company-তে কেন কাজ করতে চাও, আর কেন এই role?""",
        a_en=r"""They're checking that you researched them and that your interest is specific, not copy-paste. Connect two or three real things about the company (product, tech stack in the job post, domain, how the team works) to your skills and goals.""",
        a_bn=r"""Interviewer দেখতে চান তুমি তাদের নিয়ে খোঁজ নিয়েছ কিনা আর তোমার আগ্রহ নির্দিষ্ট কিনা, copy-paste না। Company-র দুই-তিনটা সত্যিকারের বিষয় (product, job post-এর tech stack, domain, team কীভাবে কাজ করে) তোমার skill আর লক্ষ্যের সাথে যুক্ত করো।""",
        ex_en=r"""
"I've used / looked at [product] and read [something specific you found: the job description, their engineering blog, an open-source repo]. The role uses [stack from the job post], which is what I've been building with in [project]. I'm also interested in [their domain, e.g. fintech or e-commerce] because [genuine reason]. I think I can contribute with [skill], and I'd like to learn [something the team clearly does well]." """,
        ex_bn=r"""
"আমি [product] ব্যবহার করেছি / দেখেছি, আর [নির্দিষ্ট কিছু: job description, তাদের engineering blog, কোনো open-source repo] পড়েছি। এই role-এ [job post-এর stack] লাগে, যেটা দিয়েই আমি [project]-এ কাজ করছি। [তাদের domain, যেমন fintech বা e-commerce] নিয়েও আমার আগ্রহ আছে, কারণ [সত্যিকারের কারণ]। আমার মনে হয় আমি [skill] দিয়ে অবদান রাখতে পারব, আর [team যেটা ভালো করে] সেটা শিখতে চাই।" """,
        mist_en=r"""- Generic praise ("good company, good culture") that fits any employer.
- Talking only about salary or benefits.
- Getting facts about the company wrong.
- Not having read the job description.""",
        mist_bn=r"""- যেকোনো company-তে খাটে এমন সাধারণ প্রশংসা ("ভালো company, ভালো culture")।
- শুধু salary বা সুবিধা নিয়ে কথা বলা।
- Company সম্পর্কে ভুল তথ্য বলা।
- Job description না পড়া।""",
        tip_en=r"""Research before the interview (website, product, job post, public engineering content) and mention only facts you've checked.""",
        tip_bn=r"""Interview-এর আগে খোঁজ নাও (website, product, job post, public engineering content), আর শুধু যাচাই করা তথ্যই বলো।""",
        follow=[("What do you know about our product?", "আমাদের product সম্পর্কে কী জানো?"),
                ("Which other companies are you interviewing with?", "আর কোন কোন company-তে interview দিচ্ছ?")],
        related=["beh-010", "beh-018"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-010
    Q(
        id="beh-010", sub="Career Goals", diff="easy", prio="medium", mins=2, **C,
        tags=["career-goals", "growth", "future"],
        q_en=r"""Where do you see yourself in two to three years?""",
        q_bn=r"""দুই-তিন বছর পরে নিজেকে কোথায় দেখতে চাও?""",
        a_en=r"""They're checking that your ambition fits the role and that you plan to grow with them. Describe the skills and responsibility you want to build, in the direction this job leads, rather than a specific title or a plan to leave.""",
        a_bn=r"""Interviewer দেখতে চান তোমার লক্ষ্য role-টার সাথে মেলে কিনা আর তুমি তাদের সাথে থেকে বড় হতে চাও কিনা। কোনো নির্দিষ্ট পদবি বা চলে যাওয়ার পরিকল্পনা না বলে, এই job যেদিকে নিয়ে যায় সেদিকে কোন skill আর দায়িত্ব বাড়াতে চাও সেটা বলো।""",
        ex_en=r"""
"In two to three years I'd like to be a solid [full-stack / backend] developer who can own a feature end to end: design, build, test and deploy it. I want to go deeper into [area, e.g. system design, cloud or performance] and start helping newer developers on the team. I'd like that growth to happen here, working on [their product area]." """,
        ex_bn=r"""
"দুই-তিন বছরে আমি একজন ভালো [full-stack / backend] developer হতে চাই, যে একটা feature শুরু থেকে শেষ পর্যন্ত নিজে সামলাতে পারে: design, build, test আর deploy। আমি [area, যেমন system design, cloud বা performance]-এ আরও গভীরে যেতে চাই, আর team-এর নতুনদের সাহায্য করা শুরু করতে চাই। এই বড় হওয়াটা আমি এখানেই, [তাদের product area]-তে কাজ করে করতে চাই।" """,
        mist_en=r"""- "In your chair" jokes.
- Saying you plan to start your own company or move abroad soon.
- Having no plan at all.
- Naming a goal unrelated to the role (for example data science for a frontend job).""",
        mist_bn=r"""- "আপনার চেয়ারে" ধরনের রসিকতা।
- বলা যে শিগগিরই নিজের company খুলবে বা বিদেশে চলে যাবে।
- কোনো পরিকল্পনাই না থাকা।
- Role-এর সাথে সম্পর্কহীন লক্ষ্য বলা (যেমন frontend job-এ data science)।""",
        tip_en=r"""Talk about skills and ownership, and tie the growth to this role.""",
        tip_bn=r"""Skill আর ownership নিয়ে কথা বলো, আর বড় হওয়াটা এই role-এর সাথে যুক্ত করো।""",
        follow=[("What are you doing now to get there?", "সেখানে পৌঁছাতে এখন কী করছ?"),
                ("Which area of engineering interests you most?", "Engineering-এর কোন দিকটা তোমাকে সবচেয়ে বেশি টানে?")],
        related=["beh-009", "beh-016"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-011
    Q(
        id="beh-011", sub="Introduction", diff="medium", prio="high", mins=2, **C,
        tags=["strengths", "weaknesses", "self-awareness"],
        q_en=r"""What are your strengths and weaknesses?""",
        q_bn=r"""তোমার strength আর weakness কী?""",
        a_en=r"""They're checking self-awareness and honesty. Give one strength that matters for this role, backed by a short example, and one real but non-critical weakness together with the concrete steps you're taking to improve it.""",
        a_bn=r"""Interviewer তোমার নিজেকে চেনা আর সততা দেখতে চান। এই role-এর জন্য দরকারি একটা strength বলো, সাথে ছোট একটা উদাহরণ; আর একটা সত্যিকারের কিন্তু খুব গুরুতর না এমন weakness বলো, সাথে সেটা ঠিক করতে কী কী করছ।""",
        ex_en=r"""
"One strength is [e.g. patient, methodical debugging]: in [project], I [short example]. A weakness is [a real one, e.g. I used to spend too long stuck on a problem before asking for help]. Now I [action, e.g. timebox it, then ask with a summary of what I've tried], and it has [result, e.g. made me faster and helped me learn from seniors]." """,
        ex_bn=r"""
"আমার একটা strength হলো [যেমন ধৈর্য ধরে, ধাপে ধাপে debug করা]: [project]-এ আমি [ছোট উদাহরণ]। একটা weakness হলো [সত্যিকারের একটা, যেমন সাহায্য চাওয়ার আগে একটা সমস্যায় অনেক বেশি সময় আটকে থাকতাম]। এখন আমি [পদক্ষেপ, যেমন একটা সময়সীমা ঠিক করি, তারপর কী কী চেষ্টা করেছি তার summary দিয়ে জিজ্ঞেস করি], আর এতে [ফলাফল, যেমন কাজ দ্রুত হয়েছে আর senior-দের কাছ থেকে শিখতে পারছি]।" """,
        mist_en=r"""- Humble-brag weaknesses ("I'm a perfectionist").
- A weakness that is core to the job ("I don't like writing code").
- Strengths with no evidence.
- Listing five of each instead of one solid example.""",
        mist_bn=r"""- নিজের প্রশংসা লুকানো weakness ("আমি perfectionist")।
- Job-এর মূল কাজের সাথে জড়িত weakness ("code লিখতে ভালো লাগে না")।
- কোনো প্রমাণ ছাড়া strength বলা।
- একটা ভালো উদাহরণের বদলে পাঁচটা করে list করা।""",
        tip_en=r"""One strength, one weakness, each with a story; spend most of the time on what you're doing about the weakness.""",
        tip_bn=r"""একটা strength, একটা weakness, প্রতিটার সাথে একটা গল্প; বেশি সময় দাও weakness নিয়ে কী করছ সেখানে।""",
        follow=[("What feedback have you received most often?", "সবচেয়ে বেশি কোন feedback পেয়েছ?"),
                ("How would your teammates describe you?", "তোমার teammate-রা তোমাকে কীভাবে বর্ণনা করবে?")],
        related=["beh-001", "beh-004"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-012
    Q(
        id="beh-012", sub="Career Goals", diff="medium", prio="medium", mins=2, **C,
        tags=["job-change", "leaving", "motivation"],
        q_en=r"""Why did you leave your last job, or why are you looking to leave your current one?""",
        q_bn=r"""আগের job কেন ছেড়েছ, বা এখনকার job কেন ছাড়তে চাইছ?""",
        a_en=r"""They're checking that you're moving for positive reasons and that you won't badmouth employers. Be brief and honest, frame it around what you're moving *toward* (growth, scope, technology), and don't criticise your current or previous company.""",
        a_bn=r"""Interviewer দেখতে চান তুমি ইতিবাচক কারণে বদলাচ্ছ কিনা, আর আগের employer-এর বদনাম করবে কিনা। সংক্ষেপে আর সত্যি বলো, কথাটা সাজাও তুমি কোন *দিকে* যাচ্ছ সেটা দিয়ে (growth, দায়িত্বের পরিধি, technology), আর এখনকার বা আগের company-র সমালোচনা কোরো না।""",
        ex_en=r"""Sample answer (switching jobs):

"I've learned a lot at [company], especially [what you did there]. Now I'm looking for [what you want, e.g. more backend and product work, or a team with regular code reviews]. This role offers [the match], so it feels like the right next step."

Sample answer (fresher): "My [internship / contract] ended in [month], and I'm looking for a full-time role where I can [goal]." """,
        ex_bn=r"""নমুনা উত্তর (job বদলানো):

"[Company]-তে আমি অনেক কিছু শিখেছি, বিশেষ করে [সেখানে কী করেছ]। এখন আমি খুঁজছি [যা চাও, যেমন আরও backend আর product-এর কাজ, বা নিয়মিত code review হয় এমন team]। এই role-এ [মিলটা] আছে, তাই এটাকে ঠিক পরের ধাপ মনে হচ্ছে।"

নমুনা উত্তর (fresher): "আমার [internship / contract] [মাস]-এ শেষ হয়েছে, আর এখন এমন একটা full-time role খুঁজছি যেখানে [লক্ষ্য] করতে পারব।" """,
        mist_en=r"""- Complaining about your boss, salary or colleagues.
- A long, emotional story.
- Saying it's "only for the money".
- Reasons that don't match the dates on your CV.""",
        mist_bn=r"""- Boss, salary বা সহকর্মী নিয়ে অভিযোগ করা।
- লম্বা, আবেগী গল্প।
- বলা যে "শুধু টাকার জন্য"।
- CV-র তারিখের সাথে না মেলা কারণ।""",
        tip_en=r"""Two or three forward-looking sentences, then stop talking.""",
        tip_bn=r"""সামনের দিকে তাকানো দুই-তিনটা বাক্য বলো, তারপর থেমে যাও।""",
        follow=[("What would make you stay at a company for a long time?", "কী থাকলে তুমি একটা company-তে অনেক দিন থাকবে?"),
                ("What did you like most about your last role?", "আগের role-এর কোন জিনিসটা সবচেয়ে ভালো লেগেছে?")],
        related=["beh-009", "beh-010"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-013
    Q(
        id="beh-013", sub="Career Goals", diff="medium", prio="high", mins=2, **C,
        tags=["salary", "negotiation", "expectations"],
        q_en=r"""What are your salary expectations?""",
        q_bn=r"""তোমার expected salary কত?""",
        a_en=r"""They're checking whether your expectation fits their budget and whether you can discuss money calmly. Research the range for this role, level and location beforehand, know your minimum, give a researched range rather than one hard number, and stay open about the total package.""",
        a_bn=r"""Interviewer দেখতে চান তোমার প্রত্যাশা তাদের budget-এর সাথে মেলে কিনা, আর তুমি ঠান্ডা মাথায় টাকা নিয়ে কথা বলতে পারো কিনা। আগে থেকেই এই role, level আর location-এর range নিয়ে খোঁজ নাও, নিজের সর্বনিম্ন সংখ্যা জেনে রাখো, একটা কঠিন সংখ্যার বদলে খোঁজ নিয়ে বের করা range বলো, আর পুরো package নিয়ে খোলা মন রাখো।""",
        ex_en=r"""
"Based on my research for [role] at my level in [city / remote], and my skills in [stack], I'm looking for something in the range of [your researched range]. I'm flexible depending on the overall package, such as [learning budget, bonus, remote days, growth path]. Could you share the budget range for this role?" """,
        ex_bn=r"""
"[শহর / remote]-এ আমার level-এর [role]-এর জন্য আমার খোঁজখবর আর [stack]-এ আমার skill অনুযায়ী, আমি [তোমার খোঁজ নেওয়া range]-এর মধ্যে কিছু আশা করছি। পুরো package দেখে আমি নমনীয় থাকতে পারি, যেমন [learning budget, bonus, remote দিন, growth path]। এই role-এর budget range কি একটু বলবেন?" """,
        mist_en=r"""- Giving a number with no research behind it.
- Saying "anything is fine", which can signal low confidence.
- Lying about your current salary.
- Arguing aggressively or giving an ultimatum in the first round.""",
        mist_bn=r"""- কোনো খোঁজখবর ছাড়া একটা সংখ্যা বলে দেওয়া।
- "যা দেবেন তাতেই চলবে" বলা, যেটা আত্মবিশ্বাসের অভাব বোঝাতে পারে।
- এখনকার salary নিয়ে মিথ্যা বলা।
- প্রথম round-এই আক্রমণাত্মকভাবে তর্ক করা বা চূড়ান্ত শর্ত দেওয়া।""",
        tip_en=r"""Build your range from sources you trust (job posts that list salaries, people in similar roles) and decide your minimum before the call.""",
        tip_bn=r"""ভরসা করা যায় এমন উৎস থেকে range ঠিক করো (salary লেখা job post, একই ধরনের role-এ থাকা মানুষ), আর call-এর আগেই নিজের সর্বনিম্ন সংখ্যা ঠিক করে রাখো।""",
        follow=[("What is your current salary?", "তোমার এখনকার salary কত?"),
                ("Is your range negotiable?", "তোমার range কি আলোচনাসাপেক্ষ?")],
        related=["beh-012"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-014
    Q(
        id="beh-014", sub="Problem Solving", diff="medium", prio="high", mins=3, **C,
        tags=["requirements", "clarification", "communication", "star"],
        q_en=r"""Tell me about a time you got an unclear requirement. What did you do?""",
        q_bn=r"""এমন একটা সময়ের কথা বলো যখন তুমি অস্পষ্ট requirement পেয়েছিলে। তখন কী করেছিলে?""",
        a_en=r"""They're checking that you clarify before you build. Describe how you asked targeted questions, wrote down your assumptions, confirmed them with an example or a quick mock-up, and delivered in small steps.""",
        a_bn=r"""Interviewer দেখতে চান তুমি বানানোর আগে বিষয়টা পরিষ্কার করে নাও কিনা। বলো কীভাবে নির্দিষ্ট প্রশ্ন করেছ, নিজের অনুমানগুলো লিখে রেখেছ, উদাহরণ বা ছোট mock-up দিয়ে নিশ্চিত হয়েছ, আর ছোট ছোট ধাপে deliver করেছ।""",
        ex_en=r"""
"I got a task to [vague requirement, e.g. 'add a report page']. Instead of guessing, I asked [person] who would use it, what decision it should help with, and which filters and data mattered. I wrote the answers and my assumptions in [the ticket / a short doc], showed a quick [wireframe / sample output], and they changed [something important]. That saved us from building the wrong thing; the first version was ready in [time]." """,
        ex_bn=r"""
"আমাকে একটা task দেওয়া হয়েছিল [অস্পষ্ট requirement, যেমন 'একটা report page যোগ করো']। আন্দাজে না বানিয়ে আমি [ব্যক্তি]-কে জিজ্ঞেস করলাম কে এটা ব্যবহার করবে, কোন সিদ্ধান্ত নিতে এটা সাহায্য করবে, আর কোন filter আর data জরুরি। উত্তর আর আমার অনুমানগুলো [ticket / ছোট একটা doc]-এ লিখে রাখলাম, একটা ছোট [wireframe / sample output] দেখালাম, আর তারা [গুরুত্বপূর্ণ কিছু] বদলাল। এতে ভুল জিনিস বানানো থেকে বেঁচে গেছি; প্রথম version [সময়]-এ তৈরি হয়েছিল।" """,
        mist_en=r"""- Building on assumptions, then blaming the requirement.
- Asking endless questions without proposing anything.
- Agreeing verbally and never writing the decision down.""",
        mist_bn=r"""- অনুমানের ওপর বানিয়ে পরে requirement-কে দোষ দেওয়া।
- কোনো প্রস্তাব না দিয়ে শুধু প্রশ্ন করে যাওয়া।
- মুখে একমত হওয়া, কিন্তু সিদ্ধান্ত কোথাও লিখে না রাখা।""",
        tip_en=r"""Mention writing down assumptions and getting them confirmed; it shows you prevent rework.""",
        tip_bn=r"""অনুমান লিখে রাখা আর সেগুলো confirm করিয়ে নেওয়ার কথা বলো; এতে বোঝা যায় তুমি rework আটকাও।""",
        follow=[("What if the person who wrote the requirement isn't available?", "যিনি requirement দিয়েছেন তাঁকে না পাওয়া গেলে কী করবে?"),
                ("How do you handle requirements that change in the middle of a sprint?", "Sprint-এর মাঝখানে requirement বদলালে কীভাবে সামলাও?")],
        related=["beh-006", "beh-019"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-015
    Q(
        id="beh-015", sub="Teamwork", diff="easy", prio="medium", mins=2, **C,
        tags=["helping", "mentoring", "teamwork", "star"],
        q_en=r"""Tell me about a time you helped a teammate.""",
        q_bn=r"""এমন একটা সময়ের কথা বলো যখন তুমি একজন teammate-কে সাহায্য করেছ।""",
        a_en=r"""They're checking teamwork and whether you lift others up. Use **STAR**: what the teammate was stuck on, how you helped them understand rather than doing it for them, and the result for them and the team.""",
        a_bn=r"""Interviewer teamwork দেখতে চান, আর তুমি অন্যদের এগিয়ে নিতে পারো কিনা। **STAR** ব্যবহার করো: teammate কোথায় আটকে ছিল, তার কাজ নিজে করে না দিয়ে কীভাবে তাকে বুঝতে সাহায্য করেছ, আর তার ও team-এর জন্য ফলাফল কী হয়েছে।""",
        ex_en=r"""
"A [classmate / new teammate] was stuck on [e.g. connecting the frontend to our API and the CORS errors]. I paired with them for [time], explained [concept] using our own code, and let them write the fix while I guided. Afterwards I added [a short README section / checklist]. They [result, e.g. handled the next integration alone], and the next person who joined used that doc too." """,
        ex_bn=r"""
"একজন [classmate / নতুন teammate] [যেমন frontend-কে আমাদের API-এর সাথে যুক্ত করা আর CORS error]-এ আটকে ছিল। আমি [সময়] তার সাথে pair করেছি, আমাদের নিজেদের code দিয়েই [concept] বুঝিয়েছি, আর fix-টা তাকেই লিখতে দিয়েছি, আমি শুধু পথ দেখিয়েছি। পরে আমি [README-তে ছোট একটা অংশ / checklist] যোগ করেছি। সে [ফলাফল, যেমন পরের integration একাই করেছে], আর পরে যে নতুন এসেছে সেও ওই doc ব্যবহার করেছে।" """,
        mist_en=r"""- Sounding condescending about the teammate.
- A story where you simply took over their work.
- No outcome for the person you helped.""",
        mist_bn=r"""- Teammate-কে ছোট করে কথা বলা।
- এমন গল্প যেখানে তুমি শুধু তার কাজটা নিজে করে দিয়েছ।
- যাকে সাহায্য করলে তার কী লাভ হলো সেটা না বলা।""",
        tip_en=r"""Emphasise teaching over doing it yourself; that's what signals future seniority.""",
        tip_bn=r"""নিজে করে দেওয়ার চেয়ে শেখানোর দিকটায় জোর দাও; ভবিষ্যতে senior হওয়ার সম্ভাবনা এখান থেকেই বোঝা যায়।""",
        follow=[("How do you balance helping others with your own tasks?", "অন্যকে সাহায্য করা আর নিজের কাজের মধ্যে ভারসাম্য কীভাবে রাখো?"),
                ("Tell me about a time you asked a teammate for help.", "তুমি কোনো teammate-এর কাছে সাহায্য চেয়েছ এমন একটা ঘটনা বলো।")],
        related=["beh-005", "beh-008"],
        refs=[STAR],
    ),
    # ------------------------------------------------------------------ beh-016
    Q(
        id="beh-016", sub="Growth & Learning", diff="easy", prio="medium", mins=2, **C,
        tags=["learning", "staying-current", "curiosity"],
        q_en=r"""How do you keep up with new technologies?""",
        q_bn=r"""নতুন technology-র সাথে কীভাবে তাল মিলিয়ে চলো?""",
        a_en=r"""They're checking curiosity and a realistic habit, not a long list of websites. Name a few specific sources (official docs and release notes, a newsletter or community), say how you filter what's worth learning, and give one recent thing you actually tried.""",
        a_bn=r"""Interviewer কৌতূহল আর একটা বাস্তব অভ্যাস দেখতে চান, website-এর লম্বা list না। কয়েকটা নির্দিষ্ট উৎসের নাম বলো (official docs আর release notes, কোনো newsletter বা community), কোনটা শেখার যোগ্য তা কীভাবে বাছো সেটা বলো, আর সম্প্রতি সত্যিই চেষ্টা করেছ এমন একটা জিনিসের উদাহরণ দাও।""",
        ex_en=r"""
"I follow the release notes and blogs of the tools I use, like [React / Node.js / your stack], plus [a newsletter, community or local meetup]. I don't chase every trend: I try new things in a small side project first and only bring them to real work when they solve a problem. Recently I learned [topic] and used it in [where]." """,
        ex_bn=r"""
"আমি যে tool-গুলো ব্যবহার করি, যেমন [React / Node.js / তোমার stack], সেগুলোর release notes আর blog follow করি, সাথে [কোনো newsletter, community বা local meetup]। আমি সব trend-এর পেছনে ছুটি না: নতুন কিছু আগে ছোট একটা side project-এ চেষ্টা করি, আর সেটা কোনো সমস্যার সমাধান করলে তবেই আসল কাজে আনি। সম্প্রতি [topic] শিখেছি আর [কোথায়] ব্যবহার করেছি।" """,
        mist_en=r"""- A vague "I read blogs".
- Listing many sources with nothing learned from them.
- Only social media as a source.
- Not being able to name anything recent.""",
        mist_bn=r"""- অস্পষ্টভাবে "blog পড়ি" বলা।
- অনেক উৎসের নাম বলা কিন্তু সেখান থেকে কিছু শেখার উদাহরণ না থাকা।
- শুধু social media-কে উৎস বলা।
- সাম্প্রতিক কোনো কিছুর নাম বলতে না পারা।""",
        tip_en=r"""Name one recent change in your stack that you actually tried; that proves the habit.""",
        tip_bn=r"""তোমার stack-এর একটা সাম্প্রতিক পরিবর্তনের কথা বলো যেটা নিজে চেষ্টা করেছ; সেটাই অভ্যাসের প্রমাণ।""",
        follow=[("What's a recent change in your main framework, and how does it affect you?", "তোমার মূল framework-এ সাম্প্রতিক কোন পরিবর্তন এসেছে, আর সেটা তোমার কাজে কী প্রভাব ফেলে?"),
                ("How do you decide whether to adopt a new tool?", "নতুন একটা tool নেবে কিনা, সেটা কীভাবে ঠিক করো?")],
        related=["beh-007"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-017
    Q(
        id="beh-017", sub="Teamwork", diff="medium", prio="medium", mins=3, **C,
        tags=["remote-work", "async", "communication", "time-zones"],
        q_en=r"""How do you work and collaborate in a remote or async team?""",
        q_bn=r"""Remote বা async team-এ তুমি কীভাবে কাজ আর সহযোগিতা করো?""",
        a_en=r"""They're checking whether you communicate well without someone watching: clear written updates, raising blockers early, respecting time-zone overlap, and keeping decisions in writing. Describe concrete habits and one example.""",
        a_bn=r"""Interviewer দেখতে চান কেউ পাশে না থাকলেও তুমি ভালোভাবে যোগাযোগ রাখো কিনা: পরিষ্কার লিখিত update, blocker আগেভাগে জানানো, time zone-এর overlap মেনে চলা, আর সিদ্ধান্ত লিখে রাখা। নির্দিষ্ট অভ্যাস আর একটা উদাহরণ দিয়ে বলো।""",
        ex_en=r"""
"On [remote project / freelance work / open-source contribution], the team was spread across [time zones]. I posted a short daily update: what I finished, what's next, and any blockers. When I was blocked, I wrote the question with context, what I'd tried and links, so someone could answer while I was offline, and I switched to another task meanwhile. We used [GitHub issues, Slack, a shared doc], and I kept decisions in the PR or ticket so nothing got lost in chat." """,
        ex_bn=r"""
"[Remote project / freelance কাজ / open-source contribution]-এ team ছড়িয়ে ছিল [কোন কোন time zone]-এ। আমি প্রতিদিন ছোট একটা update দিতাম: কী শেষ করেছি, পরে কী করব, আর কোনো blocker আছে কিনা। আটকে গেলে context, কী কী চেষ্টা করেছি আর link-সহ প্রশ্ন লিখে রাখতাম, যাতে আমি offline থাকলেও কেউ উত্তর দিতে পারে, আর ততক্ষণে অন্য task-এ চলে যেতাম। আমরা [GitHub issues, Slack, shared doc] ব্যবহার করতাম, আর সিদ্ধান্তগুলো PR বা ticket-এ লিখে রাখতাম যাতে chat-এ হারিয়ে না যায়।" """,
        mist_en=r"""- "I just need a laptop and internet" with no communication habits.
- No example of good written communication.
- Going silent when blocked.
- Ignoring time-zone overlap and meeting expectations.""",
        mist_bn=r"""- "আমার শুধু laptop আর internet লাগে" বলা, যোগাযোগের কোনো অভ্যাসের কথা না বলা।
- ভালো লিখিত যোগাযোগের কোনো উদাহরণ না থাকা।
- আটকে গেলে চুপ হয়ে যাওয়া।
- Time zone-এর overlap আর meeting-এর প্রত্যাশা উপেক্ষা করা।""",
        tip_en=r"""Remember that your emails and messages during the hiring process are evidence of your written communication.""",
        tip_bn=r"""মনে রেখো, hiring process-এর সময় তোমার email আর message-ই তোমার লিখিত যোগাযোগের প্রমাণ।""",
        follow=[("What do you do if a teammate doesn't reply for a whole day?", "কোনো teammate সারা দিন উত্তর না দিলে কী করো?"),
                ("How do you stay productive working from home?", "বাসা থেকে কাজ করার সময় কীভাবে productive থাকো?")],
        related=["beh-006", "beh-015"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-018
    Q(
        id="beh-018", sub="Closing", diff="easy", prio="high", mins=2, **C,
        tags=["closing", "questions-for-interviewer", "engagement"],
        q_en=r"""Do you have any questions for us? What should you ask the interviewer at the end?""",
        q_bn=r"""আমাদের জন্য তোমার কোনো প্রশ্ন আছে? Interview-এর শেষে interviewer-কে কী জিজ্ঞেস করা উচিত?""",
        a_en=r"""They're checking genuine interest and judgement. Always have two or three thoughtful questions about the work, the team and how you'd grow; avoid questions their website already answers, and don't make perks your first question in an early round.""",
        a_bn=r"""Interviewer সত্যিকারের আগ্রহ আর বিচারবুদ্ধি দেখতে চান। কাজ, team আর তুমি কীভাবে grow করবে তা নিয়ে সবসময় দুই-তিনটা ভেবে-চিন্তে তৈরি প্রশ্ন রাখো; website-এ যার উত্তর আছে এমন প্রশ্ন কোরো না, আর শুরুর round-এ প্রথম প্রশ্নই সুবিধা নিয়ে কোরো না।""",
        ex_en=r"""Sample questions:

- "What does a typical week look like for someone in this role?"
- "What would you expect me to achieve in the first three months?"
- "How does the team handle code reviews and deployments?"
- "What's the biggest technical challenge the team is working on right now?"
- "What are the next steps in the process?" """,
        ex_bn=r"""নমুনা প্রশ্ন:

- "এই role-এ একজনের সাধারণ একটা সপ্তাহ কেমন কাটে?"
- "প্রথম তিন মাসে আমার কাছ থেকে কী আশা করবেন?"
- "Team-এ code review আর deployment কীভাবে হয়?"
- "Team এখন সবচেয়ে বড় কোন technical challenge নিয়ে কাজ করছে?"
- "Process-এর পরের ধাপ কী?" """,
        mist_en=r"""- "No, I don't have any questions."
- Asking only about salary or leave in a first-round interview.
- Questions easily answered by the company website.
- Long, rambling questions.""",
        mist_bn=r"""- "না, আমার কোনো প্রশ্ন নেই" বলা।
- প্রথম round-এ শুধু salary বা ছুটি নিয়ে প্রশ্ন করা।
- Company-র website দেখলেই উত্তর পাওয়া যায় এমন প্রশ্ন।
- লম্বা, এলোমেলো প্রশ্ন।""",
        tip_en=r"""Prepare five questions and ask the two or three that weren't already answered during the interview.""",
        tip_bn=r"""পাঁচটা প্রশ্ন তৈরি রাখো, আর interview-এর মধ্যে যেগুলোর উত্তর এখনো আসেনি তার থেকে দুই-তিনটা জিজ্ঞেস করো।""",
        follow=[("Is there anything else you'd like to add before we finish?", "শেষ করার আগে আর কিছু যোগ করতে চাও?"),
                ("Do you have any concerns about this role?", "এই role নিয়ে তোমার কোনো দুশ্চিন্তা আছে?")],
        related=["beh-009"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-019
    Q(
        id="beh-019", sub="Communication", diff="medium", prio="medium", mins=2, **C,
        tags=["communication", "non-technical", "explaining", "analogy"],
        q_en=r"""How would you explain a technical concept, such as an API, to a non-technical person?""",
        q_bn=r"""একজন non-technical মানুষকে একটা technical concept, যেমন API, কীভাবে বোঝাবে?""",
        a_en=r"""They're checking clarity and empathy, often by asking you to explain something live. Start from what the listener cares about, use a simple analogy that is accurate, skip jargon, and check that they understood.""",
        a_bn=r"""Interviewer স্পষ্টতা আর অন্যের জায়গা থেকে ভাবার ক্ষমতা দেখতে চান, প্রায়ই সাথে সাথে কিছু একটা বোঝাতে বলে। শ্রোতা কী নিয়ে চিন্তা করেন সেখান থেকে শুরু করো, সহজ কিন্তু সঠিক একটা উপমা দাও, jargon বাদ দাও, আর শেষে জেনে নাও তিনি বুঝেছেন কিনা।""",
        ex_en=r"""
"If a [client / manager] asks what an API is, I'd say: 'Think of a restaurant. The kitchen is our server, where the data lives. The API is the menu plus the waiter: it lists what you're allowed to ask for and brings back the answer in a fixed format. When the mobile app shows your orders, it's asking our API for them.' Then I'd check it made sense and link it to their real question, for example why a new feature needs backend work." """,
        ex_bn=r"""
"কোনো [client / manager] যদি জিজ্ঞেস করেন API কী, আমি বলব: 'একটা restaurant-এর কথা ভাবুন। রান্নাঘর হলো আমাদের server, যেখানে data থাকে। API হলো menu আর waiter মিলিয়ে: কী কী চাওয়া যাবে তার list দেয়, আর উত্তরটা একটা নির্দিষ্ট format-এ নিয়ে আসে। Mobile app যখন আপনার order দেখায়, তখন সেটা আমাদের API-এর কাছে order-গুলো চায়।' তারপর জেনে নেব বোঝা গেল কিনা, আর তাঁর আসল প্রশ্নের সাথে যুক্ত করব, যেমন নতুন feature-এ কেন backend-এর কাজ লাগে।" """,
        mist_en=r"""- Using jargon to explain jargon.
- Analogies that are wrong or take longer than the explanation itself.
- Talking down to the listener.
- Never checking whether they understood.""",
        mist_bn=r"""- Jargon বোঝাতে আরও jargon ব্যবহার করা।
- ভুল উপমা, বা এমন উপমা যেটা আসল ব্যাখ্যার চেয়েও লম্বা।
- শ্রোতাকে ছোট করে কথা বলা।
- তিনি বুঝলেন কিনা কখনো জিজ্ঞেস না করা।""",
        tip_en=r"""Practise explaining three basics (API, database, cache) in under a minute each.""",
        tip_bn=r"""তিনটা মৌলিক জিনিস (API, database, cache) প্রতিটা এক মিনিটের কম সময়ে বোঝানোর practice করো।""",
        follow=[("Now explain caching the same way.", "এবার একইভাবে caching বোঝাও।"),
                ("How would you tell a client that a feature will take longer than expected?", "Client-কে কীভাবে বলবে যে একটা feature-এ আশার চেয়ে বেশি সময় লাগবে?")],
        related=["beh-014"],
        refs=[],
    ),
    # ------------------------------------------------------------------ beh-020
    Q(
        id="beh-020", sub="Introduction", diff="medium", prio="medium", mins=2, **C,
        tags=["career-gap", "career-switch", "honesty"],
        q_en=r"""There's a gap in your CV, or you're switching into tech from another field. Can you explain?""",
        q_bn=r"""তোমার CV-তে একটা gap আছে, বা তুমি অন্য field থেকে tech-এ আসছ। একটু ব্যাখ্যা করবে?""",
        a_en=r"""They're checking that the gap or switch is explained honestly and that you're ready now. Explain it briefly and truthfully, then spend most of the answer on proof: what you built and learned, and why you're committed to this path.""",
        a_bn=r"""Interviewer দেখতে চান gap বা field বদলের ব্যাখ্যা সৎ কিনা, আর তুমি এখন তৈরি কিনা। সংক্ষেপে আর সত্যি করে ব্যাখ্যা করো, তারপর উত্তরের বেশিরভাগ সময় দাও প্রমাণে: কী বানিয়েছ আর শিখেছ, আর কেন এই পথে তুমি সিরিয়াস।""",
        ex_en=r"""
"After [previous degree / job], I [honest reason for the gap, e.g. had family responsibilities / was preparing for exams / worked in another field]. During [period], I [what you did: learned JavaScript and Node.js from the official docs and a course, built [projects], contributed to [something]]. It's all on my GitHub at [link]. I'm moving into development because [genuine reason], and my [previous background, e.g. accounting] helps me understand [a relevant domain]." """,
        ex_bn=r"""
"[আগের degree / job]-এর পরে আমি [gap-এর সত্যি কারণ, যেমন পারিবারিক দায়িত্ব ছিল / পরীক্ষার প্রস্তুতি নিচ্ছিলাম / অন্য field-এ কাজ করছিলাম]। [সময়]-এর মধ্যে আমি [কী করেছ: official docs আর একটা course থেকে JavaScript ও Node.js শিখেছি, [project] বানিয়েছি, [কিছুতে] contribute করেছি]। সব আমার GitHub-এ আছে, [link]। Development-এ আসছি কারণ [সত্যিকারের কারণ], আর আমার [আগের background, যেমন accounting] আমাকে [প্রাসঙ্গিক domain] বুঝতে সাহায্য করে।" """,
        mist_en=r"""- Hiding the gap or inventing a job to cover it.
- Over-sharing personal details.
- Apologising instead of showing progress.
- No visible evidence of your skills (projects, code, certificates you can explain).""",
        mist_bn=r"""- Gap লুকানো বা সেটা ঢাকতে কোনো job বানিয়ে বলা।
- ব্যক্তিগত বিষয় অতিরিক্ত বলা।
- অগ্রগতি না দেখিয়ে শুধু ক্ষমা চাওয়া।
- Skill-এর দৃশ্যমান কোনো প্রমাণ না থাকা (project, code, এমন certificate যা তুমি ব্যাখ্যা করতে পারো)।""",
        tip_en=r"""One or two sentences on the gap, then move to proof: projects and what you can do today.""",
        tip_bn=r"""Gap নিয়ে এক-দুই বাক্য, তারপর প্রমাণে চলে যাও: project আর আজ তুমি কী করতে পারো।""",
        follow=[("Why should we pick you over a candidate with a CS degree?", "CS degree আছে এমন candidate-এর বদলে তোমাকে কেন নেব?"),
                ("How will you keep learning while working full time?", "Full time কাজের পাশাপাশি কীভাবে শেখা চালিয়ে যাবে?")],
        related=["beh-001", "beh-007"],
        refs=[],
    ),
]

if __name__ == "__main__":
    save("behavioral", "b1", QUESTIONS)
