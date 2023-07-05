import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel, { a11yProps } from '../../../components/TabPanel';
import {UploadSpeciesDetailInterface, getDefaultUploadSpeciesDetail} from '../../../models/Upload'
import './index.scss';
import PropertyInterface from '../../../models/Property';
import SpeciesDetail from './SpeciesDetail';

interface FormWizardInterface {
    propertyItem: PropertyInterface;
}

function FormWizard(props: FormWizardInterface) {
    const [loading, setLoading] = useState<boolean>(true)
    const [uploadSession, setUploadSession] = useState<string>('')
    const [selectedTab, setSelectedTab] = useState(0)
    const [isDirty, setIsDirty] = useState(false)
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(props.propertyItem.id))

    return (
        <Grid container className='OnlineFormWizard' flexDirection={'column'}>
            <Box className='TabHeaders'>
                <Tabs value={selectedTab}
                    onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTab(newValue)
                    }} aria-label="Online Form Wizard Tabs"
                >
                        <Tab key={0} label={'SPECIES DETAIL'} {...a11yProps(0)} />
                        <Tab key={1} label={'ACTIVITY DETAIL'} {...a11yProps(1)} />
                        <Tab key={2} label={'REVIEW'} {...a11yProps(2)} />
                </Tabs>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='OnlineFormWizardContent'>
                    <TabPanel key={0} value={selectedTab} index={0} noPadding>
                        <SpeciesDetail initialData={data} />
                    </TabPanel>
                    <TabPanel key={1} value={selectedTab} index={1} noPadding>
                        <span>ACTIVITY DETAIL FORM</span>
                    </TabPanel>
                    <TabPanel key={2} value={selectedTab} index={2} noPadding>
                        <span>REVIEW & Save</span>
                    </TabPanel>
                </Box>
            </Box>
        </Grid>
    )
}

export default FormWizard;