import React from 'react';
import ResponsiveNavbar from '../../components/Navbar';
import SideBar from '../../components/SideBar';
import Map from '../../components/Map';
import './index.scss';

function MainPage() {
  return (
    <div className="App">
      <ResponsiveNavbar/>
      <div className="MainPage">
        <SideBar/>
        <Map/>      
      </div>
    </div>
  );
}

export default MainPage;
