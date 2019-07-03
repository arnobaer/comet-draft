// header.js

import React from 'react';
import icon from '../images/icon.svg'

export default class Header extends React.Component {
  render() {
    const {name, caption} = this.props.meta;
    const {state, color} = this.props.statemachine;
    return (
      <div id="app-header" className="w3-container w3-top w3-theme">
        <div className="w3-cell-row w3-padding">
            <div className="w3-cell w3-cell-middle">
              <img className="w3-left w3-margin-right" id="app-logo" src={icon} />
              <div className="app-title w3-left w3-margin-right">{name}</div>
              <span className="w3-left w3-margin-top w3"><span className={`w3-${color} w3-tag w3-round`}>{state}</span></span>
            </div>
            <div className="w3-cell w3-cell-middle w3-hide-small">
              <div className="w3-right w3-small">{caption}</div>
            </div>
        </div>
      </div>
    );
  }
}
