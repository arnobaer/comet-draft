// devices.js

import React from 'react';

export default class Devices extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      devices: []
    };
  }
  componentDidMount() {
    fetch('/api/devices')
    .then(response => response.json())
    .then(data => this.setState({devices: data.app.devices}));
  }
  render() {
    const devices = this.state.devices.map(device =>
      <li key={device}>{device} <span className="w3-tag w3-round w3-green w3-right">OK</span></li>
    );
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Devices</header>
        <ul id="app-devices" className="w3-ul">{devices}</ul>
      </div>
    );
  }
}
