// panels.js

import React from 'react';

function JobList(props) {
  const jobs = props.jobs;
  if (jobs.length) {
    const items = jobs.map((job) =>
      <li key={job[0].toLowerCase()}>{job[0]} {job[1].toFixed(2)} %</li>
    );
    return (
      <ul className="w3-ul">{items}</ul>
    );
  }
  return (<p>No active jobs.</p>);
}

export default class Panels extends React.Component {
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
    const panels = this.state.collections.map(collection =>
      <div key={collection} className="w3-card">
        <header className="w3-panel w3-light-grey w3-padding w3-margin-top">{collection} chart</header>
        <div className="w3-container app-panel-content">
          <div id={'dygraph_' + collection} style={{width: '100%', height: '300px'}}></div>
        </div>
      </div>
    );
    return (
      <div id="app-component-panels">

        <div className="w3-card">
          <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Job panel</header>
          <div className="w3-container app-panel-content">
            <JobList jobs={this.props.activeJobs}/>
          </div>
        </div>

        {panels}

      </div>
    );
  }
}
