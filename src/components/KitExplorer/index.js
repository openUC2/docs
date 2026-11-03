import React, {useState} from 'react';
import Link from '@docusaurus/Link';
import {useAllDocsData} from '@docusaurus/plugin-content-docs/client';
import data from './kits.json';
import styles from './styles.module.css';

const kitById = Object.fromEntries(data.kits.map((k) => [k.id, k]));

// doc id -> url; null = not documented, false = id not found (broken)
function useDocUrl() {
  const paths = {};
  for (const plugin of Object.values(useAllDocsData())) {
    for (const version of plugin.versions) {
      for (const doc of version.docs) paths[doc.id] = doc.path;
    }
  }
  return (doc) => (!doc ? null : doc.startsWith('http') ? doc : paths[doc] || false);
}

function DocLink({url, label = 'Tutorial'}) {
  if (url) return <Link to={url}>📖 {label}</Link>;
  return <span className={styles.missing}>{url === false ? '⚠️ Broken doc link' : '✏️ Not documented yet'}</span>;
}

function KitChip({kit, onClick}) {
  return (
    <span className={styles.chip}>
      <button className="button button--sm button--outline button--primary" onClick={onClick}>{kit.name}</button>
      {kit.shop && <a href={kit.shop} target="_blank" rel="noopener noreferrer">🛒 Shop</a>}
    </span>
  );
}

export default function KitExplorer() {
  const docUrl = useDocUrl();
  const [tab, setTab] = useState('experiments');
  const [kitId, setKitId] = useState(data.kits[0].id);
  const [expId, setExpId] = useState(null);
  const [query, setQuery] = useState('');

  const showKit = (id) => { setKitId(id); setTab('boxes'); };
  const undocumented = data.experiments.filter((e) => !docUrl(e.doc));
  const q = query.toLowerCase();
  const experiments = data.experiments.filter((e) => (e.name + ' ' + e.description).toLowerCase().includes(q));
  const kit = kitById[kitId];

  const tabs = [['experiments', 'By experiment'], ['boxes', 'By box'], ['todo', `Undocumented (${undocumented.length})`]];

  return (
    <div className={styles.explorer}>
      <ul className="pills">
        {tabs.map(([id, label]) => (
          <li key={id} className={'pills__item' + (tab === id ? ' pills__item--active' : '')} onClick={() => setTab(id)}>{label}</li>
        ))}
      </ul>

      {tab === 'experiments' && (
        <>
          <input className={styles.search} placeholder="Search experiments…" value={query} onChange={(e) => setQuery(e.target.value)} />
          {data.kits.map((k) => {
            // group each experiment under the last (most advanced) box it needs
            const list = experiments.filter((e) => e.kits[e.kits.length - 1] === k.id);
            if (!list.length) return null;
            return (
              <div key={k.id}>
                <h3 className={styles.group}>{k.name}</h3>
                {list.map((e) => (
                  <div key={e.id} className={styles.row + (expId === e.id ? ' ' + styles.open : '')}>
                    <button className={styles.title} onClick={() => setExpId(expId === e.id ? null : e.id)}>
                      {e.name} {!docUrl(e.doc) && <span className={styles.badge}>no docs</span>}
                    </button>
                    {expId === e.id && (
                      <div className={styles.detail}>
                        <p>{e.description}</p>
                        <p><DocLink url={docUrl(e.doc)} /></p>
                        <strong>You need:</strong>
                        <div className={styles.chips}>{e.kits.map((id) => <KitChip key={id} kit={kitById[id]} onClick={() => showKit(id)} />)}</div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            );
          })}
        </>
      )}

      {tab === 'boxes' && (
        <>
          <div className={styles.chips}>
            {data.kits.map((k) => (
              <button key={k.id} className={'button button--sm ' + (k.id === kitId ? 'button--primary' : 'button--secondary')} onClick={() => setKitId(k.id)}>{k.name}</button>
            ))}
          </div>
          <div className={'card ' + styles.card}>
            <div className="card__body">
              <h3>{kit.name}</h3>
              <p>{kit.description}</p>
              <p className={styles.links}>
                {kit.shop ? <a href={kit.shop} target="_blank" rel="noopener noreferrer">🛒 Buy in shop</a> : <span className={styles.missing}>Not in the shop yet</span>}
                <DocLink url={docUrl(kit.doc)} label="Box documentation" />
              </p>
              {kit.requires.length > 0 && (
                <>
                  <strong>Requires:</strong>
                  <div className={styles.chips}>{kit.requires.map((id) => <KitChip key={id} kit={kitById[id]} onClick={() => setKitId(id)} />)}</div>
                </>
              )}
              <strong>Contents:</strong>
              <ul>{kit.contents.map((c) => <li key={c}>{c}</li>)}</ul>
              <strong>Experiments with this box:</strong>
              <ul>
                {data.experiments.filter((e) => e.kits.includes(kit.id)).map((e) => (
                  <li key={e.id}>
                    {e.name} – <DocLink url={docUrl(e.doc)} />
                    {e.kits.length > 1 && <small> (needs {e.kits.map((id) => kitById[id].name).join(' + ')})</small>}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}

      {tab === 'todo' && (
        <table>
          <thead><tr><th>Experiment</th><th>Boxes</th><th>Status</th></tr></thead>
          <tbody>
            {undocumented.map((e) => (
              <tr key={e.id}>
                <td><strong>{e.name}</strong><br /><small>{e.description}</small></td>
                <td>{e.kits.map((id) => kitById[id].name).join(', ')}</td>
                <td><DocLink url={docUrl(e.doc)} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
