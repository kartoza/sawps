import React from 'react';
import Grid from "@mui/material/Grid";
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import InputAdornment from "@mui/material/InputAdornment";
import SearchIcon from '@mui/icons-material/Search';
import {RootState} from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { setMapMode } from '../../../reducers/MapState';

import './index.scss';

function Upload() {
    const dispatch = useAppDispatch()
    const mapSelectionMode = useAppSelector((state: RootState) => state.mapState.selectionMode)
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
                                label="Password"
                            />
                        </FormControl>
                    </Grid>
                    <Grid item>
                        <Grid container className='UploadContent'>
                            <Grid item>
                                Select Property
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Boundary'></span>
                                        <span>Create Property Boundary/Update</span>
                                    </Grid>
                                    <Grid item className='UploadSectionContent CreateBoundary'>
                                        <Grid container flexDirection={'column'}>
                                            <Grid item>
                                                <p>Create your property boundary by either selecting the cadastral parcels that make up the property or manually digitising your property boundary using the tools below</p>
                                            </Grid>
                                            <Grid item>
                                                <Grid container flexDirection={'row'} flexWrap={'wrap'} spacing={1} rowGap={1} justifyContent={'space-evenly'}>
                                                    { mapSelectionMode === 'parcel' ? 
                                                        <Button variant='contained' onClick={() => dispatch(setMapMode('property')) }>CANCEL</Button> :
                                                        <Button variant='contained' onClick={() => dispatch(setMapMode('parcel')) }>SELECT</Button>
                                                    } 
                                                    <Button variant='contained'>DIGITISE</Button>
                                                    <Button variant='contained'>UPLOAD</Button>
                                                    <Button variant='contained'>SAVE PROPERTY</Button>
                                                </Grid>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Property'></span>
                                        <span>Property Information</span>
                                    </Grid>
                                    <Grid item className='UploadSectionContent'>

                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                <Grid container className='UploadSection'>
                                    <Grid item className='UploadSectionHeader'>
                                        <span className='UploadSectionHeaderIcon Population'></span>
                                        <span>Population Data</span>
                                    </Grid>
                                    <Grid item className='UploadSectionContent'>

                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item>
                                Save Button
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}


export default Upload;
