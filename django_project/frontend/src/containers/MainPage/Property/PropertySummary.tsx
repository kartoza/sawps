import React, {useEffect, useState} from 'react';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {RootState} from '../../../app/store';
import {useAppSelector } from '../../../app/hooks';


export default function PropertySummary() {
    const propertyItem = useAppSelector((state: RootState) => state.mapState.selectedProperty)


    return (
        <Grid container flexDirection={'column'} className='PropertySummary'>
            <Grid item className='EmptyHeader'>
                
            </Grid>
            <Grid item className='FlexContainerFill'>
                <Grid container className='ContentContainer'>
                    <Grid item className='Header'>
                        <Grid container flexDirection={'row'} justifyContent={'space-between'}>
                            <Grid item className='SiteDetailTitle'>
                                <span className='SiteDetailIcon'></span>
                                <span>{ `Property: ID${propertyItem.id}` }</span>
                            </Grid>
                            <Grid item>
                                <Button variant='contained'>UPLOAD SPECIES DATA</Button>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item className='FlexContainerFillHeight'>
                        <Grid container className='SummaryContent'>
                            <Grid item>
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
                                                    { `ID${propertyItem.id}` }
                                                </TableCell>
                                            </TableRow>
                                            <TableRow key='property_name'>
                                                <TableCell component="th" scope="row">
                                                    Property Name
                                                </TableCell>
                                                <TableCell>
                                                    {propertyItem.name}
                                                </TableCell>
                                            </TableRow>
                                            <TableRow key='owner_name'>
                                                <TableCell component="th" scope="row">
                                                    Owner Name
                                                </TableCell>
                                                <TableCell>
                                                    {propertyItem.owner}
                                                </TableCell>
                                            </TableRow>
                                            <TableRow key='property_type'>
                                                <TableCell component="th" scope="row">
                                                    Property Type
                                                </TableCell>
                                                <TableCell>
                                                    {propertyItem.property_type}
                                                </TableCell>
                                            </TableRow>
                                            <TableRow key='size'>
                                                <TableCell component="th" scope="row">
                                                    Property Size (in ha)
                                                </TableCell>
                                                <TableCell>
                                                    {propertyItem.size}
                                                </TableCell>
                                            </TableRow>
                                            <TableRow key='organisation'>
                                                <TableCell component="th" scope="row">
                                                    Organisation
                                                </TableCell>
                                                <TableCell>
                                                    {propertyItem.organisation}
                                                </TableCell>
                                            </TableRow>
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                            </Grid>
                            <Grid item>
                                {/* Species data chart */}
                            </Grid>
                            <Grid item>
                                {/* Total species table */}
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}
