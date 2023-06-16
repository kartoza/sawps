import React, { useEffect, useState } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {RootState} from '../../app/store';
import {useAppDispatch, useAppSelector } from '../../app/hooks';
import ResponsiveNavbar from '../../components/Navbar';
import TabPanel, { a11yProps } from '../../components/TabPanel';
import { LeftSideBar, RightSideBar } from './SideBar';
import Upload from './Upload';
import Map from './Map';
import './index.scss';
import { PropertySummary } from './Property';
import { MapSelectionMode } from "../../models/Map";
import { UploadMode } from "../../models/Upload";
import {
    setUploadState
} from '../../reducers/UploadState';
import {
    setSelectedParcels,
    resetSelectedProperty,
    setMapSelectionMode
} from '../../reducers/MapState';


enum RightSideBarMode {
  None = -1,
  Upload = 0,
  PropertySummary = 1,
  FilteredResult = 2
}

function MainPage() {
  const dispatch = useAppDispatch()
  const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
  const [selectedTab, setSelectedTab] = useState(0)
  const [rightSideBarMode, setRightSideBarMode] = useState(RightSideBarMode.None) // 0: upload data, 1: property summary, 2: filtered properties summary
  const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)
  const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)

  useEffect(() => {
    if (rightSideBarMode === RightSideBarMode.None) {
      dispatch(setUploadState(UploadMode.None))
      dispatch(setMapSelectionMode(MapSelectionMode.Property))
      dispatch(resetSelectedProperty())
      dispatch(setSelectedParcels([]))
    }
  }, [rightSideBarMode])

  useEffect(() => {
    if (mapSelectionMode === MapSelectionMode.Property && uploadMode === UploadMode.None) {
      if (propertyItem.id > 0) {
        // show right side bar
        setRightSideBarMode(RightSideBarMode.PropertySummary)
      } else {
        setRightSideBarMode(RightSideBarMode.None)
      }
    } else if (uploadMode === UploadMode.PropertySelected && rightSideBarMode !== RightSideBarMode.Upload) {
      setSelectedTab(3)
      setRightSideBarMode(RightSideBarMode.Upload)
    }
  }, [propertyItem, mapSelectionMode, uploadMode])

  return (
    <div className="App">
      {/* <ResponsiveNavbar /> */}
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
                        if (newValue === 3) {
                          setRightSideBarMode(RightSideBarMode.Upload)
                          dispatch(setUploadState(UploadMode.SelectProperty))
                        } else {
                          setRightSideBarMode(RightSideBarMode.None)
                        }
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
                <TabPanel key={0} value={selectedTab} index={-1} indexList={[0, 3]} noPadding>
                  <Map />
                </TabPanel>
                <TabPanel key={1} value={selectedTab} index={1} noPadding>
                </TabPanel>
                <TabPanel key={2} value={selectedTab} index={2} noPadding>
                </TabPanel>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        { rightSideBarMode === RightSideBarMode.Upload ? <RightSideBar element={Upload} /> : null}
        { rightSideBarMode === RightSideBarMode.PropertySummary ? <RightSideBar element={PropertySummary} /> : null}
      </div>
    </div>
  );
}

export default MainPage;
