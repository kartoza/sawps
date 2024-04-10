import React, { useEffect, useState } from 'react';
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel, { a11yProps } from '../../../components/TabPanel';
import PropertyInterface, { createNewProperty } from '../../../models/Property';
import Step1 from './Step1';
import Step2 from './Step2';
import Step3 from './Step3';
import './index.scss';

interface UploadWizardInterface {
    initialProperty?: PropertyInterface;
}


export default function UploadWizard(props: UploadWizardInterface) {
    const [property, setProperty] = useState<PropertyInterface>(createNewProperty())
    const [isPropertyInfoValid, setIsPropertyInfoValid] = useState(false)
    const [selectedTab, setSelectedTab] = useState(0)

    useEffect(() => {
        if (props.initialProperty?.id) {
            // has selection, redirect to step 3
            setProperty({...props.initialProperty})
            setIsPropertyInfoValid(true)
            setSelectedTab(2)
        }
    }, [props.initialProperty])


    return (
        <Grid container className='UploadWizard' flexDirection={'column'}>
            <Box className='TabHeaders'>
                <Tabs value={selectedTab}
                    onChange={(event: React.SyntheticEvent, newValue: number) => {
                        setSelectedTab(newValue)
                    }} aria-label="Upload Wizard Tabs"
                >
                        <Tab key={0} label={'STEP 1'} {...a11yProps(0)} sx={{flex:1}} />
                        <Tab key={1} label={'STEP 2'} {...a11yProps(1)} disabled={!isPropertyInfoValid} sx={{flex:1}} />
                        <Tab key={2} label={'STEP 3'} {...a11yProps(2)} disabled={property.id===0} sx={{flex:1}} />
                </Tabs>
            </Box>
            <Box className='TabPanels FlexContainerFill'>
                <Box className='UploadWizardContent'>
                    <TabPanel key={0} value={selectedTab} index={0} noPadding>
                        <Step1 onSave={(data: PropertyInterface) => {
                            setProperty(data)
                            setIsPropertyInfoValid(true)
                            setSelectedTab(1)
                        }} initialProperty={property} />
                    </TabPanel>
                    <TabPanel key={1} value={selectedTab} index={1} noPadding>
                        <Step2 property={property} onSave={(data: PropertyInterface) => {
                            setProperty(data)
                            setSelectedTab(2)
                        }} onBoundaryPropertyUpdated={(source: string) => {
                            setProperty({
                                ...property,
                                boundary_source: source
                            })
                        }} />
                    </TabPanel>
                    <TabPanel key={2} value={selectedTab} index={2} noPadding>
                        <Step3 property={property} onUpdateBoundary={() => setSelectedTab(1)}/>
                    </TabPanel>
                </Box>
            </Box>
        </Grid>
    )
}
