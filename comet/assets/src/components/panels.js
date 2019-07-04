// panels.js

import React from 'react';
import Dygraph from 'dygraphs';

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

class LineChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      offset: 0,
      records: [],
    };
  }
  componentDidMount() {
    const {name} = this.props;
    const {offset} = this.state;
    fetch(`/api/collections/${name}/data/offset/${offset}`)
    .then(response => response.json())
    .then(data => {
      const {records} = data.app.collection;
      const labels = data.app.collection.metrics.map(metric => metric.label);
      var g = new Dygraph(this.refs.chart, records, {
        drawPoints: true,
        // showRoller: true,
        // valueRange: [0.0, 1.2],
        labels: labels
      });
      setInterval(() => {
        const {name} = this.props;
        const {offset} = this.state;
        fetch(`/api/collections/${name}/data/offset/${offset}`)
        .then(response => response.json())
        .then(data => {
          const {size} = data.app.collection;
          const {records} = data.app.collection;
          this.setState(prevState => ({
            records: [...prevState.records, ...records]
          }));
          g.updateOptions( { 'file': this.state.records } );
          this.setState({offset: size});
        });
      },1000);
    });
  }
  render() {
    const {name} = this.props;
    if (this.state.records)
      return <div ref="chart" style={{width: '100%'}}></div>;
    return <p>No data available.</p>;
  }
}

export default class Panels extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      collections: [],
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
          <LineChart name={collection} />
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
