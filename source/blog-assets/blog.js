/* Interview Prep BD — blog enhancements. Articles are complete without this file. */
(function () {
  'use strict';

  // Opened from disk (file://), "dir/" links would show a directory listing; point them at index.html.
  if (location.protocol === 'file:') {
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (/^[a-z]+:/i.test(href) || href.charAt(0) === '#') return;
      a.setAttribute('href', href.replace(/(^|\/)(#|$)/, '$1index.html$2'));
    });
  }

  // Copy buttons on code blocks.
  if (!navigator.clipboard) return;
  document.querySelectorAll('.post-body .code').forEach(function (fig) {
    var bar = fig.querySelector('.code__bar');
    var code = fig.querySelector('pre code');
    if (!bar || !code) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = 'Copy'; }, 1600);
      }, function () { btn.textContent = 'Copy failed'; });
    });
    bar.appendChild(btn);
  });
})();
