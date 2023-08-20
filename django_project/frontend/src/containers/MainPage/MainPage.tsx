import React, { useEffect, useState } from 'react';
import {useSearchParams, useLocation, useNavigate} from "react-router-dom";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {RootState} from '../../app/store';
import {useAppDispatch, useAppSelector } from '../../app/hooks';
import TabPanel, { a11yProps } from '../../components/TabPanel';
import {
  LeftSideBar,
  RightSideBar,
  LayerFilterTabs
} from './SideBar';
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
import DataList from './Data';
import Metrics from './Metrics';




enum RightSideBarMode {
  None = -1,
  Upload = 0,
  PropertySummary = 1,
  FilteredResult = 2
}

function MainPage() {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams()
  const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
  const [rightSideBarMode, setRightSideBarMode] = useState(RightSideBarMode.None) // 0: upload data, 1: property summary, 2: filtered properties summary
  const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)
  const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)

  const initialTabParam = new URLSearchParams(location.search).get('tab');
  const initialSelectedTab = initialTabParam !== null ? parseInt(initialTabParam) : 0;
  const [selectedTab, setSelectedTab] = useState(initialSelectedTab);

  useEffect(() => {
    const tabParam = new URLSearchParams(location.search).get('tab');
    if (tabParam !== null) {
      const tab = parseInt(tabParam);
      if (tab >= 0 && tab <= 3) {
        setSelectedTab(tab); // Set the selected tab based on URL parameter
      }
    }
  }, [location.search]);

  useEffect(() => {
    if (location.search !== `?tab=${selectedTab}`) {
      // Update URL when tab is changed and only if it's not already set
      navigate(`?tab=${selectedTab}`);
    }
  }, [selectedTab, navigate,location.search]);

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
      <div className="MainPage">
        <Grid container flexDirection={'row'}>
          <Grid item>
            { rightSideBarMode === RightSideBarMode.Upload ? <LeftSideBar element={Upload} /> : <LeftSideBar element={LayerFilterTabs} />}
          </Grid>
          <Grid item flex={1} className="grayBg customWidth">
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
                  <DataList/>
                </TabPanel>
                <TabPanel key={2} value={selectedTab} index={2} noPadding>
                  <Metrics/>
                </TabPanel>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        { rightSideBarMode === RightSideBarMode.PropertySummary ? <RightSideBar element={PropertySummary} /> : null}
      </div>
    </div>
  );
}

export default MainPage;
