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
    AnnualPopulationPerActivityErrorMessage
} from '../../../models/Upload';
import { REQUIRED_FIELD_ERROR_MESSAGE, getErrorMessage } from '../../../utils/Validation';
import NumberInputWithNA from '../../../components/NumberInputWithNA';

export enum EventType {
    intake = 'intake',
    offtake = 'offtake'
}

interface EventDetailFormInterface {
    initialData?: AnnualPopulationPerActivityInterface,
    eventType: EventType,
    eventMetadataList: CommonUploadMetadata[],
    setIsDirty: (isDirty: boolean) => void,
    validate: (data: AnnualPopulationPerActivityInterface) => [AnnualPopulationPerActivityValidation, AnnualPopulationPerActivityErrorMessage],
    onSave: (isCreate: boolean, data: AnnualPopulationPerActivityInterface, isCancel?: boolean) => void
}

const cleanActivityName = (activityName: string) => {
    if (activityName) {
        let _name = activityName.toLocaleLowerCase()
        // replace non word characters
        _name = _name.replaceAll(/[\W_]+/g, ' ')
        // replace one or more spaces/tabs
        _name = _name.replaceAll(/\s\s+/g, ' ')
        return _name
    }
    return ''
}

const isTranslocationSourceFieldVisible = (selectedActivityName: string) => {
    let _name = cleanActivityName(selectedActivityName)
    if (_name.includes('translocation intake')) return true
    return false
}

const isTranslocationDestinationFieldVisible = (selectedActivityName: string) => {
    let _name = cleanActivityName(selectedActivityName)
    if (_name.includes('translocation offtake')) {
        return true
    }
    return false
}

const isPermitNumberFieldVisible = (selectedActivityName: string) => {
    let _name = cleanActivityName(selectedActivityName)
    if (_name.includes('translocation offtake') || _name.includes('translocation intake') ||
        _name.includes('planned hunt') || _name.includes('planned euthanasia')) {
        return true
    }
    return false
}

