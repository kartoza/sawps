import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
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
                <colgroup>
                    <col width="60%" />
                    <col width="40%" />
                </colgroup>
                <TableHead>
                    <TableRow>
                        <TableCell>Parcel ID</TableCell>
                        <TableCell>Parcel Type</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    { props.parcels.map((parcel: ParcelInterface, index: number) => {
                        return (
                            <TableRow key={index}>
                                <TableCell>
                                    <FormControlLabel control={<Checkbox checked defaultChecked onChange={() => props.onRemoveParcel(parcel)} />} label={parcel.cname} />
                                </TableCell>
                                <TableCell>
                                    {capitalize(parcel.type)}
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
