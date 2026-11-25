import React from 'react';
import Content from '@theme-original/DocItem/Content';
import Link from '@docusaurus/Link';
import {useDoc} from '@docusaurus/plugin-content-docs/client';

// UTC so the server-rendered and hydrated text match.
const fmt = new Intl.DateTimeFormat('en-GB', {
  dateStyle: 'medium',
  timeStyle: 'short',
  timeZone: 'UTC',
});

export default function ContentWrapper(props) {
  const {lastUpdatedAt, lastUpdatedBy} = useDoc().metadata;
  return (
    <>
      {lastUpdatedAt && (
        <div className="theme-last-updated margin-bottom--md" style={{fontSize: '0.85em', opacity: 0.75}}>
          Last updated:{' '}
          <time dateTime={new Date(lastUpdatedAt).toISOString()}>
            {fmt.format(lastUpdatedAt)} UTC
          </time>
          {lastUpdatedBy && <> by {lastUpdatedBy}</>}
          {' · '}
          <Link to="/change-history">change history</Link>
        </div>
      )}
      <Content {...props} />
    </>
  );
}
