import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import ParcelInterface from '../../../models/Parcel';
import {capitalize} from '../../../utils/Helpers';


interface SelectedParcelTableInterface {
    parcels: ParcelInterface[];
    onRemoveParcel: (parcel: ParcelInterface) => void
}

export default function SelectedParcelTable(props: SelectedParcelTableInterface) {
    return (
        <TableContainer component={Paper}>
            <Table className='PropertySiteDetailTable' aria-label="property site detail table" size='medium'>
                <TableHead>
                    <TableRow>
                        <TableCell style={{width: '60%'}}>Parcel ID</TableCell>
                        <TableCell style={{width: '30%'}}>Parcel Type</TableCell>
                        <TableCell style={{width: '10%'}}></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    { props.parcels.map((parcel: ParcelInterface, index: number) => {
                        return (
                            <TableRow key={index}>
                                <TableCell style={{width: '60%'}}>
                                    {parcel.cname}
                                </TableCell>
                                <TableCell style={{width: '30%'}}>
                                    {capitalize(parcel.type)}
                                </TableCell>
                                <TableCell style={{width: '10%'}}>
                                    <IconButton aria-label='Delete' title='Delete' onClick={() => props.onRemoveParcel(parcel)}>
                                        <DeleteOutlinedIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        )
                    })                      
                    }
                </TableBody>
            </Table>
        </TableContainer>
    )
}
