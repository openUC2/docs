import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

const LABEL = {A: 'new', M: 'updated', R: 'moved', C: 'copied'};
const REPO = 'https://github.com/openUC2/docs/commit/';

export default function ChangeHistory({commits}) {
  return (
    <Layout title="Change history" description="Recent changes to the openUC2 documentation">
      <main className="container margin-vert--lg">
        <h1>Change history</h1>
        <p>The most recent changes to this documentation, taken from the git history.</p>
        {commits.map((c) => (
          <section key={c.hash} className="margin-bottom--lg">
            <h3 style={{marginBottom: '0.25rem'}}>{c.subject}</h3>
            <small>
              {c.date.slice(0, 16).replace('T', ' ')} · {c.author} ·{' '}
              <a href={REPO + c.hash}>{c.hash.slice(0, 7)}</a>
            </small>
            <ul>
              {c.files.map((f) => (
                <li key={f.permalink}>
                  <Link to={f.permalink}>{f.title}</Link> <small>({LABEL[f.status] ?? f.status})</small>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </main>
    </Layout>
  );
}
