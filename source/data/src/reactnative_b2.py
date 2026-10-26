# React Native (with Expo) — batch 2 (rn-009..016)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R_FLATLIST = ("React Native — FlatList", "https://reactnative.dev/docs/flatlist")
R_SECTIONLIST = ("React Native — SectionList", "https://reactnative.dev/docs/sectionlist")
R_SCROLLVIEW = ("React Native — ScrollView", "https://reactnative.dev/docs/scrollview")
R_OPT_FLATLIST = ("React Native — Optimizing FlatList Configuration", "https://reactnative.dev/docs/optimizing-flatlist-configuration")
R_FLASHLIST = ("FlashList (GitHub, Shopify)", "https://github.com/Shopify/flash-list")
R_SAFEAREAVIEW = ("React Native — SafeAreaView (deprecated)", "https://reactnative.dev/docs/safeareaview")
R_EXPO_SAFE = ("Expo — Safe areas", "https://docs.expo.dev/develop/user-interface/safe-areas/")
R_ANDROID15 = ("Android 15 — Behavior changes (edge-to-edge enforcement)", "https://developer.android.com/about/versions/15/behavior-changes-15")
R_KAV = ("React Native — KeyboardAvoidingView", "https://reactnative.dev/docs/keyboardavoidingview")
R_EXPO_KEYBOARD = ("Expo — Keyboard handling", "https://docs.expo.dev/guides/keyboard-handling/")
R_USEWINDOW = ("React Native — useWindowDimensions", "https://reactnative.dev/docs/usewindowdimensions")
R_DIMENSIONS = ("React Native — Dimensions", "https://reactnative.dev/docs/dimensions")
R_EXPO_IMAGE = ("Expo — Image (expo-image)", "https://docs.expo.dev/versions/latest/sdk/image/")
R_EXPO_VIDEO = ("Expo — Video (expo-video)", "https://docs.expo.dev/versions/latest/sdk/video/")
R_EXPO_AUDIO = ("Expo — Audio (expo-audio)", "https://docs.expo.dev/versions/latest/sdk/audio/")
R_TEXTINPUT = ("React Native — TextInput", "https://reactnative.dev/docs/textinput")
R_REACT_MEMO = ("react.dev — memo", "https://react.dev/reference/react/memo")

VER = "React Native 0.88, Expo SDK 58"

