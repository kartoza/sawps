import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel, { a11yProps } from '../../../components/TabPanel';
import './index.scss';


function FormWizard() {
    const [loading, setLoading] = useState<boolean>(true)
    const [uploadSession, setUploadSession] = useState<string>('')
    const [selectedTab, setSelectedTab] = useState(0)
    const [isDirty, setIsDirty] = useState(false)


    return (
        <Grid container className='OnlineFormWizard' flexDirection={'column'}>
            <Box className='TabHeaders'>
                <Tabs value={selectedTab}
                    onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTab(newValue)
                    }} aria-label="Online Form Wizard Tabs"
                >
                        <Tab key={0} label={'SPECIES DETAIL'} {...a11yProps(0)} sx={{flex:1}} />
                        <Tab key={1} label={'ACTIVITY DETAIL'} {...a11yProps(1)} sx={{flex:1}} />
                        <Tab key={2} label={'NOTES'} {...a11yProps(2)} sx={{flex:1}} />
                        <Tab key={3} label={'REVIEW'} {...a11yProps(3)} sx={{flex:1}} />
                </Tabs>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='OnlineFormWizardContent'>
                    <TabPanel key={0} value={selectedTab} index={0} noPadding>
                        <span>SPECIES DETAIL FORM</span>
                    </TabPanel>
                    <TabPanel key={1} value={selectedTab} index={1} noPadding>
                        <span>ACTIVITY DETAIL FORM</span>
                    </TabPanel>
                    <TabPanel key={2} value={selectedTab} index={2} noPadding>
                        <span>NOTES FORM</span>
                    </TabPanel>
                    <TabPanel key={3} value={selectedTab} index={3} noPadding>
                        <span>REVIEW & CONFIRM</span>
                    </TabPanel>
                </Box>
            </Box>
        </Grid>
    )
}

export default FormWizard;