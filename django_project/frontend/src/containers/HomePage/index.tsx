import React from 'react';
import ResponsiveNavbar from '../../components/Navbar';
import './index.scss';

function HomePage() {
  return (
    <div className="App">
      <ResponsiveNavbar/>
      <div className="App-content">
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          React
        </a>
      </div>
    </div>
  );
}

export default HomePage;
