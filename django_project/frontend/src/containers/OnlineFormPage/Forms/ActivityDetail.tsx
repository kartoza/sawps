import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationPerActivityInterface,
    TaxonMetadata,
    CommonUploadMetadata,
    FIELD_COUNTER,
    OTHER_NUMBER_FIELDS,
    UploadSpeciesDetailValidation
} from '../../../models/Upload';
import { REQUIRED_FIELD_ERROR_MESSAGE } from '../../../utils/Validation';


interface ActivityDetailInterface {
    initialData: UploadSpeciesDetailInterface;
    intakeEventMetadataList: CommonUploadMetadata[];
    offtakeEventMetadataList: CommonUploadMetadata[];
    setIsDirty: (isDirty: boolean) => void;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
    handleNext: (data: UploadSpeciesDetailInterface) => void;
}

export default function ActivityDetail(props: ActivityDetailInterface) {
    const {
        initialData, intakeEventMetadataList, offtakeEventMetadataList,
        setIsDirty, handleBack, handleNext
    } = props
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(0))
    const [validation, setValidation] = useState<UploadSpeciesDetailValidation>({})

    const updateIntakePopulation = (field: keyof AnnualPopulationPerActivityInterface, value: any) => {
        let _total = data.intake_population.total
        if (FIELD_COUNTER.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
            let _currentValue = data.intake_population[field] as number
            _total = _total - (isNaN(_currentValue) ? 0 : _currentValue) + (value as number)
        } else if (OTHER_NUMBER_FIELDS.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
        }
        setData({
            ...data,
            annual_population: {...data.annual_population},
            intake_population: {
                ...data.intake_population,
                [field]: value,
                total: _total,
            },
            offtake_population: {...data.offtake_population}            
        })
        setIsDirty(true)
        setValidation({
            ...validation,
            intake_population: {
                ...validation.intake_population,
                [field]: false
            }
        })
    }

    const updateOfftakePopulation = (field: keyof AnnualPopulationPerActivityInterface, value: any) => {
        let _total = data.offtake_population.total
        if (FIELD_COUNTER.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
            let _currentValue = data.offtake_population[field] as number
            _total = _total - (isNaN(_currentValue) ? 0 : _currentValue) + (value as number)
        } else if (OTHER_NUMBER_FIELDS.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
        }
        setData({
            ...data,
            annual_population: {...data.annual_population},
            offtake_population: {
                ...data.offtake_population,
                [field]: value,
                total: _total,
            },
            intake_population: {...data.intake_population}            
        })
        setIsDirty(true)
        setValidation({
            ...validation,
            offtake_population: {
                ...validation.offtake_population,
                [field]: false
            }
        })
    }

    const updateActivityPopulationSelectValue = (field: keyof AnnualPopulationPerActivityInterface, value: number, sourceList: CommonUploadMetadata[], isIntake: boolean) => {
        let _name_field = field.replace('_id', '_name')
        let _selected = sourceList.find(element => element.id === value)
        if (_selected) {
            setIsDirty(true)
            let _updated: UploadSpeciesDetailInterface;
            let _validation: UploadSpeciesDetailValidation;
            if (isIntake) {
                _updated = {
                    ...data,
                    annual_population: {...data.annual_population},
                    intake_population: {
                        ...data.intake_population,
                        [field]: value,
                        [_name_field]: _selected.name
                    },
                    offtake_population: {...data.offtake_population}            
                }
                _validation = {
                    ...validation,
                    intake_population: {
                        ...validation.intake_population,
                        [field]: false
                    }
                }
            } else {
                _updated = {
                    ...data,
                    annual_population: {...data.annual_population},
                    offtake_population: {
                        ...data.offtake_population,
                        [field]: value,
                        [_name_field]: _selected.name
                    },
                    intake_population: {...data.intake_population}            
                }
                _validation = {
                    ...validation,
                    offtake_population: {
                        ...validation.offtake_population,
                        [field]: false
                    }
                }
            }
            setData(_updated)
            setValidation(_validation)
        }
    }

    const validateActivityDetail = () => {
        let _error_validation:UploadSpeciesDetailValidation = {}
        // Validate Intake
        if (data.intake_population.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                intake_population: {
                    ..._error_validation.intake_population,
                    activity_type_id: true
                }
            }
        }
        if (!data.intake_population.reintroduction_source || data.intake_population.reintroduction_source.trim() === '') {
            _error_validation = {
                ..._error_validation,
                intake_population: {
                    ..._error_validation.intake_population,
                    reintroduction_source: true
                }
            }
        }
        // Validate Offtake
        if (data.offtake_population.activity_type_id === 0) {
            _error_validation = {
                ..._error_validation,
                offtake_population: {
                    ..._error_validation.offtake_population,
                    activity_type_id: true
                }
            }
        }
        if (!data.offtake_population.translocation_destination || data.offtake_population.translocation_destination.trim() === '') {
            _error_validation = {
                ..._error_validation,
                offtake_population: {
                    ..._error_validation.offtake_population,
                    translocation_destination: true
                }
            }
        }
        setValidation(_error_validation)
        return Object.keys(_error_validation).length === 0
    }

    useEffect(() => {
        setData({
            ...initialData,
            annual_population: {...initialData.annual_population},
            intake_population: {...initialData.intake_population},
            offtake_population: {...initialData.offtake_population}
        })
    }, [initialData])

    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.intake_population.adult_male}
                                            onChange={(e) => updateIntakePopulation('adult_male', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.intake_population.adult_female}
                                            onChange={(e) => updateIntakePopulation('adult_female', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.intake_population.juvenile_male}
                                            onChange={(e) => updateIntakePopulation('juvenile_male', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.intake_population.juvenile_female}
                                            onChange={(e) => updateIntakePopulation('juvenile_female', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.intake_population.total}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <FormControl fullWidth>
                                            <FormLabel id="founder-population" className='CustomRadioButtonLabel' required>Founder Population</FormLabel>
                                            <RadioGroup
                                                aria-labelledby="founder-population"
                                                name="founder-population-radio-buttons"
                                                row
                                                aria-required
                                                className='RadioGroup'
                                                value={data.intake_population.founder_population}
                                                onChange={(e) => updateIntakePopulation('founder_population', e.target.value === 'true')}
                                            >
                                                <FormControlLabel value={true} control={<Radio size='small' />} label="Yes" />
                                                <FormControlLabel value={false} control={<Radio size='small' />} label="No" />
                                            </RadioGroup>
                                            <FormHelperText>{' '}</FormHelperText>
                                        </FormControl>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.intake_population?.activity_type_id}>
                                    <InputLabel id="intake-activity-label">Event</InputLabel>
                                    <Select
                                        labelId="intake-activity-label"
                                        id="intake-activity-select"
                                        value={data.intake_population.activity_type_id ? data.intake_population.activity_type_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateActivityPopulationSelectValue('activity_type_id', parseInt(event.target.value), intakeEventMetadataList, true)}
                                        displayEmpty
                                        label="Event"
                                    >
                                        { intakeEventMetadataList.map((common: CommonUploadMetadata) => {
                                            return (
                                                <MenuItem key={common.id} value={common.id}>
                                                    {common.name}
                                                </MenuItem>
                                            )
                                        })                                            
                                        }
                                    </Select>
                                    <FormHelperText>{validation.intake_population?.activity_type_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_source' label='Source' required value={data.intake_population.reintroduction_source}
                                    error={validation.intake_population?.reintroduction_source}
                                    variant='standard'
                                    onChange={(e) => updateIntakePopulation('reintroduction_source', e.target.value) } fullWidth
                                    helperText={validation.intake_population?.reintroduction_source ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_permit' label='Permit Number' value={data.intake_population.permit}
                                    variant='standard'
                                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                    onChange={(e) => updateIntakePopulation('permit', parseInt(e.target.value)) } fullWidth
                                    helperText={validation.intake_population?.permit ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='intake_note' label='Notes' value={data.intake_population.note}
                                    variant='standard'
                                    onChange={(e) => updateIntakePopulation('note', e.target.value) } fullWidth
                                    helperText=" " />
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.offtake_population.adult_male}
                                            onChange={(e) => updateOfftakePopulation('adult_male', parseInt(e.target.value))}
                                            helperText=" "
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.offtake_population.adult_female}
                                            onChange={(e) => updateOfftakePopulation('adult_female', parseInt(e.target.value))}
                                            helperText=" "
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.offtake_population.juvenile_male}
                                            onChange={(e) => updateOfftakePopulation('juvenile_male', parseInt(e.target.value))}
                                            helperText=" "
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.offtake_population.juvenile_female}
                                            onChange={(e) => updateOfftakePopulation('juvenile_female', parseInt(e.target.value))}
                                            helperText=" "
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.offtake_population.total}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.offtake_population?.activity_type_id}>
                                    <InputLabel id="offtake-activity-label">Event</InputLabel>
                                    <Select
                                        labelId="offtake-activity-label"
                                        id="offtake-activity-select"
                                        value={data.offtake_population.activity_type_id ? data.offtake_population.activity_type_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateActivityPopulationSelectValue('activity_type_id', parseInt(event.target.value), offtakeEventMetadataList, false)}
                                        displayEmpty
                                        label="Event"
                                    >
                                        { offtakeEventMetadataList.map((common: CommonUploadMetadata) => {
                                            return (
                                                <MenuItem key={common.id} value={common.id}>
                                                    {common.name}
                                                </MenuItem>
                                            )
                                        })
                                        }
                                    </Select>
                                    <FormHelperText>{validation.offtake_population?.activity_type_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_translocation_destination' label='Translocation Destination' required value={data.offtake_population.translocation_destination}
                                    variant='standard'
                                    onChange={(e) => updateOfftakePopulation('translocation_destination', e.target.value) } fullWidth
                                    error={validation.offtake_population?.translocation_destination}
                                    helperText={validation.offtake_population?.translocation_destination ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_permit' label='Permit Number' value={data.offtake_population.permit}
                                    variant='standard'
                                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                    onChange={(e) => updateOfftakePopulation('permit', parseInt(e.target.value)) } fullWidth
                                    error={validation.offtake_population?.permit}
                                    helperText={validation.offtake_population?.permit ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='offtake_note' label='Notes' value={data.offtake_population.note}
                                    variant='standard'
                                    onChange={(e) => updateOfftakePopulation('note', e.target.value) } fullWidth
                                    helperText=" " />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                <Grid item>
                    <Button variant='outlined' onClick={() => handleBack(data)}>BACK</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => {
                        if (validateActivityDetail()) {
                            handleNext(data)
                        }
                    }}>NEXT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}