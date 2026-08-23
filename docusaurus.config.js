// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).

import {themes as prismThemes} from 'prism-react-renderer';
import remarkCjkFriendly from 'remark-cjk-friendly';
import searchLocal from '@easyops-cn/docusaurus-search-local';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Yupitek Wiki',
  tagline: 'Technical documentation for ALFA, Hak5, Flipper Zero, SDRLAB and ACS',
  favicon: 'img/favicon.ico',

  // Each locale is deployed to its own domain (see i18n.localeConfigs below).
  // The `url`/`baseUrl` here act as defaults; per-locale deployments override
  // them via localeConfigs[locale].{url, baseUrl}.
  url: 'https://doc.yupitek.com',
  baseUrl: '/',

  organizationName: 'yupitek',
  projectName: 'yupitek-wiki',

  onBrokenLinks: 'throw',

  // Per-page cross-domain hreflang, injected client-side (see module).
  // Do NOT replace with static headTags: a site-wide <head> injection
  // cannot vary per page and would point every deep page at the homepage.
  clientModules: ['./src/clientModules/yupitekHreflang.js'],

  // Multi-domain internationalization.
  // - en:    https://doc.yupitek.com       (source of truth, English)
  // - zh-CN: https://doczhcn.yupitek.com   (Simplified Chinese mirror)
  // - zh-TW: https://doczhtw.yupitek.com   (Traditional Chinese mirror)
  // Each `docusaurus build --locale <code>` deploys to its own domain.
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh-CN', 'zh-TW'],
    localeConfigs: {
      en: {
        label: 'English',
        htmlLang: 'en',
        url: 'https://doc.yupitek.com',
        baseUrl: '/',
      },
      'zh-CN': {
        label: '简体中文',
        htmlLang: 'zh-CN',
        url: 'https://doczhcn.yupitek.com',
        baseUrl: '/',
      },
      'zh-TW': {
        label: '繁體中文',
        htmlLang: 'zh-TW',
        url: 'https://doczhtw.yupitek.com',
        baseUrl: '/',
      },
    },
  },

  markdown: {
    mermaid: true,
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
          remarkPlugins: [remarkCjkFriendly],
        },
        // Wiki is documentation only; no blog.
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themes: [
    [
      searchLocal,
      /** @type {import('@easyops-cn/docusaurus-search-local').PluginOptions} */
      ({
        hashed: true,
        language: ['en', 'zh'],
        // Exclude the generated search-wide pages from results.
        indexPages: false,
        docsRouteBasePath: '/',
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/favicon-512.png',
      // Documented at https://docusaurus.io/docs/markdown-features/diagrams
      mermaid: {
        theme: {light: 'neutral', dark: 'dark'},
      },
      colorMode: {
        defaultMode: 'light',
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Yupitek Wiki',
        logo: {
          alt: 'Yupitek',
          src: 'img/logo.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'wiki-home',
            position: 'left',
            label: 'Home',
          },
          {
            type: 'doc',
            docId: 'alfa-network/alfa-index',
            position: 'left',
            label: 'ALFA Network',
          },
          {
            type: 'doc',
            docId: 'hak5/hak5-index',
            position: 'left',
            label: 'Hak5',
          },
          {
            type: 'doc',
            docId: 'flipper-zero/flipper-index',
            position: 'left',
            label: 'Flipper Zero',
          },
          {
            type: 'doc',
            docId: 'sdrlab/sdrlab-index',
            position: 'left',
            label: 'SDRLAB',
          },
          {
            type: 'doc',
            docId: 'acs/acs-index',
            position: 'left',
            label: 'ACS',
          },
          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            href: 'https://www.yupitek.com',
            label: 'Shop',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Guides',
            items: [
              {label: 'Getting Started', to: '/getting-started/'},
              {label: 'ALFA Network', to: '/alfa-network/'},
              {label: 'Hak5', to: '/hak5/'},
            ],
          },
          {
            title: 'Products',
            items: [
              {label: 'Flipper Zero', to: '/flipper-zero/'},
              {label: 'SDRLAB', to: '/sdrlab/'},
              {label: 'ACS', to: '/acs/'},
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Yupitek Official Website',
                href: 'https://www.yupitek.com',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/yupitek',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Yupitek. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
