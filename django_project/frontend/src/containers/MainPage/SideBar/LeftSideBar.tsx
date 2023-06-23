import React from 'react';
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import './index.scss';

interface LeftSideBarInterface {
    element?: React.ElementType,
    additionalClasses?: string
}

const LeftSideBarContent = (Component: React.ElementType) => {
    return <Component />
}

function LeftSideBar(props: LeftSideBarInterface) {
    return (
        <Box className={`LeftSideBar ${props.additionalClasses ? props.additionalClasses : ''}`}>
            { props.element ?
                LeftSideBarContent(props.element) : <Skeleton />
            }
        </Box>
    )
}

export default LeftSideBar;
