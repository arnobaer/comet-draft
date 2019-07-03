// collections.js

import React from 'react';

export default class Collections extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collections: []
    };
  }
  componentDidMount() {
    fetch('/api/collections')
    .then(response => response.json())
    .then(data => this.setState({collections: data.app.collections}));
  }
  render() {
    const collections = this.state.collections.map(collection =>
      <li key={collection}>{collection}</li>
    );
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Collections</header>
        <ul id="app-devices" className="w3-ul">{collections}</ul>
      </div>
    );
  }
}
