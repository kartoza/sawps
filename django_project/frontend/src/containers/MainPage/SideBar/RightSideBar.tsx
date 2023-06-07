import React from 'react';
import Box from "@mui/material/Box";
import './index.scss';

function RightSideBar() {
    return (
        <Box className='RightSideBar'>
            This is right sidebar
            <Box sx={{marginTop: '200px'}}>
                This is right sidebar content
            </Box>
        </Box>
    )
}

export default RightSideBar;
