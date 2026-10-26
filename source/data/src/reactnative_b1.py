# React Native (with Expo) — batch 1 (rn-001..008)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_CORE = ("React Native — Core Components and Native Components", "https://reactnative.dev/docs/intro-react-native-components")
R_GET_STARTED = ("React Native — Get Started with React Native", "https://reactnative.dev/docs/environment-setup")
R_ARCH = ("React Native — Architecture Overview", "https://reactnative.dev/architecture/landing-page")
R_TEXT = ("React Native — Text", "https://reactnative.dev/docs/text")
R_VIEW = ("React Native — View", "https://reactnative.dev/docs/view")
R_STYLE = ("React Native — Style", "https://reactnative.dev/docs/style")
R_STYLESHEET = ("React Native — StyleSheet", "https://reactnative.dev/docs/stylesheet")
R_FLEX = ("React Native — Layout with Flexbox", "https://reactnative.dev/docs/flexbox")
R_PLATFORM_CODE = ("React Native — Platform-Specific Code", "https://reactnative.dev/docs/platform-specific-code")
R_PLATFORM = ("React Native — Platform", "https://reactnative.dev/docs/platform")
R_DEV_BUILD = ("Expo — Introduction to development builds", "https://docs.expo.dev/develop/development-builds/introduction/")
R_CNG = ("Expo — Continuous Native Generation (CNG)", "https://docs.expo.dev/workflow/continuous-native-generation/")
R_EAS_BUILD = ("Expo — EAS Build", "https://docs.expo.dev/build/introduction/")
R_MMKV = ("react-native-mmkv (GitHub)", "https://github.com/mrousavy/react-native-mmkv")
R_PRESSABLE = ("React Native — Pressable", "https://reactnative.dev/docs/pressable")
R_A11Y = ("React Native — Accessibility", "https://reactnative.dev/docs/accessibility")

VER = "React Native 0.88, Expo SDK 58"

