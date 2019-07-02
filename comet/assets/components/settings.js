// settings.js

import React from 'react';

export default class Settings extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      settings: {}
    };
  }
  componentDidMount() {
    fetch('/api/settings')
    .then(response => response.json())
    .then(data => this.setState({settings: data.app.settings}));
  }
  render() {
    const settings = Object.keys(this.state.settings).map(key =>
      <li key={key}>{key}: {this.state.settings[key]}</li>
    );
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Settings</header>
        <ul id="app-devices" className="w3-ul">{settings}</ul>
      </div>
    );
  }
}
