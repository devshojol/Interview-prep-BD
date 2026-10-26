# React Native (with Expo) — quick-recall questions (rn-q01..q10)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

QUESTIONS = [
    # ------------------------------------------------------------------ rn-q01
    Q(
        id="rn-q01", sub="Tooling", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["metro", "bundler", "fast-refresh"],
        ver="React Native 0.88 (Metro 0.87)", vs=False, status="stable",
        q_en=r"""What is Metro in React Native?""",
        q_bn=r"""React Native-এ Metro কী?""",
        a_en=r"""Metro is React Native's JavaScript bundler. It resolves your imports (including platform files like `Button.ios.tsx`), transforms TS/JSX with Babel and serves the bundle to the app over HTTP during development with Fast Refresh; for a release build it produces the bundle that ships inside the app.""",
        a_bn=r"""Metro হলো React Native-এর JavaScript bundler। এটা import resolve করে (`Button.ios.tsx`-এর মতো platform file-সহ), Babel দিয়ে TS/JSX transform করে, আর development-এ Fast Refresh-সহ HTTP দিয়ে app-কে bundle দেয়; release build-এ app-এর ভেতরে যাওয়া bundle-টা তৈরি করে।""",
        ex_en=r"""It plays the role webpack or Vite plays on the web, but tuned for React Native. When something looks stale or a weird resolution error appears, restarting with a cleared cache (`npx expo start --clear`) is the classic first step.""",
        ex_bn=r"""Web-এ webpack বা Vite যে কাজ করে, Metro সেটাই করে, তবে React Native-এর জন্য বানানো। কিছু পুরোনো দেখালে বা অদ্ভুত resolution error এলে প্রথম কাজ হলো cache clear করে restart করা (`npx expo start --clear`)।""",
        tip_en=r"""Say "Metro is the bundler, like webpack for React Native" and mention Fast Refresh and platform-specific file resolution.""",
        tip_bn=r"""বলো "Metro হলো bundler, React Native-এর webpack-এর মতো", আর Fast Refresh ও platform-specific file resolution-এর কথা বলো।""",
        follow=[("Why would you clear Metro's cache?", "Metro-র cache কেন clear করবে?")],
        related=["rn-005", "rn-006"],
        refs=[("reactnative.dev — Metro", "https://reactnative.dev/docs/metro")],
    ),
    # ------------------------------------------------------------------ rn-q02
    Q(
        id="rn-q02", sub="Architecture", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["hermes", "js-engine", "bytecode"],
        ver="React Native 0.88 (Hermes V1 default since 0.84)", vs=True, status="stable",
        q_en=r"""What is Hermes?""",
        q_bn=r"""Hermes কী?""",
        a_en=r"""Hermes is the JavaScript engine built for React Native and used by default. It compiles your JS to bytecode at build time, so the app skips parsing on startup, starts faster and uses less memory; Hermes V1 has been the default since React Native 0.84.""",
        a_bn=r"""Hermes হলো React Native-এর জন্য বানানো JavaScript engine, আর এটাই default। এটা build-এর সময় JS-কে bytecode-এ compile করে, ফলে app start-এর সময় parse করতে হয় না, দ্রুত চালু হয় আর memory কম লাগে; React Native 0.84 থেকে Hermes V1 default।""",
        code=r"""
            const isHermes = () => !!global.HermesInternal;
            console.log(isHermes()); // true in a Hermes-powered app
        """, lang="javascript",
        ex_en=r"""Hermes is the engine, not the architecture: JSI sits on top of it. Older apps sometimes used JavaScriptCore; that's now community-maintained.""",
        ex_bn=r"""Hermes হলো engine, architecture না: JSI এর ওপরে বসে। পুরোনো app-এ মাঝে মাঝে JavaScriptCore ব্যবহার হতো; সেটা এখন community-maintained।""",
        tip_en=r"""Link it to a user benefit: "bytecode at build time means faster startup on cheap phones".""",
        tip_bn=r"""User-এর লাভের সাথে মেলাও: "build-এর সময় bytecode মানে কম দামের phone-এ দ্রুত startup"।""",
        follow=[("How is Hermes related to JSI and the New Architecture?", "Hermes-এর সাথে JSI আর New Architecture-এর সম্পর্ক কী?")],
        related=["rn-033", "rn-038"],
        refs=[("reactnative.dev — Using Hermes", "https://reactnative.dev/docs/hermes")],
    ),
    # ------------------------------------------------------------------ rn-q03
    Q(
        id="rn-q03", sub="Styling", diff="easy", type="quick",
        prio="medium", market="both", mins=2,
        tags=["dp", "pixelratio", "density", "units"],
        ver="Version-independent concept (React Native 0.88)", vs=False, status="stable",
        q_en=r"""Style sizes in React Native are unitless. Are they pixels? What is `PixelRatio`?""",
        q_bn=r"""React Native-এ style-এর size-এ কোনো unit থাকে না। এগুলো কি pixel? `PixelRatio` কী?""",
        a_en=r"""No, they are density-independent pixels (dp on Android, points on iOS), so `width: 100` looks about the same physical size on every screen. `PixelRatio.get()` returns how many physical pixels make one dp on the device (e.g. 2 or 3), which you use when you need real pixel sizes, such as requesting an image of the right resolution.""",
        a_bn=r"""না, এগুলো density-independent pixel (Android-এ dp, iOS-এ point), তাই `width: 100` সব screen-এ মোটামুটি একই physical size-এ দেখায়। `PixelRatio.get()` বলে device-এ এক dp-তে কতগুলো physical pixel (যেমন 2 বা 3); আসল pixel size লাগলে এটা ব্যবহার করো, যেমন সঠিক resolution-এর image চাওয়ার সময়।""",
        code=r"""
            import { PixelRatio } from 'react-native';
            const px = PixelRatio.getPixelSizeForLayoutSize(100);
            // → 300 on a device with PixelRatio 3, 263 with PixelRatio 2.625
        """, lang="typescript",
        ex_en=r"""Sizing images for the screen this way avoids blurry images on dense screens and wasted memory on small ones. `PixelRatio.getFontScale()` is separate: it reflects the user's font-size setting.""",
        ex_bn=r"""এভাবে screen অনুযায়ী image-এর size ঠিক করলে dense screen-এ ঝাপসা image আর ছোট screen-এ memory অপচয় দুটোই এড়ানো যায়। `PixelRatio.getFontScale()` আলাদা জিনিস: এটা user-এর font-size setting দেখায়।""",
        tip_en=r"""Say "dp, not pixels", then give the image-resolution use case for `PixelRatio`.""",
        tip_bn=r"""বলো "pixel না, dp", তারপর `PixelRatio`-এর image-resolution ব্যবহারের উদাহরণ দাও।""",
        follow=[("How would you draw a hairline border that is exactly one physical pixel?", "ঠিক এক physical pixel-এর একটা hairline border কীভাবে আঁকবে?")],
        related=["rn-003", "rn-014"],
        refs=[("reactnative.dev — PixelRatio", "https://reactnative.dev/docs/pixelratio")],
    ),
    # ------------------------------------------------------------------ rn-q04
    Q(
        id="rn-q04", sub="Styling", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["stylesheet", "styles", "typescript"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""What does `StyleSheet.create` do, and why use it instead of inline style objects?""",
        q_bn=r"""`StyleSheet.create` কী করে, আর inline style object-এর বদলে কেন এটা ব্যবহার করবে?""",
        a_en=r"""`StyleSheet.create` defines named style objects once, outside the component. It keeps styles out of the render function (no new object on every render), gives TypeScript checking and editor autocompletion for style props, and keeps JSX readable.""",
        a_bn=r"""`StyleSheet.create` component-এর বাইরে একবারে নাম দেওয়া style object তৈরি করে। এতে style render function-এর বাইরে থাকে (প্রতি render-এ নতুন object তৈরি হয় না), style prop-এ TypeScript checking আর editor autocompletion পাওয়া যায়, আর JSX পরিষ্কার থাকে।""",
        code=r"""
            const styles = StyleSheet.create({
              card: { padding: 16, borderRadius: 12, backgroundColor: '#fff' },
              title: { fontSize: 18, fontWeight: '600' },
            });
            // <View style={[styles.card, isActive && { borderColor: 'green' }]} />
        """, lang="typescript",
        ex_en=r"""Inline styles are fine for values that truly depend on props or state; combine them with an array (`style={[styles.card, dynamic]}`). Later items in the array win.""",
        ex_bn=r"""যে value সত্যিই props বা state-এর ওপর নির্ভর করে, তার জন্য inline style ঠিক আছে; array দিয়ে মেলাও (`style={[styles.card, dynamic]}`)। Array-এর পরের item জেতে।""",
        tip_en=r"""Mention the array syntax for combining static and dynamic styles; it's the follow-up interviewers usually ask.""",
        tip_bn=r"""Static আর dynamic style মেলানোর array syntax-এর কথা বলো; interviewer সাধারণত এটাই follow-up-এ জিজ্ঞেস করে।""",
        follow=[("In `style={[a, b]}`, which style wins when both set `color`?", "`style={[a, b]}`-এ দুটোই `color` set করলে কোনটা জেতে?")],
        related=["rn-003"],
        refs=[("reactnative.dev — StyleSheet", "https://reactnative.dev/docs/stylesheet")],
    ),
    # ------------------------------------------------------------------ rn-q05
    Q(
        id="rn-q05", sub="Navigation (Expo Router)", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["usefocuseffect", "useeffect", "navigation", "screens"],
        ver="Expo Router ~58 / React Navigation 7", vs=False, status="stable",
        q_en=r"""On a screen, what is the difference between `useEffect` and `useFocusEffect`?""",
        q_bn=r"""একটা screen-এ `useEffect` আর `useFocusEffect`-এর পার্থক্য কী?""",
        a_en=r"""In a stack, screens you navigate away from usually stay mounted, so `useEffect` runs only on mount and doesn't run again when you come back. `useFocusEffect` runs every time the screen gains focus and cleans up when it loses focus, so it's the right place to refresh data or start/stop a subscription per visit.""",
        a_bn=r"""Stack-এ যে screen থেকে অন্য জায়গায় যাও, সেটা সাধারণত mounted থেকে যায়, তাই `useEffect` শুধু mount-এ চলে, ফিরে এলে আবার চলে না। `useFocusEffect` প্রতিবার screen focus পেলে চলে আর focus হারালে cleanup করে, তাই প্রতি visit-এ data refresh বা subscription চালু/বন্ধ করার সঠিক জায়গা এটা।""",
        code=r"""
            import { useFocusEffect } from 'expo-router';
            import { useCallback } from 'react';

            useFocusEffect(useCallback(() => {
              const sub = subscribeToCart(setCart);
              return () => sub.unsubscribe(); // runs when the screen loses focus
            }, []));
        """, lang="tsx",
        ex_en=r"""Wrap the callback in `useCallback`; otherwise it changes on every render and the effect re-runs while the screen is focused.""",
        ex_bn=r"""Callback-টা `useCallback`-এ মোড়াও; নইলে প্রতি render-এ এটা বদলায় আর screen focused থাকা অবস্থাতেই effect বারবার চলে।""",
        tip_en=r"""Start with the fact that screens stay mounted in a stack; the rest of the answer follows from it.""",
        tip_bn=r"""শুরু করো এই কথা দিয়ে যে stack-এ screen mounted থেকে যায়; বাকি উত্তর এখান থেকেই আসে।""",
        follow=[("How else could you refetch data when a screen is revisited?", "Screen-এ ফিরে এলে আর কীভাবে data refetch করা যায়?")],
        related=["rn-017", "rn-018"],
        refs=[("React Navigation — useFocusEffect", "https://reactnavigation.org/docs/use-focus-effect")],
    ),
    # ------------------------------------------------------------------ rn-q06
    Q(
        id="rn-q06", sub="App Store Release", diff="easy", type="quick",
        prio="medium", market="both", mins=2,
        tags=["apk", "aab", "ipa", "release", "eas-build"],
        ver="Expo SDK 58, eas-cli 25.x", vs=False, status="stable",
        q_en=r"""What is the difference between an APK, an AAB and an IPA?""",
        q_bn=r"""APK, AAB আর IPA-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""An APK is an Android package you can install directly on a device. An AAB (Android App Bundle) is the publishing format Google Play requires for new apps; Play generates optimised APKs per device from it. An IPA is the iOS app archive you upload to App Store Connect or install through TestFlight.""",
        a_bn=r"""APK হলো Android package, যেটা সরাসরি device-এ install করা যায়। AAB (Android App Bundle) হলো নতুন app-এর জন্য Google Play-এর বাধ্যতামূলক publishing format; Play এটা থেকে প্রতিটা device-এর জন্য optimise করা APK তৈরি করে। IPA হলো iOS app archive, যেটা App Store Connect-এ upload করো বা TestFlight দিয়ে install করো।""",
        code=r"""
            {
              "build": {
                "preview": { "distribution": "internal", "android": { "buildType": "apk" } },
                "production": {}
              }
            }
        """, lang="json",
        ex_en=r"""In `eas.json` above, `production` makes an AAB (the default) and `preview` makes an APK. For sharing a build with testers directly, an APK is easier because an AAB can't be installed by tapping it.""",
        ex_bn=r"""ওপরের `eas.json`-এ `production` AAB বানায় (default), আর `preview` বানায় APK। Tester-দের সরাসরি build দিতে APK সহজ, কারণ AAB tap করে install করা যায় না।""",
        tip_en=r"""Answer "install vs publish" in one line, then mention how you'd get an APK from EAS for testers.""",
        tip_bn=r"""এক লাইনে "install বনাম publish" বলো, তারপর tester-দের জন্য EAS থেকে কীভাবে APK নেবে সেটা বলো।""",
        follow=[("Why does the same app need both a `version` and a build number?", "একই app-এর কেন `version` আর build number দুটোই লাগে?")],
        related=["rn-040", "rn-006"],
        refs=[("Expo — Build APKs for Android emulators and devices", "https://docs.expo.dev/build-reference/apk/")],
    ),
    # ------------------------------------------------------------------ rn-q07
    Q(
        id="rn-q07", sub="Expo Basics", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["expo-cli", "dev-server", "expo-go", "development-build"],
        ver="Expo SDK 58", vs=False, status="stable",
        q_en=r"""What happens when you run `npx expo start`?""",
        q_bn=r"""`npx expo start` চালালে কী হয়?""",
        a_en=r"""It starts the Expo dev server (Metro) and prints a QR code. You scan it with a development build (or Expo Go for simple projects) or press `a`/`i` to open an Android emulator or iOS simulator; the app then loads the JS bundle from your computer, with Fast Refresh on every save.""",
        a_bn=r"""এটা Expo dev server (Metro) চালু করে আর একটা QR code দেখায়। Development build (বা সাধারণ project-এ Expo Go) দিয়ে সেটা scan করো, অথবা `a`/`i` চেপে Android emulator বা iOS simulator খোলো; তারপর app তোমার computer থেকে JS bundle load করে, প্রতিবার save-এ Fast Refresh হয়।""",
        ex_en=r"""It doesn't build native code; the native app must already be installed. If `expo-dev-client` is installed, the CLI targets your development build by default. Press `j` to open the debugger.""",
        ex_bn=r"""এটা native code build করে না; native app আগে থেকেই install থাকতে হয়। `expo-dev-client` install থাকলে CLI default-ভাবে তোমার development build-কে target করে। Debugger খুলতে `j` চাপো।""",
        tip_en=r"""Separate "JS dev server" from "native app": the command serves JS; the native part comes from Expo Go or your development build.""",
        tip_bn=r""""JS dev server" আর "native app" আলাদা করে বলো: command-টা JS serve করে; native অংশ আসে Expo Go বা তোমার development build থেকে।""",
        follow=[("Phone and laptop are on different networks; how do you still connect?", "Phone আর laptop আলাদা network-এ থাকলে তবু কীভাবে connect করবে?")],
        related=["rn-006", "rn-007"],
        refs=[("Expo — Expo CLI", "https://docs.expo.dev/more/expo-cli/")],
    ),
    # ------------------------------------------------------------------ rn-q08
    Q(
        id="rn-q08", sub="Core Components", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["alert", "dialog", "ui"],
        ver="React Native 0.88", vs=False, status="stable",
        q_en=r"""How do you show a native confirmation dialog in React Native?""",
        q_bn=r"""React Native-এ native confirmation dialog কীভাবে দেখাবে?""",
        a_en=r"""Use `Alert.alert(title, message, buttons)`. Each button has a `text`, an optional `onPress` and a `style` (`'cancel'`, `'destructive'` or `'default'`); the call doesn't block, so put the follow-up action in `onPress`.""",
        a_bn=r"""`Alert.alert(title, message, buttons)` ব্যবহার করো। প্রতিটা button-এ থাকে `text`, ঐচ্ছিক `onPress` আর `style` (`'cancel'`, `'destructive'` বা `'default'`); call-টা block করে না, তাই পরের কাজ `onPress`-এ রাখো।""",
        code=r"""
            Alert.alert('Delete address?', 'This cannot be undone.', [
              { text: 'Cancel', style: 'cancel' },
              { text: 'Delete', style: 'destructive', onPress: () => deleteAddress(id) },
            ]);
        """, lang="typescript",
        ex_en=r"""Android shows at most three buttons; `style: 'destructive'` only changes the look on iOS. `Alert.prompt` (text input) is iOS-only, so for custom content build a modal instead.""",
        ex_bn=r"""Android সর্বোচ্চ তিনটা button দেখায়; `style: 'destructive'` শুধু iOS-এ চেহারা বদলায়। `Alert.prompt` (text input) শুধু iOS-এ আছে, তাই custom content লাগলে modal বানাও।""",
        tip_en=r"""Point out that it isn't blocking like the browser's `confirm()`; the result comes through callbacks.""",
        tip_bn=r"""বলো যে এটা browser-এর `confirm()`-এর মতো block করে না; ফলাফল আসে callback দিয়ে।""",
        follow=[("How would you wrap `Alert.alert` in a Promise that resolves to true/false?", "`Alert.alert`-কে কীভাবে একটা Promise-এ মোড়াবে যেটা true/false দিয়ে resolve হয়?")],
        related=["rn-002", "rn-005"],
        refs=[("reactnative.dev — Alert", "https://reactnative.dev/docs/alert")],
    ),
    # ------------------------------------------------------------------ rn-q09
    Q(
        id="rn-q09", sub="Deep Linking", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["linking", "urls", "phone", "browser"],
        ver="React Native 0.88, Expo SDK 58", vs=False, status="stable",
        q_en=r"""How do you open a phone dialer, an email draft or a website from a React Native app?""",
        q_bn=r"""React Native app থেকে phone dialer, email draft বা website কীভাবে খুলবে?""",
        a_en=r"""Call `Linking.openURL()` with the right URL scheme: `tel:` for the dialer, `mailto:` for email, `https:` for the browser. It returns a Promise, so catch the error in case no app can handle the URL. For web pages you want to keep inside the app, `expo-web-browser` opens an in-app browser.""",
        a_bn=r"""সঠিক URL scheme দিয়ে `Linking.openURL()` call করো: dialer-এর জন্য `tel:`, email-এর জন্য `mailto:`, browser-এর জন্য `https:`। এটা Promise return করে, তাই কোনো app URL-টা handle করতে না পারলে error catch করো। Web page app-এর ভেতরেই রাখতে চাইলে `expo-web-browser` একটা in-app browser খোলে।""",
        code=r"""
            import { Linking } from 'react-native';
            await Linking.openURL('tel:+8801700000000');
            await Linking.openURL('mailto:support@example.com?subject=Order%201042');
        """, lang="typescript",
        ex_en=r"""`Linking.canOpenURL()` needs extra setup to check other apps' schemes (`LSApplicationQueriesSchemes` on iOS, `<queries>` on Android 11+), so many apps simply try `openURL` and catch the failure.""",
        ex_bn=r"""অন্য app-এর scheme check করতে `Linking.canOpenURL()`-এর বাড়তি setup লাগে (iOS-এ `LSApplicationQueriesSchemes`, Android 11+-এ `<queries>`), তাই অনেক app সরাসরি `openURL` চেষ্টা করে failure catch করে।""",
        tip_en=r"""Name the schemes (`tel:`, `mailto:`, `https:`) and mention error handling; that's what the question checks.""",
        tip_bn=r"""Scheme-গুলোর নাম বলো (`tel:`, `mailto:`, `https:`) আর error handling-এর কথা বলো; প্রশ্নটা এটাই যাচাই করে।""",
        follow=[("How is opening a URL different from handling an incoming deep link?", "URL খোলা আর ভেতরে আসা deep link handle করার মধ্যে পার্থক্য কী?")],
        related=["rn-020"],
        refs=[("reactnative.dev — Linking", "https://reactnative.dev/docs/linking")],
    ),
    # ------------------------------------------------------------------ rn-q10
    Q(
        id="rn-q10", sub="Permissions", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["permissions", "camera", "privacy"],
        ver="Expo SDK 58 (expo-camera ~58)", vs=False, status="stable",
        q_en=r"""What is the usual pattern for asking for a runtime permission such as the camera?""",
        q_bn=r"""Camera-র মতো runtime permission চাওয়ার স্বাভাবিক pattern কী?""",
        a_en=r"""Check the current status first, ask only when the user starts the feature that needs it, and handle all three outcomes: granted (continue), denied but can ask again (explain and offer a retry), and permanently denied (explain and open Settings with `Linking.openSettings()`). The usage text also has to be declared in the app config.""",
        a_bn=r"""আগে বর্তমান status দেখো, user যখন feature-টা শুরু করে কেবল তখনই চাও, আর তিনটা ফলাফলই handle করো: granted (চালিয়ে যাও), denied কিন্তু আবার চাওয়া যায় (কারণ বুঝিয়ে retry দাও), আর স্থায়ীভাবে denied (বুঝিয়ে `Linking.openSettings()` দিয়ে Settings খোলো)। Usage text app config-এও declare করতে হয়।""",
        code=r"""
            const [permission, requestPermission] = useCameraPermissions(); // expo-camera
            if (!permission) return null;                  // still loading
            if (!permission.granted) {
              return permission.canAskAgain
                ? <Button title="Allow camera" onPress={requestPermission} />
                : <Button title="Open Settings" onPress={() => Linking.openSettings()} />;
            }
        """, lang="tsx",
        ex_en=r"""On iOS the system prompt appears only once; after a denial only Settings can change it, which is why asking in context matters. Without the iOS usage description (e.g. via the `expo-camera` config plugin) the app crashes when it asks or is rejected in review.""",
        ex_bn=r"""iOS-এ system prompt একবারই আসে; deny করার পরে শুধু Settings থেকে বদলানো যায়, এজন্যই প্রসঙ্গ বুঝে চাওয়া জরুরি। iOS usage description (যেমন `expo-camera` config plugin দিয়ে) না থাকলে permission চাওয়ার সময় app crash করে বা review-তে reject হয়।""",
        tip_en=r"""List the three states (granted, can ask again, blocked) and say you ask at the moment of need.""",
        tip_bn=r"""তিনটা অবস্থা বলো (granted, আবার চাওয়া যায়, blocked) আর বলো যে তুমি দরকারের মুহূর্তেই চাও।""",
        follow=[("Why shouldn't you request every permission on the first launch?", "প্রথম launch-এই সব permission কেন চাওয়া উচিত না?")],
        related=["rn-037", "rn-036"],
        refs=[("Expo — Permissions", "https://docs.expo.dev/guides/permissions/")],
    ),
]

save("reactnative", "quick", QUESTIONS)
