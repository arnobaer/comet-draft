// footer.js

import React from 'react';

export default class Footer extends React.Component {
  render() {
    return (
      <div id="app-footer" className="w3-container w3-light-grey w3-margin-top">
        <div className="w3-text-grey w3-small">
          <p>{this.props.meta.name} | {this.props.meta.slogan} <span className="w3-right"><a href="https://github.com/arnobaer/comet/" target="_blank">Fork me on github!</a></span></p>
          <p>Version <span>{this.props.meta.version}</span></p>
        </div>
      </div>
    );
  }
}
