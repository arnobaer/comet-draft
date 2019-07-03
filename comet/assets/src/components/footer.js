// footer.js

import React from 'react';

export default class Footer extends React.Component {
  render() {
    const {name, slogan, github, version} = this.props.meta;
    return (
      <div id="app-footer" className="w3-container w3-light-grey">
        <div className="w3-text-grey w3-small">
          <p>{name} | {slogan} <span className="w3-right"><a href="{github}" target="_blank">Fork me on github!</a></span></p>
          <p>Version <span>{version}</span></p>
        </div>
      </div>
    );
  }
}
