# React Native (with Expo) — batch 3 (rn-017..rn-024): navigation, deep linking, storage, expo-sqlite
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_ROUTER_CORE = ("Expo docs — Expo Router core concepts", "https://docs.expo.dev/router/basics/core-concepts/")
R_ROUTER_NOTATION = ("Expo docs — Expo Router notation", "https://docs.expo.dev/router/basics/notation/")
R_ROUTER_NAV = ("Expo docs — Navigate between pages", "https://docs.expo.dev/router/basics/navigation/")
R_ROUTER_PARAMS = ("Expo docs — URL parameters", "https://docs.expo.dev/router/reference/url-parameters/")
R_ROUTER_MODALS = ("Expo docs — Modals", "https://docs.expo.dev/router/advanced/modals/")
R_ROUTER_TABS = ("Expo docs — Tabs", "https://docs.expo.dev/router/advanced/tabs/")
R_RN_NESTING = ("React Navigation — Nesting navigators", "https://reactnavigation.org/docs/nesting-navigators/")
R_LINK_INTO = ("Expo docs — Linking into your app", "https://docs.expo.dev/linking/into-your-app/")
R_LINK_IOS = ("Expo docs — iOS Universal Links", "https://docs.expo.dev/linking/ios-universal-links/")
R_LINK_ANDROID = ("Expo docs — Android App Links", "https://docs.expo.dev/linking/android-app-links/")
R_STORE_DATA = ("Expo docs — Store data", "https://docs.expo.dev/develop/user-interface/store-data/")
R_SECURESTORE = ("Expo docs — SecureStore", "https://docs.expo.dev/versions/latest/sdk/securestore/")
R_MMKV = ("react-native-mmkv (GitHub)", "https://github.com/mrousavy/react-native-mmkv")
R_SQLITE = ("Expo docs — SQLite (expo-sqlite)", "https://docs.expo.dev/versions/latest/sdk/sqlite/")
R_SQLITE_PRAGMA = ("SQLite — PRAGMA statements", "https://www.sqlite.org/pragma.html")
R_SQLITE_WAL = ("SQLite — Write-Ahead Logging", "https://www.sqlite.org/wal.html")
R_OWASP_SQLI = ("OWASP — SQL Injection Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html")

VER = "React Native 0.88, Expo SDK 58 (expo-router ~58)"
VER_SQL = "Expo SDK 58 (expo-sqlite ~58), React Native 0.88"

