import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from '@mui/icons-material/Search';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import UploadWizard from './UploadWizard';
import { PropertySelectItem } from '../../../models/Property';
import './index.scss';

const FETCH_PROPERTY_LIST_URL = '/api/property/list/'

enum UploadMode {
    None = 'none',
    CreateNew = 'CreateNew',
    PropertySelected = 'PropertySelected'
}

function Upload() {
    const [loading, setLoading] = useState(false)
    const [uploadMode, setUploadMode] = useState(UploadMode.None)
    const [selectedPropertyId, setSelectedPropertyId] = useState<number>(0)
    const [propertyList, setPropertyList] = useState<PropertySelectItem[]>([
        {
            'id': 1,
            'name': 'test123'
        }
    ])

    const fetchPropertyList = () => {
        setLoading(true)
    }

    useEffect(() => {
        if (selectedPropertyId) {
            setUploadMode(UploadMode.PropertySelected)
        }
    }, [selectedPropertyId])

    return (
        <Grid container flexDirection={'column'} className='Upload'>
            <Grid item className='Header'>
                DATA UPLOAD
            </Grid>
            <Grid item>
                <Grid container className='UploadContainer'>
                    <Grid item>
                        <FormControl className='SearchArea' variant="outlined">
                            <InputLabel htmlFor="search-area">Search area</InputLabel>
                            <OutlinedInput
                                id="search-area"
                                type={'text'}
                                endAdornment={
                                    <InputAdornment position="end">
                                        <IconButton
                                        aria-label="search"
                                        edge="end"
                                        >
                                        <SearchIcon />
                                        </IconButton>
                                    </InputAdornment>
                                }
                                label="Search Area"
                            />
                        </FormControl>
                    </Grid>
                    <Grid item>
                        <Grid container className='UploadContent'>
                            { uploadMode === UploadMode.None &&
                                <Grid container flexDirection={'column'}>
                                    <Grid item>
                                        <FormControl fullWidth>
                                            <Select
                                                id="property-select"
                                                value={selectedPropertyId.toString()}
                                                displayEmpty
                                                disabled={loading}
                                                onChange={(event: SelectChangeEvent) => {
                                                    setSelectedPropertyId(parseInt(event.target.value))
                                                }}
                                            >
                                                { propertyList.map((property: PropertySelectItem) => {
                                                    return (
                                                        <MenuItem key={property.id} value={property.id}>{property.name}</MenuItem>
                                                    )
                                                })}
                                            </Select>
                                        </FormControl>
                                    </Grid>
                                    <Grid item className='ButtonContainer'>
                                        <Button variant='contained' onClick={() => setUploadMode(UploadMode.CreateNew) }>CREATE A NEW PROPERTY</Button>
                                    </Grid>
                                </Grid>
                            }
                            { uploadMode === UploadMode.CreateNew && 
                                <Grid item>
                                    <UploadWizard />
                                </Grid>
                            }
                            { uploadMode === UploadMode.PropertySelected && selectedPropertyId && 
                                <Grid item>
                                    <UploadWizard selectedPropertyId={selectedPropertyId} />
                                </Grid>
                            }
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}


export default Upload;
