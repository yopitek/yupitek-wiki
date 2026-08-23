/**
 * Cross-domain hreflang injection (multi-domain i18n).
 *
 * Each locale is deployed to its own domain (see i18n.localeConfigs in
 * docusaurus.config.js) with an identical URL structure (baseUrl '/'),
 * so the language alternates of any page can be derived from the
 * current pathname alone.
 *
 * Injected tags carry `data-yk-hreflang` and are removed before each
 * re-injection, keeping the operation idempotent across route changes.
 */
const DOMAIN_BY_LANG = {
  en: 'https://doc.yupitek.com',
  'zh-CN': 'https://doczhcn.yupitek.com',
  'zh-TW': 'https://doczhtw.yupitek.com',
};

function injectHreflang() {
  if (typeof window === 'undefined') {
    return;
  }
  const lang = document.documentElement.lang;
  const origin = DOMAIN_BY_LANG[lang];
  if (!origin) {
    return;
  }

  const path = window.location.pathname;

  // Idempotency: drop tags injected by a previous route first.
  document.head
    .querySelectorAll('link[data-yk-hreflang]')
    .forEach((el) => el.remove());

  const alternates = [
    ...Object.entries(DOMAIN_BY_LANG).map(([hreflang, domain]) => ({
      hreflang,
      href: `${domain}${path}`,
    })),
    {hreflang: 'x-default', href: `${DOMAIN_BY_LANG.en}${path}`},
  ];

  for (const {hreflang, href} of alternates) {
    const link = document.createElement('link');
    link.rel = 'alternate';
    link.hreflang = hreflang;
    link.href = href;
    link.setAttribute('data-yk-hreflang', '');
    document.head.appendChild(link);
  }
}

export function onRouteDidUpdate() {
  injectHreflang();
}

// Initial page load.
injectHreflang();
