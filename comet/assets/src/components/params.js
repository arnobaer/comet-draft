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
  render() {
    const {name, label, type, value, unit} = this.props.param;
    const id = `app-param-${name}`
    const suffix = unit ? ` [${unit}]` : '';
    const inputType = getType(type);
    return (
      <div className="w3-margin-bottom">
        <label htmlFor={id}>{label}{suffix}</label>
        <input id={id} className="w3-input" type={inputType} name={name} defaultValue={value} disabled={this.props.disabled} />
      </div>
    );
  }
}

export default class Params extends React.Component {
  render() {
    const {state, color} = this.props.statemachine;
    const disabled = state !== 'halted';
    const params = this.props.params.map(param =>
      <ParamInput key={param.name} disabled={disabled} param={param} />
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
