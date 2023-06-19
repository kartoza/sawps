import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import PropertyInterface from '../../../models/Property';


interface PropertySummaryTableInterface {
    propertyItem: PropertyInterface;
}

export default function PropertySummaryTable(props: PropertySummaryTableInterface) {
    return (
        <TableContainer component={Paper}>
            <Table className='PropertySiteDetailTable' aria-label="property site detail table" size='medium'>
                <colgroup>
                    <col width="50%" />
                    <col width="50%" />
                </colgroup>
                <TableHead>
                    <TableRow>
                        <TableCell colSpan={2}>Site Details</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow key='property_code'>
                        <TableCell component="th" scope="row">
                            Property Code
                        </TableCell>
                        <TableCell>
                            { `ID${props.propertyItem.id}` }
                        </TableCell>
                    </TableRow>
                    <TableRow key='property_name'>
                        <TableCell component="th" scope="row">
                            Property Name
                        </TableCell>
                        <TableCell>
                            {props.propertyItem.name}
                        </TableCell>
                    </TableRow>
                    <TableRow key='owner_name'>
                        <TableCell component="th" scope="row">
                            Owner Name
                        </TableCell>
                        <TableCell>
                            {props.propertyItem.owner}
                        </TableCell>
                    </TableRow>
                    <TableRow key='property_type'>
                        <TableCell component="th" scope="row">
                            Property Type
                        </TableCell>
                        <TableCell>
                            {props.propertyItem.property_type}
                        </TableCell>
                    </TableRow>
                    <TableRow key='size'>
                        <TableCell component="th" scope="row">
                            Property Size (in ha)
                        </TableCell>
                        <TableCell>
                            {props.propertyItem.size}
                        </TableCell>
                    </TableRow>
                    <TableRow key='organisation'>
                        <TableCell component="th" scope="row">
                            Organisation
                        </TableCell>
                        <TableCell>
                            {props.propertyItem.organisation}
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    )
}
