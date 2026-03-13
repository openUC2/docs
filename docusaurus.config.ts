import type {Config} from '@docusaurus/types';
import type {Options, ThemeConfig} from '@docusaurus/preset-classic';

import {themes} from 'prism-react-renderer';
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

import {siteURL, baseURL, variant, releaseChannel, shortTitle, announcement, buildDate} from './config/site';

/** @type {() => Promise<import('@docusaurus/types').Config>} */
module.exports = async function createConfigAsync() {
  const math = (await import('remark-math')).default;
  const katex = (await import('rehype-katex')).default;

  return {
    title: shortTitle,
    tagline: 'Documentation for openUC2\'s products and projects',
    url: siteURL,
    baseUrl: baseURL,
    onBrokenLinks: 'throw',
    onBrokenAnchors: 'throw',
    favicon: 'img/favicon.ico',

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.
    organizationName: 'openUC2', // Usually your GitHub org/user name.
    projectName: 'docs', // Usually your repo name.

    // Even if you don't use internalization, you can use this field to set useful
    // metadata like html lang. For example, if your site is Chinese, you may want
    // to replace "en" with "zh-Hans".
    i18n: {
      defaultLocale: 'en',
      locales: ['en'],
    },

    plugins: [
      [
        'docusaurus-plugin-dotenv',
        {
          systemvars: true,
        },
      ],
      [
        '@docusaurus/plugin-client-redirects',
        {
          redirects: require(`./config/redirects.js`)(variant),
        },
      ],
      './plugins/html-assets',
      // NOTE: docusaurus-plugin-papersaurus is not compatible with Docusaurus v3.
      // Uncomment or replace once a v3-compatible version is available.
      // [
      //   'docusaurus-plugin-papersaurus',
      //   {
      //     keepDebugHtmls: true,
      //     addDownloadButton: true,
      //     autoBuildPdfs: false,
      //     ignoreDocs: ['licenses'],
      //     author: 'Benedict Diederich',
      //     puppeteerTimeout: 300000,
      //   },
      // ],
    ],

    presets: [
      [
        'classic',
        /** @type {import('@docusaurus/preset-classic').Options} */
        ({
          docs: {
            routeBasePath: '/',
            sidebarPath: require.resolve(`./config/sidebars.${variant}.ts`),
            remarkPlugins: [math],
            rehypePlugins: [katex],
            // Please change this to your repo.
            // Remove this to remove the "edit this page" links.
            //editUrl:
            //  'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          },
          blog: false,
          theme: {
            customCss: require.resolve('./src/css/custom.css'),
          },
          gtag: {
            trackingID: 'G-GTM-N3FGG2VX',
            anonymizeIP: true,
          },
        } satisfies Options),
      ],
    ],
    stylesheets: [
      {
        href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
        type: 'text/css',
        integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
        crossorigin: 'anonymous',
      },
    ],
    themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      announcementBar: ((announcement) => {
        if (announcement === '') {
          return undefined;
        }
        return {
          content: announcement,
          isCloseable: false,
          backgroundColor: 'var(--ifm-color-warning-contrast-background)',
          textColor: 'var(--ifm-color-warning-contrast-foreground)',
        };
      })(announcement),
      navbar: {
        title: shortTitle,
        logo: {
          alt: 'openUC2 Logo',
          src: 'img/Artboard4@4x.png',
        },
        items: require(`./config/navbar-items.${variant}.js`),
      },
      algolia: {
        // The application ID provided by Algolia
        appId: 'DB3UCAMZ89',

        // Public API key: it is safe to commit it
        apiKey: 'ee1437989ff3a8cb821cc0ec3cddc083',

        indexName: `docs-${releaseChannel}`,

        // Optional: see doc section below
        contextualSearch: true,

        // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
        //externalUrlRegex: 'external\\.com|domain\\.com',

        // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
        /*replaceSearchResultPathname: {
          from: '/docs/', // or as RegExp: /\/docs\//
          to: '/',
        },

        // Optional: Algolia search parameters
        searchParameters: {},

        // Optional: path for search page that enabled by default (`false` to disable it)
        searchPagePath: 'search',
        */

        //... other Algolia params
      },
      footer: {
        style: 'dark',
        links: [
          require(`./config/footer-docs.${variant}.js`)(releaseChannel),
          {
            title: 'Community',
            items: [
              {
                label: 'Discourse',
                href: 'https://youseetoo.org',
              },
              {
                label: 'LinkedIn',
                href: 'https://www.linkedin.com/company/openuc2/',
              },
              {
                label: 'Bluesky',
                href: 'https://bsky.app/profile/openuc2.bsky.social',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                href: 'https://openuc2.com/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/openUC2/',
              },
              {
                label: 'Contact',
                href: 'https://openuc2.com/imprint/',
              },
            ],
          },
        ],
        copyright: ((update, channel) => {
          if (!update) {
            return 'Copyright openUC2.';
          }
          switch (channel) {
            case '':
            case 'stable':
            case 'production':
            case 'prod':
              return `Copyright openUC2. Last update: ${update}.`;
            case 'offline':
              return `Copyright openUC2. Offline snapshot: ${update}.`;
            default:
              return `Copyright openUC2. Last <strong>${releaseChannel}</strong> preview update: ${update}.`;
          }
        })(buildDate, releaseChannel),
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['bash', 'diff', 'json'],
      },
    } satisfies ThemeConfig),
  } satisfies Config;
};
