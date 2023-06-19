import React from 'react';
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import './index.scss';

interface RightSideBarInterface {
    element?: React.ElementType,
    additionalClasses?: string
}

const RightSideBarContent = (Component: React.ElementType) => {
    return <Component />
  }

function RightSideBar(props: RightSideBarInterface) {
    return (
        <Box className={`RightSideBar ${props.additionalClasses ? props.additionalClasses : ''}`}>
            { props.element ?
                RightSideBarContent(props.element) : <Skeleton />
            }
        </Box>
    )
}

export default RightSideBar;