QUESTIONS = [
    # ------------------------------------------------------------------ rn-009
    Q(
        id="rn-009", sub="Lists", diff="easy", type="comparison",
        prio="high", market="both", mins=3,
        tags=["scrollview", "flatlist", "sectionlist", "virtualization"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""Compare `ScrollView` + `.map()`, `FlatList` and `SectionList`. When would you use each?""",
        q_bn=r"""`ScrollView` + `.map()`, `FlatList` আর `SectionList`-এর তুলনা করো। কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **`ScrollView` + `.map()`** renders **every** child at once, even off-screen ones. That's fine for short, bounded content: a settings page, a form, a product detail screen.
            - **`FlatList`** is virtualised: it renders only the rows near the viewport and unmounts far-away ones, so memory and startup stay flat as data grows. It also gives `keyExtractor`, `onEndReached` (infinite scroll), `refreshing`/`onRefresh` (pull to refresh), `ListEmptyComponent`, `ItemSeparatorComponent`, `numColumns` and horizontal mode.
            - **`SectionList`** is the same virtualised list for grouped data (`sections: [{ title, data }]`) with section headers, for example orders grouped by date or contacts by letter.

            My rule: if the data comes from an API or can grow, it's a `FlatList`/`SectionList` (or FlashList for very large or complex feeds), never a `ScrollView`.
        """,
        a_bn=r"""
            - **`ScrollView` + `.map()`** **সব** child একসাথে render করে, screen-এর বাইরে থাকাগুলোও। ছোট আর সীমিত content-এর জন্য এটা ঠিক আছে: settings page, form, product detail screen।
            - **`FlatList`** virtualised: viewport-এর কাছের row-গুলোই শুধু render করে আর দূরেরগুলো unmount করে, তাই data বাড়লেও memory আর startup প্রায় একই থাকে। সাথে পাওয়া যায় `keyExtractor`, `onEndReached` (infinite scroll), `refreshing`/`onRefresh` (pull to refresh), `ListEmptyComponent`, `ItemSeparatorComponent`, `numColumns` আর horizontal mode।
            - **`SectionList`** হলো grouped data-র জন্য একই virtualised list (`sections: [{ title, data }]`), section header-সহ, যেমন তারিখ অনুযায়ী order বা অক্ষর অনুযায়ী contact।

            আমার নিয়ম: data যদি API থেকে আসে বা বাড়তে পারে, তাহলে `FlatList`/`SectionList` (খুব বড় বা জটিল feed-এ FlashList), কখনোই `ScrollView` না।
        """,
        quick_en=r"""`ScrollView` renders all children at once, so it suits short, fixed content. `FlatList` virtualises rows (only those near the screen are mounted) for long or growing data, and `SectionList` does the same for grouped data with section headers.""",
        quick_bn=r"""`ScrollView` সব child একসাথে render করে, তাই ছোট আর নির্দিষ্ট content-এর জন্য ঠিক। লম্বা বা বাড়তে থাকা data-র জন্য `FlatList` row virtualise করে (শুধু screen-এর কাছেরগুলো mount থাকে), আর grouped data-র জন্য section header-সহ একই কাজ করে `SectionList`।""",
        ex_en=r"""
            - **Why `ScrollView` hurts at scale:** 1,000 rows means 1,000 mounted component trees and native views, so the first render is slow and memory keeps climbing, especially with images.
            - **Virtualisation has a cost:** rows far off-screen are unmounted, so their local state is lost when you scroll back. Keep important row state (selected, expanded) in the parent or a store, keyed by id.
            - **Don't nest a `FlatList` inside a `ScrollView` of the same direction;** React Native warns about it and virtualisation stops working. Put the content above the list in `ListHeaderComponent` instead.
            - **`FlatList` is a `PureComponent`:** if `renderItem` depends on something outside `data` (a selected id), pass it through `extraData`, or rows won't update.
            - `SectionList` headers are sticky by default on iOS (`stickySectionHeadersEnabled`).
        """,
        ex_bn=r"""
            - **Scale-এ `ScrollView` কেন সমস্যা:** 1,000 row মানে 1,000টা mount করা component tree আর native view, তাই প্রথম render ধীর হয় আর memory বাড়তেই থাকে, বিশেষ করে image থাকলে।
            - **Virtualisation-এরও দাম আছে:** screen থেকে অনেক দূরের row unmount হয়, তাই scroll করে ফিরে এলে তাদের local state হারিয়ে যায়। গুরুত্বপূর্ণ row state (selected, expanded) parent বা store-এ id দিয়ে রাখো।
            - **একই direction-এর `ScrollView`-এর ভেতরে `FlatList` রেখো না;** React Native warning দেয় আর virtualisation কাজ করা বন্ধ করে দেয়। List-এর উপরের content `ListHeaderComponent`-এ রাখো।
            - **`FlatList` একটা `PureComponent`:** `renderItem` যদি `data`-এর বাইরের কিছুর (যেমন selected id) উপর নির্ভর করে, সেটা `extraData` দিয়ে পাঠাও, নইলে row update হবে না।
            - iOS-এ `SectionList`-এর header default-ভাবে sticky থাকে (`stickySectionHeadersEnabled`)।
        """,
        tip_en=r"""Lead with the key word "virtualisation" and the rule for choosing. Then mention one gotcha (nested lists or `extraData`) to show you've shipped real lists.""",
        tip_bn=r"""শুরুতেই মূল শব্দ "virtualisation" আর বেছে নেওয়ার নিয়মটা বলো। তারপর একটা gotcha (nested list বা `extraData`) বলো, যাতে বোঝা যায় তুমি সত্যিকারের list ship করেছ।""",
        mist_en=r"""Wrapping a `FlatList` in a `ScrollView` to add a header above it, which disables virtualisation and triggers the "VirtualizedLists should never be nested" warning.""",
        mist_bn=r"""List-এর উপরে header বসাতে `FlatList`-কে একটা `ScrollView` দিয়ে মোড়ানো, এতে virtualisation বন্ধ হয়ে যায় আর "VirtualizedLists should never be nested" warning আসে।""",
        code=r"""
            import { SectionList, Text, View } from 'react-native';

            type Order = { id: string; total: number };
            const sections = [
              { title: 'Today', data: [{ id: 'o-3', total: 1200 }] },
              { title: 'Yesterday', data: [{ id: 'o-2', total: 450 }, { id: 'o-1', total: 980 }] },
            ];

            export function OrderHistory() {
              return (
                <SectionList<Order, { title: string }>
                  sections={sections}
                  keyExtractor={(item) => item.id}
                  renderSectionHeader={({ section }) => <Text style={{ fontWeight: '700' }}>{section.title}</Text>}
                  renderItem={({ item }) => (
                    <View style={{ paddingVertical: 12 }}>
                      <Text>Order {item.id}: ৳{item.total}</Text>
                    </View>
                  )}
                  ListEmptyComponent={<Text>No orders yet</Text>}
                />
              );
            }
        """,
        lang="tsx",
        follow=[
            ("How do you add a header and pull-to-refresh to a `FlatList` without wrapping it in a `ScrollView`?", "`ScrollView` দিয়ে না মুড়িয়ে `FlatList`-এ header আর pull-to-refresh কীভাবে যোগ করবে?"),
            ("Why might a row lose its local state after you scroll far away and back?", "অনেক দূরে scroll করে ফিরে এলে একটা row কেন তার local state হারাতে পারে?"),
        ],
        related=["rn-010", "rn-016", "react-029"],
        refs=[R_FLATLIST, R_SECTIONLIST, R_SCROLLVIEW],
    ),
    # ------------------------------------------------------------------ rn-010
    Q(
        id="rn-010", sub="Lists", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["flatlist", "keys", "keyextractor", "pagination"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""In this chat screen, new messages are added to the **start** of `messages`. Users report two bugs: (1) when a new message arrives, the "show translation" panel a user opened jumps to the neighbouring message; (2) after loading older messages, the console warns "Encountered two children with the same key" and a message appears twice. Find the root causes and fix them.""",
        q_bn=r"""এই chat screen-এ নতুন message `messages`-এর **শুরুতে** যোগ হয়। User-রা দুটো bug report করেছে: (১) নতুন message এলে user যে message-এর "show translation" panel খুলেছিল, সেটা পাশের message-এ চলে যায়; (২) পুরনো message load করার পর console-এ "Encountered two children with the same key" warning আসে আর একটা message দুইবার দেখায়। Root cause খুঁজে বের করো আর ঠিক করো।""",
        code=r"""
            type Message = { messageId: string; text: string; sentAt: string };

            function MessageRow({ message }: { message: Message }) {
              const [showTranslation, setShowTranslation] = useState(false);
              // ... renders text + a "Translate" toggle
            }

            export function ChatScreen() {
              const [messages, setMessages] = useState<Message[]>([]);

              useChatSocket((msg) => setMessages((prev) => [msg, ...prev]));

              async function loadOlder() {
                const page = await api.getMessages({ before: messages.at(-1)?.sentAt });
                setMessages((prev) => [...prev, ...page]); // the API may return overlapping rows
              }

              return (
                <FlatList
                  data={messages}
                  keyExtractor={(_, index) => String(index)}
                  renderItem={({ item }) => <MessageRow message={item} />}
                  onEndReached={loadOlder}
                />
              );
            }
        """,
        lang="tsx",
        a_en=r"""
            **Bug 1: index keys.** The key is the row's position, not its identity. When a message is prepended, every message shifts one index down, but React keeps each component's state by key. So the `MessageRow` with key `"0"` (which had `showTranslation: true`) is now rendering a different message, and the open panel "jumps".

            **Fix:** use the stable id: `keyExtractor={(item) => item.messageId}`.

            **Bug 2: duplicate data.** Once keys are real ids, the overlapping page shows up as duplicate keys, which is exactly the warning. The list isn't wrong; the data is. Merge pages by id (a `Map`) instead of blindly concatenating, then sort.

            Also guard `onEndReached`, which can fire more than once while a request is in flight.
        """,
        a_bn=r"""
            **Bug 1: index key।** Key এখানে row-এর অবস্থান, তার পরিচয় না। নতুন message শুরুতে যোগ হলে প্রতিটা message এক index নিচে সরে যায়, কিন্তু React প্রতিটা component-এর state key অনুযায়ী রাখে। ফলে key `"0"`-এর `MessageRow` (যেটার `showTranslation: true` ছিল) এখন অন্য একটা message দেখাচ্ছে, আর খোলা panel "লাফিয়ে" যায়।

            **Fix:** stable id ব্যবহার করো: `keyExtractor={(item) => item.messageId}`।

            **Bug 2: duplicate data।** Key আসল id হওয়ার পর overlap করা page duplicate key হিসেবে ধরা পড়ে, warning-টা ঠিক এটাই। List-এর দোষ না, দোষ data-র। অন্ধভাবে জোড়া না লাগিয়ে page-গুলো id দিয়ে (`Map`) merge করো, তারপর sort করো।

            সাথে `onEndReached`-এ guard দাও, কারণ request চলার সময় এটা একাধিকবার fire করতে পারে।
        """,
        quick_en=r"""Index keys tie row state to a position, so prepending a message moves the open translation panel to another message; use `keyExtractor={(item) => item.messageId}`. The duplicate-key warning means the data really has duplicates, so merge pages by id instead of concatenating.""",
        quick_bn=r"""Index key row-এর state-কে অবস্থানের সাথে বেঁধে দেয়, তাই শুরুতে message যোগ হলে খোলা translation panel অন্য message-এ চলে যায়; `keyExtractor={(item) => item.messageId}` ব্যবহার করো। Duplicate-key warning মানে data-তে সত্যিই duplicate আছে, তাই জোড়া না লাগিয়ে page-গুলো id দিয়ে merge করো।""",
        ex_en=r"""
            - **Default `keyExtractor`:** `FlatList` checks `item.key`, then `item.id`, then falls back to the index. Our items use `messageId`, so even deleting the custom extractor would leave index keys. Always set it explicitly when the id field has another name.
            - **Keys must be strings** and unique within the list; don't use `Math.random()` or `Date.now()`, which change every render and remount every row.
            - **Why index keys "work" in demos:** if you only ever append and never reorder, positions don't change. Chat, feeds with "new posts" and sorting all break that assumption.
            - **Duplicate keys are a data bug:** fix them where the data is merged (or with a primary key in SQLite), not by adding the index to the key, which only hides the duplicate row.
            - The merge below keeps the newest version of each message and sorts newest first; verified with Node: merging `[m3, m2]` with `[m2, m1]` gives `['m3', 'm2', 'm1']`.
        """,
        ex_bn=r"""
            - **Default `keyExtractor`:** `FlatList` আগে `item.key`, তারপর `item.id` দেখে, না পেলে index ব্যবহার করে। আমাদের item-এ আছে `messageId`, তাই custom extractor মুছে দিলেও index key-ই থেকে যেত। Id field-এর নাম অন্য কিছু হলে সবসময় স্পষ্টভাবে extractor দাও।
            - **Key string হতে হবে** আর list-এর মধ্যে unique; `Math.random()` বা `Date.now()` ব্যবহার করো না, এগুলো প্রতি render-এ বদলায় আর প্রতিটা row আবার mount করে।
            - **Demo-তে index key কেন "চলে":** শুধু শেষে append করলে আর কখনো reorder না করলে অবস্থান বদলায় না। Chat, "new posts" থাকা feed আর sorting এই ধারণা ভেঙে দেয়।
            - **Duplicate key আসলে data-র bug:** data যেখানে merge হয় সেখানে (বা SQLite-এ primary key দিয়ে) ঠিক করো; key-তে index জুড়ে দিলে শুধু duplicate row-টা লুকানো হয়।
            - নিচের merge প্রতিটা message-এর সবচেয়ে নতুন version রাখে আর newest first sort করে; Node দিয়ে যাচাই করা: `[m3, m2]`-এর সাথে `[m2, m1]` merge করলে পাওয়া যায় `['m3', 'm2', 'm1']`।
        """,
        tip_en=r"""Explain bug 1 with the phrase "React keeps state by key, not by data". Then say the duplicate warning is the list telling you the truth about your data; that shows mature debugging.""",
        tip_bn=r"""Bug 1 ব্যাখ্যা করো এই কথা দিয়ে: "React state রাখে key অনুযায়ী, data অনুযায়ী না"। তারপর বলো duplicate warning আসলে list-এর মাধ্যমে data-র সত্যিটা জানিয়ে দিচ্ছে; এতে পরিণত debugging-এর পরিচয় পাওয়া যায়।""",
        mist_en=r"""Silencing the duplicate-key warning with ``keyExtractor={(item, i) => `${item.messageId}-${i}`}``. The warning disappears, but the user still sees the same message twice.""",
        mist_bn=r"""``keyExtractor={(item, i) => `${item.messageId}-${i}`}`` দিয়ে duplicate-key warning চুপ করিয়ে দেওয়া। Warning চলে যায়, কিন্তু user তখনও একই message দুইবার দেখে।""",
        extra=[
            dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                function mergeById(prev: Message[], incoming: Message[]): Message[] {
                  const byId = new Map(prev.map((m) => [m.messageId, m]));
                  for (const m of incoming) byId.set(m.messageId, m);
                  return [...byId.values()].sort((a, b) => b.sentAt.localeCompare(a.sentAt));
                }

                export function ChatScreen() {
                  const [messages, setMessages] = useState<Message[]>([]);
                  const loadingRef = useRef(false);

                  useChatSocket((msg) => setMessages((prev) => mergeById(prev, [msg])));

                  async function loadOlder() {
                    if (loadingRef.current) return; // onEndReached can fire repeatedly
                    loadingRef.current = true;
                    try {
                      const page = await api.getMessages({ before: messages.at(-1)?.sentAt });
                      setMessages((prev) => mergeById(prev, page));
                    } finally {
                      loadingRef.current = false;
                    }
                  }

                  return (
                    <FlatList
                      data={messages}
                      keyExtractor={(item) => item.messageId}
                      renderItem={({ item }) => <MessageRow message={item} />}
                      onEndReached={loadOlder}
                      onEndReachedThreshold={0.5}
                    />
                  );
                }
            """),
        ],
        follow=[
            ("What does the default `keyExtractor` use if you don't pass one?", "`keyExtractor` না দিলে default-ভাবে কী ব্যবহার হয়?"),
            ("Where should `showTranslation` live if it must survive scrolling far away?", "অনেক দূরে scroll করার পরও `showTranslation` টিকিয়ে রাখতে হলে এটা কোথায় রাখা উচিত?"),
        ],
        related=["rn-009", "react-004", "react-021"],
        refs=[R_FLATLIST, R_OPT_FLATLIST],
    ),
    # ------------------------------------------------------------------ rn-011
    Q(
        id="rn-011", sub="Layout & Safe Areas", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["safe-area", "edge-to-edge", "android-15", "notch", "status-bar"],
        ver=VER, vs=True, status="stable",
        q_en=r"""After raising `targetSdkVersion` to 35, QA reports that on Android 15 phones the custom header of this screen is drawn under the status bar and camera cutout, and the bottom button sits behind the gesture bar. On iPhone it looks fine. Why, and how do you fix it?""",
        q_bn=r"""`targetSdkVersion` 35-এ তোলার পর QA জানাল, Android 15 phone-এ এই screen-এর custom header status bar আর camera cutout-এর নিচে আঁকা হচ্ছে, আর নিচের button gesture bar-এর পেছনে চলে যাচ্ছে। iPhone-এ সব ঠিক দেখায়। কেন, আর কীভাবে ঠিক করবে?""",
        code=r"""
            import { SafeAreaView, View, Text, Pressable, StyleSheet } from 'react-native';

            export default function CartScreen() {
              return (
                <SafeAreaView style={styles.container}>
                  <View style={styles.header}>
                    <Text style={styles.title}>Your cart</Text>
                  </View>
                  {/* ...cart items... */}
                  <Pressable style={styles.checkout}>
                    <Text>Checkout</Text>
                  </Pressable>
                </SafeAreaView>
              );
            }

            const styles = StyleSheet.create({
              container: { flex: 1 },
              header: { height: 56, justifyContent: 'center', paddingHorizontal: 16 },
              title: { fontSize: 20, fontWeight: '700' },
              checkout: { marginTop: 'auto', padding: 16 },
            });
        """,
        lang="tsx",
        a_en=r"""
            Two things combine here:

            1. **Android 15 enforces edge-to-edge** for apps targeting API 35+: the app now draws behind the status bar and navigation/gesture bar, and it's the app's job to pad content away from them. React Native itself fully supports edge-to-edge on Android 15+.
            2. **`SafeAreaView` from `react-native` only ever worked on iOS**, so on Android it adds no padding at all. It is also deprecated since React Native 0.81.

            **Fix:** use `react-native-safe-area-context`. Either its `SafeAreaView` with `edges` (padding only where you want it), or `useSafeAreaInsets()` when you need the numbers, for example `paddingTop: insets.top` on a custom header and `paddingBottom: insets.bottom` under the button. The hooks need a `SafeAreaProvider` at the app root; Expo Router adds it for you, so only apps without Expo Router wrap the root themselves.

            If the screen uses the navigator's own header, don't add the top inset again: the header already handles it.
        """,
        a_bn=r"""
            এখানে দুটো জিনিস একসাথে ঘটছে:

            1. **Android 15, API 35+ target করা app-এ edge-to-edge বাধ্যতামূলক করে**: app এখন status bar আর navigation/gesture bar-এর পেছনেও আঁকে, আর content-কে ওগুলো থেকে সরিয়ে রাখার দায়িত্ব app-এর। React Native নিজে Android 15+-এ edge-to-edge পুরোপুরি support করে।
            2. **`react-native`-এর `SafeAreaView` সবসময় শুধু iOS-এ কাজ করত**, তাই Android-এ এটা কোনো padding-ই যোগ করে না। তাছাড়া React Native 0.81 থেকে এটা deprecated।

            **Fix:** `react-native-safe-area-context` ব্যবহার করো। হয় এর `SafeAreaView`, `edges` দিয়ে (যেদিকে চাও শুধু সেদিকে padding), নয়তো সংখ্যাগুলো দরকার হলে `useSafeAreaInsets()`, যেমন custom header-এ `paddingTop: insets.top` আর button-এর নিচে `paddingBottom: insets.bottom`। এগুলোর জন্য app-এর root-এ একটা `SafeAreaProvider` লাগে; Expo Router নিজেই সেটা যোগ করে দেয়, তাই শুধু Expo Router ছাড়া app-এ root নিজে wrap করতে হয়।

            Screen যদি navigator-এর নিজের header ব্যবহার করে, তাহলে top inset আবার যোগ করো না: header নিজেই সেটা সামলায়।
        """,
        quick_en=r"""Android 15 forces edge-to-edge for apps targeting API 35, and `SafeAreaView` from `react-native` only pads on iOS (and is deprecated). Use `SafeAreaView` or `useSafeAreaInsets` from `react-native-safe-area-context` to pad the header and the bottom button.""",
        quick_bn=r"""API 35 target করা app-এ Android 15 edge-to-edge বাধ্যতামূলক করে, আর `react-native`-এর `SafeAreaView` শুধু iOS-এ padding দেয় (এবং deprecated)। Header আর নিচের button-এ padding দিতে `react-native-safe-area-context`-এর `SafeAreaView` বা `useSafeAreaInsets` ব্যবহার করো।""",
        ex_en=r"""
            - **Why it looked fine on iPhone:** the core `SafeAreaView` did pad on iOS, so the bug only showed on Android once edge-to-edge became mandatory.
            - **`edges` matters:** a screen inside a tab navigator usually wants `edges={['top']}` because the tab bar already handles the bottom; padding both doubles the gap.
            - **Insets change at runtime:** rotation, split screen and the keyboard can change them. The hook re-renders with new values, which a hard-coded `StatusBar.currentHeight` or a fixed `paddingTop: 24` can't do (and those ignore cutouts and the bottom bar).
            - **Status bar icons:** with content drawn behind the status bar, set the icon color with `expo-status-bar` (`<StatusBar style="dark" />`) so icons stay readable.
            - **Test** on an Android 15+ device or emulator with gesture navigation and a cutout, and in landscape.
        """,
        ex_bn=r"""
            - **iPhone-এ কেন ঠিক দেখাচ্ছিল:** core `SafeAreaView` iOS-এ padding দিত, তাই edge-to-edge বাধ্যতামূলক হওয়ার পর bug-টা শুধু Android-এ ধরা পড়ল।
            - **`edges` গুরুত্বপূর্ণ:** tab navigator-এর ভেতরের screen-এ সাধারণত `edges={['top']}` দরকার, কারণ নিচের দিকটা tab bar নিজেই সামলায়; দুই জায়গাতেই padding দিলে ফাঁক দ্বিগুণ হয়ে যায়।
            - **Inset runtime-এ বদলায়:** rotation, split screen আর keyboard এগুলো বদলাতে পারে। Hook নতুন value নিয়ে re-render করে, যা hard-coded `StatusBar.currentHeight` বা fixed `paddingTop: 24` পারে না (আর ওগুলো cutout ও নিচের bar-কে হিসাবেই ধরে না)।
            - **Status bar icon:** content যখন status bar-এর পেছনে আঁকা হয়, তখন `expo-status-bar` দিয়ে icon-এর রং ঠিক করো (`<StatusBar style="dark" />`), যাতে icon পড়া যায়।
            - **Test করো** gesture navigation আর cutout থাকা Android 15+ device বা emulator-এ, landscape-এও।
        """,
        tip_en=r"""Name both causes (Android 15 edge-to-edge + core `SafeAreaView` is iOS-only and deprecated) before the fix. Interviewers want to hear that you know why it only broke on Android.""",
        tip_bn=r"""Fix বলার আগে দুটো কারণই বলো (Android 15 edge-to-edge + core `SafeAreaView` শুধু iOS-এর আর deprecated)। Interviewer শুনতে চায় যে তুমি জানো কেন এটা শুধু Android-এ ভাঙল।""",
        mist_en=r"""Patching it with `paddingTop: StatusBar.currentHeight` or a magic number. It ignores cutouts, the bottom gesture bar and rotation, and breaks again on the next device.""",
        mist_bn=r"""`paddingTop: StatusBar.currentHeight` বা কোনো magic number দিয়ে জোড়াতালি দেওয়া। এটা cutout, নিচের gesture bar আর rotation হিসাবে ধরে না, আর পরের device-এ আবার ভাঙে।""",
        extra=[
            dict(lang="tsx", label_en="Fixed version (react-native-safe-area-context)", label_bn="সংশোধিত version (react-native-safe-area-context)", src=r"""
                import { View, Text, Pressable, StyleSheet } from 'react-native';
                import { useSafeAreaInsets } from 'react-native-safe-area-context';

                export default function CartScreen() {
                  const insets = useSafeAreaInsets(); // { top, right, bottom, left }

                  return (
                    <View style={[styles.container, { paddingLeft: insets.left, paddingRight: insets.right }]}>
                      <View style={[styles.header, { paddingTop: insets.top, height: 56 + insets.top }]}>
                        <Text style={styles.title}>Your cart</Text>
                      </View>
                      {/* ...cart items... */}
                      <Pressable style={[styles.checkout, { paddingBottom: 16 + insets.bottom }]}>
                        <Text>Checkout</Text>
                      </Pressable>
                    </View>
                  );
                }

                // Simpler alternative when no custom header math is needed:
                // import { SafeAreaView } from 'react-native-safe-area-context';
                // <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>...</SafeAreaView>

                const styles = StyleSheet.create({
                  container: { flex: 1 },
                  header: { justifyContent: 'center', paddingHorizontal: 16 },
                  title: { fontSize: 20, fontWeight: '700' },
                  checkout: { marginTop: 'auto', padding: 16 },
                });
            """),
        ],
        follow=[
            ("When would you pass `edges={['top']}` instead of all edges?", "কখন সব edge-এর বদলে `edges={['top']}` দেবে?"),
            ("How do you keep the status bar icons readable on a dark header?", "Dark header-এ status bar icon কীভাবে পড়ার মতো রাখবে?"),
        ],
        related=["rn-013", "rn-012"],
        refs=[R_EXPO_SAFE, R_SAFEAREAVIEW, R_ANDROID15],
    ),
    # ------------------------------------------------------------------ rn-012
    Q(
        id="rn-012", sub="Forms & Keyboard", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["keyboard", "keyboardavoidingview", "scrollview", "forms"],
        ver=VER, vs=False, status="stable",
        q_en=r"""On this checkout screen (inside a stack with a header), two bugs are reported on iPhone: the keyboard covers the phone-number field, and when the keyboard is open, the first tap on "Place order" only closes the keyboard; the user has to tap again. Explain both and fix them.""",
        q_bn=r"""এই checkout screen-এ (header-সহ একটা stack-এর ভেতরে) iPhone-এ দুটো bug report হয়েছে: keyboard phone-number field ঢেকে দেয়, আর keyboard খোলা থাকলে "Place order"-এ প্রথম tap শুধু keyboard বন্ধ করে; user-কে আবার tap করতে হয়। দুটোই ব্যাখ্যা করো আর ঠিক করো।""",
        code=r"""
            export default function CheckoutScreen() {
              const [address, setAddress] = useState('');
              const [phone, setPhone] = useState('');

              return (
                <ScrollView contentContainerStyle={styles.content}>
                  <OrderSummary />
                  <TextInput value={address} onChangeText={setAddress} placeholder="Delivery address" style={styles.input} />
                  <TextInput value={phone} onChangeText={setPhone} placeholder="Phone" keyboardType="phone-pad" style={styles.input} />
                  <Pressable onPress={placeOrder} style={styles.button}>
                    <Text>Place order</Text>
                  </Pressable>
                </ScrollView>
              );
            }
        """,
        lang="tsx",
        a_en=r"""
            **Bug 1: nothing makes room for the keyboard.** On iOS the keyboard simply slides over the window; the layout doesn't shrink. Wrap the screen in `KeyboardAvoidingView` with `behavior="padding"` on iOS, `style={{ flex: 1 }}`, and `keyboardVerticalOffset` equal to the header height (from `useHeaderHeight()`), because the view's top isn't at the top of the screen. Inside a `ScrollView`, the focused field can then be scrolled into view.

            **Bug 2: `keyboardShouldPersistTaps`.** Its default, `"never"`, means a tap outside the focused input while the keyboard is up just dismisses the keyboard and the child doesn't receive it. Set `keyboardShouldPersistTaps="handled"` so taps on buttons go through, while taps on empty space still dismiss.

            On Android, the window normally resizes for the keyboard, so many apps pass `behavior={Platform.OS === 'ios' ? 'padding' : undefined}`, which is also what the Expo guide shows. For complex forms I use `react-native-keyboard-controller`'s `KeyboardAwareScrollView` (development build needed).
        """,
        a_bn=r"""
            **Bug 1: keyboard-এর জন্য কেউ জায়গা ছাড়ছে না।** iOS-এ keyboard শুধু window-এর উপর দিয়ে উঠে আসে; layout ছোট হয় না। Screen-টাকে `KeyboardAvoidingView` দিয়ে মোড়াও, iOS-এ `behavior="padding"`, `style={{ flex: 1 }}`, আর `keyboardVerticalOffset` হিসেবে header-এর height (`useHeaderHeight()` থেকে), কারণ view-এর উপরের দিক screen-এর একদম উপরে না। তারপর `ScrollView`-এর ভেতরে focused field scroll করে দেখানো যায়।

            **Bug 2: `keyboardShouldPersistTaps`।** এর default `"never"`, মানে keyboard খোলা অবস্থায় focused input-এর বাইরে tap করলে শুধু keyboard বন্ধ হয়, child tap-টা পায় না। `keyboardShouldPersistTaps="handled"` দাও, তাহলে button-এ tap কাজ করবে, আর ফাঁকা জায়গায় tap করলে তখনও keyboard বন্ধ হবে।

            Android-এ সাধারণত keyboard-এর জন্য window নিজেই resize হয়, তাই অনেক app `behavior={Platform.OS === 'ios' ? 'padding' : undefined}` দেয়, Expo guide-ও এটাই দেখায়। জটিল form-এর জন্য আমি `react-native-keyboard-controller`-এর `KeyboardAwareScrollView` ব্যবহার করি (development build লাগে)।
        """,
        quick_en=r"""iOS doesn't shrink the layout for the keyboard, so wrap the screen in `KeyboardAvoidingView` with `behavior="padding"` and the header height as `keyboardVerticalOffset`. The double tap comes from `keyboardShouldPersistTaps="never"` (the default); set it to `"handled"` on the `ScrollView`.""",
        quick_bn=r"""iOS keyboard-এর জন্য layout ছোট করে না, তাই screen-টাকে `KeyboardAvoidingView` দিয়ে মোড়াও, `behavior="padding"` আর `keyboardVerticalOffset` হিসেবে header-এর height দিয়ে। দুইবার tap-এর কারণ `keyboardShouldPersistTaps="never"` (default); `ScrollView`-এ এটা `"handled"` করে দাও।""",
        ex_en=r"""
            - **Why the offset:** `KeyboardAvoidingView` measures from its own position. Under a navigation header it's 50–100 pt lower than the screen top, so without `keyboardVerticalOffset` the padding comes out too small and the last field stays hidden.
            - **`behavior` values:** `padding`, `height`, `position`. The docs recommend setting it on both platforms and experimenting; `padding` usually works best on iOS.
            - **`keyboardShouldPersistTaps` values:** `never` (default), `always` (keyboard never auto-dismisses; can feel stuck), `handled` (dismisses only when the tap wasn't handled by a child). It must be set on every ancestor `ScrollView`/list.
            - **Better form UX:** `returnKeyType="next"` + `onSubmitEditing` to focus the next field, `keyboardDismissMode="on-drag"` to close it while scrolling, and the right `keyboardType`.
            - **Tab bars:** on Android the keyboard can push a bottom tab bar up; the Expo guide suggests `softwareKeyboardLayoutMode: 'pan'` or `tabBarHideOnKeyboard: true`.
        """,
        ex_bn=r"""
            - **Offset কেন:** `KeyboardAvoidingView` নিজের অবস্থান থেকে মাপে। Navigation header-এর নিচে এটা screen-এর উপর থেকে 50–100 pt নিচে থাকে, তাই `keyboardVerticalOffset` না দিলে padding কম হয় আর শেষ field লুকিয়েই থাকে।
            - **`behavior`-এর value:** `padding`, `height`, `position`। Docs দুই platform-এই এটা set করতে আর পরীক্ষা করে দেখতে বলে; iOS-এ সাধারণত `padding` সবচেয়ে ভালো কাজ করে।
            - **`keyboardShouldPersistTaps`-এর value:** `never` (default), `always` (keyboard কখনো নিজে বন্ধ হয় না; আটকে আছে মনে হতে পারে), `handled` (tap কোনো child handle না করলে তবেই বন্ধ হয়)। এটা প্রতিটা ancestor `ScrollView`/list-এ দিতে হয়।
            - **Form-এর UX আরও ভালো করতে:** `returnKeyType="next"` + `onSubmitEditing` দিয়ে পরের field-এ focus, `keyboardDismissMode="on-drag"` দিয়ে scroll করলে keyboard বন্ধ, আর সঠিক `keyboardType`।
            - **Tab bar:** Android-এ keyboard নিচের tab bar-কে উপরে ঠেলে দিতে পারে; Expo guide `softwareKeyboardLayoutMode: 'pan'` বা `tabBarHideOnKeyboard: true` দিতে বলে।
        """,
        tip_en=r"""Treat them as two separate bugs with two separate props. Mentioning `keyboardVerticalOffset` under a header is the detail that shows you've debugged this on a real device.""",
        tip_bn=r"""এগুলোকে আলাদা দুটো bug হিসেবে ধরো, আলাদা দুটো prop দিয়ে। Header-এর নিচে `keyboardVerticalOffset`-এর কথা বললে বোঝা যায় তুমি আসল device-এ এটা debug করেছ।""",
        mist_en=r"""Putting `KeyboardAvoidingView` inside the `ScrollView` or forgetting `flex: 1` on it. It then has no fixed height to shrink and does nothing.""",
        mist_bn=r"""`KeyboardAvoidingView`-কে `ScrollView`-এর ভেতরে রাখা বা এতে `flex: 1` দিতে ভুলে যাওয়া। তখন এর ছোট হওয়ার মতো কোনো নির্দিষ্ট height থাকে না, ফলে এটা কিছুই করে না।""",
        extra=[
            dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                import { useRef, useState } from 'react';
                import { KeyboardAvoidingView, Platform, Pressable, ScrollView, Text, TextInput } from 'react-native';
                import { useHeaderHeight } from '@react-navigation/elements';

                export default function CheckoutScreen() {
                  const headerHeight = useHeaderHeight();
                  const phoneRef = useRef<TextInput>(null);
                  const [address, setAddress] = useState('');
                  const [phone, setPhone] = useState('');

                  return (
                    <KeyboardAvoidingView
                      style={{ flex: 1 }}
                      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
                      keyboardVerticalOffset={headerHeight}
                    >
                      <ScrollView
                        contentContainerStyle={styles.content}
                        keyboardShouldPersistTaps="handled"
                        keyboardDismissMode="on-drag"
                      >
                        <OrderSummary />
                        <TextInput
                          value={address}
                          onChangeText={setAddress}
                          placeholder="Delivery address"
                          returnKeyType="next"
                          onSubmitEditing={() => phoneRef.current?.focus()}
                          style={styles.input}
                        />
                        <TextInput
                          ref={phoneRef}
                          value={phone}
                          onChangeText={setPhone}
                          placeholder="Phone"
                          keyboardType="phone-pad"
                          style={styles.input}
                        />
                        <Pressable onPress={placeOrder} style={styles.button}>
                          <Text>Place order</Text>
                        </Pressable>
                      </ScrollView>
                    </KeyboardAvoidingView>
                  );
                }
            """),
        ],
        follow=[
            ("Why might the same `KeyboardAvoidingView` behave differently inside a modal?", "Modal-এর ভেতরে একই `KeyboardAvoidingView` কেন অন্যভাবে আচরণ করতে পারে?"),
            ("When would you reach for `react-native-keyboard-controller` instead?", "কখন এর বদলে `react-native-keyboard-controller` ব্যবহার করবে?"),
        ],
        related=["rn-015", "rn-011"],
        refs=[R_KAV, R_EXPO_KEYBOARD, R_SCROLLVIEW],
    ),
    # ------------------------------------------------------------------ rn-013
    Q(
        id="rn-013", sub="Responsive Layout", diff="medium", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["usewindowdimensions", "dimensions", "responsive", "rotation"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""A product grid uses the code below. The user rotates the tablet to landscape (or opens the app in split screen). What happens?""",
        q_bn=r"""একটা product grid নিচের code ব্যবহার করে। User tablet-টা landscape-এ ঘোরাল (বা split screen-এ app খুলল)। কী হবে?""",
        code=r"""
            import { Dimensions, FlatList, StyleSheet } from 'react-native';

            const { width } = Dimensions.get('window');
            const COLUMNS = width > 700 ? 3 : 2;

            const styles = StyleSheet.create({
              card: { width: width / COLUMNS, aspectRatio: 1 },
            });

            export function ProductGrid({ products }: { products: Product[] }) {
              return <FlatList data={products} numColumns={COLUMNS} renderItem={renderCard} />;
            }
        """,
        lang="tsx",
        options=[
            ("The grid recalculates automatically, because `Dimensions.get` always returns the current size", "Grid নিজে থেকেই আবার হিসাব হয়, কারণ `Dimensions.get` সবসময় বর্তমান size দেয়"),
            ("The app crashes, because `Dimensions` can't be read at module level", "App crash করে, কারণ module level-এ `Dimensions` পড়া যায় না"),
            ("The layout keeps the old width and column count; reading `useWindowDimensions()` inside the component fixes it", "Layout পুরনো width আর column সংখ্যাই রেখে দেয়; component-এর ভেতরে `useWindowDimensions()` পড়লে ঠিক হয়"),
            ("Nothing changes until you also listen to `Dimensions.addEventListener`, because `useWindowDimensions` only reads the screen size once", "`Dimensions.addEventListener`-ও না শুনলে কিছুই বদলায় না, কারণ `useWindowDimensions` screen size শুধু একবার পড়ে"),
        ],
        correct=2,
        a_en=r"""**C** (the layout keeps the old values; `useWindowDimensions()` fixes it) is correct. `width` and `COLUMNS` are computed **once**, when the module is first imported, and baked into the stylesheet. Nothing re-renders when the window changes. `useWindowDimensions()` is a hook that re-renders the component with new `width`/`height` whenever the window size changes.""",
        a_bn=r"""**C** (layout পুরনো value রেখে দেয়; `useWindowDimensions()` দিয়ে ঠিক হয়) সঠিক। `width` আর `COLUMNS` module প্রথমবার import হওয়ার সময় **একবারই** হিসাব হয় আর stylesheet-এর ভেতরে স্থির হয়ে যায়। Window বদলালে কিছুই re-render হয় না। `useWindowDimensions()` একটা hook, যেটা window size বদলালেই নতুন `width`/`height` দিয়ে component re-render করে।""",
        quick_en=r"""The layout keeps the old width and column count, because `Dimensions.get` was read once at import time. `useWindowDimensions()` inside the component re-renders it with the new size on rotation or split screen.""",
        quick_bn=r"""Layout পুরনো width আর column সংখ্যাই রেখে দেয়, কারণ `Dimensions.get` import-এর সময় একবারই পড়া হয়েছিল। Component-এর ভেতরে `useWindowDimensions()` ব্যবহার করলে rotation বা split screen-এ নতুন size নিয়ে re-render হয়।""",
        ex_en=r"""
            - **A** is the tempting one. `Dimensions.get('window')` does return the current size *when you call it*, but this code called it once at import time and never again.
            - **D** has it backwards: `useWindowDimensions` is the one that updates; `Dimensions.addEventListener('change', ...)` is the older manual way to do the same thing.
            - **B** is wrong: reading `Dimensions` at module level is allowed; it's just stale.

            Extra details: `FlatList` can't change `numColumns` on the fly; give it `key={columns}` so it remounts when the column count changes. On Android, `window` excludes the status bar (if not translucent) and the navigation bar, while `screen` is the whole display; for layout you almost always want `window`.
        """,
        ex_bn=r"""
            - **A** সবচেয়ে লোভনীয় ভুল। `Dimensions.get('window')` *যখন call করো তখনকার* size ঠিকই দেয়, কিন্তু এই code import-এর সময় একবার call করেছে, আর কখনো না।
            - **D** উল্টো বলছে: update হয় `useWindowDimensions`; `Dimensions.addEventListener('change', ...)` হলো একই কাজ হাতে করার পুরনো উপায়।
            - **B** ভুল: module level-এ `Dimensions` পড়া যায়; শুধু value-টা পুরনো থেকে যায়।

            আরও কিছু কথা: `FlatList` চলতি অবস্থায় `numColumns` বদলাতে পারে না; column সংখ্যা বদলালে remount করাতে `key={columns}` দাও। Android-এ `window` থেকে status bar (translucent না হলে) আর navigation bar বাদ যায়, আর `screen` হলো পুরো display; layout-এর জন্য প্রায় সবসময় `window`-ই দরকার।
        """,
        tip_en=r"""Say "module-level values are computed once", then give the hook as the fix and mention the `numColumns` + `key` detail; that last bit shows real experience with grids.""",
        tip_bn=r"""বলো "module-level value একবারই হিসাব হয়", তারপর fix হিসেবে hook-টা দাও আর `numColumns` + `key`-এর কথা বলো; শেষ কথাটা grid নিয়ে বাস্তব অভিজ্ঞতা দেখায়।""",
        extra=[
            dict(lang="tsx", label_en="Fixed version", label_bn="সংশোধিত version", src=r"""
                import { FlatList, useWindowDimensions } from 'react-native';

                export function ProductGrid({ products }: { products: Product[] }) {
                  const { width } = useWindowDimensions(); // re-renders on rotation/split screen
                  const columns = width > 700 ? 3 : 2;
                  const cardSize = width / columns;

                  return (
                    <FlatList
                      key={columns} // numColumns can't change on the fly: remount instead
                      data={products}
                      numColumns={columns}
                      renderItem={({ item }) => <ProductCard product={item} size={cardSize} />}
                    />
                  );
                }
            """),
        ],
        follow=[
            ("What's the difference between the `window` and `screen` dimensions on Android?", "Android-এ `window` আর `screen` dimension-এর পার্থক্য কী?"),
            ("How would you switch to a two-pane layout on tablets?", "Tablet-এ two-pane layout-এ কীভাবে যাবে?"),
        ],
        related=["rn-004", "rn-011"],
        refs=[R_USEWINDOW, R_DIMENSIONS],
    ),
    # ------------------------------------------------------------------ rn-014
    Q(
        id="rn-014", sub="Images & Media", diff="medium", type="security-performance",
        prio="high", market="both", mins=6,
        tags=["expo-image", "memory", "caching", "expo-video", "expo-audio"],
        ver=VER, vs=True, status="stable",
        q_en=r"""A marketplace app shows product photos in a feed and on detail screens, plus short product videos. Low-end Android phones run out of memory and images flicker while scrolling. How do you handle images and media in an Expo SDK 58 app for performance and safety?""",
        q_bn=r"""একটা marketplace app feed আর detail screen-এ product-এর ছবি দেখায়, সাথে ছোট product video। কম দামের Android phone-এ memory শেষ হয়ে যায় আর scroll করার সময় image flicker করে। Expo SDK 58 app-এ performance আর নিরাপত্তার কথা মাথায় রেখে image আর media কীভাবে সামলাবে?""",
        a_en=r"""
            **The real cost is decoded size, not file size.** A 4000×3000 photo becomes about 48 MB of bitmap in memory (4 bytes per pixel), even if the JPEG is 2 MB. A feed of those runs low-end phones out of memory.

            - **Request the right size:** have the CDN/API return thumbnails close to the display size × pixel ratio (a 300×200 pt card at 3× needs about 900×600 px), and load the full image only on the detail screen.
            - **Use `expo-image`:** disk caching by default (`cachePolicy` can be `'memory-disk'`), `placeholder` with a `blurhash`/`thumbhash` so there's no blank box, `transition` for a smooth fade, `contentFit` instead of resizing yourself, and `recyclingKey` in recycled lists (FlashList) so an old image doesn't flash in a reused cell. `Image.prefetch()` warms the cache for the next screen.
            - **Media:** use `expo-video` (`useVideoPlayer` + `VideoView`) and `expo-audio` (`useAudioPlayer`). `expo-av` is legacy and no longer part of the SDK. Don't autoplay off-screen videos; pause them when they leave the viewport.
            - **Safety:** only load images over HTTPS, send auth through `source.headers` rather than putting tokens in URLs (URLs end up in caches and logs), and treat user-uploaded images as untrusted (size limits, re-encode on the server).
        """,
        a_bn=r"""
            **আসল খরচ decoded size-এর, file size-এর না।** একটা 4000×3000 ছবি memory-তে প্রায় 48 MB bitmap হয়ে যায় (প্রতি pixel-এ 4 byte), JPEG file 2 MB হলেও। এরকম ছবির feed কম দামের phone-এর memory শেষ করে দেয়।

            - **ঠিক size চাও:** CDN/API থেকে display size × pixel ratio-এর কাছাকাছি thumbnail আনো (3× screen-এ 300×200 pt card-এর জন্য দরকার মোটামুটি 900×600 px), আর পুরো image শুধু detail screen-এ load করো।
            - **`expo-image` ব্যবহার করো:** default-ভাবে disk caching (`cachePolicy` `'memory-disk'` করা যায়), `blurhash`/`thumbhash` দিয়ে `placeholder` যাতে ফাঁকা box না দেখায়, smooth fade-এর জন্য `transition`, নিজে resize না করে `contentFit`, আর recycled list (FlashList)-এ `recyclingKey`, যাতে reuse হওয়া cell-এ পুরনো image ঝলক না দেয়। পরের screen-এর জন্য `Image.prefetch()` দিয়ে cache আগেই ভরে রাখা যায়।
            - **Media:** `expo-video` (`useVideoPlayer` + `VideoView`) আর `expo-audio` (`useAudioPlayer`) ব্যবহার করো। `expo-av` legacy, এখন আর SDK-এর অংশ না। Screen-এর বাইরের video autoplay করো না; viewport থেকে বের হলে pause করো।
            - **নিরাপত্তা:** image শুধু HTTPS দিয়ে load করো, token URL-এ না বসিয়ে `source.headers` দিয়ে auth পাঠাও (URL cache আর log-এ থেকে যায়), আর user-এর upload করা image-কে untrusted ধরো (size limit, server-এ re-encode)।
        """,
        quick_en=r"""Memory depends on decoded pixels (4000×3000 is about 48 MB), so serve thumbnails near display size and use `expo-image` for caching, blurhash placeholders and `recyclingKey` in lists. Use `expo-video`/`expo-audio` (`expo-av` is legacy) and load media over HTTPS without tokens in URLs.""",
        quick_bn=r"""Memory নির্ভর করে decoded pixel-এর উপর (4000×3000 মানে প্রায় 48 MB), তাই display size-এর কাছাকাছি thumbnail দাও আর caching, blurhash placeholder ও list-এ `recyclingKey`-এর জন্য `expo-image` ব্যবহার করো। `expo-video`/`expo-audio` ব্যবহার করো (`expo-av` legacy), আর media HTTPS দিয়ে load করো, URL-এ token ছাড়া।""",
        ex_en=r"""
            - **Numbers checked with Node:** 4000 × 3000 × 4 = 48,000,000 bytes (≈ 45.8 MiB); a 900 × 600 thumbnail is 2,160,000 bytes (≈ 2 MB). That's a 22× difference per visible image.
            - **`allowDownscaling`** (default `true`) lets `expo-image` decode a smaller bitmap when the view is smaller than the source, but the full file is still downloaded; server-side resizing saves both bandwidth and memory.
            - **Flicker** usually comes from no placeholder plus no cache hit, or from a recycled cell showing its previous image; `placeholder`, `transition` and `recyclingKey` address each case.
            - **Clearing caches:** `Image.clearMemoryCache()` / `clearDiskCache()` exist, but call them for a reason (logout, a "clear cache" setting), not on every screen.
            - **Video players** created with `useVideoPlayer` are released when the component unmounts; keep the number of mounted players small in a feed.
            - **Measure** in a release build with the memory tools in Android Studio, not in a debug build.
        """,
        ex_bn=r"""
            - **Node দিয়ে যাচাই করা হিসাব:** 4000 × 3000 × 4 = 48,000,000 byte (≈ 45.8 MiB); একটা 900 × 600 thumbnail হলো 2,160,000 byte (≈ 2 MB)। প্রতিটা দৃশ্যমান image-এ পার্থক্য 22 গুণ।
            - **`allowDownscaling`** (default `true`) view source-এর চেয়ে ছোট হলে `expo-image`-কে ছোট bitmap decode করতে দেয়, কিন্তু পুরো file তখনও download হয়; server-side resize করলে bandwidth আর memory দুটোই বাঁচে।
            - **Flicker** সাধারণত হয় placeholder না থাকলে আর cache hit না হলে, অথবা recycled cell আগের image দেখালে; `placeholder`, `transition` আর `recyclingKey` এগুলোর প্রতিটা সমাধান করে।
            - **Cache clear করা:** `Image.clearMemoryCache()` / `clearDiskCache()` আছে, কিন্তু কারণ থাকলে call করো (logout, "clear cache" setting), প্রতিটা screen-এ না।
            - **`useVideoPlayer` দিয়ে বানানো video player** component unmount হলে release হয়; feed-এ একসাথে mount থাকা player-এর সংখ্যা কম রাখো।
            - **মাপো** release build-এ Android Studio-র memory tool দিয়ে, debug build-এ না।
        """,
        tip_en=r"""Start with the decoded-size calculation; it reframes the problem in one sentence. Then go through size, cache, placeholder, recycling, and finish with media and security.""",
        tip_bn=r"""শুরু করো decoded-size-এর হিসাব দিয়ে; এক লাইনেই সমস্যাটা পরিষ্কার হয়ে যায়। তারপর ধাপে ধাপে size, cache, placeholder, recycling বলো, আর শেষ করো media আর security দিয়ে।""",
        mist_en=r"""Assuming a small JPEG means small memory use, and loading full-resolution originals into thumbnails. Also still recommending `expo-av` for new code.""",
        mist_bn=r"""ধরে নেওয়া যে ছোট JPEG মানে memory-ও কম লাগবে, আর thumbnail-এ পুরো resolution-এর original load করা। নতুন code-এ এখনও `expo-av` recommend করাও একটা ভুল।""",
        code=r"""
            import { Image } from 'expo-image';
            import { useVideoPlayer, VideoView } from 'expo-video';

            export function ProductCard({ product, token }: { product: Product; token: string }) {
              return (
                <Image
                  source={{ uri: product.thumbUrl, headers: { Authorization: `Bearer ${token}` } }} // 900x600 thumbnail
                  placeholder={{ blurhash: product.blurhash }}
                  contentFit="cover"
                  transition={200}
                  cachePolicy="memory-disk"
                  recyclingKey={product.id} // reused cells don't flash the previous image
                  style={{ width: '100%', aspectRatio: 3 / 2 }}
                  accessibilityLabel={product.name}
                />
              );
            }

            export function ProductVideo({ url }: { url: string }) {
              const player = useVideoPlayer(url, (p) => {
                p.muted = true;
                p.loop = true;
              });
              return <VideoView player={player} style={{ width: '100%', aspectRatio: 16 / 9 }} />;
            }
        """,
        lang="tsx",
        follow=[
            ("How would you pause videos that scroll out of view in a feed?", "Feed-এ screen থেকে বের হয়ে যাওয়া video কীভাবে pause করবে?"),
            ("Where would you generate the blurhash: on the device or on the server?", "Blurhash কোথায় generate করবে: device-এ না server-এ?"),
        ],
        related=["rn-016", "rn-038"],
        refs=[R_EXPO_IMAGE, R_EXPO_VIDEO, R_EXPO_AUDIO],
    ),
    # ------------------------------------------------------------------ rn-015
    Q(
        id="rn-015", sub="Forms & Keyboard", diff="medium", type="coding",
        prio="high", market="both", mins=10,
        tags=["textinput", "forms", "validation", "secure-text-entry"],
        ver="React Native 0.88 (React 19.3)", vs=False, status="stable",
        q_en=r"""
            Write a `LoginForm` component (TSX) for a React Native app:

            - Email and password fields, both controlled.
            - Email must look like an email; password must be at least 8 characters. Show an error under a field only after the user has left it (blur).
            - The email field uses the email keyboard and no auto-capitalisation; the password is hidden.
            - "Log in" is disabled while the form is invalid or a request is in flight, and shows a spinner while submitting.
            - It calls `onSubmit(email, password)` (returns a Promise) and shows a general error if that rejects.

            Example: typing `rahim@example` and leaving the field shows "Enter a valid email"; `rahim@example.com` with `secret123` enables the button.
        """,
        q_bn=r"""
            React Native app-এর জন্য একটা `LoginForm` component (TSX) লেখো:

            - Email আর password field, দুটোই controlled।
            - Email দেখতে email-এর মতো হতে হবে; password অন্তত 8 character। User field ছেড়ে যাওয়ার (blur) পরেই শুধু field-এর নিচে error দেখাবে।
            - Email field-এ email keyboard আর auto-capitalisation বন্ধ; password লুকানো থাকবে।
            - Form invalid থাকলে বা request চলার সময় "Log in" disabled থাকবে, আর submit করার সময় spinner দেখাবে।
            - এটা `onSubmit(email, password)` call করবে (একটা Promise return করে), আর সেটা reject হলে একটা সাধারণ error দেখাবে।

            Example: `rahim@example` লিখে field ছেড়ে গেলে "Enter a valid email" দেখাবে; `rahim@example.com` আর `secret123` দিলে button enabled হবে।
        """,
        a_en=r"""
            I keep `email`, `password`, a `touched` map, `submitting` and a form-level error in state. Validation errors are **derived** on every render from the current values (a pure `validate` function), not stored, so they can never go out of sync.

            - `keyboardType="email-address"`, `autoCapitalize="none"`, `autoComplete="email"` and `textContentType="emailAddress"` for email; `secureTextEntry` and `autoComplete="current-password"` for the password, so password managers can fill it.
            - Errors show only when `touched.email` is true, set in `onBlur`.
            - `canSubmit = isValid && !submitting`; the `Pressable` gets `disabled={!canSubmit}` and `accessibilityState={{ disabled, busy }}`.
            - `handleSubmit` guards against double submits, sets `submitting`, awaits `onSubmit`, catches to show a general message, and always resets in `finally`.
            - `returnKeyType="next"` moves focus to the password; `onSubmitEditing` on the password submits.

            Validation is O(n) in the input length; the server must validate again, because client checks are only for UX.
        """,
        a_bn=r"""
            আমি state-এ রাখি `email`, `password`, একটা `touched` map, `submitting` আর form-level error। Validation error প্রতি render-এ বর্তমান value থেকে **derive** করা হয় (একটা pure `validate` function দিয়ে), state-এ রাখা হয় না, তাই কখনো out of sync হতে পারে না।

            - Email-এর জন্য `keyboardType="email-address"`, `autoCapitalize="none"`, `autoComplete="email"` আর `textContentType="emailAddress"`; password-এর জন্য `secureTextEntry` আর `autoComplete="current-password"`, যাতে password manager fill করতে পারে।
            - Error শুধু তখনই দেখায় যখন `touched.email` true, যেটা `onBlur`-এ set হয়।
            - `canSubmit = isValid && !submitting`; `Pressable` পায় `disabled={!canSubmit}` আর `accessibilityState={{ disabled, busy }}`।
            - `handleSubmit` দুইবার submit ঠেকায়, `submitting` set করে, `onSubmit`-এর জন্য await করে, error হলে catch করে সাধারণ message দেখায়, আর `finally`-তে সবসময় reset করে।
            - `returnKeyType="next"` focus password-এ নিয়ে যায়; password-এর `onSubmitEditing` submit করে।

            Validation input-এর দৈর্ঘ্যের উপর O(n); server-কে আবার validate করতেই হবে, কারণ client-এর check শুধু UX-এর জন্য।
        """,
        quick_en=r"""Keep the two inputs controlled, derive errors from a pure `validate()` on every render, show them after blur, and disable the `Pressable` while invalid or submitting. Use `keyboardType="email-address"`, `autoCapitalize="none"` and `secureTextEntry`; validation is O(n) and the server must validate again.""",
        quick_bn=r"""দুটো input controlled রাখো, প্রতি render-এ একটা pure `validate()` থেকে error derive করো, blur-এর পর দেখাও, আর invalid বা submitting অবস্থায় `Pressable` disabled রাখো। `keyboardType="email-address"`, `autoCapitalize="none"` আর `secureTextEntry` ব্যবহার করো; validation O(n), আর server-কে আবার validate করতেই হবে।""",
        ex_en=r"""
            - **Verified logic (Node):** `validate('', '')` → both errors; `validate(' rahim@example.com ', 'secret123')` → `{}` (email is trimmed); `validate('rahim@example', 'short')` → both errors.
            - **Why derive errors:** storing them in state and updating them in effects causes extra renders and "error still showing after I fixed it" bugs.
            - **Trim the email, never the password:** spaces can be part of a real password.
            - **Disabled `Pressable`:** `disabled` stops `onPress`, but you must change the style yourself (and set `accessibilityState`) so sighted and screen-reader users both know.
            - **After success** the screen usually navigates away; setting state on an unmounted component is harmless in modern React, but the `finally` keeps the button usable if navigation doesn't happen.
            - **Larger forms:** a library like React Hook Form with a schema (Zod) scales better; the principles stay the same.
            - **Security:** never log the password, and store the returned token in `expo-secure-store`, not AsyncStorage.
        """,
        ex_bn=r"""
            - **যাচাই করা logic (Node):** `validate('', '')` → দুটো error; `validate(' rahim@example.com ', 'secret123')` → `{}` (email trim হয়); `validate('rahim@example', 'short')` → দুটো error।
            - **Error কেন derive করব:** state-এ রেখে effect দিয়ে update করলে বাড়তি render হয় আর "ঠিক করার পরও error দেখাচ্ছে" ধরনের bug হয়।
            - **Email trim করো, password কখনো না:** space আসল password-এর অংশ হতে পারে।
            - **Disabled `Pressable`:** `disabled` দিলে `onPress` বন্ধ হয়, কিন্তু style নিজেকেই বদলাতে হয় (আর `accessibilityState` দিতে হয়), যাতে চোখে দেখা user আর screen-reader user দুজনেই বুঝতে পারে।
            - **Success-এর পর** সাধারণত screen অন্য জায়গায় navigate করে; আধুনিক React-এ unmount হওয়া component-এ state set করলে ক্ষতি নেই, আর navigation না হলেও `finally` button-কে আবার ব্যবহারযোগ্য রাখে।
            - **বড় form-এ:** schema (Zod)-সহ React Hook Form-এর মতো library ভালো scale করে; মূলনীতি একই থাকে।
            - **Security:** password কখনো log করো না, আর return হওয়া token `expo-secure-store`-এ রাখো, AsyncStorage-এ না।
        """,
        tip_en=r"""Talk through state first (what's stored vs derived), then the input props, then the submit flow with `finally`. Mention that client validation is UX only; interviewers often wait for that line.""",
        tip_bn=r"""আগে state নিয়ে বলো (কী store হচ্ছে আর কী derive হচ্ছে), তারপর input-এর props, তারপর `finally`-সহ submit flow। বলো যে client validation শুধু UX-এর জন্য; interviewer প্রায়ই এই কথাটার অপেক্ষায় থাকে।""",
        mist_en=r"""Showing every error on the first render before the user types, forgetting `autoCapitalize="none"` (so emails start with a capital letter), and not resetting `submitting` when the request fails, which leaves the button disabled forever.""",
        mist_bn=r"""User টাইপ করার আগেই প্রথম render-এ সব error দেখানো, `autoCapitalize="none"` দিতে ভুলে যাওয়া (ফলে email বড় হাতের অক্ষর দিয়ে শুরু হয়), আর request fail করলে `submitting` reset না করা, যাতে button চিরকাল disabled থেকে যায়।""",
        code=r"""
            import { useRef, useState } from 'react';
            import { ActivityIndicator, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';

            type Errors = { email?: string; password?: string };
            const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            export function validate(email: string, password: string): Errors {
              const errors: Errors = {};
              if (!EMAIL_RE.test(email.trim())) errors.email = 'Enter a valid email';
              if (password.length < 8) errors.password = 'Use at least 8 characters';
              return errors;
            }

            type Props = { onSubmit: (email: string, password: string) => Promise<void> };

            export function LoginForm({ onSubmit }: Props) {
              const [email, setEmail] = useState('');
              const [password, setPassword] = useState('');
              const [touched, setTouched] = useState({ email: false, password: false });
              const [submitting, setSubmitting] = useState(false);
              const [formError, setFormError] = useState<string | null>(null);
              const passwordRef = useRef<TextInput>(null);

              const errors = validate(email, password); // derived, not state
              const canSubmit = Object.keys(errors).length === 0 && !submitting;

              async function handleSubmit() {
                if (!canSubmit) return; // also blocks double taps
                setSubmitting(true);
                setFormError(null);
                try {
                  await onSubmit(email.trim(), password);
                } catch {
                  setFormError('Login failed. Check your details and try again.');
                } finally {
                  setSubmitting(false);
                }
              }

              return (
                <View style={styles.form}>
                  <TextInput
                    value={email}
                    onChangeText={setEmail}
                    onBlur={() => setTouched((t) => ({ ...t, email: true }))}
                    placeholder="Email"
                    keyboardType="email-address"
                    autoCapitalize="none"
                    autoComplete="email"
                    textContentType="emailAddress"
                    returnKeyType="next"
                    onSubmitEditing={() => passwordRef.current?.focus()}
                    accessibilityLabel="Email"
                    style={styles.input}
                  />
                  {touched.email && errors.email ? <Text style={styles.error}>{errors.email}</Text> : null}

                  <TextInput
                    ref={passwordRef}
                    value={password}
                    onChangeText={setPassword}
                    onBlur={() => setTouched((t) => ({ ...t, password: true }))}
                    placeholder="Password"
                    secureTextEntry
                    autoCapitalize="none"
                    autoComplete="current-password"
                    textContentType="password"
                    returnKeyType="go"
                    onSubmitEditing={handleSubmit}
                    accessibilityLabel="Password"
                    style={styles.input}
                  />
                  {touched.password && errors.password ? <Text style={styles.error}>{errors.password}</Text> : null}

                  {formError ? <Text style={styles.error} accessibilityLiveRegion="polite">{formError}</Text> : null}

                  <Pressable
                    onPress={handleSubmit}
                    disabled={!canSubmit}
                    accessibilityRole="button"
                    accessibilityState={{ disabled: !canSubmit, busy: submitting }}
                    style={({ pressed }) => [styles.button, !canSubmit && styles.disabled, pressed && styles.pressed]}
                  >
                    {submitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Log in</Text>}
                  </Pressable>
                </View>
              );
            }

            const styles = StyleSheet.create({
              form: { gap: 8, padding: 16 },
              input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12, fontSize: 16 },
              error: { color: '#b00020' },
              button: { backgroundColor: '#0a7', borderRadius: 8, padding: 14, alignItems: 'center', minHeight: 48 },
              disabled: { opacity: 0.5 },
              pressed: { opacity: 0.8 },
              buttonText: { color: '#fff', fontWeight: '600' },
            });
        """,
        lang="tsx",
        time="O(n) per render (n = input length, for validation)",
        space="O(1)",
        follow=[
            ("How would you add a show/hide password toggle accessibly?", "Accessible ভাবে password show/hide toggle কীভাবে যোগ করবে?"),
            ("How would you move this to React Hook Form with a Zod schema?", "এটাকে Zod schema-সহ React Hook Form-এ কীভাবে নিয়ে যাবে?"),
        ],
        related=["rn-012", "rn-008", "rn-030", "react-005"],
        refs=[R_TEXTINPUT, R_KAV],
    ),
    # ------------------------------------------------------------------ rn-016
    Q(
        id="rn-016", sub="Lists", diff="hard", type="security-performance",
        prio="high", market="both", mins=8,
        tags=["flatlist", "flashlist", "performance", "memo", "getitemlayout"],
        ver=VER, vs=True, status="stable",
        q_en=r"""A news feed renders 5,000 rows with `FlatList`. Scrolling fast shows blank areas, taps feel delayed, and the React Profiler shows every row re-rendering when the user likes one post. Rows are a fixed 72 pt tall with a 1 pt separator. How do you tune it?""",
        q_bn=r"""একটা news feed `FlatList` দিয়ে 5,000 row render করে। দ্রুত scroll করলে ফাঁকা জায়গা দেখা যায়, tap দেরিতে কাজ করে, আর user একটা post like করলে React Profiler দেখায় প্রতিটা row আবার render হচ্ছে। প্রতিটা row fixed 72 pt উঁচু, সাথে 1 pt separator। কীভাবে tune করবে?""",
        a_en=r"""
            First I measure in a **release build** (dev mode is much slower) with the React Native DevTools profiler, then fix the causes in this order:

            1. **Stop the re-render storm.** Every row re-renders because of an unstable prop: usually an inline `renderItem`/`onPress` or a new `style` object each render, or the whole `posts` array being recreated. Wrap the row in `memo`, pass primitive props (`id`, `title`, `liked`), keep callbacks stable with `useCallback`, and update only the liked post immutably so other row objects keep their identity. (React Compiler can automate much of the memoisation if it's enabled.)
            2. **Skip measurement.** With fixed heights, `getItemLayout={(_, i) => ({ length: 72, offset: 73 * i, index: i })}`; the separator is included in the offset. Scrolling and `scrollToIndex` no longer need to measure rows.
            3. **Tune the window.** `initialNumToRender` just enough to fill the screen; `windowSize` (default 21 screens) lower if memory is the problem, higher if blanks are; `maxToRenderPerBatch` balances fill rate against JS-thread time.
            4. **Lighter rows:** pre-format dates and numbers when data arrives, not in render; small cached thumbnails via `expo-image`.
            5. **Paginate:** load pages with `onEndReached` instead of holding 5,000 rows if the user rarely scrolls that far.

            If it's still janky, I switch to **FlashList v2** (bundled with SDK 58, New Architecture only): it recycles cell views instead of mounting new ones and needs no size estimates.
        """,
        a_bn=r"""
            প্রথমে আমি **release build**-এ মাপি (dev mode অনেক ধীর), React Native DevTools-এর profiler দিয়ে, তারপর এই ক্রমে কারণগুলো ঠিক করি:

            1. **Re-render-এর ঝড় থামাও।** কোনো unstable prop-এর কারণে প্রতিটা row re-render হচ্ছে: সাধারণত inline `renderItem`/`onPress` বা প্রতি render-এ নতুন `style` object, অথবা পুরো `posts` array নতুন করে তৈরি হওয়া। Row-কে `memo` দিয়ে মোড়াও, primitive props দাও (`id`, `title`, `liked`), `useCallback` দিয়ে callback stable রাখো, আর শুধু like করা post-টা immutably update করো, যাতে বাকি row object-গুলোর identity একই থাকে। (React Compiler চালু থাকলে memoisation-এর অনেকটা সে নিজেই করে।)
            2. **Measurement বাদ দাও।** Height fixed হলে `getItemLayout={(_, i) => ({ length: 72, offset: 73 * i, index: i })}`; offset-এ separator ধরা আছে। তখন scroll আর `scrollToIndex`-এ row মাপতে হয় না।
            3. **Window tune করো।** `initialNumToRender` শুধু screen ভরার মতো; memory সমস্যা হলে `windowSize` (default 21 screen) কমাও, ফাঁকা জায়গা সমস্যা হলে বাড়াও; `maxToRenderPerBatch` fill rate আর JS-thread-এর সময়ের মধ্যে ভারসাম্য রাখে।
            4. **Row হালকা করো:** date আর number data আসার সময়েই format করো, render-এ না; `expo-image` দিয়ে ছোট cached thumbnail।
            5. **Paginate করো:** user যদি কমই অতদূর scroll করে, 5,000 row ধরে না রেখে `onEndReached` দিয়ে page ধরে load করো।

            তারপরও janky হলে আমি **FlashList v2**-এ যাই (SDK 58-এ bundled, শুধু New Architecture): এটা নতুন cell mount না করে cell view recycle করে, আর কোনো size estimate লাগে না।
        """,
        quick_en=r"""Profile in a release build, then stop rows re-rendering with `memo`, primitive props and stable callbacks, add `getItemLayout` for the fixed 73 pt pitch, and tune `initialNumToRender`/`windowSize`. If it still janks, switch to FlashList v2, which recycles cells and needs no size estimates.""",
        quick_bn=r"""Release build-এ profile করো, তারপর `memo`, primitive props আর stable callback দিয়ে row re-render থামাও, fixed 73 pt pitch-এর জন্য `getItemLayout` দাও, আর `initialNumToRender`/`windowSize` tune করো। তারপরও jank থাকলে FlashList v2-এ যাও, যেটা cell recycle করে আর size estimate চায় না।""",
        ex_en=r"""
            - **Why taps feel delayed:** rendering rows runs on the JS thread; if a like triggers 30 visible rows plus the render window to re-render, the next touch waits behind that work.
            - **`getItemLayout` math (checked with Node):** with a 72 pt row and 1 pt separator, row 100 starts at offset 7,300 and row 4,999 at 364,927. Forgetting the separator makes `scrollToIndex` drift further the deeper you go.
            - **`FlatList` is a `PureComponent`:** if a memoised `renderItem` depends on outside state (a selected id), pass it as `extraData`, or rows won't update at all; the opposite bug.
            - **`removeClippedSubviews`** is already `true` on Android; it can cause missing content on iOS and doesn't free much memory.
            - **FlashList v2 caveats:** because views are recycled, `useState` inside a row can leak into another item; use FlashList's `useRecyclingState`, or keep that state outside. Use `getItemType` for rows with very different layouts, and `recyclingKey` on `expo-image`.
            - **Verify the fix** with the Profiler (rows that didn't change shouldn't render on a like) and by scrolling fast on a low-end Android device.
        """,
        ex_bn=r"""
            - **Tap কেন দেরিতে কাজ করে:** row render হয় JS thread-এ; একটা like-এ যদি 30টা দৃশ্যমান row আর render window-এর বাকি row আবার render হয়, পরের touch ওই কাজের পেছনে অপেক্ষা করে।
            - **`getItemLayout`-এর হিসাব (Node দিয়ে যাচাই করা):** 72 pt row আর 1 pt separator হলে row 100 শুরু হয় offset 7,300-এ আর row 4,999 শুরু হয় 364,927-এ। Separator ভুলে গেলে যত নিচে যাবে `scrollToIndex` তত বেশি সরে যাবে।
            - **`FlatList` একটা `PureComponent`:** memoised `renderItem` যদি বাইরের state-এর (যেমন selected id) উপর নির্ভর করে, সেটা `extraData` দিয়ে পাঠাও, নইলে row একদমই update হবে না; এটা উল্টো ধরনের bug।
            - **`removeClippedSubviews`** Android-এ আগে থেকেই `true`; iOS-এ এটা content হারিয়ে যাওয়ার কারণ হতে পারে, আর খুব একটা memory বাঁচায় না।
            - **FlashList v2-এর সতর্কতা:** view recycle হয় বলে row-এর ভেতরের `useState` অন্য item-এ চলে যেতে পারে; FlashList-এর `useRecyclingState` ব্যবহার করো, নয়তো ওই state বাইরে রাখো। একদম আলাদা layout-এর row-এর জন্য `getItemType` দাও, আর `expo-image`-এ `recyclingKey`।
            - **Fix যাচাই করো** Profiler দিয়ে (like করলে যে row বদলায়নি সেটা render হওয়া উচিত না), আর কম দামের Android device-এ দ্রুত scroll করে।
        """,
        tip_en=r"""Structure it as measure → fix re-renders → skip layout work → tune the window → change the list implementation. Saying "release build first" and doing the `getItemLayout` math out loud are strong signals.""",
        tip_bn=r"""এভাবে সাজাও: মাপো → re-render ঠিক করো → layout-এর কাজ বাদ দাও → window tune করো → list-এর implementation বদলাও। "আগে release build" বলা আর `getItemLayout`-এর হিসাব মুখে করে দেখানো খুব ভালো signal দেয়।""",
        mist_en=r"""Jumping straight to "use FlashList" without fixing the re-renders (they make FlashList slow too), measuring only in development mode, and cranking `windowSize` up until memory runs out.""",
        mist_bn=r"""Re-render ঠিক না করেই সরাসরি "FlashList ব্যবহার করো" বলা (ওগুলো FlashList-কেও ধীর করে), শুধু development mode-এ মাপা, আর memory শেষ না হওয়া পর্যন্ত `windowSize` বাড়াতে থাকা।""",
        code=r"""
            import { memo, useCallback } from 'react';
            import { FlatList, Pressable, Text, View } from 'react-native';

            const ROW = 72;
            const SEPARATOR = 1;

            const PostRow = memo(function PostRow({ id, title, timeLabel, liked, onToggleLike }: {
              id: string; title: string; timeLabel: string; liked: boolean; onToggleLike: (id: string) => void;
            }) {
              return (
                <View style={{ height: ROW, justifyContent: 'center', paddingHorizontal: 16 }}>
                  <Text numberOfLines={1}>{title}</Text>
                  <Text>{timeLabel}</Text>
                  <Pressable onPress={() => onToggleLike(id)} accessibilityRole="button">
                    <Text>{liked ? 'Unlike' : 'Like'}</Text>
                  </Pressable>
                </View>
              );
            });

            export function Feed({ posts, setPosts }: { posts: Post[]; setPosts: SetPosts }) {
              const onToggleLike = useCallback((id: string) => {
                // only the changed post gets a new object; others keep their identity
                setPosts((prev) => prev.map((p) => (p.id === id ? { ...p, liked: !p.liked } : p)));
              }, [setPosts]);

              const renderItem = useCallback(({ item }: { item: Post }) => (
                <PostRow id={item.id} title={item.title} timeLabel={item.timeLabel}
                         liked={item.liked} onToggleLike={onToggleLike} />
              ), [onToggleLike]);

              return (
                <FlatList
                  data={posts}
                  renderItem={renderItem}
                  keyExtractor={(item) => item.id}
                  ItemSeparatorComponent={Separator}
                  getItemLayout={(_, index) => ({ length: ROW, offset: (ROW + SEPARATOR) * index, index })}
                  initialNumToRender={12}
                  windowSize={11}
                  maxToRenderPerBatch={10}
                />
              );
            }

            function Separator() {
              return <View style={{ height: SEPARATOR, backgroundColor: '#eee' }} />;
            }
        """,
        lang="tsx",
        extra=[
            dict(lang="tsx", label_en="FlashList v2 alternative", label_bn="FlashList v2 বিকল্প", src=r"""
                import { FlashList } from '@shopify/flash-list';

                // No estimatedItemSize in v2; views are recycled, so keep row state outside
                // or use useRecyclingState from @shopify/flash-list.
                <FlashList
                  data={posts}
                  renderItem={renderItem}
                  keyExtractor={(item) => item.id}
                  getItemType={(item) => (item.imageUrl ? 'with-image' : 'text')}
                  onEndReached={loadMore}
                  onEndReachedThreshold={0.5}
                />
            """),
        ],
        follow=[
            ("Why can local `useState` inside a FlashList row show up on another item?", "FlashList row-এর ভেতরের local `useState` কেন অন্য item-এ দেখা দিতে পারে?"),
            ("How would you confirm that a like now re-renders only one row?", "একটা like-এ যে এখন শুধু একটা row re-render হয়, সেটা কীভাবে নিশ্চিত হবে?"),
            ("When does `getItemLayout` not apply, and what do you do then?", "কখন `getItemLayout` কাজে লাগে না, আর তখন কী করবে?"),
        ],
        related=["rn-009", "rn-010", "rn-038", "react-029", "react-014"],
        refs=[R_OPT_FLATLIST, R_FLASHLIST, R_REACT_MEMO],
    ),
]

save("reactnative", "b2", QUESTIONS)
