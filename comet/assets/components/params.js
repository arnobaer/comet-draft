// params.js

import React from 'react';

function getType(type) {
  switch (type) {
    case 'int':
    case 'float':
      return 'number';
    default:
      return 'text';
  }
}

class ParamInput extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const id = `app-param-${this.props.name}`
    const unit = this.props.unit ? ` [${this.props.unit}]` : '';
    const type = getType(this.props.type);
    return (
      <div>
        <label htmlFor={id}>{this.props.label}{unit}</label>
        <input id={id} className="w3-input" type={type} name={this.props.name} defaultValue={this.props.value} disabled={this.props.disabled} />
      </div>
    );
  }
}

export default class Params extends React.Component {
  render() {
    const disabled = this.props.currentState !== 'halted';
    const params = this.props.params.map(param =>
      <ParamInput disabled={disabled} key={param.name} name={param.name} label={param.label} type={param.type} value={param.value} unit={param.unit} />
    );
    return (
      <div id="app-component-params">

        <div className="w3-card">
          <header className="w3-panel w3-light-grey w3-padding w3-margin-top">Parameters</header>
          <div id="app-params" className="w3-container">
            {params}
          </div>
        </div>

      </div>
    );
  }
}