export default function EventDetailForm(props: EventDetailFormInterface) {
    const {
        initialData, eventType, eventMetadataList, setIsDirty, validate, onSave
    } = props
    const [data, setData] = useState<AnnualPopulationPerActivityInterface>(getDefaultAnnualPopulationPerActivity())
    const [validation, setValidation] = useState<AnnualPopulationPerActivityValidation>({})
    const [validationMessages, setValidationMessages] = useState<AnnualPopulationPerActivityErrorMessage>({})

    const updateActivityPopulation = (field: keyof AnnualPopulationPerActivityInterface, value: any) => {
        if (field === 'total') {
            // if total is updated, then reset other number fields
            if (value === null) {
                setData({
                    ...data,
                    total: null,
                    adult_male: null,
                    adult_female: null,
                    juvenile_male: null,
                    juvenile_female: null,
                })
            } else {
                if (isNaN(value)) {
                    value = 0
                }
                setData({
                    ...data,
                    total: value,
                    adult_male: 0,
                    adult_female: 0,
                    juvenile_male: 0,
                    juvenile_female: 0,
                })
            }
        } else {
            let _total = data.total
            if (FIELD_COUNTER.includes(field)) {
                if (isNaN(value)) {
                    value = 0
                }
                // sum the counter fields
                _total = 0
                for (let _field of FIELD_COUNTER) {
                    if (_field === field) {
                        _total += value
                    } else {
                        let _keyField = _field as keyof AnnualPopulationPerActivityInterface
                        let _fieldVal = data[_keyField] as number
                        _total += isNaN(_fieldVal) ? 0 : _fieldVal
                    }
                }
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
        }
        setIsDirty(true)
        setValidation({
            ...validation,
            [field]: false
        })
        setValidationMessages({
            ...validationMessages,
            [field]: ''
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
            setValidationMessages({
                ...validationMessages,
                [field]: ''
            })
        }
    }

    const saveForm = () => {
        let _validationWithErrorMessage = validate(data)
        let _validationResult = _validationWithErrorMessage[0]
        if (Object.keys(_validationResult).length === 0) {
            onSave(!(props.initialData && props.initialData.id >= 0), {...data})
            setData(getDefaultAnnualPopulationPerActivity())
        } else {
            setValidation({..._validationResult})
            setValidationMessages({..._validationWithErrorMessage[1]})
        }
    }

    const cancelUpdate = () => {
        onSave(!(props.initialData && props.initialData.id >= 0), {...data}, true)
        setData(getDefaultAnnualPopulationPerActivity())
        setValidation({})
        setValidationMessages({})
    }

    useEffect(() => {
        if (initialData) {
            setData({...initialData})
        } else {
            setData(getDefaultAnnualPopulationPerActivity())
        }
        setValidation({})
        setValidationMessages({})
    }, [initialData])

    const isValidForm = () => {
        if (Object.keys(validation).length === 0) return true
        var idx = Object.values(validation).findIndex(v => v)
        return idx === -1
    }

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
                                inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                variant="standard"
                                fullWidth
                                value={data.total}
                                onChange={(e) => updateActivityPopulation('total', parseInt(e.target.value))}
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
                        <FormHelperText>{validation?.activity_type_id ? getErrorMessage(validationMessages, 'activity_type_id') : ' '}</FormHelperText>
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
                        onChange={(e) => updateActivityPopulation('permit', e.target.value) } fullWidth
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
                        <NumberInputWithNA
                            id='offtake_adult_male'
                            label='Adult Males'
                            initialValue={data.adult_male}
                            icon={<MaleIcon />}
                            onValueChange={(value: number) => {
                                updateActivityPopulation('adult_male', value)
                            }}
                            onValidationError={() => {
                                let field = 'adult_male'
                                setValidation({
                                    ...validation,
                                    [field]: true
                                })
                                setValidationMessages({
                                    ...validationMessages,
                                    [field]: 'Invalid value'
                                })
                            }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <NumberInputWithNA
                            id='offtake_adult_female'
                            label='Adult Females'
                            initialValue={data.adult_female}
                            icon={<FemaleIcon />}
                            onValueChange={(value: number) => {
                                updateActivityPopulation('adult_female', value)
                            }}
                            onValidationError={() => {
                                let field = 'adult_female'
                                setValidation({
                                    ...validation,
                                    [field]: true
                                })
                                setValidationMessages({
                                    ...validationMessages,
                                    [field]: 'Invalid value'
                                })
                            }}
                        />
                    </Grid>
                </Grid>
            </Grid>
            <Grid item className='InputContainer'>
                <Grid container flexDirection={'row'} spacing={2}>
                    <Grid item xs={6}>
                        <NumberInputWithNA
                            id='offtake_juvenile_male'
                            label='Juvenile Males'
                            initialValue={data.juvenile_male}
                            icon={<MaleIcon />}
                            onValueChange={(value: number) => {
                                updateActivityPopulation('juvenile_male', value)
                            }}
                            onValidationError={() => {
                                let field = 'juvenile_male'
                                setValidation({
                                    ...validation,
                                    [field]: true
                                })
                                setValidationMessages({
                                    ...validationMessages,
                                    [field]: 'Invalid value'
                                })
                            }}
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <NumberInputWithNA
                            id='offtake_juvenile_female'
                            label='Juvenile Females'
                            initialValue={data.juvenile_female}
                            icon={<FemaleIcon />}
                            onValueChange={(value: number) => {
                                updateActivityPopulation('juvenile_female', value)
                            }}
                            onValidationError={() => {
                                let field = 'juvenile_female'
                                setValidation({
                                    ...validation,
                                    [field]: true
                                })
                                setValidationMessages({
                                    ...validationMessages,
                                    [field]: 'Invalid value'
                                })
                            }}
                        />
                    </Grid>
                </Grid>
            </Grid>
            <Grid item className='InputContainer'>
                <Grid container flexDirection={'row'} spacing={2}>
                    <Grid item xs={6}>
                        <NumberInputWithNA
                            id='offtake_total_count'
                            label='Total Count'
                            initialValue={data.total}
                            onValueChange={(value: number) => {
                                updateActivityPopulation('total', value)
                            }}
                            onValidationError={() => {
                                let field = 'total'
                                setValidation({
                                    ...validation,
                                    [field]: true
                                })
                                setValidationMessages({
                                    ...validationMessages,
                                    [field]: 'Invalid value'
                                })
                            }}
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
                    <FormHelperText>{validation.activity_type_id ? getErrorMessage(validationMessages, 'activity_type_id') : ' '}</FormHelperText>
                </FormControl>
            </Grid>
            { isTranslocationSourceFieldVisible(data.activity_type_name) &&
                <Grid item className='InputContainer'>
                    <TextField id='offtake_translocation_source' label='Translocation Source' value={data.reintroduction_source}
                        variant='standard'
                        onChange={(e) => updateActivityPopulation('reintroduction_source', e.target.value) } fullWidth
                        error={validation?.reintroduction_source}
                        helperText={validation?.reintroduction_source ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                </Grid>
            }
            { isTranslocationDestinationFieldVisible(data.activity_type_name) &&
                <Grid item className='InputContainer'>
                    <TextField id='offtake_translocation_destination' label='Translocation Destination' value={data.translocation_destination}
                        variant='standard'
                        onChange={(e) => updateActivityPopulation('translocation_destination', e.target.value) } fullWidth
                        error={validation?.translocation_destination}
                        helperText={validation?.translocation_destination ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                </Grid>
            }
            { isPermitNumberFieldVisible(data.activity_type_name) &&
                <Grid item className='InputContainer'>
                    <TextField id='offtake_permit' label='Permit Number' value={data.permit}
                        variant='standard'
                        onChange={(e) => updateActivityPopulation('permit', e.target.value) } fullWidth
                        error={validation?.permit}
                        helperText={validation?.permit ? REQUIRED_FIELD_ERROR_MESSAGE : ' '} />
                </Grid>
            }            
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
                <Button variant="outlined" disabled={!isValidForm()} startIcon={ initialData ? <ModeEditIcon /> : <AddIcon />} onClick={saveForm}>
                    { initialData ? 'Update' : 'Add' }
                </Button>
            </Grid>
        </Grid>
    )
}
