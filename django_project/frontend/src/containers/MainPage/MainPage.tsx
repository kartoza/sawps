import React, { useState } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import { Button } from '@mui/material';
import ResponsiveNavbar from '../../components/Navbar';
import TabPanel, { a11yProps } from '../../components/TabPanel';
import { LeftSideBar, RightSideBar } from './SideBar';
import Map from './Map';
import './index.scss';

function MainPage() {
  const [selectedTab, setSelectedTab] = useState(0)
  const [showRightSideBar, setShowRightSideBar] = useState(false)


  return (
    <div className="App">
      <ResponsiveNavbar />
      <div className="MainPage">
        <Grid container flexDirection={'row'}>
          <Grid item>
            <LeftSideBar />
          </Grid>
          <Grid item flex={1}>
            <Grid container className="Content" flexDirection={'column'}>
              <Grid item>
                <Box className="TabHeaders">
                  <Tabs value={selectedTab}
                      onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTab(newValue)
                      }} aria-label="Main Page Tabs"
                  >
                      <Tab key={0} label={'MAP'} {...a11yProps(0)} />
                      <Tab key={1} label={'DATA'} {...a11yProps(1)} />
                      <Tab key={2} label={'METRICS'} {...a11yProps(2)} />
                      <Tab key={3} label={'DATA UPLOAD'} {...a11yProps(3)} />
                  </Tabs>
               </Box>
              </Grid>
              <Grid item className="TabPanels">
                <TabPanel key={0} value={selectedTab} index={0} noPadding>
                  <Map />
                </TabPanel>
                <TabPanel key={1} value={selectedTab} index={1} noPadding>
                    <Button onClick={() => {
                      setShowRightSideBar(!showRightSideBar)
                  }}>Open Right Side</Button>
                </TabPanel>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        { showRightSideBar ? <RightSideBar /> : null}
      </div>
    </div>
  );
}

export default MainPage;
