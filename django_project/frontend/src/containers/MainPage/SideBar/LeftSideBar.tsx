import React from 'react';
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";
import './index.scss';

interface LeftSideBarInterface {
    element?: React.ElementType,
    additionalClasses?: string,
    additionalProps?: any
}

const LeftSideBarContent = (Component: React.ElementType, givenProps?: any) => {
    return <Component {...givenProps} />
}

function LeftSideBar(props: LeftSideBarInterface) {
    return (
        <Box className={`LeftSideBar ${props.additionalClasses ? props.additionalClasses : ''}`}>
            { props.element ?
                LeftSideBarContent(props.element, props.additionalProps) : <Skeleton />
            }
        </Box>
    )
}

export default LeftSideBar;
