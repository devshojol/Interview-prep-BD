# EXAMPLE batch file — copy this pattern. (This file lives in docs/ and is NOT part of the bank.)
# Real batches go in data/src/<tech>_b<N>.py and are run with: python3 data/src/<tech>_b<N>.py
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from qb import Q, save  # noqa: E402

MDN_LET = ("MDN — let", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let")
MDN_CONST = ("MDN — const", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const")
MDN_VAR = ("MDN — var", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var")

QUESTIONS = [
    Q(
        id="js-example-001", sub="Variables & Scope", diff="easy", type="conceptual",
        prio="high", market="both", mins=2,
        tags=["var", "let", "const", "scope", "hoisting"],
        ver="Version-independent (ES2015+; current spec ECMAScript 2026)", vs=False, status="stable",
        q_en=r"""What is the difference between `let`, `const`, and `var` in JavaScript?""",
        q_bn=r"""JavaScript-এ `let`, `const` এবং `var`-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""
            `var` is function-scoped, while `let` and `const` are block-scoped. A variable declared with `let` can be reassigned, but a `const` binding cannot be reassigned. Their initialization and hoisting behaviour also differ: `var` is hoisted and initialised to `undefined`, while `let`/`const` are hoisted but stay in the **temporal dead zone** until the declaration runs.

            In modern JavaScript I use `const` by default and switch to `let` only when I really need reassignment. I avoid `var` in new code.
        """,
        a_bn=r"""
            `var` হলো function-scoped, আর `let` ও `const` হলো block-scoped। `let` দিয়ে তৈরি variable-এর value পরিবর্তন করা যায়, কিন্তু `const` binding-কে নতুন value assign করা যায় না। এদের initialization ও hoisting-এর আচরণেও পার্থক্য আছে: `var` hoist হয়ে `undefined` দিয়ে initialize হয়, আর `let`/`const` hoist হলেও declaration line execute না হওয়া পর্যন্ত **temporal dead zone**-এ থাকে।

            আধুনিক JavaScript-এ আমি default হিসেবে `const` ব্যবহার করি, আর reassignment সত্যিই দরকার হলে `let`। নতুন code-এ `var` এড়িয়ে চলি।
        """,
        ex_en=r"""
            - **Scope:** `var` ignores `if`/`for` blocks, which is why the classic loop-with-`setTimeout` bug happens.
            - **Re-declaration:** `var x; var x;` is allowed; `let`/`const` re-declaration in the same scope is a SyntaxError.
            - **Global object:** a top-level `var` in a classic script becomes a property of `globalThis`; `let`/`const` do not.
            - **`const` is not immutability:** `const user = {}` still allows `user.name = 'A'`. Use `Object.freeze` for shallow immutability.
        """,
        ex_bn=r"""
            - **Scope:** `var` `if`/`for` block মানে না — এজন্যই loop-এর ভেতর `setTimeout`-এর classic bug হয়।
            - **Re-declaration:** `var x; var x;` চলে, কিন্তু একই scope-এ `let`/`const` আবার declare করলে SyntaxError হয়।
            - **Global object:** classic script-এর top-level `var`, `globalThis`-এর property হয়ে যায়; `let`/`const` হয় না।
            - **`const` মানেই immutable নয়:** `const user = {}` করার পরও `user.name = 'A'` করা যায়। Shallow immutability-র জন্য `Object.freeze` ব্যবহার করতে হয়।
        """,
        tip_en=r"""Explain scope first, then reassignment, and finally hoisting and the temporal dead zone if the interviewer asks for more detail.""",
        tip_bn=r"""প্রথমে scope-এর পার্থক্য বোঝাও। এরপর reassignment, আর interviewer আরও জানতে চাইলে hoisting ও temporal dead zone ব্যাখ্যা করো।""",
        mist_en=r"""Saying `const` makes objects immutable, or saying `let`/`const` are "not hoisted".""",
        mist_bn=r"""`const` দিলে object immutable হয়ে যায় বলা, অথবা `let`/`const` "hoist হয় না" বলা।""",
        code=r"""
            function example() {
              if (true) {
                var a = 10;
                let b = 20;
                const c = 30;
              }
              console.log(a); // 10
              // console.log(b); // ReferenceError
              // console.log(c); // ReferenceError
            }
            example();
        """,
        lang="javascript", output=r"""10""",
        follow=[
            ("What is the temporal dead zone?", "Temporal dead zone (TDZ) কী?"),
            ("Why does `for (var i...)` with `setTimeout` print the same number?", "`for (var i...)` আর `setTimeout` একসাথে ব্যবহার করলে একই সংখ্যা কেন print হয়?"),
        ],
        related=["js-example-002"],
        refs=[MDN_LET, MDN_CONST, MDN_VAR],
    ),
    Q(
        id="js-example-002", sub="Variables & Scope", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["tdz", "let", "hoisting"],
        ver="Version-independent (ES2015+)", status="stable",
        q_en=r"""What happens when this runs?  `console.log(x); let x = 5;`""",
        q_bn=r"""এই code run করলে কী হবে?  `console.log(x); let x = 5;`""",
        options=[
            ("It logs `undefined`", "`undefined` log হবে"),
            ("It throws a `ReferenceError`", "`ReferenceError` throw হবে"),
            ("It logs `5`", "`5` log হবে"),
            ("It throws a `SyntaxError`", "`SyntaxError` throw হবে"),
        ],
        correct=1,
        a_en=r"""It throws a `ReferenceError` because `x` is in the temporal dead zone until the `let` declaration is evaluated.""",
        a_bn=r"""`ReferenceError` throw হবে, কারণ `let` declaration evaluate না হওয়া পর্যন্ত `x` temporal dead zone-এ থাকে।""",
        ex_en=r"""
            `let` bindings are hoisted (the engine knows about them when the scope is created) but they are **not initialised**. Reading them before the declaration throws. With `var`, the same code would log `undefined`, which is why many candidates pick option A — that's the classic trap.
        """,
        ex_bn=r"""
            `let` binding hoist হয় (scope তৈরির সময়ই engine এগুলো জানে), কিন্তু **initialize হয় না**। Declaration-এর আগে read করলে error throw হয়। `var` হলে একই code `undefined` log করত — এজন্য অনেকে option A বেছে নেয়, এটাই classic trap।
        """,
        tip_en=r"""Mention that `let` IS hoisted — the difference is initialisation. That one sentence shows depth.""",
        tip_bn=r"""বলো যে `let`-ও hoist হয় — পার্থক্য হলো initialization-এ। এই একটা কথাই তোমার গভীর বোঝাপড়া দেখায়।""",
        refs=[MDN_LET],
    ),
]

if __name__ == "__main__":
    save("javascript", "example", QUESTIONS)