QUESTIONS = [
    # ------------------------------------------------------------------ rn-001
    Q(
        id="rn-001", sub="React Native Basics", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["react-native", "native-views", "flutter", "pwa", "cross-platform"],
        ver="React Native 0.88 (New Architecture)", vs=False, status="stable",
        q_en=r"""What is React Native? Does it run your app inside a WebView, and where does it fit compared with fully native apps, Flutter and a PWA?""",
        q_bn=r"""React Native কী? এটা কি app-কে একটা WebView-এর ভেতরে চালায়? Fully native app, Flutter আর PWA-এর তুলনায় React Native কোথায় fit করে?""",
        a_en=r"""
            React Native is a framework for building iOS and Android apps with React and JavaScript/TypeScript. It is **not** a WebView: when I render `<View>` or `<Text>`, React Native creates real platform views (`UIView` on iOS, `android.view.View` on Android). My JS runs in the Hermes engine and talks to native code directly through JSI on the New Architecture.

            - **vs fully native (Swift/Kotlin):** one shared codebase and React skills, at the cost of an extra layer; for very platform-heavy apps native can still win.
            - **vs Flutter:** Flutter uses Dart and paints its own widgets with its own rendering engine; React Native uses the platform's own UI components.
            - **vs PWA:** a PWA runs in the browser with limited device APIs (especially on iOS) and no normal store presence; React Native ships a real store app.
        """,
        a_bn=r"""
            React Native হলো React আর JavaScript/TypeScript দিয়ে iOS ও Android app বানানোর একটা framework। এটা WebView **না**: আমি যখন `<View>` বা `<Text>` render করি, React Native আসল platform view তৈরি করে (iOS-এ `UIView`, Android-এ `android.view.View`)। আমার JS চলে Hermes engine-এ, আর New Architecture-এ JSI দিয়ে সরাসরি native code-এর সাথে কথা বলে।

            - **Fully native (Swift/Kotlin)-এর তুলনায়:** একটাই shared codebase আর React-এর জ্ঞান কাজে লাগে, তবে মাঝে একটা বাড়তি layer থাকে; খুব বেশি platform-নির্ভর app-এ native এখনও এগিয়ে থাকতে পারে।
            - **Flutter-এর তুলনায়:** Flutter Dart ব্যবহার করে আর নিজের rendering engine দিয়ে নিজের widget নিজেই আঁকে; React Native platform-এর নিজস্ব UI component ব্যবহার করে।
            - **PWA-এর তুলনায়:** PWA browser-এ চলে, device API সীমিত (বিশেষ করে iOS-এ), আর সাধারণভাবে store-এ থাকে না; React Native দিয়ে আসল store app ship করা যায়।
        """,
        quick_en=r"""React Native lets you build iOS and Android apps with React and JS/TS, and it renders real native views, not a WebView. Flutter paints its own widgets with Dart, and a PWA runs in the browser with limited device access.""",
        quick_bn=r"""React Native দিয়ে React আর JS/TS ব্যবহার করে iOS ও Android app বানানো যায়, আর এটা WebView না, আসল native view render করে। Flutter Dart দিয়ে নিজের widget নিজে আঁকে, আর PWA browser-এ চলে, device access সীমিত।""",
        ex_en=r"""
            - **Who renders what:** React decides *what* the UI should be; the React Native renderer (Fabric) turns that tree into native views. Layout is calculated with Yoga, a Flexbox engine, so styling feels like CSS Flexbox.
            - **Where JS runs:** on a JS thread inside Hermes (the default engine). Heavy work on that thread delays touches and updates, which is why list and animation performance matter so much in interviews.
            - **WebView-based tools** such as Cordova/Ionic render HTML inside a browser view; that is the main difference people confuse.
            - **New Architecture:** since 0.82 React Native runs only on the New Architecture (Fabric, TurboModules, JSI, bridgeless). The old asynchronous JSON "bridge" is history.
            - **Code sharing:** business logic, state and most UI are shared; platform differences are handled with `Platform` or `.ios.tsx`/`.android.tsx` files.
        """,
        ex_bn=r"""
            - **কে কী render করে:** UI কেমন হবে সেটা ঠিক করে React; React Native renderer (Fabric) সেই tree-কে native view-এ রূপান্তর করে। Layout হিসাব করে Yoga নামের একটা Flexbox engine, তাই styling অনেকটা CSS Flexbox-এর মতো লাগে।
            - **JS কোথায় চলে:** Hermes (default engine)-এর ভেতরে একটা JS thread-এ। ওই thread-এ ভারী কাজ চললে touch আর update দেরিতে হয়, এজন্যই interview-এ list আর animation performance এত গুরুত্বপূর্ণ।
            - **WebView-based tool** যেমন Cordova/Ionic browser view-এর ভেতরে HTML render করে; মানুষ সাধারণত এখানেই গুলিয়ে ফেলে।
            - **New Architecture:** 0.82 থেকে React Native শুধু New Architecture-এ চলে (Fabric, TurboModules, JSI, bridgeless)। পুরনো asynchronous JSON "bridge" এখন শুধু ইতিহাস।
            - **Code sharing:** business logic, state আর বেশিরভাগ UI shared থাকে; platform-এর পার্থক্য `Platform` বা `.ios.tsx`/`.android.tsx` file দিয়ে সামলানো হয়।
        """,
        tip_en=r"""Open with "real native views driven by JavaScript, not a WebView", then give one honest trade-off for each alternative. Mentioning Hermes and the New Architecture in one sentence shows you're current.""",
        tip_bn=r"""শুরু করো "JavaScript দিয়ে চালানো আসল native view, WebView না" বলে, তারপর প্রতিটা বিকল্পের একটা করে সৎ trade-off বলো। এক লাইনে Hermes আর New Architecture উল্লেখ করলে বোঝা যায় তুমি আপডেটেড।""",
        mist_en=r"""Saying React Native "compiles JavaScript to native code" or "runs in a WebView". JavaScript is executed by Hermes at runtime (as bytecode); only the UI components are native.""",
        mist_bn=r"""বলা যে React Native "JavaScript-কে native code-এ compile করে" বা "WebView-এ চলে"। আসলে JavaScript runtime-এ Hermes চালায় (bytecode হিসেবে); শুধু UI component-গুলো native।""",
        code=r"""
            import { View, Text, Image } from 'react-native';

            // Each tag becomes a real platform view:
            // View  -> UIView (iOS) / android.view.View (Android)
            // Text  -> native text view
            // Image -> native image view
            export function ProductCard({ name, imageUrl }: { name: string; imageUrl: string }) {
              return (
                <View style={{ padding: 16 }}>
                  <Image source={{ uri: imageUrl }} style={{ width: 120, height: 120 }} />
                  <Text>{name}</Text>
                </View>
              );
            }
        """,
        lang="tsx",
        follow=[
            ("What does Hermes do, and why is it the default engine?", "Hermes কী করে, আর এটা default engine কেন?"),
            ("When would you choose fully native over React Native for a project?", "কোন project-এ তুমি React Native-এর বদলে fully native বেছে নেবে?"),
        ],
        related=["rn-033", "rn-006", "react-001"],
        refs=[R_CORE, R_ARCH],
    ),
    # ------------------------------------------------------------------ rn-002
    Q(
        id="rn-002", sub="Core Components", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["text", "view", "core-components", "rendering-error"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""Assume `name = 'Rahim'` and `count = 0`. Which snippet renders without the error "Text strings must be rendered within a `<Text>` component"?""",
        q_bn=r"""ধরো `name = 'Rahim'` আর `count = 0`। কোন snippet "Text strings must be rendered within a `<Text>` component" error ছাড়া render হবে?""",
        options=[
            (r"`<View>Hello {name}</View>`", r"`<View>Hello {name}</View>`"),
            (r"`<View><Text>Hello {name}</Text></View>`", r"`<View><Text>Hello {name}</Text></View>`"),
            (r"`<Text><View>Hello {name}</View></Text>`", r"`<Text><View>Hello {name}</View></Text>`"),
            (r"`<View>{count && <Text>{count} new</Text>}</View>`", r"`<View>{count && <Text>{count} new</Text>}</View>`"),
        ],
        correct=1,
        a_en=r"""**B** (`<View><Text>Hello {name}</Text></View>`) is correct. In React Native every string or number you render must sit directly inside a `<Text>`. `<View>` is a layout container like a `div`, but unlike the web it cannot hold raw text.""",
        a_bn=r"""**B** (`<View><Text>Hello {name}</Text></View>`) সঠিক। React Native-এ যত string বা number render করবে, সবকিছু সরাসরি একটা `<Text>`-এর ভেতরে থাকতে হবে। `<View>` হলো `div`-এর মতো layout container, কিন্তু web-এর মতো এর ভেতরে সরাসরি text রাখা যায় না।""",
        quick_en=r"""Only `<View><Text>Hello {name}</Text></View>` works: every string or number must be inside a `<Text>`. Raw text in a `<View>`, even a stray `0` from `count && ...`, throws.""",
        quick_bn=r"""শুধু `<View><Text>Hello {name}</Text></View>` কাজ করে: প্রতিটা string বা number একটা `<Text>`-এর ভেতরে থাকতে হবে। `<View>`-এর ভেতরে সরাসরি text, এমনকি `count && ...` থেকে আসা একটা `0`-ও error দেয়।""",
        ex_en=r"""
            - **A** (`<View>Hello {name}</View>`) is the classic web habit: the string is a direct child of `View`, so React Native throws.
            - **C** (`<Text><View>Hello {name}</View></Text>`) still puts the string inside a `View`. Wrapping the outside in `Text` doesn't help; the string's direct parent must be `Text`.
            - **D** is the tempting one. With `count = 0`, `count && ...` evaluates to `0`, and React renders numbers. That `0` lands inside the `View` as raw text and crashes the screen. On the web it would just show a stray "0"; on mobile it's an error. Use `count > 0 && ...` or a ternary.

            Other core components to know: `View` (layout box), `Text` (all text, can be nested for inline styling), `Image` (needs a `source` and, for remote images, explicit width/height), `TextInput`, `Pressable`, `ScrollView`.
        """,
        ex_bn=r"""
            - **A** (`<View>Hello {name}</View>`) হলো web-এর পুরনো অভ্যাস: string-টা সরাসরি `View`-এর child, তাই React Native error দেয়।
            - **C** (`<Text><View>Hello {name}</View></Text>`)-এও string-টা `View`-এর ভেতরেই আছে। বাইরে `Text` দিয়ে মোড়ালে লাভ নেই; string-এর সরাসরি parent হতে হবে `Text`।
            - **D** সবচেয়ে লোভনীয় ভুল। `count = 0` হলে `count && ...`-এর মান হয় `0`, আর React number render করে। ওই `0` raw text হিসেবে `View`-এর ভেতরে পড়ে আর screen crash করে। Web-এ এটা শুধু একটা বাড়তি "0" দেখাত; mobile-এ এটা error। এর বদলে `count > 0 && ...` বা ternary লেখো।

            আরও কিছু core component জানা দরকার: `View` (layout box), `Text` (সব text, inline styling-এর জন্য nest করা যায়), `Image` (`source` লাগে, আর remote image-এর জন্য width/height স্পষ্টভাবে দিতে হয়), `TextInput`, `Pressable`, `ScrollView`।
        """,
        tip_en=r"""Say the rule ("all text inside `<Text>`") and then point out the `count && ...` trap. Interviewers like that you know the web bug becomes a crash in React Native.""",
        tip_bn=r"""নিয়মটা বলো ("সব text `<Text>`-এর ভেতরে"), তারপর `count && ...` ফাঁদটা দেখাও। Web-এর ছোট bug যে React Native-এ crash হয়ে যায়, এটা জানলে interviewer খুশি হয়।""",
        mist_en=r"""Fixing the error by wrapping the whole screen in one big `<Text>`. Layout boxes should stay `View`s; wrap only the strings in `Text`.""",
        mist_bn=r"""পুরো screen-কে একটা বড় `<Text>` দিয়ে মুড়িয়ে error ঠিক করা। Layout box `View` হিসেবেই থাকা উচিত; শুধু string-গুলোকে `Text` দিয়ে মোড়াও।""",
        follow=[
            ("How does style inheritance work for nested `<Text>` elements?", "Nested `<Text>`-এ style inheritance কীভাবে কাজ করে?"),
            ("Why does a remote `<Image>` need an explicit width and height?", "Remote `<Image>`-এ কেন width আর height স্পষ্টভাবে দিতে হয়?"),
        ],
        related=["rn-003", "rn-001"],
        refs=[R_TEXT, R_VIEW, R_CORE],
    ),
    # ------------------------------------------------------------------ rn-003
    Q(
        id="rn-003", sub="Styling", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["stylesheet", "styling", "no-cascade", "dp", "flexbox"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""How is styling in React Native different from CSS on the web? Explain `StyleSheet`, units, inheritance and the Flexbox defaults.""",
        q_bn=r"""React Native-এর styling web-এর CSS থেকে কীভাবে আলাদা? `StyleSheet`, unit, inheritance আর Flexbox-এর default-গুলো ব্যাখ্যা করো।""",
        a_en=r"""
            Styles are plain JavaScript objects, usually created with `StyleSheet.create`, and passed through the `style` prop. There are no CSS files, selectors or class names.

            - **Names are camelCase:** `backgroundColor`, `fontSize`, `borderRadius`.
            - **Numbers have no unit:** `padding: 16` means 16 density-independent pixels (dp/pt), so it looks about the same size on every screen density. Percentages are strings (`width: '50%'`).
            - **No cascade:** a `View`'s color or font never reaches its children. The only inheritance is from a parent `<Text>` to nested `<Text>`.
            - **Flexbox is always on**, but `flexDirection` defaults to `'column'` (the web default is `row`), and `flex: 1` means "take the free space".
            - **Arrays combine styles:** `style={[styles.card, isActive && styles.active]}`; later entries win, falsy entries are ignored.
        """,
        a_bn=r"""
            Style হলো সাধারণ JavaScript object, সাধারণত `StyleSheet.create` দিয়ে বানানো হয় আর `style` prop দিয়ে পাঠানো হয়। কোনো CSS file, selector বা class name নেই।

            - **নাম camelCase-এ:** `backgroundColor`, `fontSize`, `borderRadius`।
            - **Number-এর কোনো unit নেই:** `padding: 16` মানে 16 density-independent pixel (dp/pt), তাই যেকোনো screen density-তে মোটামুটি একই আকারে দেখায়। Percentage লিখতে হয় string হিসেবে (`width: '50%'`)।
            - **Cascade নেই:** একটা `View`-এর color বা font তার children-এর কাছে যায় না। একমাত্র inheritance হয় parent `<Text>` থেকে nested `<Text>`-এ।
            - **Flexbox সবসময় চালু**, কিন্তু `flexDirection`-এর default `'column'` (web-এ default `row`), আর `flex: 1` মানে "বাকি খালি জায়গা নিয়ে নাও"।
            - **Array দিয়ে style মেলানো যায়:** `style={[styles.card, isActive && styles.active]}`; পরের entry জেতে, falsy entry বাদ পড়ে।
        """,
        quick_en=r"""React Native styles are JS objects (usually from `StyleSheet.create`) with camelCase names and unitless numbers in density-independent pixels. There is no cascade except nested `<Text>`, and Flexbox defaults to `flexDirection: 'column'`.""",
        quick_bn=r"""React Native-এর style হলো JS object (সাধারণত `StyleSheet.create` থেকে), নাম camelCase-এ আর number-এর unit নেই, মানে density-independent pixel। Nested `<Text>` ছাড়া কোনো cascade নেই, আর Flexbox-এর default `flexDirection: 'column'`।""",
        ex_en=r"""
            - **Why `StyleSheet.create`?** It gives type checking and editor hints, and keeps style objects defined once outside render so they aren't recreated on every render. Inline objects work but get messy.
            - **No pseudo-classes or media queries:** pressed state comes from `Pressable`'s `style={({ pressed }) => ...}`, and responsive layout from `useWindowDimensions`.
            - **Other Flexbox differences:** `alignContent` defaults to `flex-start`, `flexShrink` defaults to `0`, and `flex` accepts only a single number.
            - **Text inheritance:** in `<Text style={{ fontSize: 18 }}>Order <Text style={{ color: 'teal' }}>#1042</Text></Text>`, the inner text keeps the 18 size and adds the color. Put a font on a `View` and nothing happens.
            - **Theming:** since there's no cascade, apps usually pass theme values through context (or a styling library) instead of a global stylesheet.
        """,
        ex_bn=r"""
            - **কেন `StyleSheet.create`?** এতে type checking আর editor hint পাওয়া যায়, আর style object render-এর বাইরে একবারই define হয়, তাই প্রতি render-এ নতুন করে তৈরি হয় না। Inline object-ও চলে, কিন্তু code অগোছালো হয়ে যায়।
            - **Pseudo-class বা media query নেই:** pressed state আসে `Pressable`-এর `style={({ pressed }) => ...}` থেকে, আর responsive layout আসে `useWindowDimensions` থেকে।
            - **Flexbox-এর আরও পার্থক্য:** `alignContent`-এর default `flex-start`, `flexShrink`-এর default `0`, আর `flex` শুধু একটা number নেয়।
            - **Text inheritance:** `<Text style={{ fontSize: 18 }}>Order <Text style={{ color: 'teal' }}>#1042</Text></Text>`-এ ভেতরের text 18 size রাখে আর সাথে color যোগ করে। কিন্তু `View`-এ font দিলে কিছুই হয় না।
            - **Theming:** cascade নেই বলে app-গুলো সাধারণত global stylesheet-এর বদলে context (বা কোনো styling library) দিয়ে theme value পাঠায়।
        """,
        tip_en=r"""List three concrete differences (camelCase objects, unitless dp, no cascade) and the column default. A tiny nested-`Text` example proves you've actually hit the inheritance rule.""",
        tip_bn=r"""তিনটা স্পষ্ট পার্থক্য বলো (camelCase object, unit ছাড়া dp, cascade নেই), সাথে column default। ছোট একটা nested-`Text` example দেখালে বোঝা যায় তুমি সত্যিই inheritance-এর নিয়মটার মুখোমুখি হয়েছ।""",
        mist_en=r"""Writing `padding: '16px'` or expecting a `color` on a container `View` to color the text inside it. Neither works in React Native.""",
        mist_bn=r"""`padding: '16px'` লেখা, বা আশা করা যে container `View`-এ `color` দিলে ভেতরের text-এর রং বদলাবে। React Native-এ দুটোর কোনোটাই কাজ করে না।""",
        code=r"""
            import { StyleSheet, Text, View } from 'react-native';

            export function OrderBadge({ isActive }: { isActive: boolean }) {
              return (
                <View style={[styles.card, isActive && styles.active]}>
                  <Text style={styles.title}>
                    Order <Text style={styles.highlight}>#1042</Text>
                  </Text>
                </View>
              );
            }

            const styles = StyleSheet.create({
              card: { padding: 16, borderRadius: 12, backgroundColor: '#fff' }, // 16 = dp, no unit
              active: { borderWidth: 2, borderColor: 'teal' },                  // wins over card
              title: { fontSize: 18, fontWeight: '600' },
              highlight: { color: 'teal' }, // inherits fontSize/fontWeight from the parent Text
            });
        """,
        lang="tsx",
        follow=[
            ("How would you implement a light/dark theme without a CSS cascade?", "CSS cascade ছাড়া light/dark theme কীভাবে implement করবে?"),
            ("How do you show a different style while a button is pressed?", "Button press করা অবস্থায় আলাদা style কীভাবে দেখাবে?"),
        ],
        related=["rn-004", "rn-002", "rn-013"],
        refs=[R_STYLE, R_STYLESHEET, R_FLEX],
    ),
    # ------------------------------------------------------------------ rn-004
    Q(
        id="rn-004", sub="Flexbox Layout", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["flexbox", "layout", "flex", "align-items"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""The screen below fills a phone in portrait mode. None of the children set a width. How are the three children laid out?""",
        q_bn=r"""নিচের screen-টা portrait mode-এ পুরো phone জুড়ে আছে। কোনো child-এ width দেওয়া নেই। তিনটা child কীভাবে সাজানো হবে?""",
        code=r"""
            <View style={{ flex: 1 }}>
              <View style={{ height: 80, backgroundColor: 'navy' }} />
              <View style={{ flex: 1, backgroundColor: 'tomato' }} />
              <View style={{ flex: 2, backgroundColor: 'teal' }} />
            </View>
        """,
        lang="tsx",
        options=[
            ("Stacked top to bottom, all full width: navy is 80 tall, and the remaining height is split 1:2 between tomato and teal", "উপর থেকে নিচে সাজানো, সবগুলো পুরো width জুড়ে: navy 80 উঁচু, আর বাকি height tomato আর teal-এর মধ্যে 1:2 অনুপাতে ভাগ হয়"),
            ("Side by side in a row: navy is narrow, tomato takes one third and teal two thirds of the width", "পাশাপাশি এক row-তে: navy সরু, tomato width-এর এক-তৃতীয়াংশ আর teal দুই-তৃতীয়াংশ নেয়"),
            ("Stacked top to bottom, but all three are 0 wide because no width is set", "উপর থেকে নিচে সাজানো, কিন্তু width দেওয়া নেই বলে তিনটারই width 0"),
            ("Stacked top to bottom: navy is 80 tall, tomato is one third and teal two thirds of the whole screen height", "উপর থেকে নিচে সাজানো: navy 80 উঁচু, tomato পুরো screen height-এর এক-তৃতীয়াংশ আর teal দুই-তৃতীয়াংশ"),
        ],
        correct=0,
        a_en=r"""**A** is correct. React Native's `flexDirection` defaults to `'column'`, so children stack vertically. The default `alignItems: 'stretch'` makes each child as wide as the parent. Navy keeps its fixed 80 height, and the **remaining** height is shared by `flex` ratio: tomato gets 1 part, teal 2 parts.""",
        a_bn=r"""**A** সঠিক। React Native-এ `flexDirection`-এর default `'column'`, তাই children উপর-নিচে সাজানো হয়। Default `alignItems: 'stretch'`-এর কারণে প্রতিটা child parent-এর সমান চওড়া হয়। Navy তার fixed 80 height রাখে, আর **বাকি** height `flex` অনুপাতে ভাগ হয়: tomato পায় 1 ভাগ, teal 2 ভাগ।""",
        quick_en=r"""They stack top to bottom at full width: navy is 80 tall and tomato and teal split the remaining height 1:2. React Native defaults to `flexDirection: 'column'` and `alignItems: 'stretch'`, and `flex` divides only the free space.""",
        quick_bn=r"""এগুলো উপর থেকে নিচে পুরো width জুড়ে থাকে: navy 80 উঁচু, আর বাকি height tomato ও teal 1:2 অনুপাতে ভাগ করে। React Native-এর default `flexDirection: 'column'` আর `alignItems: 'stretch'`, আর `flex` শুধু খালি জায়গা ভাগ করে।""",
        ex_en=r"""
            - **B** (side by side) is the web habit: on the web `display: flex` defaults to `row`. In React Native you need `flexDirection: 'row'` for that.
            - **D** is the tempting one: `flex` doesn't divide the whole screen, it divides the space left after fixed-size siblings (the 80 of navy) are placed. So tomato gets one third of (screen height − 80).
            - **C** is wrong because `alignItems` defaults to `stretch`: a child without a width stretches across the cross axis (horizontal in a column).
            - The outer `flex: 1` matters too: without it the root `View` would only be as tall as its content, and the `flex` children would have no free space to share.
        """,
        ex_bn=r"""
            - **B** (পাশাপাশি) হলো web-এর অভ্যাস: web-এ `display: flex`-এর default `row`। React Native-এ এরকম চাইলে `flexDirection: 'row'` দিতে হয়।
            - **D** সবচেয়ে লোভনীয় ভুল: `flex` পুরো screen ভাগ করে না, fixed-size sibling (navy-র 80) বসানোর পর যে জায়গা বাকি থাকে সেটা ভাগ করে। তাই tomato পায় (screen height − 80)-এর এক-তৃতীয়াংশ।
            - **C** ভুল, কারণ `alignItems`-এর default `stretch`: width ছাড়া child cross axis (column-এ horizontal) বরাবর ছড়িয়ে যায়।
            - বাইরের `flex: 1`-ও গুরুত্বপূর্ণ: এটা না থাকলে root `View` শুধু content-এর সমান উঁচু হতো, আর `flex` children-এর ভাগ করার মতো কোনো খালি জায়গা থাকত না।
        """,
        tip_en=r"""Walk through it in order: direction (column), cross axis (stretch), fixed sizes first, then `flex` ratios on what's left. That method solves any layout question of this kind.""",
        tip_bn=r"""ধাপে ধাপে বলো: direction (column), cross axis (stretch), আগে fixed size, তারপর বাকি জায়গায় `flex` অনুপাত। এই পদ্ধতিতে এ ধরনের যেকোনো layout প্রশ্ন সমাধান করা যায়।""",
        follow=[
            ("How would you put an icon and a label side by side, vertically centred?", "একটা icon আর একটা label পাশাপাশি, vertically center করে কীভাবে বসাবে?"),
            ("What happens to the `flex` children if you remove `flex: 1` from the root?", "Root থেকে `flex: 1` সরিয়ে দিলে `flex` children-এর কী হবে?"),
        ],
        related=["rn-003", "rn-013"],
        refs=[R_FLEX, R_STYLE],
    ),
    # ------------------------------------------------------------------ rn-005
    Q(
        id="rn-005", sub="Platform Differences", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["platform", "platform-select", "file-extensions", "metro"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""A project has three files: `PayButton.ios.tsx`, `PayButton.android.tsx` and `PayButton.tsx`. A screen does `import PayButton from './PayButton'` and also computes the label below. On an **Android phone**, which file is used and what is `label`?""",
        q_bn=r"""একটা project-এ তিনটা file আছে: `PayButton.ios.tsx`, `PayButton.android.tsx` আর `PayButton.tsx`। একটা screen `import PayButton from './PayButton'` করে, আর নিচের label-টাও হিসাব করে। একটা **Android phone**-এ কোন file ব্যবহার হবে আর `label`-এর মান কী হবে?""",
        code=r"""
            import { Platform } from 'react-native';

            const label = Platform.select({
              native: 'Pay with card',
              android: 'Pay with Google Pay',
              default: 'Pay',
            });
        """,
        lang="tsx",
        options=[
            (r"`PayButton.tsx`, and `label` is `'Pay'`", r"`PayButton.tsx`, আর `label` হবে `'Pay'`"),
            (r"`PayButton.android.tsx`, and `label` is `'Pay with card'`", r"`PayButton.android.tsx`, আর `label` হবে `'Pay with card'`"),
            (r"`PayButton.android.tsx`, and `label` is `'Pay with Google Pay'`", r"`PayButton.android.tsx`, আর `label` হবে `'Pay with Google Pay'`"),
            ("The build fails because the import is ambiguous", "Import ambiguous বলে build fail করবে"),
        ],
        correct=2,
        a_en=r"""**C** (`PayButton.android.tsx`, `'Pay with Google Pay'`) is correct. Metro resolves `./PayButton` to the platform-specific file first, so Android gets `.android.tsx` and iOS gets `.ios.tsx`. In `Platform.select`, the `ios`/`android` keys win over `native`, which wins over `default`.""",
        a_bn=r"""**C** (`PayButton.android.tsx`, `'Pay with Google Pay'`) সঠিক। Metro `./PayButton`-কে আগে platform-specific file-এ resolve করে, তাই Android পায় `.android.tsx` আর iOS পায় `.ios.tsx`। `Platform.select`-এ `ios`/`android` key সবচেয়ে বেশি গুরুত্ব পায়, তারপর `native`, তারপর `default`।""",
        quick_en=r"""Android uses `PayButton.android.tsx`, and `label` is `'Pay with Google Pay'`. Metro picks the platform-specific file first, and `Platform.select` prefers `android`/`ios` over `native`, then `default`.""",
        quick_bn=r"""Android ব্যবহার করে `PayButton.android.tsx`, আর `label` হয় `'Pay with Google Pay'`। Metro আগে platform-specific file নেয়, আর `Platform.select` আগে `android`/`ios`, তারপর `native`, তারপর `default` দেখে।""",
        ex_en=r"""
            - **B** is the tempting one: `native` matches both phones, but it's only a fallback when there's no exact `ios`/`android` key.
            - **A** is wrong: the plain `PayButton.tsx` is used only when no platform file matches, for example on web (where `.web.tsx` would also take priority).
            - **D** is wrong: having both platform files and a base file is a normal pattern, not an ambiguity. You always import without the extension.

            When to use what: `Platform.OS === 'ios'` or `Platform.select` for small differences (a value, a style, a prop); separate `.ios.tsx`/`.android.tsx` files when the components really differ. Keep the props of both files identical so TypeScript and callers don't care which one loads. `Platform.Version` is a number (API level) on Android and a string on iOS.
        """,
        ex_bn=r"""
            - **B** সবচেয়ে লোভনীয় ভুল: `native` দুই phone-এর সাথেই মেলে, কিন্তু এটা শুধু fallback, যখন নির্দিষ্ট `ios`/`android` key থাকে না।
            - **A** ভুল: সাধারণ `PayButton.tsx` তখনই ব্যবহার হয় যখন কোনো platform file মেলে না, যেমন web-এ (সেখানে `.web.tsx` থাকলে সেটাই আগে নেওয়া হতো)।
            - **D** ভুল: platform file আর base file দুটো একসাথে রাখা খুব সাধারণ pattern, কোনো ambiguity না। Import সবসময় extension ছাড়াই করা হয়।

            কখন কোনটা: ছোট পার্থক্যের জন্য (একটা value, style বা prop) `Platform.OS === 'ios'` বা `Platform.select`; component সত্যিই আলাদা হলে আলাদা `.ios.tsx`/`.android.tsx` file। দুই file-এর props একই রাখো, যাতে TypeScript বা caller-কে মাথা ঘামাতে না হয় কোনটা load হলো। `Platform.Version` Android-এ একটা number (API level) আর iOS-এ string।
        """,
        tip_en=r"""State the resolution order for both mechanisms (file extensions and `Platform.select` keys) and when you'd pick each. That's the whole answer in two sentences.""",
        tip_bn=r"""দুটো mechanism-এরই (file extension আর `Platform.select` key) resolution order বলো, আর কখন কোনটা বেছে নেবে সেটা বলো। দুই লাইনেই পুরো উত্তর হয়ে যায়।""",
        follow=[
            ("When would you use `.native.tsx` instead of `.ios.tsx`/`.android.tsx`?", "কখন `.ios.tsx`/`.android.tsx`-এর বদলে `.native.tsx` ব্যবহার করবে?"),
            ("How do you check the Android API level at runtime?", "Runtime-এ Android API level কীভাবে check করবে?"),
        ],
        related=["rn-001", "rn-012"],
        refs=[R_PLATFORM_CODE, R_PLATFORM],
    ),
    # ------------------------------------------------------------------ rn-006
    Q(
        id="rn-006", sub="Expo Basics", diff="easy", type="comparison",
        prio="high", market="both", mins=4,
        tags=["expo", "cng", "prebuild", "eas", "development-build"],
        ver=VER, vs=True, status="stable",
        q_en=r"""Compare starting a new app with Expo and with a "bare" React Native project (React Native Community CLI). What do CNG/prebuild, development builds and EAS give you, and why do the React Native docs recommend using a framework?""",
        q_bn=r"""নতুন app Expo দিয়ে শুরু করা আর "bare" React Native project (React Native Community CLI) দিয়ে শুরু করার তুলনা করো। CNG/prebuild, development build আর EAS কী সুবিধা দেয়, আর React Native docs কেন framework ব্যবহার করতে বলে?""",
        a_en=r"""
            The React Native docs recommend starting new apps with a framework, and Expo is that framework. A bare project gives you the core library plus committed `ios/` and `android/` folders that you maintain by hand.

            - **CNG (Continuous Native Generation):** with Expo you describe native settings in `app.json`/`app.config.ts` and config plugins; `npx expo prebuild` generates `ios/` and `android/` from that. You can regenerate them any time, which makes SDK upgrades much easier. In bare, you edit Xcode/Gradle files directly and upgrade them yourself.
            - **Development builds:** your own debug app with your native libraries plus `expo-dev-client`, built with `npx expo run:android` or EAS. Expo Go is only a sandbox for learning.
            - **EAS:** cloud services for Build, Submit (to the stores) and Update (OTA JS updates). They are optional; you can still build locally.
            - **Batteries:** Expo Router, the Expo SDK modules, and the Expo Modules API for your own native code.

            So I start with Expo; bare makes sense mainly for a large existing native app that embeds React Native.
        """,
        a_bn=r"""
            React Native docs নতুন app framework দিয়ে শুরু করতে বলে, আর সেই framework হলো Expo। Bare project-এ থাকে core library আর commit করা `ios/` ও `android/` folder, যেগুলো হাতে maintain করতে হয়।

            - **CNG (Continuous Native Generation):** Expo-তে native setting লেখা হয় `app.json`/`app.config.ts` আর config plugin-এ; `npx expo prebuild` সেখান থেকে `ios/` আর `android/` generate করে। যখন খুশি আবার generate করা যায়, তাই SDK upgrade অনেক সহজ হয়। Bare-এ Xcode/Gradle file সরাসরি edit করতে হয় আর upgrade নিজেকেই করতে হয়।
            - **Development build:** তোমার native library আর `expo-dev-client` দিয়ে বানানো নিজের debug app, `npx expo run:android` বা EAS দিয়ে build করা হয়। Expo Go শুধু শেখার জন্য একটা sandbox।
            - **EAS:** Build, Submit (store-এ পাঠানো) আর Update (OTA JS update)-এর cloud service। এগুলো optional; local-এও build করা যায়।
            - **সাথে যা আসে:** Expo Router, Expo SDK module, আর নিজের native code-এর জন্য Expo Modules API।

            তাই আমি Expo দিয়েই শুরু করি; bare মূলত তখনই যুক্তিসঙ্গত যখন একটা বড় existing native app-এর ভেতরে React Native বসানো হচ্ছে।
        """,
        quick_en=r"""Expo is the framework the React Native docs recommend: it generates `ios/`/`android/` from `app.json` and config plugins (CNG/prebuild), uses development builds, and offers EAS Build, Submit and Update. A bare project means maintaining native folders and upgrades by hand.""",
        quick_bn=r"""Expo হলো সেই framework যেটা React Native docs recommend করে: এটা `app.json` আর config plugin থেকে `ios/`/`android/` generate করে (CNG/prebuild), development build ব্যবহার করে, আর EAS Build, Submit ও Update দেয়। Bare project মানে native folder আর upgrade হাতে সামলানো।""",
        ex_en=r"""
            - **Native folders:** generated (often git-ignored) vs committed and hand-edited.
            - **Native config:** `app.json` + config plugins vs `Info.plist`, `AndroidManifest.xml`, Gradle edits.
            - **Custom native code:** fully possible in both (Expo Modules API, local modules, any React Native library).
            - **Routing:** Expo Router built in vs choose and wire up a navigation library yourself.
            - **Builds/release:** EAS or local `npx expo run:*` vs Xcode/Gradle and your own CI scripts.

            Common myths: "Expo can't use native code" (false since development builds and config plugins) and "Expo means you must pay for EAS" (false; EAS has a free tier and local builds work). Note: if you prebuild and then hand-edit `ios/`/`android/`, the next `prebuild --clean` wipes those edits; move them into a config plugin instead.
        """,
        ex_bn=r"""
            - **Native folder:** Expo-তে generate হয় (প্রায়ই git-ignore করা থাকে); bare-এ commit করা থাকে আর হাতে edit করা হয়।
            - **Native config:** Expo-তে `app.json` + config plugin; bare-এ `Info.plist`, `AndroidManifest.xml`, Gradle edit।
            - **Custom native code:** দুটোতেই পুরোপুরি সম্ভব (Expo Modules API, local module, যেকোনো React Native library)।
            - **Routing:** Expo-তে Expo Router built in; bare-এ নিজে একটা navigation library বেছে নিয়ে জুড়তে হয়।
            - **Build/release:** Expo-তে EAS বা local `npx expo run:*`; bare-এ Xcode/Gradle আর নিজের CI script।

            প্রচলিত ভুল ধারণা: "Expo-তে native code ব্যবহার করা যায় না" (development build আর config plugin আসার পর থেকে এটা ভুল) আর "Expo মানেই EAS-এর জন্য টাকা দিতে হবে" (ভুল; EAS-এর free tier আছে আর local build-ও চলে)। খেয়াল রাখো: prebuild করার পর `ios/`/`android/` হাতে edit করলে পরের `prebuild --clean` সেই edit মুছে দেয়; তাই ওই পরিবর্তন config plugin-এ নিয়ে যাও।
        """,
        tip_en=r"""Frame it as "Expo is the recommended framework, not a limited mode". Then explain CNG in one sentence; it's the concept most candidates can't explain clearly.""",
        tip_bn=r"""এভাবে বলো: "Expo হলো recommended framework, কোনো সীমিত mode না"। তারপর এক লাইনে CNG ব্যাখ্যা করো; বেশিরভাগ candidate এই concept-টা পরিষ্কারভাবে বলতে পারে না।""",
        mist_en=r"""Treating "Expo" and "Expo Go" as the same thing, or claiming you must eject from Expo to add a native library. Today you add the library and make a development build.""",
        mist_bn=r""""Expo" আর "Expo Go"-কে একই জিনিস ভাবা, বা বলা যে native library যোগ করতে Expo থেকে eject করতে হবে। এখন library যোগ করে একটা development build বানালেই হয়।""",
        code=r"""
            # Expo: create, generate native projects, build a dev client
            npx create-expo-app@latest my-shop
            cd my-shop
            npx expo install expo-dev-client
            npx expo prebuild --clean          # ios/ + android/ from app.json + config plugins
            npx expo run:android               # local development build (needs Android Studio)
            eas build --profile development --platform android   # or build it in the cloud
            npx expo start                     # start Metro and open the dev build

            # Bare React Native (Community CLI): native folders are yours to maintain
            npx @react-native-community/cli@latest init MyShop
        """,
        lang="bash",
        follow=[
            ("What does a config plugin do, and when would you write one?", "Config plugin কী করে, আর কখন তুমি নিজে একটা লিখবে?"),
            ("Should the generated `ios/` and `android/` folders be committed to git?", "Generate হওয়া `ios/` আর `android/` folder কি git-এ commit করা উচিত?"),
        ],
        related=["rn-007", "rn-036", "rn-035"],
        refs=[R_GET_STARTED, R_CNG, R_DEV_BUILD],
    ),
    # ------------------------------------------------------------------ rn-007
    Q(
        id="rn-007", sub="Expo Basics", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["expo-go", "development-build", "native-modules", "mmkv"],
        ver=VER, vs=True, status="stable",
        q_en=r"""Your team prototypes in Expo Go. Which change forces you to switch to a development build?""",
        q_bn=r"""তোমার team Expo Go-তে prototype বানাচ্ছে। কোন পরিবর্তনের জন্য development build-এ যেতেই হবে?""",
        options=[
            ("Rewriting a screen's layout and business logic in TypeScript", "একটা screen-এর layout আর business logic TypeScript-এ নতুন করে লেখা"),
            (r"Using `expo-camera` to scan a QR code", r"QR code scan করতে `expo-camera` ব্যবহার করা"),
            (r"Adding `react-native-mmkv` for fast key-value storage", r"দ্রুত key-value storage-এর জন্য `react-native-mmkv` যোগ করা"),
            (r"Calling a REST API with `fetch` and caching it in state", r"`fetch` দিয়ে REST API call করে state-এ cache করা"),
        ],
        correct=2,
        a_en=r"""**C** (`react-native-mmkv`) is correct. MMKV ships its own native code, and Expo Go is a prebuilt app that contains only a fixed set of native modules, so the library simply isn't inside it. You build your own app that includes it: a development build with `expo-dev-client`.""",
        a_bn=r"""**C** (`react-native-mmkv`) সঠিক। MMKV-এর নিজস্ব native code আছে, আর Expo Go একটা আগে থেকে build করা app যেখানে শুধু নির্দিষ্ট কিছু native module থাকে, তাই এই library-টা ওর ভেতরে নেই। তখন এমন একটা নিজের app build করতে হয় যেখানে এটা আছে: `expo-dev-client`-সহ একটা development build।""",
        quick_en=r"""Adding `react-native-mmkv` forces a development build, because it contains custom native code that the prebuilt Expo Go app doesn't include. JS-only changes and Expo SDK modules like `expo-camera` work in Expo Go.""",
        quick_bn=r"""`react-native-mmkv` যোগ করলে development build লাগবেই, কারণ এর নিজস্ব native code আছে যা prebuilt Expo Go app-এ নেই। শুধু JS-এর পরিবর্তন আর `expo-camera`-এর মতো Expo SDK module Expo Go-তেই চলে।""",
        ex_en=r"""
            - **B** (`expo-camera`) is the tempting one because a camera "feels native". It is native, but it's part of the Expo SDK and already compiled into Expo Go.
            - **A** and **D** are JavaScript-only changes: Metro sends new JS to the app and Fast Refresh reloads it; no native rebuild is needed in either Expo Go or a development build.
            - Other triggers for a development build: changing native config in `app.json` (custom URL scheme, app icon, permissions text), adding a config plugin, or testing push notifications properly.

            Version note (October 2026): Expo Go supports one SDK at a time, and the SDK 58 Expo Go app isn't in the stores yet, so SDK 58 projects need a development build anyway. For a real product I'd move to a development build early regardless.
        """,
        ex_bn=r"""
            - **B** (`expo-camera`) লোভনীয়, কারণ camera শুনলেই "native" মনে হয়। এটা native ঠিকই, কিন্তু Expo SDK-এর অংশ আর আগে থেকেই Expo Go-র ভেতরে compile করা আছে।
            - **A** আর **D** শুধু JavaScript-এর পরিবর্তন: Metro app-এ নতুন JS পাঠায় আর Fast Refresh সেটা reload করে; Expo Go বা development build কোনোটাতেই native rebuild লাগে না।
            - Development build লাগার আরও কারণ: `app.json`-এ native config বদলানো (custom URL scheme, app icon, permission-এর লেখা), config plugin যোগ করা, বা push notification ঠিকমতো test করা।

            Version note (অক্টোবর ২০২৬): Expo Go একবারে একটাই SDK support করে, আর SDK 58-এর Expo Go app এখনও store-এ আসেনি, তাই SDK 58 project-এ এমনিতেই development build লাগে। আসল product-এর জন্য আমি যেভাবেই হোক শুরুতেই development build-এ চলে যাই।
        """,
        tip_en=r"""Give the rule, not a list: "anything that needs native code or native config not already inside Expo Go needs a development build". Then name MMKV as the example.""",
        tip_bn=r"""List না দিয়ে নিয়মটা বলো: "যা কিছু Expo Go-তে আগে থেকে নেই এমন native code বা native config চায়, তার জন্য development build লাগে"। তারপর example হিসেবে MMKV-এর নাম বলো।""",
        follow=[
            ("After adding a native library, which changes still reach testers without a rebuild?", "Native library যোগ করার পর কোন পরিবর্তনগুলো rebuild ছাড়াই tester-দের কাছে পৌঁছায়?"),
        ],
        related=["rn-006", "rn-021", "rn-036"],
        refs=[R_DEV_BUILD, R_MMKV],
    ),
    # ------------------------------------------------------------------ rn-008
    Q(
        id="rn-008", sub="Touch & Accessibility", diff="easy", type="conceptual",
        prio="medium", market="both", mins=3,
        tags=["pressable", "accessibility", "hitslop", "touch-targets", "screen-reader"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""How do you build an accessible, easy-to-tap button in React Native? Explain `Pressable` (pressed state, `hitSlop`), the accessibility props, and touch target sizes.""",
        q_bn=r"""React Native-এ accessible আর সহজে tap করা যায় এমন button কীভাবে বানাবে? `Pressable` (pressed state, `hitSlop`), accessibility prop আর touch target-এর আকার ব্যাখ্যা করো।""",
        a_en=r"""
            I use `Pressable` (the more flexible successor to the `Touchable*` components). It gives `onPress`, `onLongPress`, `onPressIn`/`onPressOut`, and a `style` or `children` function that receives `{ pressed }`, so I can show feedback without extra state. `android_ripple` adds the native ripple on Android.

            **Touch size:** Apple recommends at least 44×44 pt and Material at least 48×48 dp. If the icon is visually smaller, I keep its look and grow only the touchable area with `hitSlop` (for example, a 24 pt icon with `hitSlop={10}` reaches 44).

            **Screen readers:** `accessibilityRole="button"` (or the newer `role` prop) so VoiceOver/TalkBack announce it as a button; `accessibilityLabel` for icon-only buttons ("Delete order 1042"); `accessibilityHint` for a non-obvious result; `accessibilityState={{ disabled, busy }}` so the state is announced too.
        """,
        a_bn=r"""
            আমি `Pressable` ব্যবহার করি (এটা `Touchable*` component-গুলোর চেয়ে বেশি flexible উত্তরসূরি)। এতে আছে `onPress`, `onLongPress`, `onPressIn`/`onPressOut`, আর একটা `style` বা `children` function যেটা `{ pressed }` পায়, তাই বাড়তি state ছাড়াই feedback দেখানো যায়। `android_ripple` দিয়ে Android-এ native ripple পাওয়া যায়।

            **Touch-এর আকার:** Apple অন্তত 44×44 pt আর Material অন্তত 48×48 dp recommend করে। Icon দেখতে ছোট হলে আমি তার চেহারা একই রেখে শুধু touch করার জায়গা `hitSlop` দিয়ে বাড়াই (যেমন 24 pt icon-এ `hitSlop={10}` দিলে 44 হয়ে যায়)।

            **Screen reader:** `accessibilityRole="button"` (বা নতুন `role` prop), যাতে VoiceOver/TalkBack এটাকে button হিসেবে পড়ে; শুধু icon থাকা button-এ `accessibilityLabel` ("Delete order 1042"); ফলাফল স্পষ্ট না হলে `accessibilityHint`; আর `accessibilityState={{ disabled, busy }}`, যাতে state-ও পড়ে শোনানো হয়।
        """,
        quick_en=r"""Use `Pressable` with its `{ pressed }` style for feedback, keep targets at least 44 pt (iOS) / 48 dp (Android) using `hitSlop` for small icons, and add `accessibilityRole`, `accessibilityLabel` and `accessibilityState` so screen readers announce it correctly.""",
        quick_bn=r"""Feedback-এর জন্য `Pressable` আর তার `{ pressed }` style ব্যবহার করো, ছোট icon-এ `hitSlop` দিয়ে target অন্তত 44 pt (iOS) / 48 dp (Android) রাখো, আর `accessibilityRole`, `accessibilityLabel` ও `accessibilityState` দাও যাতে screen reader ঠিকভাবে পড়ে।""",
        ex_en=r"""
            - **`role` vs `accessibilityRole`:** both work; if you set both, `role` wins. `role` uses web-like names (`heading` instead of `header`).
            - **Labels default to the text children** of a touchable, so a text button often needs no label. An icon-only button always does.
            - **`link` vs `button`:** use `link` only for something that opens a URL; in-app navigation is a `button`.
            - **`pressRetentionOffset`** controls how far the finger can drift before the press is cancelled; `delayLongPress` defaults to 500 ms.
            - **Dynamic font size:** `Text` scales with the user's system font setting. Don't disable it; design layouts that grow, and cap extreme sizes with `maxFontSizeMultiplier` only where a layout truly breaks.
            - **Test it:** turn on VoiceOver/TalkBack and swipe through the screen once; it catches most problems quickly.
        """,
        ex_bn=r"""
            - **`role` বনাম `accessibilityRole`:** দুটোই কাজ করে; দুটো দিলে `role` জেতে। `role` web-এর মতো নাম ব্যবহার করে (`header`-এর বদলে `heading`)।
            - **Label default-ভাবে touchable-এর text children থেকে আসে**, তাই text থাকা button-এ প্রায়ই label লাগে না। কিন্তু শুধু icon থাকা button-এ সবসময় লাগে।
            - **`link` বনাম `button`:** `link` শুধু URL খোলার জন্য; app-এর ভেতরে navigation হলো `button`।
            - **`pressRetentionOffset`** ঠিক করে আঙুল কতদূর সরে গেলে press বাতিল হবে; `delayLongPress`-এর default 500 ms।
            - **Dynamic font size:** `Text` user-এর system font setting অনুযায়ী বড়-ছোট হয়। এটা বন্ধ করো না; এমন layout বানাও যেটা বাড়তে পারে, আর শুধু যেখানে layout সত্যিই ভেঙে যায় সেখানে `maxFontSizeMultiplier` দিয়ে সীমা দাও।
            - **Test করো:** VoiceOver/TalkBack চালু করে একবার পুরো screen swipe করে দেখো; বেশিরভাগ সমস্যা দ্রুত ধরা পড়ে।
        """,
        tip_en=r"""Show one icon button with `hitSlop`, a role, a label and a disabled state. Mentioning that you actually test with VoiceOver/TalkBack sets you apart.""",
        tip_bn=r"""`hitSlop`, role, label আর disabled state-সহ একটা icon button দেখাও। তুমি যে আসলেই VoiceOver/TalkBack দিয়ে test করো, এটা বললে তুমি অন্যদের থেকে আলাদা হয়ে যাবে।""",
        mist_en=r"""Leaving icon-only buttons without an `accessibilityLabel` (the screen reader just says "button"), and making a small icon bigger with padding that pushes the layout around instead of using `hitSlop`.""",
        mist_bn=r"""শুধু icon থাকা button-এ `accessibilityLabel` না দেওয়া (screen reader তখন শুধু "button" বলে), আর `hitSlop`-এর বদলে padding দিয়ে ছোট icon বড় করা, যাতে পুরো layout সরে যায়।""",
        code=r"""
            import { Pressable, StyleSheet } from 'react-native';
            import { Ionicons } from '@expo/vector-icons';

            export function DeleteButton({ orderId, onDelete, isDeleting }: {
              orderId: string; onDelete: () => void; isDeleting: boolean;
            }) {
              return (
                <Pressable
                  onPress={onDelete}
                  disabled={isDeleting}
                  hitSlop={10} // 24 pt icon + 10 on each side = 44 pt target
                  accessibilityRole="button"
                  accessibilityLabel={`Delete order ${orderId}`}
                  accessibilityHint="Removes this order from your cart"
                  accessibilityState={{ disabled: isDeleting, busy: isDeleting }}
                  android_ripple={{ color: '#ddd', borderless: true }}
                  style={({ pressed }) => pressed && styles.pressed}
                >
                  <Ionicons name="trash-outline" size={24} />
                </Pressable>
              );
            }

            const styles = StyleSheet.create({
              pressed: { opacity: 0.5 },
            });
        """,
        lang="tsx",
        follow=[
            ("How would you announce 'Order placed' to a screen-reader user after a submit?", "Submit-এর পর screen-reader user-কে 'Order placed' কীভাবে শোনাবে?"),
            ("How do you make a custom checkbox accessible?", "একটা custom checkbox কীভাবে accessible করবে?"),
        ],
        related=["rn-015", "react-011"],
        refs=[R_PRESSABLE, R_A11Y],
    ),
]

save("reactnative", "b1", QUESTIONS)
