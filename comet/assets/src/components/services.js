// services.js

import React from 'react';

export default class Services extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      services: []
    };
  }
  componentDidMount() {
    fetch('/api/services')
    .then(response => response.json())
    .then(data => this.setState({services: data.app.services}));
  }
  render() {
    const services = this.state.services.map(service =>
      <li key={service}>{service}</li>
    );
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Services</header>
        <ul id="app-devices" className="w3-ul">{services}</ul>
      </div>
    );
  }
}
