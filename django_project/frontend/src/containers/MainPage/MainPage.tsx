import React, {useEffect, useState} from 'react';
import {useLocation, useNavigate} from "react-router-dom";
import {v4 as uuidv4} from 'uuid';
import Button from '@mui/material/Button';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import MenuIcon from '@mui/icons-material/Menu';
import {RootState} from '../../app/store';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import TabPanel, {a11yProps} from '../../components/TabPanel';
import {LayerFilterTabs, LeftSideBar, RightSideBar} from './SideBar';
import Upload from './Upload';
import Map from './Map';
import './index.scss';
import {PropertySummary} from './Property';
import {MapSelectionMode, MapEvents} from "../../models/Map";
import {UploadMode} from "../../models/Upload";
import {setUploadState} from '../../reducers/UploadState';
import {resetMapState, resetSelectedProperty, setMapSelectionMode, setSelectedParcels, triggerMapEvent} from '../../reducers/MapState';
import DataList from './Data';
import Metrics from './Metrics';
import Trends from './Trends';
import { HelperContainerWithToggle } from "../../components/HelperContainer";
import { setStartYear, DEFAULT_START_YEAR_FILTER } from '../../reducers/SpeciesFilter';

const tabNames = ['map', 'reports', 'charts', 'trends', 'upload'];

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
  const uploadMode = useAppSelector((state: RootState) => state.uploadState.uploadMode)
  const [rightSideBarMode, setRightSideBarMode] = useState(RightSideBarMode.None) // 0: upload data, 1: property summary, 2: filtered properties summary
  const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)
  const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
  const isMapReady = useAppSelector((state: RootState) => state.mapState.isMapReady)

  const initialTabParam = new URLSearchParams(location.search).get('tab');
  const initialSelectedTab = initialTabParam !== null ? parseInt(initialTabParam) : 0;
  const [selectedTab, setSelectedTab] = useState(initialSelectedTab);
  const isUploadUrl = location.pathname === '/upload';
  const [prevPath, setPrevPath] = useState('');

  useEffect(() => {
    const handlePopState = () => {
      setPrevPath(location.pathname);
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  const tabNameToValue: { [key: string]: number } = {
    'map': 0,
    'reports': 1,
    'charts': 2,
    'trends': 3,
    'upload': 4,
  };

  useEffect(() => {
    const tabParam = new URLSearchParams(location.search).get('tab');
    if (tabParam !== null) {
      const tabName = Object.keys(tabNameToValue).find(key => tabNameToValue[key] === parseInt(tabParam));
      if (tabName) {
        setSelectedTab(tabNameToValue[tabName]); // Set the selected tab based on URL parameter
      }
    }
  }, [location.search]);

  useEffect(() => {
    const selectedTabName = tabNames[selectedTab];
    const newPath = `/${selectedTabName}`;
    if ([1, 2, 3].includes(selectedTab)) {
      // dispatch to reset map state in data or charts tab
      dispatch(resetMapState())
    }

    const currentPathHasSlash = location.pathname.endsWith('/');
    const adjustedNewPath = currentPathHasSlash && !newPath.endsWith('/') ? `${newPath}/` : newPath;

    const isHomePage = location.pathname === '/';
    if (isHomePage && location.pathname !== adjustedNewPath) {
      window.history.pushState(null, '', adjustedNewPath);
    } else if (!isHomePage && location.pathname !== adjustedNewPath) {
      navigate(newPath); // Update the URL with the tab name
    }

    if (isUploadUrl) {
      setRightSideBarMode(RightSideBarMode.Upload);
      dispatch(setUploadState(UploadMode.SelectProperty));
      return; //hide all tabs
    }

    // Replace the tab parameter in the URL
    if (!isHomePage) {
      const newUrl = window.location.href.replace(/\?tab=\d/, adjustedNewPath);
      window.history.replaceState(null, '', newUrl);
    }

    if (prevPath === '/map/' && selectedTabName === 'upload') {
      navigate('/');
      window.location.href = '/'
    }
    setPrevPath(location.pathname);

  }, [selectedTab, navigate, location.pathname, isUploadUrl]);

  useEffect(() => {
    if (!isUploadUrl) return;
    if (!isMapReady) return;
    dispatch(triggerMapEvent({
      'id': uuidv4(),
      'name': MapEvents.UPLOAD_MAP_NGI_BASE,
      'date': Date.now(),
      'payload': null
  }))
  }, [isUploadUrl, isMapReady])

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
      setSelectedTab(4)
      setRightSideBarMode(RightSideBarMode.Upload)
    }
  }, [propertyItem, mapSelectionMode, uploadMode])

  const [showLeftSidebar, setShowLeftSidebar] = useState(true);
  const [height, setHeight] = useState(0);
  const toggleShowFilter = () => {
    setShowLeftSidebar(!showLeftSidebar);
  }

  const [tab, setTab] = useState<string>('')

  useEffect(() => {
      const pathname = window.location.pathname.replace(/\//g, '');
      setTab(pathname)
  }, [window.location.pathname])

  return (
    <div className="App">
      <div className={`MainPage MainPage-${tab}`}>
        <Grid container flexDirection={'row'} id={'main-container'}>
          <Grid item
                id={'toggle-left-sidebar'}
                xs={12} md={12}
          >
              <Button variant="outlined" onClick={toggleShowFilter}>
                <MenuIcon/>
              </Button>
          </Grid>
          <Grid item
                id={'left-sidebar-container'}
                xs={12} md={12}
                className={showLeftSidebar ? '' : 'hidden'}
          >
            { rightSideBarMode === RightSideBarMode.Upload ? <LeftSideBar element={Upload} /> : <LeftSideBar element={LayerFilterTabs} additionalProps={{
              'selectedMainTabIdx': selectedTab
            }} />}
          </Grid>
          <Grid item flex={1}
                xs={12} md={12}
                id={'right-sidebar-container'}
                className={"grayBg customWidth"}>
            <Grid container className="Content" flexDirection={'row'}>
              <Grid item
                    xs={12} md={12}
                    lg={12}
                    className='ContentTabHeaders'
              >
                <Box className="TabHeaders" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  {rightSideBarMode === RightSideBarMode.Upload || isUploadUrl ? null : (
                    <Tabs
                      value={selectedTab}
                      onChange={(event: React.SyntheticEvent, newValue: number) => {
                        const tabNames = ['map', 'reports', 'charts', 'trends', 'upload'];
                        // if navigated from reports tab, then reset the startYear value back to DEFAULT_START_YEAR_FILTER
                        if (selectedTab === 1 && newValue !== 1) {
                          dispatch(setStartYear(DEFAULT_START_YEAR_FILTER))
                        }
                        const selectedTabName = tabNames[newValue];
                        setSelectedTab(newValue);
                        if (selectedTabName === 'upload') {
                          setRightSideBarMode(RightSideBarMode.Upload);
                          dispatch(setUploadState(UploadMode.SelectProperty));
                        } else {
                          setRightSideBarMode(RightSideBarMode.None);
                        }
                        navigate(`/${selectedTabName}`);
                      }}
                      aria-label="Main Page Tabs"
                      sx={{
                        '& .MuiTabs-flexContainer': {
                          flexWrap: 'wrap',
                        },
                      }}
                    >
                      <Tab key={0} label={'MAP'} {...a11yProps(0)} />
                      <Tab key={1} label={'REPORTS'} {...a11yProps(1)} />
                      <Tab key={2} label={'CHARTS'} {...a11yProps(2)} />
                      <Tab key={3} label={'TRENDS'} {...a11yProps(3)} />
                    </Tabs>
                  )}
                  <div style={{ flex: 1, paddingRight: "1rem" }}>
                    <div style={{ width: "100%", display: "flex"}}>
                      {
                        rightSideBarMode === RightSideBarMode.Upload ?
                        <HelperContainerWithToggle key={'/upload/'} relativeUrl='/upload/'/>:
                        <HelperContainerWithToggle key={`/${tabNames[selectedTab]}/`} relativeUrl={`/${tabNames[selectedTab]}/`} />
                      }
                    </div>
                  </div>
                </Box>
              </Grid>
              <Grid item
                    xs={12} md={12}
                    lg={12}
                    id={'right-sidebar-tab'}
                    className="TabPanels"
              >
                <TabPanel key={0} value={selectedTab} index={-1} indexList={[0, 4]} noPadding>
                  <Map isDataUpload={isUploadUrl || selectedTab === 4} />
                </TabPanel>
                <TabPanel key={1} value={selectedTab} index={1} noPadding>
                  <DataList/>
                </TabPanel>
                <TabPanel key={2} value={selectedTab} index={2} noPadding>
                  <Metrics/>
                </TabPanel>
                <TabPanel key={3} value={selectedTab} index={3} noPadding>
                  <Trends/>
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
