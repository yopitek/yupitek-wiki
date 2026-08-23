/**
 * Yupitek Multi-Domain Cross-Language Navigation & SEO Hreflang System
 * 
 * Domains:
 * - en:    https://doc.yupitek.com
 * - zh-CN: https://doczhcn.yupitek.com
 * - zh-TW: https://doczhtw.yupitek.com
 */

const DOMAIN_BY_LANG = {
  en: 'https://doc.yupitek.com',
  'zh-CN': 'https://doczhcn.yupitek.com',
  'zh-TW': 'https://doczhtw.yupitek.com',
};

function updateLanguageSwitcherAndHreflang() {
  if (typeof window === 'undefined') {
    return;
  }

  const currentPath = window.location.pathname;

  // 1. Inject / update <link rel="alternate" hreflang="..."> tags in <head>
  document.head
    .querySelectorAll('link[data-yk-hreflang]')
    .forEach((el) => el.remove());

  const alternates = [
    ...Object.entries(DOMAIN_BY_LANG).map(([hreflang, domain]) => ({
      hreflang,
      href: `${domain}${currentPath}`,
    })),
    { hreflang: 'x-default', href: `${DOMAIN_BY_LANG.en}${currentPath}` },
  ];

  for (const { hreflang, href } of alternates) {
    const link = document.createElement('link');
    link.rel = 'alternate';
    link.hreflang = hreflang;
    link.href = href;
    link.setAttribute('data-yk-hreflang', '');
    document.head.appendChild(link);
  }

  // 2. Update navbar language dropdown items for cross-domain switching
  const dropdownLinks = document.querySelectorAll(
    '.dropdown__menu a[lang], .menu__list-item a[lang]'
  );

  dropdownLinks.forEach((a) => {
    const lang = a.getAttribute('lang');
    const targetDomain = DOMAIN_BY_LANG[lang];
    if (targetDomain) {
      const targetUrl = `${targetDomain}${currentPath}`;
      a.setAttribute('href', targetUrl);
      a.setAttribute('target', '_self');

      // Ensure click navigates directly across domains
      if (!a.dataset.ykBound) {
        a.dataset.ykBound = 'true';
        a.addEventListener('click', (e) => {
          e.preventDefault();
          window.location.href = `${targetDomain}${window.location.pathname}${window.location.search}${window.location.hash}`;
        });
      }
    }
  });
}

export function onRouteDidUpdate() {
  setTimeout(updateLanguageSwitcherAndHreflang, 100);
}

if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', updateLanguageSwitcherAndHreflang);
  } else {
    setTimeout(updateLanguageSwitcherAndHreflang, 50);
  }
}
