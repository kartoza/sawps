import React, { useState } from 'react';
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel, { a11yProps } from '../../../components/TabPanel';
import Layers from './Layers';
import './index.scss';
import Filter from './Filter';

function LayerFilterTabs(props: { selectedMainTabIdx: number }) {
    const [selectedTabSideBar, setSelectedTabSideBar] = useState(0);
    const [containsCharts, setContainsCharts] = useState(false);

    useEffect(() => {
        // Extract the current URL
        const currentUrl = window.location.href;

        // Check if the URL contains a pattern that indicates the presence of charts
        if (
            currentUrl.includes('/charts') || 
            currentUrl.includes('/?tab=2')
        ) {
            setContainsCharts(true);
            setSelectedTabSideBar(1);
        }else setContainsCharts(false)

    }, [props.selectedMainTabIdx]);

    return (
        <Box className='LeftSideBar'>
            <Box className='TabHeaders'>
                <Tabs value={selectedTabSideBar}
                    onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTabSideBar(newValue);
                    }} aria-label="Left Side Bar Tabs"
                    centered={containsCharts}
                >
                    {!containsCharts && (
                        <Tab key={0} label={'LAYERS'} {...a11yProps(0)} />
                     )} 
                
                    <Tab key={1} label={'FILTERS'} {...a11yProps(1)} />
                </Tabs>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='LeftSideBarContent'>
                    {!containsCharts && (
                        <TabPanel key={0} value={selectedTabSideBar} index={0} noPadding>
                            <Layers />
                        </TabPanel>
                    )} 
                    <TabPanel key={1} value={selectedTabSideBar} index={1} noPadding>
                        <Filter />
                    </TabPanel>
                </Box>
            </Box>
        </Box>
    );
}

export default LayerFilterTabs;
