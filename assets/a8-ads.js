(function () {
  function loadAd(slot) {
    var adName = slot.getAttribute('data-a8-ad');
    if (!adName) return;
    var body = slot.querySelector('[data-a8-ad-body]') || slot;
    var status = document.createElement('p');
    status.className = 'affiliate-ad__status';
    status.textContent = '広告を読み込んでいます。';
    body.appendChild(status);

    fetch('/assets/a8/' + adName + '.html', { cache: 'no-cache' })
      .then(function (response) {
        if (!response.ok) throw new Error('ad asset not found: ' + adName);
        return response.text();
      })
      .then(function (html) {
        body.innerHTML = html;
      })
      .catch(function () {
        status.textContent = '広告を読み込めませんでした。';
      });
  }

  function boot() {
    document.querySelectorAll('[data-a8-ad]').forEach(loadAd);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
}());
