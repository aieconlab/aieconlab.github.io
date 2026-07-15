(function () {
  'use strict';

  var STORAGE_KEY = 'aieconlab-ui-language';
  var SUPPORTED_LANGUAGES = ['ko', 'en'];
  var messages = {{ site.Data.ui.strings | jsonify | safeJS }};
  var categories = {{ site.Data.ui.categories | jsonify | safeJS }};
  var categoryLookup = {};
  var root = document.documentElement;
  var englishMonths = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  Object.keys(categories).forEach(function (key) {
    categoryLookup[normalizeCategoryKey(key)] = categories[key];
  });

  function normalizeLanguage(language) {
    return SUPPORTED_LANGUAGES.indexOf(language) !== -1 ? language : 'ko';
  }

  function currentLanguage() {
    return normalizeLanguage(root.getAttribute('data-ui-language'));
  }

  function messageFor(key, language) {
    var entry = messages[key];
    return entry && entry[language] ? entry[language] : '';
  }

  function interpolate(template, element) {
    return template.replace(/\{([a-z0-9_]+)\}/gi, function (_, token) {
      return element.getAttribute('data-ui-param-' + token.replace(/_/g, '-')) || '';
    });
  }

  function elementsIn(scope, selector) {
    var elements = [];
    if (scope.nodeType === 1 && scope.matches(selector)) {
      elements.push(scope);
    }
    if (scope.querySelectorAll) {
      elements = elements.concat(Array.prototype.slice.call(scope.querySelectorAll(selector)));
    }
    return elements;
  }

  function translateText(scope, language) {
    elementsIn(scope, '[data-ui-i18n]').forEach(function (element) {
      var translated = messageFor(element.getAttribute('data-ui-i18n'), language);
      if (!translated) return;
      translated = interpolate(translated, element);
      if (element.textContent !== translated) element.textContent = translated;
      element.setAttribute('lang', language);
    });
  }

  function translateAttribute(scope, language, dataAttribute, targetAttribute) {
    elementsIn(scope, '[' + dataAttribute + ']').forEach(function (element) {
      var translated = messageFor(element.getAttribute(dataAttribute), language);
      if (!translated) return;
      translated = interpolate(translated, element);
      if (element.getAttribute(targetAttribute) !== translated) {
        element.setAttribute(targetAttribute, translated);
      }
    });
  }

  function parseDate(value) {
    var iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value || '');
    if (iso) return [Number(iso[1]), Number(iso[2]), Number(iso[3])];
    var korean = /^(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일$/.exec(value || '');
    if (korean) return [Number(korean[1]), Number(korean[2]), Number(korean[3])];
    return null;
  }

  function translateDates(scope, language) {
    elementsIn(scope, '[data-ui-date]').forEach(function (element) {
      var parts = parseDate(element.getAttribute('data-ui-date'));
      if (!parts) return;
      var translated = language === 'en'
        ? englishMonths[parts[1] - 1] + ' ' + parts[2] + ', ' + parts[0]
        : parts[0] + '년 ' + parts[1] + '월 ' + parts[2] + '일';
      if (element.textContent !== translated) element.textContent = translated;
      element.setAttribute('lang', language);
    });
  }

  function normalizeCategoryKey(source) {
    return (source || '').trim().replace(/\s+/g, '_').toLowerCase();
  }

  function categoryEntry(source) {
    return categoryLookup[normalizeCategoryKey(source)];
  }

  function translatedCategory(source, language) {
    var normalized = (source || '').trim();
    var entry = categoryEntry(normalized);
    return entry && entry[language] ? entry[language] : normalized.replace(/_/g, ' ');
  }

  function translateCategories(scope, language) {
    elementsIn(scope, '[data-ui-category]').forEach(function (element) {
      var translated = translatedCategory(element.getAttribute('data-ui-category'), language);
      if (element.textContent !== translated) element.textContent = translated;
      if (categoryEntry(element.getAttribute('data-ui-category'))) element.setAttribute('lang', language);
    });

    elementsIn(scope, '[data-ui-category-list]').forEach(function (element) {
      if (!element.hasAttribute('data-ui-category-source')) {
        element.setAttribute('data-ui-category-source', element.textContent.trim());
      }
      var source = element.getAttribute('data-ui-category-source');
      var translated = source.split(',').map(function (category) {
        return translatedCategory(category, language);
      }).join(', ');
      if (element.textContent !== translated) element.textContent = translated;
      element.setAttribute('lang', language);
    });
  }

  function translateDocumentTitle(language) {
    var title = document.querySelector('title[data-ui-title-site]');
    if (!title) return;
    var translated = '';
    var key = title.getAttribute('data-ui-title-key');
    var category = title.getAttribute('data-ui-title-category');
    if (key) translated = messageFor(key, language);
    if (!translated && category) translated = translatedCategory(category, language);
    if (!translated) return;
    document.title = title.getAttribute('data-ui-title-standalone') === 'true'
      ? translated
      : translated + ' | ' + title.getAttribute('data-ui-title-site');
  }

  function setGeneratedControlLabel(selector, key, language) {
    var label = messageFor(key, language);
    if (!label) return;
    document.querySelectorAll(selector).forEach(function (element) {
      element.setAttribute('aria-label', label);
      element.setAttribute('lang', language);
    });
  }

  function translateGeneratedControls(language) {
    setGeneratedControlLabel('.post-slider .prevArrow', 'previous_image', language);
    setGeneratedControlLabel('.post-slider .nextArrow', 'next_image', language);
    setGeneratedControlLabel('.featured-post-slider .prevArrow', 'previous_featured_post', language);
    setGeneratedControlLabel('.featured-post-slider .nextArrow', 'next_featured_post', language);
  }

  function postGiscusLanguage(iframe, language, force) {
    if (!iframe || !iframe.contentWindow) return;
    if (!force && iframe.getAttribute('data-ui-giscus-language') === language) return;
    iframe.setAttribute('data-ui-giscus-language', language);
    iframe.contentWindow.postMessage({
      giscus: { setConfig: { lang: language } }
    }, 'https://giscus.app');
  }

  function giscusSourceLanguage(iframe) {
    try {
      var pathLanguage = new URL(iframe.src).pathname.split('/')[1];
      return normalizeLanguage(pathLanguage);
    } catch (_) {
      return 'ko';
    }
  }

  function syncGiscus(language) {
    var loader = document.querySelector('script[data-ui-giscus]');
    if (loader) loader.setAttribute('data-lang', language);

    document.querySelectorAll('iframe.giscus-frame').forEach(function (iframe) {
      if (!iframe.hasAttribute('data-ui-giscus-language')) {
        iframe.setAttribute('data-ui-giscus-language', giscusSourceLanguage(iframe));
      }
      if (iframe.getAttribute('data-ui-language-bound') !== 'true') {
        iframe.setAttribute('data-ui-language-bound', 'true');
        iframe.addEventListener('load', function () {
          var languageAtLoad = currentLanguage();
          if (giscusSourceLanguage(iframe) !== languageAtLoad) {
            postGiscusLanguage(iframe, languageAtLoad, true);
          } else {
            iframe.setAttribute('data-ui-giscus-language', languageAtLoad);
          }
        }, { once: true });
      }
      postGiscusLanguage(iframe, language);
    });
  }

  function translateScope(scope, language) {
    translateText(scope, language);
    translateAttribute(scope, language, 'data-ui-aria-label', 'aria-label');
    translateAttribute(scope, language, 'data-ui-placeholder', 'placeholder');
    translateAttribute(scope, language, 'data-ui-alt', 'alt');
    translateDates(scope, language);
    translateCategories(scope, language);
  }

  function updateLanguageControls(language) {
    document.querySelectorAll('[data-ui-language-option]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.getAttribute('data-ui-language-option') === language));
    });
    document.querySelectorAll('[data-ui-language-scope]').forEach(function (element) {
      element.setAttribute('lang', language);
    });
  }

  function persistLanguage(language) {
    try {
      window.localStorage.setItem(STORAGE_KEY, language);
    } catch (_) {
      // Storage can be unavailable in privacy-restricted browsers. The current page still works.
    }
  }

  function announceLanguage(language) {
    var status = document.getElementById('ui-language-status');
    if (!status) return;
    status.setAttribute('lang', language);
    status.textContent = messageFor('language_changed', language);
  }

  function applyLanguage(language, options) {
    language = normalizeLanguage(language);
    options = options || {};
    root.setAttribute('data-ui-language', language);
    translateScope(document, language);
    translateDocumentTitle(language);
    translateGeneratedControls(language);
    updateLanguageControls(language);
    syncGiscus(language);
    root.setAttribute('data-ui-language-ready', 'true');
    root.classList.remove('ui-language-pending');
    if (window.__aieconlabUILanguageFallbackTimer) {
      window.clearTimeout(window.__aieconlabUILanguageFallbackTimer);
    }
    if (options.persist) persistLanguage(language);
    if (options.announce) announceLanguage(language);
    document.dispatchEvent(new CustomEvent('aieconlab:ui-language-change', {
      detail: { language: language }
    }));
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest('[data-ui-language-option]');
    if (!button) return;
    applyLanguage(button.getAttribute('data-ui-language-option'), {
      persist: true,
      announce: true
    });
  });

  applyLanguage(currentLanguage());

  var observer = new MutationObserver(function (mutations) {
    var language = currentLanguage();
    mutations.forEach(function (mutation) {
      Array.prototype.forEach.call(mutation.addedNodes, function (node) {
        if (node.nodeType === 1) translateScope(node, language);
      });
    });
    translateGeneratedControls(language);
    syncGiscus(language);
  });
  observer.observe(document.body, { childList: true, subtree: true });
}());
