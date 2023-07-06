import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import EditNoteIcon from '@mui/icons-material/EditNote';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationInterface,
    TaxonMetadata,
    CommonUploadMetadata
} from '../../../models/Upload';
import moment from 'moment';



interface ReviewAndConfirmInterface {
    initialData: UploadSpeciesDetailInterface;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
}

interface ReviewItemInterface {
    data: UploadSpeciesDetailInterface;
}

const displayText = (value: string):string => {
    return value && value.trim() ? value.trim() : '-'
}

const displayNumber = (value: number):number => {
    return value ? value : 0
}

const displayBoolean = (value: Boolean):string => {
    return value ? 'Yes':'No'
}

function SpeciesDetailReview(props: ReviewItemInterface) {
    const { data } = props;
    return (
        <Grid container className='DataPreview' flexDirection={'column'} rowSpacing={2}>
            <Grid item>
                <Grid container flexDirection={'row'} spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item className='InputContainer'>
                                <TextField id='scientific-name' label='Scientific Name' defaultValue={displayText(data.taxon_name)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='common-name' label='Common Name' defaultValue={displayText(data.common_name)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField id='scientific-name' label='Month and Year of Count' defaultValue={`${moment({month: data.month - 1, year: data.year}).format('MMMM YYYY')}`}
                                            variant='standard' disabled fullWidth helperText=" " />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField id='present' label='Species Present on Property' defaultValue={displayBoolean(data.annual_population.present)}
                                            variant='standard' disabled fullWidth helperText=" " />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='open-close-system' label='Open/Closed System' defaultValue={displayText(data.annual_population.open_close_name)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='survey-method' label='Survey Method' defaultValue={displayText(data.annual_population.survey_method_name)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='area_covered' required label='Sampled Area' defaultValue={displayNumber(data.annual_population.area_covered)}
                                    variant='standard' type='number'
                                    disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='sampling_note' label='Sampling Notes' defaultValue={displayText(data.annual_population.note)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='adult_male'
                                            label='Adult Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.adult_male)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='adult_female'
                                            label='Adult Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.adult_female)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='subadult_male'
                                            label='Subadult Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.sub_adult_male)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='subadult_female'
                                            label='Subadult Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.sub_adult_female)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='juvenile_male'
                                            label='Juvenile Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.juvenile_male)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='juvenile_female'
                                            label='Juvenile Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.juvenile_female)}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='total_count'
                                            label='Total Count'
                                            disabled
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.total)}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='area_available_to_species'
                                            label='Area available to species'
                                            required
                                            variant="standard"
                                            defaultValue={displayText(data.annual_population.area_available_to_species ? `${data.annual_population.area_available_to_species} Ha` : '0 Ha')}
                                            disabled
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='group' label='Number of groups (prides, herds, etc.)' defaultValue={displayNumber(data.annual_population.group)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='count_method' label='Count Method' defaultValue={displayText(data.annual_population.count_method_name)}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={4}>
                                        <TextField
                                            id='sampling_effort'
                                            label='Sampling Effort'
                                            required
                                            type='number'
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.annual_population.sampling_effort)}
                                            disabled
                                            helperText=' '
                                        />
                                    </Grid>
                                    <Grid item xs={8}>
                                        <TextField id='sampling_unit' label='Sampling Unit' defaultValue={displayText(data.annual_population.sampling_size_unit_name)}
                                            variant='standard' disabled fullWidth helperText=" " />
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}

function ActivityDetailReview(props: ReviewItemInterface) {
    const { data } = props;
    return (
        <Grid container className='DataPreview' flexDirection={'column'} rowSpacing={2}>
            <Grid item>
                <Grid container flexDirection={'row'} spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item>
                                <Typography variant='h6'>Introduction/Reintroduction</Typography>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_adult_male'
                                            label='Adult Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            disabled
                                            defaultValue={displayNumber(data.intake_population.adult_male)}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_adult_female'
                                            label='Adult Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            disabled
                                            defaultValue={displayNumber(data.intake_population.adult_female)}
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_juvenile_male'
                                            label='Juvenile Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            disabled
                                            defaultValue={displayNumber(data.intake_population.juvenile_male)}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_juvenile_female'
                                            label='Juvenile Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth
                                            disabled
                                            defaultValue={displayNumber(data.intake_population.juvenile_female)}
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_total_count'
                                            label='Total Count'
                                            disabled
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.intake_population.total)}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='intake_founder population'
                                            label='Founder Population'
                                            disabled
                                            required
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayBoolean(data.intake_population.founder_population)}
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField
                                    id='intake_event'
                                    label='Event'
                                    disabled
                                    required
                                    variant="standard"
                                    fullWidth
                                    defaultValue={displayText(data.intake_population.activity_type_name)}
                                    helperText=" "
                                />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_source' label='Source' required defaultValue={displayText(data.intake_population.reintroduction_source)}
                                    variant='standard' fullWidth disabled helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_permit' label='Permit Number' defaultValue={displayText(data.intake_population.permit ? data.intake_population.permit.toString() : '')}
                                    variant='standard' fullWidth disabled helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_note' label='Notes' defaultValue={displayText(data.intake_population.note)}
                                    variant='standard' fullWidth disabled helperText=" " />
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item>
                                <Typography variant='h6'>Off-take</Typography>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='offtake_adult_male'
                                            label='Adult Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth disabled
                                            defaultValue={displayNumber(data.offtake_population.adult_male)} helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='offtake_adult_female'
                                            label='Adult Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth disabled
                                            defaultValue={displayNumber(data.offtake_population.adult_female)} helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='offtake_juvenile_male'
                                            label='Juvenile Males'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <MaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth disabled
                                            defaultValue={displayNumber(data.offtake_population.juvenile_male)} helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='offtake_juvenile_female'
                                            label='Juvenile Females'
                                            InputProps={{
                                                startAdornment: (
                                                    <InputAdornment position="start">
                                                        <FemaleIcon />
                                                    </InputAdornment>
                                                ),
                                            }}
                                            variant="standard"
                                            fullWidth disabled
                                            defaultValue={displayNumber(data.offtake_population.juvenile_female)} helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='offtake_total_count'
                                            label='Total Count'
                                            disabled
                                            variant="standard"
                                            fullWidth
                                            defaultValue={displayNumber(data.offtake_population.total)}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField
                                    id='offtake-activity-label'
                                    label='Event'
                                    disabled
                                    variant="standard"
                                    fullWidth
                                    defaultValue={displayText(data.offtake_population.activity_type_name)}
                                    helperText=" "
                                />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_permit' label='Permit Number' defaultValue={displayText(data.offtake_population.permit ? data.offtake_population.permit.toString() : '')}
                                    variant='standard' disabled fullWidth
                                    helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_translocation_destination' label='Translocation Destination' required defaultValue={displayText(data.offtake_population.translocation_destination)}
                                    variant='standard' disabled fullWidth
                                    helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_note' label='Notes' defaultValue={displayText(data.offtake_population.note)}
                                    variant='standard' disabled fullWidth
                                    helperText=" " />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Grid>
    )
}

export default function ReviewAndConfirm(props: ReviewAndConfirmInterface) {
    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
            <Grid item>
                <Grid container flexDirection={'column'} rowSpacing={1}>
                    <Grid item container flexDirection={'row'} alignItems={'center'}>
                        <Typography variant='h6'>Species Detail</Typography>
                        <IconButton aria-label='Edit Species Detail' title='Edit Species Detail'>
                            <EditNoteIcon />
                        </IconButton>
                    </Grid>
                    <Grid item>
                        <SpeciesDetailReview data={props.initialData} />
                    </Grid>
                </Grid>
            </Grid>
            <Grid item>
                <Grid container flexDirection={'column'} rowSpacing={1}>
                    <Grid item container flexDirection={'row'} alignItems={'center'}>
                        <Typography variant='h6'>Activity Detail</Typography>
                        <IconButton aria-label='Edit Activity Detail' title='Edit Activity Detail'>
                            <EditNoteIcon />
                        </IconButton>
                    </Grid>
                    <Grid item>
                        <ActivityDetailReview data={props.initialData} />
                    </Grid>
                </Grid>                
            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                <Grid item>
                    <Button variant='outlined' onClick={() => props.handleBack(props.initialData)}>BACK</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => {}}>SUBMIT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}