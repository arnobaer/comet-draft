// settings.js

import React from 'react';

function Tree(props) {
  const items = Object.keys(props.items).map(key => {
    const item = props.items[key];
    if (typeof item === 'object' && item !== null) {
      return (
        <li key={key}>{key}:
          <Tree items={item} />
        </li>
      );
    }
    return (
      <li key={key}>{key}: {item}</li>
    );
  });
  return (
    <ul className="w3-ul">{items}</ul>
  );
}

export default class Settings extends React.Component {
  render() {
    const items = this.props.settings;
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Settings</header>
        <Tree items={items} />
      </div>
    );
  }
}
