import React, { useEffect, useState } from 'react';
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel, { a11yProps } from '../../../components/TabPanel';
import Layers from './Layers';
import './index.scss';
import Filter from './Filter';


function LayerFilterTabs(props: any) {
    const { selectedMainTabIdx } = props
    const [selectedTabSideBar, setSelectedTabSideBar] = useState(0)

    return (
        <Box className='LeftSideBar'>
            <Box className={`TabHeaders ${selectedMainTabIdx > 0 ? 'Single' : ''}`}>
                <Tabs value={selectedTabSideBar}
                    onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTabSideBar(newValue)
                    }} aria-label="Left Side Bar Tabs"
                >
                    <Tab key={0} label={'FILTERS'} {...a11yProps(0)} />
                    {selectedMainTabIdx === 0 && <Tab key={1} label={'LAYERS'} {...a11yProps(1)} /> }
                </Tabs>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='LeftSideBarContent'>
                    <TabPanel key={0} value={selectedTabSideBar} index={0} noPadding>
                        <Filter />
                    </TabPanel>
                    <TabPanel key={1} value={selectedTabSideBar} index={1} noPadding>
                        <Layers />
                    </TabPanel>
                </Box>
            </Box>
        </Box>
    )
}

export default LayerFilterTabs;
