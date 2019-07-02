// control.js

import React from 'react';

export default class Control extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.onEngage = this.onEngage.bind(this);
    this.onStart = this.onStart.bind(this);
    this.onStop = this.onStop.bind(this);
    this.onPause = this.onPause.bind(this);
  }
  componentDidMount() {
    this.setState({engaged: false});
  }
  onEngage(event) {
    this.setState({
      engaged: !this.state.engaged,
    });
  }
  onStart(event) {
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
    fetch('/api/stop', {method: 'post'})
    .then(response => {
    });
  }
  onPause(event) {
    fetch('/api/pause', {method: 'post'})
    .then(response => {
    });
  }
  render() {
    const stateClassName = `w3-${this.props.currentStateColor} w3-tag`;
    return (
      <div className="w3-row">
        <div className="w3-full w3-container">

          <div className="w3-card">

            <div id="app-control" className="w3-light-grey">
              <button className="w3-button w3-theme" onClick={this.onEngage}>{this.state.engaged == true ? "Disengage" : "Engage"}</button>
              <button className="w3-button w3-green" onClick={this.onStart} disabled={!(this.state.engaged && this.props.currentState == 'halted')}>Start</button>
              <button className="w3-button w3-red" onClick={this.onStop} disabled={!(this.state.engaged && (this.props.currentState == 'running' || this.props.currentState == 'paused'))}>Stop</button>
              <button className="w3-button w3-orange" onClick={this.onPause} disabled={!(this.state.engaged && (this.props.currentState == 'running' || this.props.currentState == 'paused'))}>{this.props.currentState == 'paused' ? "Continue" : "Pause"}</button>
            </div>

            <div>
              <div className="w3-padding">State: <span className={stateClassName}>{this.props.currentState}</span></div>
            </div>

          </div>

        </div>
      </div>
    );
  }
}
