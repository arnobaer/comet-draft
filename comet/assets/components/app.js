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
        version: "1.0.0",
      },
      updateInterval: 500,
      waitForUpdate: false,
      params: [],
      currentState: 'undefined',
      currentStateColor: 'gray',
      activeJobs: [],
    }
    this.getStatus = this.getStatus.bind(this);
    this.getStateColor = this.getStateColor.bind(this);
  }
  componentDidMount() {
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
        currentState: state,
        currentStateColor: this.getStateColor(state),
        activeJobs: status.active_jobs
      });
    })
    fetch('/api/params')
    .then(response => response.json())
    .then(data => {
      this.setState({params: data.app.params});
    });
  }
  render() {
    const {meta} = this.state;
    const {version, slogan} = this.state;
    return (
      <div>
        <Header meta={meta} currentState={this.state.currentState} currentStateColor={this.state.currentStateColor} />
        <div id="app-main" className="w3-white">
          <Control params={this.state.params} currentState={this.state.currentState} currentStateColor={this.state.currentStateColor} />
          <div className="w3-row">
            <div className="w3-half w3-container">
              <Panels activeJobs={this.state.activeJobs} />
            </div>
            <div className="w3-quarter w3-container">
              <Params currentState={this.state.currentState} params={this.state.params}/>
            </div>
            <div className="w3-quarter w3-container">
              <Devices />
              <Collections />
              <Jobs />
              <Services />
              <Settings />
            </div>
          </div>
        </div>
        <Footer meta={meta} />
      </div>
    );
  }
}
