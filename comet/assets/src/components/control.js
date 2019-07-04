// control.js

import React from 'react';

export default class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      engaged: false
    };
    this.onEngage = this.onEngage.bind(this);
    this.onStart = this.onStart.bind(this);
    this.onStop = this.onStop.bind(this);
    this.onPause = this.onPause.bind(this);
  }
  onEngage(event) {
    this.setState({
      engaged: !this.state.engaged,
    });
  }
  onStart(event) {
    // Start a run, post parameters
    fetch('/api/start', {
      method: 'post',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(this.props.params)
    })
    .then(response => {
    });
  }
  onStop(event) {
    // Stop current run
    fetch('/api/stop', {method: 'post'})
    .then(response => {
    });
  }
  onPause(event) {
    // Pause/Unpause current run
    fetch('/api/pause', {method: 'post'})
    .then(response => {
    });
  }
  render() {
    const {engaged} = this.state;
    const {state, color} = this.props.statemachine;
    return (
      <div className="w3-row">
        <div className="w3-full w3-container">

          <div className="w3-card">

            <div id="app-control" className="w3-light-grey w3-padding">
              <button className="w3-button w3-theme" onClick={this.onEngage}>{engaged == true ? "Disengage" : "Engage"}</button>
              <button className="w3-button w3-green" onClick={this.onStart} disabled={!(engaged && state == 'halted')}>Start</button>
              <button className="w3-button w3-red" onClick={this.onStop} disabled={!(engaged && (state == 'running' || state == 'paused'))}>Stop</button>
              <button className="w3-button w3-orange" onClick={this.onPause} disabled={!(engaged && (state == 'running' || state == 'paused'))}>{state == 'paused' ? "Continue" : "Pause"}</button>
            </div>

            <div>
              <div className="w3-padding">State: <span className={`w3-${color} w3-tag w3-round`}>{state}</span></div>
            </div>

          </div>

        </div>
      </div>
    );
  }
}
