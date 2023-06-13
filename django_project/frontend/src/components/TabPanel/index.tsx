import React, {} from "react";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
    padding?: number;
    noPadding?: boolean;
    indexList?: number[]; // enable multiple tabs for same content
}


const isTabPanelVisible = (value: number, index: number, indexList?: number[]):boolean => {
    if (index === -1 && indexList) {
        // check inside indexList
        return indexList.includes(value)
    }
    return value === index;
}
 

export default function TabPanel(props: TabPanelProps) {
    const { children, value, index, padding, noPadding, indexList, ...other } = props;

    let _box_padding = padding ? padding : 3;
    if (noPadding) {
        _box_padding = 0
    }

    let _isPanelVisible = isTabPanelVisible(value, index, indexList);

    return (
        <Box
            role="tabpanel"
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            style={{flex: 1, flexDirection: 'column', justifyContent: 'flex-start' }}
            sx={{display: _isPanelVisible ? 'flex': 'none' }}
            {...other}
        >
        {_isPanelVisible && (
            <Box sx={{ p: _box_padding, flexGrow: 1, display:'flex', flexDirection: 'column', minHeight: 0 }}>
                {children}
            </Box>
        )}
        </Box>
    );
}

export function a11yProps(index: number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
}
