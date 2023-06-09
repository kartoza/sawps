import React, {useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import PropertyInterface, {PropertyValidation} from '../../../models/Property';
import './index.scss';

interface PropertyInfoInterface {
    property: PropertyInterface,
    enableForm: boolean,
    onUpdated: (data: PropertyInterface, validation: PropertyValidation) => void,
    validationError?: PropertyValidation
}

const PROPERTY_TYPE_LIST = [
    'TYPE 1',
    'TYPE 2',
    'TYPE 3'
]

const PROVINCE_LIST = [
    'PROVINCE 1',
    'PROVINCE 2',
    'PROVINCE 3'
]

const ORGANISATION_LIST = [
    'ORGANISATION 1',
    'ORGANISATION 2',
    'ORGANISATION 3'
]

export default function PropertyInfo(props: PropertyInfoInterface) {
    const [loading, setLoading] = useState(false)

    return (
        <TableContainer component={Paper}>
            <Table className='PropertyInfoTable' aria-label="property info table" size='small'>
                <colgroup>
                    <col width="50%" />
                    <col width="50%" />
                </colgroup>
                <TableHead>
                    <TableRow>
                        <TableCell>Property Information</TableCell>
                        <TableCell>Input</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    <TableRow key='property_name'>
                        <TableCell component="th" scope="row">
                            Property Name
                        </TableCell>
                        <TableCell>
                            <TextField
                                error={props.validationError?.name}
                                disabled={loading || !props.enableForm}
                                id="input_propertyname"
                                hiddenLabel={true}
                                type={"text"}
                                onChange={val => props.onUpdated({ ...props.property, name: val.target.value }, {name:false})}
                                value={props.property.name}
                                sx={{ width: '100%' }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow key='owner_name'>
                        <TableCell component="th" scope="row">
                            Owner Name
                        </TableCell>
                        <TableCell>
                            <TextField
                                disabled={true}
                                id="input_ownername"
                                hiddenLabel={true}
                                type={"text"}
                                value={props.property.owner}
                                sx={{ width: '100%' }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow key='owner_email'>
                        <TableCell component="th" scope="row">
                            Owner Email
                        </TableCell>
                        <TableCell>
                            <TextField
                                error={props.validationError?.email}
                                disabled={loading || !props.enableForm}
                                id="input_owneremail"
                                hiddenLabel={true}
                                type={"text"}
                                onChange={val => props.onUpdated({ ...props.property, owner_email: val.target.value }, {email:false})}
                                value={props.property.owner_email}
                                sx={{ width: '100%' }}
                            />
                        </TableCell>
                    </TableRow>
                    <TableRow key='property_type'>
                        <TableCell component="th" scope="row">
                            Property Type
                        </TableCell>
                        <TableCell>
                            <FormControl fullWidth size="small">
                                <Select
                                    id="property-type-select"
                                    error={props.validationError?.property_type}
                                    value={props.property.property_type}
                                    displayEmpty
                                    disabled={loading || !props.enableForm}
                                    onChange={(event: SelectChangeEvent) => props.onUpdated({ ...props.property, property_type: event.target.value }, {property_type:false})}
                                >
                                    { PROPERTY_TYPE_LIST.map((property_type: string) => {
                                        return (
                                            <MenuItem key={property_type} value={property_type}>{property_type}</MenuItem>
                                        )
                                    })}
                                </Select>
                            </FormControl>
                        </TableCell>
                    </TableRow>
                    <TableRow key='province'>
                        <TableCell component="th" scope="row">
                            Province
                        </TableCell>
                        <TableCell>
                            <FormControl fullWidth size="small">
                                <Select
                                    id="province-select"
                                    error={props.validationError?.province}
                                    value={props.property.province}
                                    displayEmpty
                                    disabled={loading || !props.enableForm}
                                    onChange={(event: SelectChangeEvent) => props.onUpdated({ ...props.property, province: event.target.value }, {province:false})}
                                >
                                    { PROVINCE_LIST.map((province: string) => {
                                        return (
                                            <MenuItem key={province} value={province}>{province}</MenuItem>
                                        )
                                    })}
                                </Select>
                            </FormControl>
                        </TableCell>
                    </TableRow>
                    <TableRow key='size'>
                        <TableCell component="th" scope="row">
                            Property Size (in ha)
                        </TableCell>
                        <TableCell>
                            <TextField
                                disabled={true}
                                id="input_size"
                                hiddenLabel={true}
                                type={"text"}
                                value={props.property.size}
                                sx={{ width: '100%' }}
                            />                            
                        </TableCell>
                    </TableRow>
                    <TableRow key='organisation'>
                        <TableCell component="th" scope="row">
                            Organisation
                        </TableCell>
                        <TableCell>
                            <FormControl fullWidth size="small">
                                <Select
                                    id="organisation-select"
                                    error={props.validationError?.organisation}
                                    value={props.property.organisation}
                                    displayEmpty
                                    disabled={loading || !props.enableForm}
                                    onChange={(event: SelectChangeEvent) => props.onUpdated({ ...props.property, organisation: event.target.value }, {organisation:false})}
                                >
                                    { ORGANISATION_LIST.map((organisation: string) => {
                                        return (
                                            <MenuItem key={organisation} value={organisation}>{organisation}</MenuItem>
                                        )
                                    })}
                                </Select>
                            </FormControl>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    )
}