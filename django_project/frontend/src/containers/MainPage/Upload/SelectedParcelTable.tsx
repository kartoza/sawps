import React, {useState, useEffect} from 'react';
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
    onRemoveParcel: (parcel: ParcelInterface) => void;
    onParcelHovered?: (parcel: ParcelInterface) => void;
}

interface RowInterface {
    index: number;
    parcel: ParcelInterface;
    onRemoveParcel: (parcel: ParcelInterface) => void;
    onParcelHovered?: (parcel: ParcelInterface) => void;
}

function Row(props: RowInterface) {
    return (
        <TableRow key={props.index}
            onMouseOver={() => { props.onParcelHovered ? props.onParcelHovered(props.parcel) : null}}
            onMouseLeave={() => { props.onParcelHovered ? props.onParcelHovered(null) : null}}
            >
            <TableCell style={{width: '60%'}}>
                {props.parcel.cname}
            </TableCell>
            <TableCell style={{width: '30%'}}>
                {capitalize(props.parcel.type)}
            </TableCell>
            <TableCell style={{width: '10%'}}>
                <IconButton aria-label='Delete' title='Delete' onClick={() => props.onRemoveParcel(props.parcel)}>
                    <DeleteOutlinedIcon />
                </IconButton>
            </TableCell>
        </TableRow>
    )
}

export default function SelectedParcelTable(props: SelectedParcelTableInterface) {
    const [parentFarms, setParentFarms] = useState<ParcelInterface[]>([])
    const [others, setOthers] = useState<ParcelInterface[]>([])

    useEffect(() => {
        let _parentFarms: ParcelInterface[] = []
        let _others: ParcelInterface[] = []
        for (let _parcel of props.parcels) {
            if (_parcel.layer === 'parent_farm') {
                _parentFarms.push(_parcel)
            } else {
                _others.push(_parcel)
            }
        }
        setParentFarms(_parentFarms)
        setOthers(_others)
    }, [props.parcels])

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
                    { parentFarms.length > 0 &&
                        <TableRow>
                            <TableCell colSpan={3} className='SelectedParcelSection'>Parent Farm</TableCell>
                        </TableRow>
                    }
                    { parentFarms.length > 0 && parentFarms.map((parcel: ParcelInterface, index: number) => {
                        return <Row key={`parent-farm-${index}`} index={index} parcel={parcel} onRemoveParcel={props.onRemoveParcel} onParcelHovered={props.onParcelHovered} />
                    })
                    }
                    { parentFarms.length > 0 && others.length > 0 &&
                        <TableRow>
                            <TableCell colSpan={3} className='SelectedParcelSection'>Others (Erf, Holding, Farm Portion)</TableCell>
                        </TableRow>
                    }
                    { others.map((parcel: ParcelInterface, index: number) => {
                        return <Row key={`others-${index}`} index={index} parcel={parcel} onRemoveParcel={props.onRemoveParcel} onParcelHovered={props.onParcelHovered} />
                    })
                    }
                </TableBody>
            </Table>
        </TableContainer>
    )
}