QUESTIONS = [
    # ------------------------------------------------------------------ rn-017
    Q(
        id="rn-017", sub="Navigation (Expo Router)", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["expo-router", "file-based-routing", "layouts", "dynamic-routes"],
        ver=VER, vs=True, status="stable",
        q_en=r"""How does file-based routing work in Expo Router? Explain what `_layout.tsx`, `index.tsx` and `[id].tsx` do, and how you move between screens with `Link` and `router.push`.""",
        q_bn=r"""Expo Router-এ file-based routing কীভাবে কাজ করে? `_layout.tsx`, `index.tsx` আর `[id].tsx` কী কাজ করে, আর `Link` ও `router.push` দিয়ে কীভাবে এক screen থেকে আরেক screen-এ যাও, ব্যাখ্যা করো।""",
        a_en=r"""
            In Expo Router every file inside the routes directory (`src/app/` in the current template; older projects use a top-level `app/`) is a screen, and its URL is its file path.

            - `index.tsx` is the default screen of its folder: `src/app/index.tsx` is `/`.
            - `[id].tsx` is a **dynamic route**: `src/app/products/[id].tsx` matches `/products/42`, and the screen reads `id` with `useLocalSearchParams()`.
            - `_layout.tsx` is not a screen. It wraps the routes in its folder, usually with a navigator (`<Stack />`, `<Tabs />`) or providers. The root `_layout.tsx` runs first, so fonts, theme and providers go there.
            - Folders in parentheses such as `(tabs)` are **groups**: they organise files and layouts without adding to the URL.

            To navigate I use `<Link href="/products/42">` (or an object href with `pathname` + `params`) for taps, and the `router` object (`router.push`, `router.navigate`, `router.replace`, `router.back`) in code. Underneath it is React Navigation 7, and because every screen has a URL, every screen is deep-linkable for free.
        """,
        a_bn=r"""
            Expo Router-এ routes directory-র (বর্তমান template-এ `src/app/`; পুরনো project-এ top-level `app/`) ভেতরের প্রতিটা file একটা screen, আর তার URL হলো তার file path।

            - `index.tsx` হলো folder-এর default screen: `src/app/index.tsx` মানে `/`।
            - `[id].tsx` একটা **dynamic route**: `src/app/products/[id].tsx` `/products/42`-এর সাথে match করে, আর screen-টা `useLocalSearchParams()` দিয়ে `id` পড়ে।
            - `_layout.tsx` কোনো screen না। এটা নিজের folder-এর route-গুলোকে wrap করে, সাধারণত একটা navigator (`<Stack />`, `<Tabs />`) বা provider দিয়ে। Root `_layout.tsx` সবার আগে চলে, তাই font, theme আর provider সেখানে রাখি।
            - `(tabs)`-এর মতো বন্ধনীর ভেতরের folder হলো **group**: URL-এ কিছু যোগ না করেই file আর layout সাজাতে সাহায্য করে।

            Navigate করতে tap-এর জন্য `<Link href="/products/42">` (অথবা `pathname` + `params`-সহ object href) আর code-এ `router` object (`router.push`, `router.navigate`, `router.replace`, `router.back`) ব্যবহার করি। ভেতরে আসলে React Navigation 7 চলে, আর প্রতিটা screen-এর URL থাকায় সব screen আপনা-আপনি deep link করা যায়।
        """,
        quick_en=r"""In Expo Router each file in `src/app/` is a screen whose URL is its path: `index.tsx` is the folder's default route, `[id].tsx` is a dynamic segment read with `useLocalSearchParams`, and `_layout.tsx` wraps sibling routes in a navigator like `Stack` or `Tabs`. You navigate with `<Link href>` or `router.push`/`router.navigate`.""",
        quick_bn=r"""Expo Router-এ `src/app/`-এর প্রতিটা file একটা screen, আর তার URL হলো file path: `index.tsx` folder-এর default route, `[id].tsx` dynamic segment যেটা `useLocalSearchParams` দিয়ে পড়া হয়, আর `_layout.tsx` পাশের route-গুলোকে `Stack` বা `Tabs`-এর মতো navigator-এ wrap করে। Navigate করা হয় `<Link href>` বা `router.push`/`router.navigate` দিয়ে।""",
        ex_en=r"""
            - **`push` vs `navigate`:** `router.push` always adds a new screen to the stack. `router.navigate` either pushes or unwinds back to an existing matching route, so it is usually the one to use for menu-style navigation. `router.replace` swaps the current screen (good after login).
            - **`Link` renders a `<Text>`** by default; to make a card or button the link, use `<Link href=... asChild>` around a `Pressable`.
            - **Special files:** `+not-found.tsx` catches unmatched URLs. Anything that isn't a screen (components, hooks, utils) must live **outside** `src/app/`, or Expo Router will try to treat it as a route.
            - **Typed routes:** with typed routes enabled, a wrong `href` like `/prodcts/42` is a TypeScript error.
            - **Screen options** can be set in the layout (`<Stack.Screen name="products/[id]" options={...} />`) or from inside the screen with `<Stack.Screen options={...} />`.
            - Before Expo Router, apps declared every screen by hand in React Navigation's `createNativeStackNavigator()` and wrote a separate linking config. That still works, but new Expo apps start with Expo Router.
        """,
        ex_bn=r"""
            - **`push` বনাম `navigate`:** `router.push` সবসময় stack-এ নতুন screen যোগ করে। `router.navigate` হয় push করে, নয়তো stack-এ আগে থেকে থাকা match করা route-এ ফিরে যায়, তাই menu-ধরনের navigation-এ সাধারণত এটাই ব্যবহার করি। `router.replace` বর্তমান screen বদলে দেয় (login-এর পরে কাজে লাগে)।
            - **`Link` default-ভাবে একটা `<Text>` render করে**; পুরো card বা button-কে link বানাতে `Pressable`-এর চারপাশে `<Link href=... asChild>` দাও।
            - **Special file:** `+not-found.tsx` match না হওয়া URL ধরে। যেটা screen না (component, hook, utils), সেটা অবশ্যই `src/app/`-এর **বাইরে** রাখতে হবে, নইলে Expo Router সেটাকে route ভাবার চেষ্টা করবে।
            - **Typed routes:** typed routes চালু থাকলে `/prodcts/42`-এর মতো ভুল `href` TypeScript error দেয়।
            - **Screen options** layout-এ (`<Stack.Screen name="products/[id]" options={...} />`) অথবা screen-এর ভেতর থেকে `<Stack.Screen options={...} />` দিয়ে set করা যায়।
            - Expo Router-এর আগে React Navigation-এর `createNativeStackNavigator()`-এ প্রতিটা screen হাতে declare করতে হতো আর আলাদা linking config লিখতে হতো। সেটা এখনো চলে, কিন্তু নতুন Expo app Expo Router দিয়েই শুরু হয়।
        """,
        tip_en=r"""Draw the folder tree first and map each file to its URL; then say "layouts hold navigators, groups don't change the URL, and every screen is deep-linkable". That covers what the interviewer wants in one minute.""",
        tip_bn=r"""আগে folder tree এঁকে প্রতিটা file-কে তার URL-এর সাথে মিলিয়ে দেখাও; তারপর বলো "layout-এ navigator থাকে, group URL বদলায় না, আর প্রতিটা screen deep link করা যায়"। এক মিনিটেই interviewer যা শুনতে চায় সব বলা হয়ে যায়।""",
        mist_en=r"""Putting shared components or hooks inside `src/app/` (they become routes), treating `_layout.tsx` as a screen, and using `router.push` everywhere so the same screen piles up on the stack.""",
        mist_bn=r"""Shared component বা hook `src/app/`-এর ভেতরে রাখা (তখন সেগুলো route হয়ে যায়), `_layout.tsx`-কে screen ভাবা, আর সব জায়গায় `router.push` ব্যবহার করা, ফলে একই screen stack-এ বারবার জমতে থাকে।""",
        code=r"""
            // src/app/_layout.tsx        → root Stack navigator (not a screen)
            // src/app/index.tsx          → "/"
            // src/app/cart.tsx           → "/cart"
            // src/app/products/[id].tsx  → "/products/42"
            // src/app/+not-found.tsx     → any unmatched URL

            // src/app/_layout.tsx
            import { Stack } from 'expo-router';

            export default function RootLayout() {
              return <Stack />;
            }

            // src/app/index.tsx
            import { Link, router } from 'expo-router';
            import { Button, View } from 'react-native';

            export default function Home() {
              return (
                <View>
                  <Link href={{ pathname: '/products/[id]', params: { id: '42' } }}>Open product 42</Link>
                  <Button title="Open cart" onPress={() => router.push('/cart')} />
                </View>
              );
            }

            // src/app/products/[id].tsx
            import { Stack, useLocalSearchParams } from 'expo-router';
            import { Text } from 'react-native';

            export default function ProductScreen() {
              const { id } = useLocalSearchParams<{ id: string }>();
              return (
                <>
                  <Stack.Screen options={{ title: `Product ${id}` }} />
                  <Text>Product id: {id}</Text>
                </>
              );
            }
        """,
        lang="tsx",
        follow=[
            ("What is the difference between `router.push`, `router.navigate` and `router.replace`?", "`router.push`, `router.navigate` আর `router.replace`-এর মধ্যে পার্থক্য কী?"),
            ("How would you protect screens that need a logged-in user?", "Login করা user লাগে এমন screen-গুলো তুমি কীভাবে protect করবে?"),
        ],
        related=["rn-018", "rn-019", "rn-020"],
        refs=[R_ROUTER_CORE, R_ROUTER_NOTATION, R_ROUTER_NAV],
    ),
    # ------------------------------------------------------------------ rn-018
    Q(
        id="rn-018", sub="Navigation (Expo Router)", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["expo-router", "tabs", "stack", "modal", "nested-navigators"],
        ver=VER, vs=True, status="stable",
        q_en=r"""Your app has a bottom tab bar with **Home** and **Settings**. A **New post** screen must slide up as a modal that covers the whole screen, including the tab bar, and its URL should be `/new-post`. Which Expo Router setup does this?""",
        q_bn=r"""তোমার app-এ **Home** আর **Settings** নিয়ে একটা bottom tab bar আছে। **New post** screen-টা modal হিসেবে নিচ থেকে উঠে পুরো screen ঢেকে দেবে, tab bar-সহ, আর তার URL হবে `/new-post`। কোন Expo Router setup এটা করবে?""",
        options=[
            ("Make the root `_layout.tsx` a `<Tabs>` navigator and add `new-post.tsx` as a third tab with `options={{ presentation: 'modal' }}`",
             "Root `_layout.tsx`-কে `<Tabs>` navigator বানাও আর `new-post.tsx`-কে তৃতীয় tab হিসেবে `options={{ presentation: 'modal' }}` দিয়ে যোগ করো"),
            ("Keep a single `<Tabs>` layout, hide the `new-post` tab with `href: null`, and open it with `router.push('/new-post')`",
             "একটাই `<Tabs>` layout রাখো, `href: null` দিয়ে `new-post` tab লুকাও, আর `router.push('/new-post')` দিয়ে খোলো"),
            ("Make the root `_layout.tsx` a `<Stack>` with two screens, `(tabs)` (`headerShown: false`) and `new-post` (`presentation: 'modal'`), and put the `<Tabs>` layout in `(tabs)/_layout.tsx`",
             "Root `_layout.tsx`-কে দুইটা screen-সহ `<Stack>` বানাও, `(tabs)` (`headerShown: false`) আর `new-post` (`presentation: 'modal'`), আর `<Tabs>` layout রাখো `(tabs)/_layout.tsx`-এ"),
            ("Any screen opens as a modal if you navigate to it with `router.replace` instead of `router.push`",
             "`router.push`-এর বদলে `router.replace` দিয়ে navigate করলে যেকোনো screen modal হিসেবে খোলে"),
        ],
        correct=2,
        a_en=r"""
            The root layout is a **Stack** whose first screen is the `(tabs)` group and whose second screen is `new-post` with `presentation: 'modal'`. Because the modal is a sibling of the whole tab navigator in the parent stack, it is presented above the tabs and covers the tab bar. The group name `(tabs)` isn't part of the URL, so the modal is `/new-post` and the tabs are `/` and `/settings`.
        """,
        a_bn=r"""
            Root layout হবে একটা **Stack**, যার প্রথম screen `(tabs)` group আর দ্বিতীয় screen `new-post`, `presentation: 'modal'`-সহ। Modal-টা parent stack-এ পুরো tab navigator-এর পাশাপাশি (sibling) থাকায় এটা tab-গুলোর ওপরে present হয় আর tab bar ঢেকে দেয়। Group-এর নাম `(tabs)` URL-এর অংশ না, তাই modal-এর URL `/new-post`, আর tab-গুলো `/` ও `/settings`।
        """,
        quick_en=r"""Use a root `<Stack>` that contains the `(tabs)` group (with `headerShown: false`) and a `new-post` screen with `presentation: 'modal'`, and put `<Tabs>` in `(tabs)/_layout.tsx`. The modal sits above the whole tab navigator, so it covers the tab bar, and groups don't change the URL.""",
        quick_bn=r"""Root-এ একটা `<Stack>` রাখো, যার ভেতরে `(tabs)` group (`headerShown: false`) আর `presentation: 'modal'`-সহ `new-post` screen, আর `<Tabs>` রাখো `(tabs)/_layout.tsx`-এ। Modal-টা পুরো tab navigator-এর ওপরে থাকে, তাই tab bar ঢেকে দেয়, আর group URL বদলায় না।""",
        ex_en=r"""
            The tempting wrong answer is the **hidden tab** (`href: null`). That hides the tab button, but the screen still renders *inside* the tab navigator: the tab bar stays visible and there's no modal presentation. `presentation` is a **stack** option (native stack), so adding it to a `Tabs` screen does nothing useful, and `router.replace` only swaps the current route; it doesn't change how a screen is presented.

            The rule to remember: a screen can only cover the navigator it belongs to, so put things that must cover the tab bar (modals, full-screen flows such as checkout or onboarding) in a stack **above** the tabs. Each tab can still have its own stack (`(tabs)/home/_layout.tsx` with a `<Stack>`) for push navigation inside the tab. Close the modal with `router.back()`.
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল উত্তর হলো **লুকানো tab** (`href: null`)। এতে tab button লুকায়, কিন্তু screen-টা তখনো tab navigator-এর *ভেতরেই* render হয়: tab bar দেখা যায়, আর কোনো modal presentation হয় না। `presentation` হলো **stack**-এর option (native stack), তাই `Tabs` screen-এ এটা দিলে কাজের কিছু হয় না, আর `router.replace` শুধু বর্তমান route বদলায়; screen কীভাবে present হবে সেটা বদলায় না।

            মনে রাখার নিয়ম: একটা screen শুধু নিজের navigator-কেই ঢাকতে পারে, তাই যেগুলো tab bar ঢাকবে (modal, checkout বা onboarding-এর মতো full-screen flow) সেগুলো tab-এর **ওপরের** stack-এ রাখো। প্রতিটা tab-এর ভেতরে push navigation-এর জন্য আলাদা stack-ও রাখা যায় (`(tabs)/home/_layout.tsx`-এ একটা `<Stack>`)। Modal বন্ধ করতে `router.back()` ব্যবহার করো।
        """,
        tip_en=r"""Sketch the navigator tree (Stack → Tabs → screens, plus the modal next to Tabs) before answering. Interviewers like hearing "a screen can only cover the navigator it lives in".""",
        tip_bn=r"""উত্তর দেওয়ার আগে navigator tree এঁকে দেখাও (Stack → Tabs → screen, আর Tabs-এর পাশে modal)। "একটা screen শুধু নিজের navigator-কেই ঢাকতে পারে" কথাটা interviewer শুনতে পছন্দ করে।""",
        mist_en=r"""Nesting the stack inside a tab and then wondering why a "full-screen" checkout still shows the tab bar.""",
        mist_bn=r"""Stack-কে tab-এর ভেতরে nest করে তারপর অবাক হওয়া যে "full-screen" checkout-এ কেন এখনো tab bar দেখা যাচ্ছে।""",
        code=r"""
            // src/app/_layout.tsx
            import { Stack } from 'expo-router';

            export default function RootLayout() {
              return (
                <Stack>
                  <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
                  <Stack.Screen name="new-post" options={{ presentation: 'modal', title: 'New post' }} />
                </Stack>
              );
            }

            // src/app/(tabs)/_layout.tsx   → "/" and "/settings"
            import { Tabs } from 'expo-router';

            export default function TabLayout() {
              return (
                <Tabs>
                  <Tabs.Screen name="index" options={{ title: 'Home' }} />
                  <Tabs.Screen name="settings" options={{ title: 'Settings' }} />
                </Tabs>
              );
            }

            // src/app/new-post.tsx           → "/new-post", open it with router.push('/new-post')
        """,
        lang="tsx",
        follow=[
            ("How would you give the Home tab its own stack so product details open inside the tab?", "Home tab-কে নিজস্ব stack কীভাবে দেবে, যাতে product details tab-এর ভেতরেই খোলে?"),
            ("How do you close the modal and pass a result back to the previous screen?", "Modal বন্ধ করে আগের screen-এ কোনো result কীভাবে ফেরত পাঠাবে?"),
        ],
        related=["rn-017", "rn-019"],
        refs=[R_ROUTER_MODALS, R_ROUTER_TABS, R_RN_NESTING],
    ),
    # ------------------------------------------------------------------ rn-019
    Q(
        id="rn-019", sub="Navigation (Expo Router)", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["expo-router", "uselocalsearchparams", "route-params", "typescript"],
        ver=VER, vs=True, status="stable",
        q_en=r"""
            `router.push('/products/42')` opens this screen, but it always shows **Not found**, although the API list contains `{ id: 42, name: 'Kurta' }`. (`useProducts()` returns the API's JSON, typed as `any`, so TypeScript doesn't complain.) What is the cause?
        """,
        q_bn=r"""
            `router.push('/products/42')` এই screen খোলে, কিন্তু সবসময় **Not found** দেখায়, যদিও API-র list-এ `{ id: 42, name: 'Kurta' }` আছে। (`useProducts()` API-র JSON return করে, type `any`, তাই TypeScript কোনো আপত্তি করে না।) কারণ কী?
        """,
        options=[
            ("`id` is the string `'42'`: route params are always strings, so `p.id === id` compares the number 42 with `'42'` and fails; convert with `Number(id)`",
             "`id` হলো string `'42'`: route param সবসময় string, তাই `p.id === id` number 42-কে `'42'`-এর সাথে তুলনা করে আর মেলে না; `Number(id)` দিয়ে convert করো"),
            ("`useLocalSearchParams` only returns query-string params like `?id=42`, not path segments, so it must be `useGlobalSearchParams`",
             "`useLocalSearchParams` শুধু `?id=42`-এর মতো query-string param দেয়, path segment দেয় না, তাই `useGlobalSearchParams` লাগবে"),
            ("Params are `undefined` on the first render and only arrive later, so the lookup has to move into a `useEffect`",
             "প্রথম render-এ param `undefined` থাকে আর পরে আসে, তাই lookup-টা `useEffect`-এর ভেতরে নিতে হবে"),
            ("The dynamic segment must also be registered in the root layout with `<Stack.Screen name='products/[id]' initialParams={{ id: 0 }} />`",
             "Dynamic segment-টা root layout-এ `<Stack.Screen name='products/[id]' initialParams={{ id: 0 }} />` দিয়ে register করতেও হবে"),
        ],
        correct=0,
        a_en=r"""
            Route params come from the URL, so they are **strings** (a catch-all `[...rest]` segment gives a `string[]`). `id` is `'42'`, the product's id is the number `42`, and strict equality fails. Fix it by converting and validating once: `const productId = Number(id)` and handle `NaN` with a not-found state.
        """,
        a_bn=r"""
            Route param আসে URL থেকে, তাই এগুলো **string** (catch-all `[...rest]` segment দিলে `string[]`)। `id` হলো `'42'`, আর product-এর id হলো number `42`, তাই strict equality মেলে না। একবার convert আর validate করে ঠিক করো: `const productId = Number(id)`, আর `NaN` হলে not-found state দেখাও।
        """,
        quick_en=r"""Route params are always strings, so `id` is `'42'` and `p.id === id` compares a number with a string. Convert once with `Number(id)` (and handle `NaN`). `useLocalSearchParams` does return path segments, and it's the right hook here.""",
        quick_bn=r"""Route param সবসময় string, তাই `id` হলো `'42'`, আর `p.id === id` number-কে string-এর সাথে তুলনা করে। একবার `Number(id)` দিয়ে convert করো (আর `NaN` handle করো)। `useLocalSearchParams` path segment ঠিকই দেয়, আর এখানে এটাই সঠিক hook।""",
        ex_en=r"""
            The tempting wrong answer is switching to **`useGlobalSearchParams`**. Both hooks return path segments and query params. The difference is *when they update*: `useLocalSearchParams` returns the params of the route this screen belongs to and only updates when the URL matches this route, while `useGlobalSearchParams` follows the global URL and updates on **every** URL change, so screens lower in the stack re-render whenever any param changes. The Expo docs recommend the local hook for normal screens (and for data fetching, so a previous screen keeps its own data when you go back); use the global one only for things like analytics that genuinely need the current URL.

            Params are available on the first render, so no effect is needed, and `initialParams` doesn't change their type. A generic such as `useLocalSearchParams<{ id: string }>()` only describes the type; it doesn't convert or validate anything, so the value is still untrusted input (it can come from a deep link).
        """,
        ex_bn=r"""
            সবচেয়ে লোভনীয় ভুল উত্তর হলো **`useGlobalSearchParams`**-এ চলে যাওয়া। দুইটা hook-ই path segment আর query param দেয়। পার্থক্য হলো *কখন update হয়*: `useLocalSearchParams` এই screen যে route-এর, শুধু তার param দেয় আর URL এই route-এর সাথে মিললেই update হয়; অন্যদিকে `useGlobalSearchParams` global URL অনুসরণ করে আর **প্রতিটা** URL পরিবর্তনে update হয়, ফলে stack-এর নিচের screen-গুলোও যেকোনো param বদলালে re-render হয়। Expo docs সাধারণ screen-এর জন্য local hook ব্যবহার করতে বলে (data fetching-এর জন্যও, যাতে back করলে আগের screen নিজের data ধরে রাখে); global hook শুধু analytics-এর মতো জায়গায়, যেখানে সত্যিই current URL লাগে।

            Param প্রথম render-এই পাওয়া যায়, তাই effect লাগে না, আর `initialParams` এদের type বদলায় না। `useLocalSearchParams<{ id: string }>()`-এর মতো generic শুধু type বর্ণনা করে; কিছু convert বা validate করে না, তাই value-টা এখনো untrusted input (deep link থেকেও আসতে পারে)।
        """,
        tip_en=r"""Say "URL params are strings" first, then explain local vs global in one sentence each, ending with "global re-renders background screens". That shows you know both the bug and the API design.""",
        tip_bn=r"""প্রথমেই বলো "URL param হলো string", তারপর local আর global এক বাক্য করে ব্যাখ্যা করো, শেষ করো "global background screen-কেও re-render করায়" দিয়ে। এতে বোঝা যায় তুমি bug আর API design দুইটাই জানো।""",
        mist_en=r"""Trusting the TypeScript generic as if it parsed the value, or passing whole objects as params instead of an id (params are serialised into the URL).""",
        mist_bn=r"""TypeScript generic-কে এমনভাবে বিশ্বাস করা যেন সেটা value parse করে দেয়, অথবা id-এর বদলে পুরো object param হিসেবে পাঠানো (param URL-এ serialise হয়)।""",
        code=r"""
            // src/app/products/[id].tsx
            import { useLocalSearchParams } from 'expo-router';
            import { Text } from 'react-native';
            import { useProducts } from '../../features/products/useProducts';

            export default function ProductScreen() {
              const { id } = useLocalSearchParams<{ id: string }>();
              const products = useProducts();
              const product = products.find((p) => p.id === id);
              return <Text>{product ? product.name : 'Not found'}</Text>;
            }
        """,
        lang="tsx",
        extra=[dict(lang="tsx", src=r"""
            const { id } = useLocalSearchParams<{ id: string }>();
            const productId = Number(id);
            const product = Number.isInteger(productId)
              ? products.find((p) => p.id === productId)
              : undefined;
        """, label_en="Fixed lookup", label_bn="সংশোধিত lookup")],
        follow=[
            ("When would `useGlobalSearchParams` actually be the right choice?", "কখন `useGlobalSearchParams` আসলেই সঠিক পছন্দ?"),
            ("Why should you pass an id in the URL instead of a whole product object?", "পুরো product object-এর বদলে URL-এ শুধু id পাঠানো কেন উচিত?"),
        ],
        related=["rn-017", "rn-020"],
        refs=[R_ROUTER_PARAMS, R_ROUTER_NAV],
    ),
    # ------------------------------------------------------------------ rn-020
    Q(
        id="rn-020", sub="Deep Linking", diff="medium", type="scenario",
        prio="medium", market="both", mins=7,
        tags=["deep-linking", "universal-links", "app-links", "expo-router", "eas"],
        ver=VER, vs=True, status="stable",
        q_en=r"""Marketing wants `https://shop.example.com/products/42` (from SMS, Facebook posts and email) to open the product screen directly in your Expo Router app if it is installed, and the website otherwise. Push notifications should also open `myshop://products/42`. How do you set this up and test it?""",
        q_bn=r"""Marketing team চায় `https://shop.example.com/products/42` (SMS, Facebook post আর email থেকে) app install থাকলে সরাসরি তোমার Expo Router app-এর product screen খুলুক, আর না থাকলে website। Push notification থেকেও `myshop://products/42` খোলা উচিত। তুমি এটা কীভাবে setup আর test করবে?""",
        a_en=r"""
            **Clarify first:** which paths should open the app (only `/products/*`?), whether logged-out users can see them, and what happens if the product no longer exists.

            **Two kinds of links:**
            - **Custom scheme** (`myshop://products/42`): set `"scheme": "myshop"` in app.json. Easy and good for notifications or OAuth redirects, but any app can claim the same scheme and it does nothing if the app isn't installed.
            - **Verified HTTPS links**, iOS **Universal Links** and Android **App Links**: the same `https://` URL opens the app if installed and the website if not. Both platforms check that you own the domain:
              - iOS: `ios.associatedDomains: ["applinks:shop.example.com"]` + an `apple-app-site-association` file at `https://shop.example.com/.well-known/` listing `TEAMID.bundleId` and the paths.
              - Android: an `intentFilters` entry with `autoVerify: true`, scheme `https`, the host and path prefix + `/.well-known/assetlinks.json` with the package name and the signing certificate's **SHA-256** (from `eas credentials -p android` or Play App Signing).

            **Routing:** Expo Router needs no linking config: `/products/42` already maps to `src/app/products/[id].tsx`. I validate `id` like any untrusted input, show a not-found state, and if the screen requires login I send the user to log in and back to the same URL afterwards. If old marketing URLs don't match the file structure, `+native-intent.tsx` (`redirectSystemPath`) can rewrite them.

            **Recommendation:** scheme for notifications, verified HTTPS links for anything shared publicly. These are native config changes, so they need a new development/store build (an OTA update can't add them).
        """,
        a_bn=r"""
            **আগে প্রশ্ন করে নিই:** কোন কোন path app খুলবে (শুধু `/products/*`?), logged-out user সেগুলো দেখতে পারবে কি না, আর product না থাকলে কী হবে।

            **দুই ধরনের link:**
            - **Custom scheme** (`myshop://products/42`): app.json-এ `"scheme": "myshop"` দাও। সহজ, notification বা OAuth redirect-এর জন্য ভালো, কিন্তু যেকোনো app একই scheme দাবি করতে পারে, আর app install না থাকলে কিছুই হয় না।
            - **Verified HTTPS link**, মানে iOS-এর **Universal Links** আর Android-এর **App Links**: একই `https://` URL app install থাকলে app খোলে, না থাকলে website। দুই platform-ই যাচাই করে domain-টা তোমার কি না:
              - iOS: `ios.associatedDomains: ["applinks:shop.example.com"]` + `https://shop.example.com/.well-known/`-এ একটা `apple-app-site-association` file, যেখানে `TEAMID.bundleId` আর path-গুলো থাকে।
              - Android: `autoVerify: true`, scheme `https`, host আর path prefix-সহ একটা `intentFilters` entry + `/.well-known/assetlinks.json`, যেখানে package name আর signing certificate-এর **SHA-256** থাকে (`eas credentials -p android` বা Play App Signing থেকে)।

            **Routing:** Expo Router-এ আলাদা linking config লাগে না: `/products/42` আপনা-আপনি `src/app/products/[id].tsx`-এ map হয়। `id`-কে অন্য যেকোনো untrusted input-এর মতো validate করি, not-found state দেখাই, আর screen-এ login লাগলে user-কে login-এ পাঠিয়ে পরে আবার একই URL-এ ফেরত আনি। পুরনো marketing URL file structure-এর সাথে না মিললে `+native-intent.tsx` (`redirectSystemPath`) দিয়ে rewrite করা যায়।

            **Recommendation:** notification-এর জন্য scheme, আর public-এ share হওয়া সব কিছুর জন্য verified HTTPS link। এগুলো native config change, তাই নতুন development/store build লাগে (OTA update দিয়ে এগুলো যোগ করা যায় না)।
        """,
        quick_en=r"""Use a custom `scheme` for notification links and verified HTTPS links for shared URLs: iOS `associatedDomains` + `apple-app-site-association`, Android `intentFilters` with `autoVerify` + `assetlinks.json`. Expo Router maps `/products/42` to `products/[id].tsx` itself; it's native config, so it needs a new build.""",
        quick_bn=r"""Notification link-এর জন্য custom `scheme`, আর share করা URL-এর জন্য verified HTTPS link: iOS-এ `associatedDomains` + `apple-app-site-association` file, Android-এ `autoVerify`-সহ `intentFilters` + `assetlinks.json`। Expo Router `/products/42`-কে নিজেই `products/[id].tsx`-এ map করে; এটা native config, তাই নতুন build লাগে।""",
        ex_en=r"""
            **Testing checklist**
            - Use a **development build** on a device or simulator: the custom scheme and associated domains are compiled into the native app, which Expo Go can't do for your own app.
            - Custom scheme: `npx uri-scheme open "myshop://products/42" --ios` (or `--android`).
            - Android App Link: `adb shell am start` with the `VIEW` action and the https URL; `adb shell pm get-app-links <package>` shows whether the domain verified. Verification can take a little while after install.
            - iOS: `xcrun simctl openurl booted <url>` on the simulator; on a device, tap the link from Notes or Messages (typing it in Safari's address bar doesn't trigger a Universal Link). iOS fetches the association file around install time, so after changing it, reinstall the app.

            **Common causes of "it opens the browser":** the `.well-known` file is missing, redirects, or isn't served as JSON over HTTPS; wrong Team ID or bundle id; `https://` included in `associatedDomains`; the SHA-256 is from the upload key instead of the Play signing key. Also handle the **cold start** (the app was killed and launched by the link) as well as the warm case; Expo Router handles both, but your auth/splash logic must not swallow the initial URL.
        """,
        ex_bn=r"""
            **Test checklist**
            - Device বা simulator-এ **development build** ব্যবহার করো: custom scheme আর associated domain native app-এ compile হয়, যেটা Expo Go তোমার নিজের app-এর জন্য করতে পারে না।
            - Custom scheme: `npx uri-scheme open "myshop://products/42" --ios` (বা `--android`)।
            - Android App Link: `VIEW` action আর https URL দিয়ে `adb shell am start`; `adb shell pm get-app-links <package>` দেখায় domain verify হয়েছে কি না। Install-এর পর verification-এ একটু সময় লাগতে পারে।
            - iOS: simulator-এ `xcrun simctl openurl booted <url>`; device-এ Notes বা Messages থেকে link-এ tap করো (Safari-র address bar-এ টাইপ করলে Universal Link trigger হয় না)। iOS association file মোটামুটি install-এর সময় নেয়, তাই file বদলালে app আবার install করো।

            **"Browser খুলে যায়"-এর সাধারণ কারণ:** `.well-known` file নেই, redirect হচ্ছে, বা HTTPS-এ JSON হিসেবে serve হচ্ছে না; ভুল Team ID বা bundle id; `associatedDomains`-এ `https://` লিখে ফেলা; Play signing key-এর বদলে upload key-এর SHA-256 দেওয়া। আর warm case-এর পাশাপাশি **cold start**-ও handle করো (app বন্ধ ছিল, link দিয়ে চালু হলো); Expo Router দুইটাই handle করে, কিন্তু তোমার auth/splash logic যেন initial URL হারিয়ে না ফেলে।
        """,
        tip_en=r"""Separate "custom scheme" from "verified HTTPS links" in the first sentence, then mention both `.well-known` files and that it needs a rebuild. Ending with a concrete test command shows you've actually done it.""",
        tip_bn=r"""প্রথম বাক্যেই "custom scheme" আর "verified HTTPS link" আলাদা করো, তারপর দুইটা `.well-known` file আর rebuild লাগার কথা বলো। শেষে একটা বাস্তব test command বললে বোঝা যায় তুমি এটা আসলেই করেছ।""",
        mist_en=r"""Expecting an OTA update to enable universal links, testing only in Expo Go, and trusting `id` from the link without validation.""",
        mist_bn=r"""ভাবা যে OTA update দিয়েই universal link চালু হবে, শুধু Expo Go-তে test করা, আর link থেকে আসা `id` validate না করেই বিশ্বাস করা।""",
        code=r"""
            {
              "expo": {
                "scheme": "myshop",
                "ios": {
                  "bundleIdentifier": "com.example.myshop",
                  "associatedDomains": ["applinks:shop.example.com"]
                },
                "android": {
                  "package": "com.example.myshop",
                  "intentFilters": [
                    {
                      "action": "VIEW",
                      "autoVerify": true,
                      "data": [{ "scheme": "https", "host": "shop.example.com", "pathPrefix": "/products" }],
                      "category": ["BROWSABLE", "DEFAULT"]
                    }
                  ]
                }
              }
            }
        """,
        lang="json",
        extra=[
            dict(lang="json", src=r"""
                [
                  {
                    "relation": ["delegate_permission/common.handle_all_urls"],
                    "target": {
                      "namespace": "android_app",
                      "package_name": "com.example.myshop",
                      "sha256_cert_fingerprints": ["<SHA-256 from eas credentials -p android>"]
                    }
                  }
                ]
            """, label_en="Android: https://shop.example.com/.well-known/assetlinks.json", label_bn="Android: https://shop.example.com/.well-known/assetlinks.json"),
            dict(lang="bash", src=r"""
                # custom scheme on a development build
                npx uri-scheme open "myshop://products/42" --ios
                npx uri-scheme open "myshop://products/42" --android

                # Android App Link + verification state
                adb shell am start -W -a android.intent.action.VIEW -c android.intent.category.BROWSABLE \
                  -d "https://shop.example.com/products/42" com.example.myshop
                adb shell pm get-app-links com.example.myshop

                # iOS simulator
                xcrun simctl openurl booted "https://shop.example.com/products/42"
            """, label_en="Testing commands", label_bn="Test করার command"),
        ],
        follow=[
            ("The link opens the app on a warm start but lands on Home after a cold start. What would you check?", "Warm start-এ link app-এর ঠিক screen খোলে, কিন্তু cold start-এ Home-এ চলে যায়। কী কী check করবে?"),
            ("How would you send a logged-out user to login and then back to the linked product?", "Logged-out user-কে login-এ পাঠিয়ে তারপর link করা product-এ কীভাবে ফেরত আনবে?"),
        ],
        related=["rn-017", "rn-019"],
        refs=[R_LINK_INTO, R_LINK_IOS, R_LINK_ANDROID],
    ),
    # ------------------------------------------------------------------ rn-021
    Q(
        id="rn-021", sub="Local Storage", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["asyncstorage", "expo-secure-store", "mmkv", "expo-sqlite", "storage"],
        ver="Expo SDK 58 (expo-secure-store, expo-sqlite ~58), react-native-mmkv 4.x", vs=True, status="stable",
        q_en=r"""Compare AsyncStorage, `expo-secure-store`, MMKV and `expo-sqlite`. Where would you store a theme setting, a refresh token, an "onboarding done" flag read at startup, and 20,000 cached orders?""",
        q_bn=r"""AsyncStorage, `expo-secure-store`, MMKV আর `expo-sqlite` তুলনা করো। Theme setting, refresh token, startup-এ পড়া একটা "onboarding done" flag, আর 20,000টা cached order তুমি কোথায় রাখবে?""",
        a_en=r"""
            - **AsyncStorage** (`@react-native-async-storage/async-storage`): async, **unencrypted** key-value strings. Fine for small, non-sensitive preferences such as the **theme**. (The old `AsyncStorage` export from `react-native` itself is legacy; it moved to the community package years ago.)
            - **`expo-secure-store`**: values encrypted by the OS, Keychain on iOS and Keystore-backed on Android. Meant for small secrets: the **refresh token**, API session data. Not for big data.
            - **MMKV** (`react-native-mmkv`): very fast **synchronous** key-value storage, optional encryption. Good for values read on every launch or render, like the **onboarding flag**. It has native code, so it needs a development build (not Expo Go).
            - **`expo-sqlite`**: a real SQL database with tables, indexes, transactions and queries. The right place for the **20,000 orders**, because you can filter, sort and paginate without loading everything into memory.

            Rule of thumb: secrets → SecureStore; small settings → a key-value store; anything you'd query → SQLite.
        """,
        a_bn=r"""
            - **AsyncStorage** (`@react-native-async-storage/async-storage`): async, **unencrypted** key-value string। ছোট, non-sensitive preference-এর জন্য ঠিক আছে, যেমন **theme**। (`react-native` থেকেই export হওয়া পুরনো `AsyncStorage` legacy; সেটা অনেক আগেই community package-এ চলে গেছে।)
            - **`expo-secure-store`**: OS value-গুলো encrypt করে রাখে, iOS-এ Keychain আর Android-এ Keystore-এর সাহায্যে। ছোট secret-এর জন্য: **refresh token**, API session data। বড় data-র জন্য না।
            - **MMKV** (`react-native-mmkv`): খুব দ্রুত **synchronous** key-value storage, চাইলে encryption-ও আছে। প্রতিবার launch বা render-এ পড়া value-র জন্য ভালো, যেমন **onboarding flag**। এতে native code আছে, তাই development build লাগে (Expo Go-তে চলে না)।
            - **`expo-sqlite`**: আসল SQL database, table, index, transaction আর query-সহ। **20,000টা order**-এর সঠিক জায়গা এটাই, কারণ সব memory-তে load না করেই filter, sort আর paginate করা যায়।

            সহজ নিয়ম: secret → SecureStore; ছোট setting → key-value store; যেটা query করবে → SQLite।
        """,
        quick_en=r"""AsyncStorage is unencrypted async key-value for small settings; `expo-secure-store` keeps small secrets in Keychain/Keystore; MMKV is fast synchronous key-value (dev build); `expo-sqlite` is a real database for large, queryable data. Theme → AsyncStorage, token → SecureStore, startup flag → MMKV, orders → SQLite.""",
        quick_bn=r"""AsyncStorage হলো ছোট preference-এর জন্য async, unencrypted key-value; `expo-secure-store` token-এর মতো ছোট secret Keychain/Keystore-এ রাখে; MMKV দ্রুত synchronous key-value (dev build লাগে); `expo-sqlite` বড়, query করার মতো data-র জন্য আসল database। তাই: theme → AsyncStorage, token → SecureStore, startup flag → MMKV, order → SQLite।""",
        ex_en=r"""
            - **Why not put everything in AsyncStorage?** It stores strings, so a big list becomes one huge `JSON.stringify` blob that you read and parse entirely to show 20 rows. It is also readable on a rooted device or from some backups, so never put tokens there.
            - **SecureStore limits:** values are strings; Expo doesn't enforce a size limit but recommends handling native errors for large values. On Android the data is removed on uninstall; on iOS Keychain items can survive reinstall (don't rely on either). It supports `requireAuthentication` for biometric-gated values.
            - **Sync vs async:** synchronous reads (MMKV, or `expo-sqlite/kv-store`'s sync methods) avoid a loading flash at startup, but large synchronous work blocks the JS thread.
            - **Fewer libraries:** `expo-sqlite/kv-store` offers an AsyncStorage-compatible API on top of SQLite, so an app that already uses SQLite might not need AsyncStorage at all.
            - **Sensitive bulk data:** if the orders contain personal data, consider SQLCipher (`useSQLCipher` config plugin) or not caching that data.
        """,
        ex_bn=r"""
            - **সব কিছু AsyncStorage-এ রাখি না কেন?** এটা string রাখে, তাই বড় list একটা বিশাল `JSON.stringify` blob হয়ে যায়, আর 20টা row দেখাতে পুরোটা পড়ে parse করতে হয়। Rooted device-এ বা কিছু backup থেকে এটা পড়াও যায়, তাই token কখনো এখানে রাখবে না।
            - **SecureStore-এর সীমা:** value string হতে হয়; Expo কোনো size limit চাপায় না, তবে বড় value-র জন্য native error handle করতে বলে। Android-এ uninstall করলে data মুছে যায়; iOS-এ Keychain item reinstall-এর পরেও থেকে যেতে পারে (কোনোটার ওপরই ভরসা কোরো না)। Biometric দিয়ে আটকানো value-র জন্য `requireAuthentication` আছে।
            - **Sync বনাম async:** synchronous read (MMKV, বা `expo-sqlite/kv-store`-এর sync method) startup-এ loading flash এড়ায়, কিন্তু বড় synchronous কাজ JS thread block করে।
            - **কম library:** `expo-sqlite/kv-store` SQLite-এর ওপরে AsyncStorage-এর মতো API দেয়, তাই যে app আগে থেকেই SQLite ব্যবহার করে, তার হয়তো AsyncStorage লাগেই না।
            - **Sensitive bulk data:** order-এ personal data থাকলে SQLCipher (`useSQLCipher` config plugin) বিবেচনা করো, অথবা সেই data cache-ই কোরো না।
        """,
        tip_en=r"""Answer with a small table in your head: encrypted? sync? queryable? needs a dev build? Then place each of the four values. Mentioning that the core `AsyncStorage` is legacy shows you're current.""",
        tip_bn=r"""মনে মনে একটা ছোট table বানিয়ে উত্তর দাও: encrypted? sync? query করা যায়? dev build লাগে? তারপর চারটা value কোথায় যাবে বলো। Core-এর `AsyncStorage` যে legacy, সেটা বললে বোঝা যায় তুমি আপডেটেড।""",
        mist_en=r"""Storing JWTs in AsyncStorage "because it's easy", or keeping a large list as one JSON string and rewriting it on every change.""",
        mist_bn=r""""সহজ বলে" JWT AsyncStorage-এ রাখা, অথবা বড় list-কে একটা JSON string হিসেবে রেখে প্রতিটা পরিবর্তনে পুরোটা আবার লেখা।""",
        code=r"""
            // Theme (small, not secret): AsyncStorage
            import AsyncStorage from '@react-native-async-storage/async-storage';
            await AsyncStorage.setItem('settings.theme', 'dark');

            // Refresh token (secret): expo-secure-store
            import * as SecureStore from 'expo-secure-store';
            await SecureStore.setItemAsync('auth.refreshToken', refreshToken);

            // Flag read synchronously at startup: MMKV v4 (development build)
            import { createMMKV } from 'react-native-mmkv';
            const storage = createMMKV();
            storage.set('onboarding.done', true);
            const onboardingDone = storage.getBoolean('onboarding.done');

            // 20,000 orders (queryable): expo-sqlite
            import * as SQLite from 'expo-sqlite';
            const db = await SQLite.openDatabaseAsync('app.db');
            const pending = await db.getAllAsync(
              'SELECT id, total, created_at FROM orders WHERE status = ? ORDER BY created_at DESC LIMIT 20',
              'pending',
            );
        """,
        lang="typescript",
        follow=[
            ("Why is a synchronous storage read sometimes better at app startup, and when is it a problem?", "App startup-এ synchronous storage read কেন কখনো কখনো ভালো, আর কখন সেটা সমস্যা?"),
            ("How would you clear a user's data from all four stores on logout?", "Logout-এর সময় চারটা store থেকেই user-এর data কীভাবে মুছবে?"),
        ],
        related=["rn-022", "rn-030", "rn-027"],
        refs=[R_STORE_DATA, R_SECURESTORE, R_MMKV],
    ),
    # ------------------------------------------------------------------ rn-022
    Q(
        id="rn-022", sub="expo-sqlite", diff="easy", type="coding",
        prio="high", market="both", mins=6,
        tags=["expo-sqlite", "runasync", "getallasync", "parameters", "typescript"],
        ver=VER_SQL, vs=True, status="stable",
        q_en=r"""
            Using `expo-sqlite` (SDK 58), write three TypeScript functions for a notes feature:

            - `openNotesDb()` opens `notes.db`, turns on WAL mode and creates a `notes` table (`id`, `title`, `body`, `created_at`) if it doesn't exist.
            - `addNote(db, title, body?)` rejects an empty title, inserts the note using `?` placeholders, and returns the new id.
            - `listNotes(db)` returns all notes, newest first.

            Example: after `addNote(db, '  Buy rice ', '5 kg miniket')` and `addNote(db, "Karim's shop")`, `listNotes` returns note 2 (`Karim's shop`) and then note 1 (`Buy rice`).
        """,
        q_bn=r"""
            `expo-sqlite` (SDK 58) ব্যবহার করে একটা notes feature-এর জন্য তিনটা TypeScript function লেখো:

            - `openNotesDb()` `notes.db` খুলবে, WAL mode চালু করবে, আর `notes` table (`id`, `title`, `body`, `created_at`) না থাকলে তৈরি করবে।
            - `addNote(db, title, body?)` খালি title reject করবে, `?` placeholder দিয়ে note insert করবে, আর নতুন id return করবে।
            - `listNotes(db)` সব note return করবে, নতুনটা আগে।

            উদাহরণ: `addNote(db, '  Buy rice ', '5 kg miniket')` আর `addNote(db, "Karim's shop")`-এর পরে `listNotes` আগে note 2 (`Karim's shop`) আর তারপর note 1 (`Buy rice`) return করবে।
        """,
        a_en=r"""
            Open the database once with `openDatabaseAsync`, and run the one-time setup with `execAsync`, which can execute several statements in one call but **does not bind parameters**, so it only ever gets fixed SQL. Every query that contains user data goes through `runAsync` (writes) or `getAllAsync` / `getFirstAsync` (reads) with `?` placeholders and the values as extra arguments. `runAsync` returns `{ lastInsertRowId, changes }`, so `addNote` returns `lastInsertRowId`.

            I trim and validate the title before touching the database, store timestamps as integers (`Date.now()` milliseconds), and sort by `created_at DESC, id DESC` so two notes created in the same millisecond still have a stable order. `getAllAsync<Note>()` takes a generic for the row type. The apostrophe in `Karim's shop` is no problem because it's a bound value, not part of the SQL text.
        """,
        a_bn=r"""
            `openDatabaseAsync` দিয়ে database একবার খুলি, আর একবারের setup `execAsync` দিয়ে চালাই; এটা এক call-এ কয়েকটা statement চালাতে পারে, কিন্তু **parameter bind করে না**, তাই এতে শুধু fixed SQL যায়। User-এর data থাকা প্রতিটা query যায় `runAsync` (write) বা `getAllAsync` / `getFirstAsync` (read) দিয়ে, `?` placeholder আর value-গুলো বাড়তি argument হিসেবে দিয়ে। `runAsync` `{ lastInsertRowId, changes }` return করে, তাই `addNote` `lastInsertRowId` return করে।

            Database-এ যাওয়ার আগেই title trim আর validate করি, timestamp integer হিসেবে রাখি (`Date.now()` millisecond), আর `created_at DESC, id DESC` দিয়ে sort করি, যাতে একই millisecond-এ তৈরি দুইটা note-এরও স্থির order থাকে। `getAllAsync<Note>()` row type-এর জন্য generic নেয়। `Karim's shop`-এর apostrophe কোনো সমস্যা না, কারণ এটা bound value, SQL text-এর অংশ না।
        """,
        quick_en=r"""Open with `openDatabaseAsync`, run fixed setup SQL (WAL pragma, `CREATE TABLE IF NOT EXISTS`) with `execAsync`, insert with `runAsync('... VALUES (?, ?, ?)', ...values)` and return `lastInsertRowId`, and read with `getAllAsync<Note>` ordered by `created_at DESC, id DESC`. Insert is O(log n); the sorted read is O(n log n) without an index.""",
        quick_bn=r"""`openDatabaseAsync` দিয়ে খোলো, fixed setup SQL (WAL pragma, `CREATE TABLE IF NOT EXISTS`) `execAsync` দিয়ে চালাও, `runAsync('... VALUES (?, ?, ?)', ...values)` দিয়ে insert করে `lastInsertRowId` return করো, আর `created_at DESC, id DESC` order-এ `getAllAsync<Note>` দিয়ে পড়ো। Insert O(log n); index ছাড়া sorted read O(n log n)।""",
        ex_en=r"""
            - **Why WAL?** In write-ahead-log mode readers don't block the writer and vice versa, and the Expo docs recommend it. It is a persistent setting of the database file.
            - **Edge cases:** whitespace-only titles (rejected), apostrophes and emoji (fine with bound params), two notes in the same millisecond (the `id DESC` tie-breaker), and a very large table (use `LIMIT` + keyset pagination instead of "all notes" in a real feed).
            - **Open once:** keep a single connection (module-level or via `SQLiteProvider`) instead of opening the database on every call.
            - **Sync API:** there are `openDatabaseSync` / `runSync` / `getAllSync` variants, but they block the JS thread, so I keep them for tiny reads at startup.
            - **Booleans and dates:** SQLite has no boolean or date type; use `0/1` and integer epoch milliseconds (or ISO strings) consistently.
        """,
        ex_bn=r"""
            - **WAL কেন?** Write-ahead-log mode-এ reader writer-কে block করে না, writer-ও reader-কে না, আর Expo docs এটাই recommend করে। এটা database file-এর একটা স্থায়ী setting।
            - **Edge case:** শুধু space-ওয়ালা title (reject হয়), apostrophe আর emoji (bound param-এ সমস্যা নেই), একই millisecond-এ দুইটা note (`id DESC` tie-breaker), আর খুব বড় table (আসল feed-এ "সব note"-এর বদলে `LIMIT` + keyset pagination)।
            - **একবার খোলো:** প্রতিটা call-এ database না খুলে একটা connection রাখো (module-level বা `SQLiteProvider` দিয়ে)।
            - **Sync API:** `openDatabaseSync` / `runSync` / `getAllSync` variant আছে, কিন্তু এগুলো JS thread block করে, তাই startup-এর ছোট read-এর জন্যই রাখি।
            - **Boolean আর date:** SQLite-এ boolean বা date type নেই; ধারাবাহিকভাবে `0/1` আর integer epoch millisecond (বা ISO string) ব্যবহার করো।
        """,
        tip_en=r"""Say out loud which method you use for what: `execAsync` only for fixed setup SQL, `runAsync` for writes, `getAllAsync`/`getFirstAsync` for reads, always with `?` params. That single sentence answers the follow-up about SQL injection before it's asked.""",
        tip_bn=r"""কোন কাজে কোন method, সেটা জোরে বলো: `execAsync` শুধু fixed setup SQL-এর জন্য, write-এর জন্য `runAsync`, read-এর জন্য `getAllAsync`/`getFirstAsync`, সবসময় `?` param দিয়ে। এই একটা বাক্যেই SQL injection নিয়ে follow-up প্রশ্নের উত্তর আগেই দেওয়া হয়ে যায়।""",
        mist_en=r"""Building the `INSERT` with a template string and `execAsync`, opening a new connection in every function, or using the legacy `openDatabase().transaction(tx => tx.executeSql(...))` API from old tutorials, which is gone from current `expo-sqlite`.""",
        mist_bn=r"""Template string আর `execAsync` দিয়ে `INSERT` বানানো, প্রতিটা function-এ নতুন connection খোলা, অথবা পুরনো tutorial-এর legacy `openDatabase().transaction(tx => tx.executeSql(...))` API ব্যবহার করা, যেটা বর্তমান `expo-sqlite`-এ আর নেই।""",
        code=r"""
            import * as SQLite from 'expo-sqlite';

            export type Note = { id: number; title: string; body: string; created_at: number };

            export async function openNotesDb() {
              const db = await SQLite.openDatabaseAsync('notes.db');
              // Fixed SQL only: execAsync does not bind or escape parameters
              await db.execAsync(`
                PRAGMA journal_mode = WAL;
                CREATE TABLE IF NOT EXISTS notes (
                  id INTEGER PRIMARY KEY NOT NULL,
                  title TEXT NOT NULL,
                  body TEXT NOT NULL DEFAULT '',
                  created_at INTEGER NOT NULL
                );
              `);
              return db;
            }

            export async function addNote(db: SQLite.SQLiteDatabase, title: string, body = '') {
              const clean = title.trim();
              if (!clean) throw new Error('Title is required');
              const result = await db.runAsync(
                'INSERT INTO notes (title, body, created_at) VALUES (?, ?, ?)',
                clean, body, Date.now(),
              );
              return result.lastInsertRowId;
            }

            export function listNotes(db: SQLite.SQLiteDatabase) {
              return db.getAllAsync<Note>(
                'SELECT id, title, body, created_at FROM notes ORDER BY created_at DESC, id DESC',
              );
            }

            // Usage
            const db = await openNotesDb();
            await addNote(db, '  Buy rice ', '5 kg miniket'); // → 1
            await addNote(db, "Karim's shop");                // → 2
            const notes = await listNotes(db);
            console.log(notes.map((n) => [n.id, n.title, n.body]));
        """,
        lang="typescript",
        output=r"""
            [ [ 2, "Karim's shop", '' ], [ 1, 'Buy rice', '5 kg miniket' ] ]
        """,
        time="O(log n) per insert; O(n log n) for the sorted list (an index on created_at avoids the sort)",
        space="O(n) for the returned list",
        follow=[
            ("How would you change `listNotes` to load 30 notes at a time for an infinite scroll?", "Infinite scroll-এর জন্য `listNotes` কীভাবে বদলাবে যাতে একবারে 30টা note load হয়?"),
            ("Where would you open the database in a real Expo Router app?", "আসল Expo Router app-এ database কোথায় খুলবে?"),
        ],
        related=["rn-023", "rn-024", "rn-021"],
        refs=[R_SQLITE, R_SQLITE_WAL],
    ),
    # ------------------------------------------------------------------ rn-023
    Q(
        id="rn-023", sub="expo-sqlite", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["expo-sqlite", "sqliteprovider", "migrations", "user-version", "usesqlitecontext"],
        ver=VER_SQL, vs=True, status="stable",
        q_en=r"""
            Set up `expo-sqlite` for a todo app with Expo Router:

            - Wrap the app in `SQLiteProvider` (database `app.db`) and run migrations in `onInit` using `PRAGMA user_version`.
            - Version 1 creates `todos (id, title, done)`. Version 2, shipped in a later release, adds a nullable `due_at` column and an index on `done`.
            - A fresh install must end at version 2, a user upgrading from version 1 must keep their todos, and running the migration again must do nothing.
            - The home screen gets the database with `useSQLiteContext()`, lists todos, adds a todo and toggles `done`.
        """,
        q_bn=r"""
            Expo Router দিয়ে একটা todo app-এর জন্য `expo-sqlite` setup করো:

            - App-কে `SQLiteProvider` (database `app.db`) দিয়ে wrap করো, আর `onInit`-এ `PRAGMA user_version` ব্যবহার করে migration চালাও।
            - Version 1 `todos (id, title, done)` তৈরি করে। পরের release-এ আসা version 2 একটা nullable `due_at` column আর `done`-এর ওপর একটা index যোগ করে।
            - Fresh install শেষে version 2-এ থাকতে হবে, version 1 থেকে upgrade করা user-এর todo হারানো যাবে না, আর migration আবার চালালে কিছুই হবে না।
            - Home screen `useSQLiteContext()` দিয়ে database নেবে, todo list দেখাবে, todo যোগ করবে আর `done` toggle করবে।
        """,
        a_en=r"""
            `SQLiteProvider` opens the database once and runs `onInit(db)` **before rendering its children**, so every screen below it can call `useSQLiteContext()` and get a ready, migrated database.

            For migrations I read `PRAGMA user_version` (an integer SQLite keeps in the file header, `0` for a new database) and apply each step in order: `0 → 1`, then `1 → 2`. Each step runs in a transaction **together with** its `PRAGMA user_version = n`, so a crash halfway leaves the database at the previous version instead of half-migrated, and the step simply runs again on the next launch. I verified that `user_version` rolls back with the transaction. `PRAGMA journal_mode = WAL` is set before any transaction because SQLite refuses to change into WAL mode inside one.

            Steps are append-only: I never edit a shipped migration, I add a new version. In the screen, every query uses `?` params; after a write I reload the list (or use a change listener / live query).
        """,
        a_bn=r"""
            `SQLiteProvider` database একবার খোলে আর **children render করার আগে** `onInit(db)` চালায়, তাই এর নিচের প্রতিটা screen `useSQLiteContext()` call করে একটা তৈরি, migrate করা database পায়।

            Migration-এর জন্য `PRAGMA user_version` পড়ি (SQLite file header-এ রাখা একটা integer, নতুন database-এ `0`) আর প্রতিটা ধাপ ক্রমানুসারে চালাই: `0 → 1`, তারপর `1 → 2`। প্রতিটা ধাপ তার `PRAGMA user_version = n`-এর **সাথে একসাথে** একটা transaction-এ চলে, তাই মাঝপথে crash হলে database অর্ধেক migrate না হয়ে আগের version-এ থাকে, আর পরের launch-এ ধাপটা আবার চলে। আমি যাচাই করেছি যে transaction-এর সাথে `user_version`-ও rollback হয়। `PRAGMA journal_mode = WAL` যেকোনো transaction-এর আগে set করি, কারণ transaction-এর ভেতরে SQLite WAL mode-এ যেতে দেয় না।

            ধাপগুলো শুধু যোগ হয়: ship হয়ে যাওয়া migration কখনো edit করি না, নতুন version যোগ করি। Screen-এ প্রতিটা query `?` param ব্যবহার করে; write-এর পরে list আবার load করি (বা change listener / live query ব্যবহার করি)।
        """,
        quick_en=r"""Wrap the app in `<SQLiteProvider databaseName="app.db" onInit={migrateDbIfNeeded}>`, read `PRAGMA user_version`, and apply each missing step in order inside a transaction that also sets the new `user_version`, so it's idempotent and crash-safe. Screens call `useSQLiteContext()` and query with `?` params.""",
        quick_bn=r"""App-কে `<SQLiteProvider databaseName="app.db" onInit={migrateDbIfNeeded}>` দিয়ে wrap করো, `PRAGMA user_version` পড়ো, আর বাকি থাকা প্রতিটা ধাপ ক্রমানুসারে এমন transaction-এ চালাও যেটা নতুন `user_version`-ও set করে, ফলে এটা idempotent আর crash-safe হয়। Screen `useSQLiteContext()` call করে `?` param দিয়ে query চালায়।""",
        ex_en=r"""
            - **Upgrade path test:** a database created by version 1 (with existing rows and `user_version = 1`) skips the first step, runs only `ALTER TABLE ... ADD COLUMN` + the index, and keeps its rows. I ran exactly this against SQLite: rows kept, `user_version` 2, and a second run is a no-op.
            - **Why string interpolation is OK here:** `PRAGMA user_version = 2` is a constant from our own code, not user input, and pragmas can't take bound parameters.
            - **`useSuspense`:** with `<SQLiteProvider useSuspense>` inside a `<Suspense fallback>` the splash/loading UI is handled by React Suspense; `onError` lets you show a recovery screen if a migration throws.
            - **SQLite `ALTER TABLE` is limited** (add/rename/drop column, rename table). Bigger changes use the "create new table, copy, drop old, rename" pattern inside one transaction.
            - **Alternative:** with Drizzle ORM, migrations are generated SQL files bundled into the app and applied by `useMigrations`; don't mix that with hand-written `user_version` migrations on the same database.
        """,
        ex_bn=r"""
            - **Upgrade path test:** version 1-এর তৈরি database (আগের row আর `user_version = 1`-সহ) প্রথম ধাপ বাদ দেয়, শুধু `ALTER TABLE ... ADD COLUMN` + index চালায়, আর row-গুলো রেখে দেয়। আমি ঠিক এটাই SQLite-এ চালিয়ে দেখেছি: row থেকে গেছে, `user_version` 2, আর দ্বিতীয়বার চালালে কিছুই হয় না।
            - **এখানে string interpolation কেন ঠিক আছে:** `PRAGMA user_version = 2` আমাদের নিজের code-এর constant, user input না, আর pragma-তে bound parameter দেওয়া যায় না।
            - **`useSuspense`:** `<Suspense fallback>`-এর ভেতরে `<SQLiteProvider useSuspense>` দিলে splash/loading UI React Suspense handle করে; migration throw করলে `onError` দিয়ে recovery screen দেখানো যায়।
            - **SQLite-এর `ALTER TABLE` সীমিত** (column add/rename/drop, table rename)। বড় পরিবর্তনের জন্য এক transaction-এর ভেতরে "নতুন table বানাও, copy করো, পুরনোটা drop করো, rename করো" pattern ব্যবহার হয়।
            - **বিকল্প:** Drizzle ORM-এ migration হলো generate করা SQL file, যেগুলো app-এ bundle হয় আর `useMigrations` apply করে; একই database-এ এর সাথে হাতে লেখা `user_version` migration মেশাবে না।
        """,
        tip_en=r"""Mention the three properties interviewers look for: ordered steps, idempotent (safe to re-run), and atomic per step. Then name the upgrade-path test, because "works on a fresh install" is where most migration bugs hide.""",
        tip_bn=r"""Interviewer যে তিনটা বৈশিষ্ট্য খোঁজে সেগুলো বলো: ক্রমানুসারে ধাপ, idempotent (আবার চালানো নিরাপদ), আর প্রতিটা ধাপ atomic। তারপর upgrade-path test-এর কথা বলো, কারণ "fresh install-এ চলে" কথাটার আড়ালেই বেশিরভাগ migration bug লুকিয়ে থাকে।""",
        mist_en=r"""Running `CREATE TABLE` without checking the version (fails or silently skips changes on upgrade), editing an old migration step after release, and setting `user_version` before the step's SQL has succeeded.""",
        mist_bn=r"""Version check না করেই `CREATE TABLE` চালানো (upgrade-এ fail করে বা চুপচাপ পরিবর্তন বাদ পড়ে), release-এর পরে পুরনো migration ধাপ edit করা, আর ধাপের SQL সফল হওয়ার আগেই `user_version` set করা।""",
        code=r"""
            // src/app/_layout.tsx
            import { Stack } from 'expo-router';
            import { SQLiteProvider, type SQLiteDatabase } from 'expo-sqlite';

            export default function RootLayout() {
              return (
                <SQLiteProvider databaseName="app.db" onInit={migrateDbIfNeeded}>
                  <Stack />
                </SQLiteProvider>
              );
            }

            const DATABASE_VERSION = 2;

            async function migrateDbIfNeeded(db: SQLiteDatabase) {
              const row = await db.getFirstAsync<{ user_version: number }>('PRAGMA user_version');
              let version = row?.user_version ?? 0;
              if (version >= DATABASE_VERSION) return;

              // journal_mode can't be changed inside a transaction, so set it first
              await db.execAsync('PRAGMA journal_mode = WAL');

              if (version === 0) {
                await db.withTransactionAsync(async () => {
                  await db.execAsync(`
                    CREATE TABLE todos (
                      id INTEGER PRIMARY KEY NOT NULL,
                      title TEXT NOT NULL,
                      done INTEGER NOT NULL DEFAULT 0
                    );
                    PRAGMA user_version = 1;
                  `);
                });
                version = 1;
              }

              if (version === 1) {
                await db.withTransactionAsync(async () => {
                  await db.execAsync(`
                    ALTER TABLE todos ADD COLUMN due_at INTEGER;
                    CREATE INDEX idx_todos_done ON todos (done);
                    PRAGMA user_version = 2;
                  `);
                });
                version = 2;
              }
            }
        """,
        lang="tsx",
        extra=[dict(lang="tsx", src=r"""
            // src/app/index.tsx
            import { useSQLiteContext } from 'expo-sqlite';
            import { useCallback, useEffect, useState } from 'react';
            import { Button, FlatList, Pressable, Text, TextInput, View } from 'react-native';

            type Todo = { id: number; title: string; done: number; due_at: number | null };

            export default function TodosScreen() {
              const db = useSQLiteContext();
              const [todos, setTodos] = useState<Todo[]>([]);
              const [title, setTitle] = useState('');

              const load = useCallback(async () => {
                setTodos(await db.getAllAsync<Todo>(
                  'SELECT id, title, done, due_at FROM todos ORDER BY done, id DESC',
                ));
              }, [db]);

              useEffect(() => {
                load();
              }, [load]);

              async function addTodo() {
                const clean = title.trim();
                if (!clean) return;
                await db.runAsync('INSERT INTO todos (title) VALUES (?)', clean);
                setTitle('');
                await load();
              }

              async function toggle(todo: Todo) {
                await db.runAsync('UPDATE todos SET done = ? WHERE id = ?', todo.done ? 0 : 1, todo.id);
                await load();
              }

              return (
                <View style={{ flex: 1, padding: 16 }}>
                  <TextInput value={title} onChangeText={setTitle} placeholder="New todo" onSubmitEditing={addTodo} />
                  <Button title="Add" onPress={addTodo} />
                  <FlatList
                    data={todos}
                    keyExtractor={(t) => String(t.id)}
                    renderItem={({ item }) => (
                      <Pressable
                        onPress={() => toggle(item)}
                        accessibilityRole="checkbox"
                        accessibilityState={{ checked: item.done === 1 }}
                      >
                        <Text>{item.done ? '[x] ' : '[ ] '}{item.title}</Text>
                      </Pressable>
                    )}
                  />
                </View>
              );
            }
        """, label_en="Screen using useSQLiteContext", label_bn="useSQLiteContext ব্যবহার করা screen")],
        time="O(1) migration checks per launch; each query O(log n) per row via the primary key",
        space="O(n) for the loaded todo list",
        follow=[
            ("Version 3 must split `title` into `title` and `notes`. How do you write that migration safely?", "Version 3-এ `title`-কে `title` আর `notes`-এ ভাগ করতে হবে। এই migration নিরাপদে কীভাবে লিখবে?"),
            ("How would you make the list refresh automatically when another screen inserts a todo?", "অন্য screen কোনো todo insert করলে list কীভাবে আপনা-আপনি refresh হবে?"),
        ],
        related=["rn-022", "rn-026", "rn-025"],
        refs=[R_SQLITE, R_SQLITE_PRAGMA],
    ),
    # ------------------------------------------------------------------ rn-024
    Q(
        id="rn-024", sub="expo-sqlite", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["expo-sqlite", "sql-injection", "execasync", "parameters", "security"],
        ver=VER_SQL, vs=True, status="stable",
        q_en=r"""
            Two bug reports for the notes app: renaming a note to `Karim's shop` crashes with a SQL syntax error, and after a QA tester renamed a note to `x'; DROP TABLE notes; --` **every** note disappeared. Find the root cause in this code and fix it.
        """,
        q_bn=r"""
            Notes app-এর দুইটা bug report: একটা note-এর নাম `Karim's shop` দিলে SQL syntax error দিয়ে crash হয়, আর একজন QA tester একটা note-এর নাম `x'; DROP TABLE notes; --` দেওয়ার পরে **সব** note উধাও হয়ে গেছে। এই code-এ মূল কারণ খুঁজে বের করো আর ঠিক করো।
        """,
        a_en=r"""
            Root cause: **user input is concatenated into the SQL text**, so the input can change the SQL itself. In `renameNote` the apostrophe in `Karim's` closes the string literal early, which is a syntax error. The tester's title is worse: `execAsync` runs **multiple statements** and does no escaping, so the database receives

            `UPDATE notes SET title = 'x'; DROP TABLE notes; --' WHERE id = 1;`

            That is an `UPDATE` with no `WHERE` (every title becomes `x`), then `DROP TABLE notes`, then a comment that swallows the rest. I ran this string in sqlite3 and the `notes` table was gone. `searchNotes` has the same flaw: a term like `%' OR 1=1 --` rewrites its `WHERE` clause.

            Fix: never build SQL from input. Use `runAsync` / `getAllAsync` with `?` placeholders (or prepared statements) so values are **bound** separately from the SQL. Keep `execAsync` for fixed setup SQL only. For the search, keep the `%` wildcards in SQL: `title LIKE '%' || ? || '%'`.
        """,
        a_bn=r"""
            মূল কারণ: **user input SQL text-এর সাথে জোড়া লাগানো হচ্ছে**, তাই input নিজেই SQL বদলে দিতে পারে। `renameNote`-এ `Karim's`-এর apostrophe string literal আগেভাগে বন্ধ করে দেয়, ফলে syntax error হয়। Tester-এর title আরও খারাপ: `execAsync` **একাধিক statement** চালায় আর কোনো escaping করে না, তাই database পায়

            `UPDATE notes SET title = 'x'; DROP TABLE notes; --' WHERE id = 1;`

            মানে `WHERE` ছাড়া একটা `UPDATE` (সব title `x` হয়ে যায়), তারপর `DROP TABLE notes`, তারপর একটা comment যেটা বাকিটা গিলে ফেলে। আমি এই string sqlite3-এ চালিয়ে দেখেছি, `notes` table মুছে গেছে। `searchNotes`-এও একই সমস্যা: `%' OR 1=1 --`-এর মতো term তার `WHERE` clause বদলে দেয়।

            সমাধান: কখনো input দিয়ে SQL বানাবে না। `?` placeholder (বা prepared statement)-সহ `runAsync` / `getAllAsync` ব্যবহার করো, যাতে value SQL থেকে আলাদাভাবে **bind** হয়। `execAsync` শুধু fixed setup SQL-এর জন্য রাখো। Search-এর জন্য `%` wildcard SQL-এই রাখো: `title LIKE '%' || ? || '%'`।
        """,
        quick_en=r"""The title is concatenated into SQL and run with `execAsync`, which doesn't escape and runs multiple statements, so an apostrophe breaks the query and `x'; DROP TABLE notes; --` drops the table. Fix: `runAsync('UPDATE notes SET title = ? WHERE id = ?', title, id)` and bound params everywhere.""",
        quick_bn=r"""Title SQL-এর সাথে জোড়া লাগিয়ে `execAsync` দিয়ে চালানো হচ্ছে, যেটা escape করে না আর একাধিক statement চালায়, তাই apostrophe query ভেঙে দেয় আর `x'; DROP TABLE notes; --` table drop করে দেয়। সমাধান: `runAsync('UPDATE notes SET title = ? WHERE id = ?', title, id)` আর সব জায়গায় bound param।""",
        ex_en=r"""
            - **Why binding works:** with `?` the SQL is compiled first and the value is attached afterwards as data, so quotes, semicolons and `--` inside it are just characters. That also fixes the apostrophe bug, which is why "escaping quotes by hand" is the wrong fix.
            - **What can't be bound:** table and column names, `ASC`/`DESC`, and pragma values. If a user picks the sort column, map it through an allowlist (`{ newest: 'created_at DESC' }[sort]`), never pass the raw string.
            - **`LIKE` wildcards:** a bound term containing `%` or `_` still acts as a wildcard. That isn't injection, but if exact matching matters, escape them and add an `ESCAPE` clause.
            - **"It's a local database, who cares?"** Input also comes from deep links, synced server data and clipboard pastes; a crash or wiped table loses the user's offline data, and with SQLCipher or multi-user data the impact grows.
            - The fixed `renameNote` also checks `changes` so a missing id is reported instead of silently ignored.
        """,
        ex_bn=r"""
            - **Binding কেন কাজ করে:** `?` দিলে আগে SQL compile হয় আর পরে value data হিসেবে যুক্ত হয়, তাই এর ভেতরের quote, semicolon আর `--` শুধুই character। এতে apostrophe bug-ও ঠিক হয়ে যায়, এজন্যই "হাতে quote escape করা" ভুল সমাধান।
            - **যা bind করা যায় না:** table আর column-এর নাম, `ASC`/`DESC`, আর pragma value। User যদি sort column বেছে নেয়, সেটা allowlist দিয়ে map করো (`{ newest: 'created_at DESC' }[sort]`), raw string কখনো পাঠাবে না।
            - **`LIKE` wildcard:** bound term-এ `%` বা `_` থাকলে সেটা তখনো wildcard হিসেবে কাজ করে। এটা injection না, কিন্তু exact match দরকার হলে এগুলো escape করে `ESCAPE` clause যোগ করো।
            - **"Local database, এত চিন্তা কীসের?"** Input deep link, sync হওয়া server data আর clipboard paste থেকেও আসে; crash বা মুছে যাওয়া table user-এর offline data হারিয়ে দেয়, আর SQLCipher বা multi-user data থাকলে ক্ষতি আরও বাড়ে।
            - সংশোধিত `renameNote` `changes`-ও check করে, যাতে id না পেলে চুপচাপ উপেক্ষা না করে error জানায়।
        """,
        tip_en=r"""Show the exact SQL string the database receives; it makes the bug obvious. Then say the rule: "`execAsync` for fixed SQL, bound params for every value", and mention the allowlist for identifiers.""",
        tip_bn=r"""Database ঠিক কোন SQL string পায় সেটা দেখাও; তাতে bug পরিষ্কার হয়ে যায়। তারপর নিয়মটা বলো: "fixed SQL-এর জন্য `execAsync`, প্রতিটা value-র জন্য bound param", আর identifier-এর জন্য allowlist-এর কথা উল্লেখ করো।""",
        mist_en=r"""Fixing it with `title.replace("'", "''")` (misses cases and other inputs), or switching to `runAsync` but still building the string with a template literal.""",
        mist_bn=r"""`title.replace("'", "''")` দিয়ে ঠিক করার চেষ্টা (কিছু case আর অন্য input বাদ পড়ে), অথবা `runAsync`-এ গিয়েও template literal দিয়েই string বানানো।""",
        code=r"""
            import type { SQLiteDatabase } from 'expo-sqlite';

            export async function renameNote(db: SQLiteDatabase, id: number, title: string) {
              await db.execAsync(`UPDATE notes SET title = '${title}' WHERE id = ${id}`);
            }

            export function searchNotes(db: SQLiteDatabase, term: string) {
              return db.getAllAsync(`SELECT id, title FROM notes WHERE title LIKE '%${term}%'`);
            }
        """,
        lang="typescript",
        extra=[
            dict(lang="typescript", src=r"""
                import type { SQLiteDatabase } from 'expo-sqlite';

                export async function renameNote(db: SQLiteDatabase, id: number, title: string) {
                  const result = await db.runAsync('UPDATE notes SET title = ? WHERE id = ?', title, id);
                  if (result.changes === 0) throw new Error(`Note ${id} not found`);
                }

                export function searchNotes(db: SQLiteDatabase, term: string) {
                  return db.getAllAsync<{ id: number; title: string }>(
                    "SELECT id, title FROM notes WHERE title LIKE '%' || ? || '%'",
                    term,
                  );
                }
            """, label_en="Fixed version (bound parameters)", label_bn="সংশোধিত version (bound parameter)"),
            dict(lang="sql", src=r"""
                -- What execAsync actually ran for title = x'; DROP TABLE notes; --
                UPDATE notes SET title = 'x'; DROP TABLE notes; --' WHERE id = 1;
                -- 1) UPDATE without WHERE: every title becomes 'x'
                -- 2) DROP TABLE notes
                -- 3) the rest of the line is a comment
            """, label_en="The injected SQL (verified in sqlite3)", label_bn="Inject হওয়া SQL (sqlite3-এ যাচাই করা)"),
        ],
        follow=[
            ("The user can sort notes by title or date. How do you build the `ORDER BY` safely?", "User title বা date দিয়ে note sort করতে পারে। `ORDER BY` নিরাপদে কীভাবে বানাবে?"),
            ("Does using Drizzle ORM remove the risk of SQL injection completely?", "Drizzle ORM ব্যবহার করলে কি SQL injection-এর ঝুঁকি পুরোপুরি চলে যায়?"),
        ],
        related=["rn-022", "rn-032", "sql-021"],
        refs=[R_SQLITE, R_OWASP_SQLI],
    ),
]

save("reactnative", "b3", QUESTIONS)
