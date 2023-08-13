import React, { useState, useEffect } from 'react';
import Grid from "@mui/material/Grid";
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
import AddIcon from '@mui/icons-material/Add';
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import CloseIcon from '@mui/icons-material/Close';
import {
    CommonUploadMetadata,
    AnnualPopulationPerActivityInterface,
    AnnualPopulationPerActivityValidation,
    getDefaultAnnualPopulationPerActivity,
    FIELD_COUNTER,
    OTHER_NUMBER_FIELDS,
} from '../../../models/Upload';
import { REQUIRED_FIELD_ERROR_MESSAGE } from '../../../utils/Validation';

export enum EventType {
    intake = 'intake',
    offtake = 'offtake'
}

interface EventDetailFormInterface {
    initialData?: AnnualPopulationPerActivityInterface,
    eventType: EventType,
    eventMetadataList: CommonUploadMetadata[],
    setIsDirty: (isDirty: boolean) => void,
    validate: (data: AnnualPopulationPerActivityInterface) => AnnualPopulationPerActivityValidation,
    onSave: (isCreate: boolean, data: AnnualPopulationPerActivityInterface, isCancel?: boolean) => void
}

export default function EventDetailForm(props: EventDetailFormInterface) {
    const {
        initialData, eventType, eventMetadataList, setIsDirty, validate, onSave
    } = props
    const [data, setData] = useState<AnnualPopulationPerActivityInterface>(getDefaultAnnualPopulationPerActivity())
    const [validation, setValidation] = useState<AnnualPopulationPerActivityValidation>({})

    const updateActivityPopulation = (field: keyof AnnualPopulationPerActivityInterface, value: any) => {
        let _total = data.total
        if (FIELD_COUNTER.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
            let _currentValue = data[field] as number
            _total = _total - (isNaN(_currentValue) ? 0 : _currentValue) + (value as number)
        } else if (OTHER_NUMBER_FIELDS.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
        }
        setData({
            ...data,
            [field]: value,
            total: _total           
        })
        setIsDirty(true)
        setValidation({
            ...validation,
            [field]: false
        })
    }

    const updateActivityPopulationSelectValue = (field: keyof AnnualPopulationPerActivityInterface, value: number, sourceList: CommonUploadMetadata[]) => {
        let _name_field = field.replace('_id', '_name')
        let _selected = sourceList.find(element => element.id === value)
        if (_selected) {
            setIsDirty(true)
            let _updated: AnnualPopulationPerActivityInterface;
            let _validation: AnnualPopulationPerActivityValidation;
            _updated = {
                ...data,
                [field]: value,
                [_name_field]: _selected.name
            }
            _validation = {
                ...validation,
                [field]: false
            }
            setData(_updated)
            setValidation(_validation)
        }
    }

    const saveForm = () => {
        let _validationResult = validate(data)
        if (Object.keys(_validationResult).length === 0) {
            onSave(!(props.initialData && props.initialData.id >= 0), {...data})
            setData(getDefaultAnnualPopulationPerActivity())
        } else {
            setValidation({..._validationResult})
        }
    }

    const cancelUpdate = () => {
        onSave(!(props.initialData && props.initialData.id >= 0), {...data}, true)
        setData(getDefaultAnnualPopulationPerActivity())
    }

    useEffect(() => {
        if (initialData) {
            setData({...initialData})
        } else {
            setData(getDefaultAnnualPopulationPerActivity())
        }
    }, [initialData])

    if (eventType === EventType.intake) {
        return (
            <Grid container flexDirection={'column'} rowSpacing={1}>
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
                                value={data.adult_male}
                                onChange={(e) => updateActivityPopulation('adult_male', parseInt(e.target.value))}
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
                                value={data.adult_female}
                                onChange={(e) => updateActivityPopulation('adult_female', parseInt(e.target.value))}
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
                                value={data.juvenile_male}
                                onChange={(e) => updateActivityPopulation('juvenile_male', parseInt(e.target.value))}
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
                                value={data.juvenile_female}
                                onChange={(e) => updateActivityPopulation('juvenile_female', parseInt(e.target.value))}
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
                                value={data.total}
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
                                    value={data.founder_population}
                                    onChange={(e) => updateActivityPopulation('founder_population', e.target.value === 'true')}
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
                    <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation?.activity_type_id}>
                        <InputLabel id="intake-activity-label">Event</InputLabel>
                        <Select
                            labelId="intake-activity-label"
                            id="intake-activity-select"
                            value={data.activity_type_id ? data.activity_type_id.toString() : ""}
                            onChange={(event: SelectChangeEvent) => updateActivityPopulationSelectValue('activity_type_id', parseInt(event.target.value), eventMetadataList)}
                            displayEmpty
                            label="Event"
                        >
                            { eventMetadataList.map((common: CommonUploadMetadata) => {
                                return (
                                    <MenuItem key={common.id} value={common.id}>
                                        {common.name}
                                    </MenuItem>
                                )
                            })                                            
                            }
                        </Select>
                        <FormHelperText>{validation?.activity_type_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                    </FormControl>
                </Grid>
                <Grid item className='InputContainer'>
                    <TextField id='intake_source' label='Source' required value={data.reintroduction_source}
                        error={validation?.reintroduction_source}
                        variant='standard'
                        onChange={(e) => updateActivityPopulation('reintroduction_source', e.target.value) } fullWidth
                        helperText={validation?.reintroduction_source ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                </Grid>
                <Grid item className='InputContainer'>
                    <TextField id='intake_permit' label='Permit Number' value={data.permit}
                        variant='standard'
                        inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                        onChange={(e) => updateActivityPopulation('permit', parseInt(e.target.value)) } fullWidth
                        helperText={validation?.permit ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                </Grid>
                <Grid item className='InputContainer'>
                    <TextField id='intake_note' label='Notes' value={data.note}
                        variant='standard'
                        onChange={(e) => updateActivityPopulation('note', e.target.value) } fullWidth
                        helperText=" " />
                </Grid>
                <Grid item className='ButtonContainer'>
                    { initialData ? 
                       <Button variant="outlined" className='CancelUpdateButton' startIcon={<CloseIcon />} onClick={cancelUpdate}>
                            Cancel
                        </Button> : null
                    }
                    <Button variant="outlined" startIcon={ initialData ? <ModeEditIcon /> : <AddIcon />} onClick={saveForm}>
                        { initialData ? 'Update' : 'Add' }
                    </Button>
                </Grid>
            </Grid>
        )
    }

    return (
        <Grid container flexDirection={'column'} rowSpacing={1}>
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
                            value={data.adult_male}
                            onChange={(e) => updateActivityPopulation('adult_male', parseInt(e.target.value))}
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
                            value={data.adult_female}
                            onChange={(e) => updateActivityPopulation('adult_female', parseInt(e.target.value))}
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
                            value={data.juvenile_male}
                            onChange={(e) => updateActivityPopulation('juvenile_male', parseInt(e.target.value))}
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
                            value={data.juvenile_female}
                            onChange={(e) => updateActivityPopulation('juvenile_female', parseInt(e.target.value))}
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
                            value={data.total}
                            helperText=" "
                        />
                    </Grid>
                    <Grid item xs={6}>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item className='InputContainer'>
                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation?.activity_type_id}>
                    <InputLabel id="offtake-activity-label">Event</InputLabel>
                    <Select
                        labelId="offtake-activity-label"
                        id="offtake-activity-select"
                        value={data.activity_type_id ? data.activity_type_id.toString() : ""}
                        onChange={(event: SelectChangeEvent) => updateActivityPopulationSelectValue('activity_type_id', parseInt(event.target.value), eventMetadataList)}
                        displayEmpty
                        label="Event"
                    >
                        { eventMetadataList.map((common: CommonUploadMetadata) => {
                            return (
                                <MenuItem key={common.id} value={common.id}>
                                    {common.name}
                                </MenuItem>
                            )
                        })
                        }
                    </Select>
                    <FormHelperText>{validation.activity_type_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                </FormControl>
            </Grid>
            <Grid item className='InputContainer'>
                <TextField id='offtake_translocation_destination' label='Translocation Destination' required value={data.translocation_destination}
                    variant='standard'
                    onChange={(e) => updateActivityPopulation('translocation_destination', e.target.value) } fullWidth
                    error={validation?.translocation_destination}
                    helperText={validation?.translocation_destination ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
            </Grid>
            <Grid item className='InputContainer'>
                <TextField id='offtake_permit' label='Permit Number' value={data.permit}
                    variant='standard'
                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                    onChange={(e) => updateActivityPopulation('permit', parseInt(e.target.value)) } fullWidth
                    error={validation?.permit}
                    helperText={validation?.permit ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
            </Grid>
            <Grid item className='InputContainer'>
                <TextField id='offtake_note' label='Notes' value={data.note}
                    variant='standard'
                    onChange={(e) => updateActivityPopulation('note', e.target.value) } fullWidth
                    helperText=" " />
            </Grid>
            <Grid item className='ButtonContainer'>
                { initialData ? 
                    <Button variant="outlined" className='CancelUpdateButton' startIcon={<CloseIcon />} onClick={cancelUpdate}>
                        Cancel
                    </Button> : null
                }
                <Button variant="outlined" startIcon={ initialData ? <ModeEditIcon /> : <AddIcon />} onClick={saveForm}>
                    { initialData ? 'Update' : 'Add' }
                </Button>
            </Grid>
        </Grid>
    )
}
