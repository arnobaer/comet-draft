// jobs.js

import React from 'react';

export default class Jobs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      jobs: []
    };
  }
  componentDidMount() {
    fetch('/api/jobs')
    .then(response => response.json())
    .then(data => this.setState({jobs: data.app.jobs}));
  }
  render() {
    const jobs = this.state.jobs.map(job =>
      <li key={job}>{job}</li>
    );
    return (
      <div className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Jobs</header>
        <ul id="app-devices" className="w3-ul">{jobs}</ul>
      </div>
    );
  }
}
