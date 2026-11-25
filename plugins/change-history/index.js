// Builds /change-history from `git log` over docs/, linking each changed file to its page.
const path = require('path');
const {execFileSync} = require('child_process');

const MAX_COMMITS = 300; // ponytail: fixed window, paginate if older history is wanted

function readGitLog(siteDir) {
  try {
    return execFileSync(
      'git',
      ['log', `-n${MAX_COMMITS}`, '--date=iso-strict', '--name-status',
        '--pretty=format:%x1e%H%x1f%ad%x1f%an%x1f%s', '--', 'docs'],
      {cwd: siteDir, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024},
    );
  } catch (e) {
    console.warn('[change-history] git log failed, page will be empty:', e.message);
    return '';
  }
}

module.exports = function changeHistory(context) {
  return {
    name: 'change-history',
    async allContentLoaded({allContent, actions}) {
      // "docs/foo/bar.md" -> {permalink, title}
      const docs = {};
      const docsContent = allContent['docusaurus-plugin-content-docs']?.default;
      for (const version of docsContent?.loadedVersions ?? []) {
        for (const doc of version.docs) {
          docs[doc.source.replace(/^@site\//, '')] = {permalink: doc.permalink, title: doc.title};
        }
      }

      const commits = [];
      for (const block of readGitLog(context.siteDir).split('\x1e').slice(1)) {
        const [header, ...lines] = block.split('\n');
        const [hash, date, author, subject] = header.split('\x1f');
        const files = [];
        for (const line of lines) {
          if (!line) continue;
          const parts = line.split('\t');
          const status = parts[0][0]; // A, M, D, R, C
          const doc = docs[parts[parts.length - 1]];
          // Only list files that are pages in this build (skips images and excluded variants).
          if (doc && status !== 'D') files.push({status, ...doc});
        }
        if (files.length) commits.push({hash, date, author, subject, files});
      }

      const data = await actions.createData('change-history.json', JSON.stringify(commits));
      actions.addRoute({
        path: path.posix.join(context.baseUrl, 'change-history'),
        component: path.resolve(__dirname, 'ChangeHistory.js'),
        modules: {commits: data},
        exact: true,
      });
    },
  };
};
