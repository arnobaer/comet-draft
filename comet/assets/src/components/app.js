// app.js

import React from 'react';

import Header from './header';
import Control from './control';
import Panels from './panels';
import Params from './params';
import Devices from './devices';
import Collections from './collections';
import Jobs from './jobs';
import Services from './services';
import Settings from './settings';
import Footer from './footer';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      meta: {
        name: "COMET",
        slogan: "Control & Measurement Toolkit",
        caption: "Technical demonstrator",
        github: "https://github.com/arnobaer/comet/",
        version: "1.0.0"
      },
      statemachine: {
        state: 'undefined',
        color: 'gray'
      },
      settings: {},
      updateInterval: 500,
      waitForUpdate: false,
      params: [],
      activeJobs: [],
    }
    this.getStatus = this.getStatus.bind(this);
    this.getStateColor = this.getStateColor.bind(this);
  }
  componentDidMount() {
    // Load application settings
    fetch('/api/settings')
    .then(response => response.json())
    .then(data => this.setState({settings: data.app.settings}));
    // Run continious updates
    var updateIntervalId = setInterval(this.getStatus, this.state.updateInterval);
    this.setState({updateIntervalId: updateIntervalId});
  }
  componentWillUnmount() {
    clearInterval(this.state.updateIntervalId);
  }
  getStateColor(state) {
    switch (state) {
      case 'halted': return 'green';
      case 'configure': return 'orange';
      case 'running': return 'green';
      case 'paused': return 'orange';
      case 'stopping': return 'orange';
    }
    return 'grey';
  }
  getStatus() {
    fetch('/api/status')
    .then(response => response.json())
    .then(data => {
      const status = data.app.status;
      const state = status.state.toLowerCase();
      this.setState({
        statemachine: {
          state: state,
          color: this.getStateColor(state)
        },
        activeJobs: status.active_jobs
      });
    })
    if (this.state.statemachine.state !== 'halted') {
      fetch('/api/params')
      .then(response => response.json())
      .then(data => {
        this.setState({params: data.app.params});
      });
    }
  }
  render() {
    const {meta} = this.state;
    const {version, slogan} = this.state;
    const {statemachine} = this.state;
    const {params, settings} = this.state;
    const {activeJobs} = this.state;
    return (
      <div>
        <Header meta={meta} statemachine={statemachine} />
        <div id="app-main" className="w3-white">
          <Control statemachine={statemachine} params={params} />
          <div className="w3-row">
            <div className="w3-half w3-container">
              <Panels activeJobs={activeJobs} />
            </div>
            <div className="w3-quarter w3-container">
              <Params statemachine={statemachine} params={params} />
            </div>
            <div className="w3-quarter w3-container">
              <Devices />
              <Collections />
              <Jobs />
              <Services />
              <Settings settings={settings} />
            </div>
          </div>
        </div>
        <Footer meta={meta} />
      </div>
    );
  }
}
