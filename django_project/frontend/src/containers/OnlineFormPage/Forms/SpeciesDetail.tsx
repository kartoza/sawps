import React, { useState, useEffect } from 'react';
import moment, { Moment } from 'moment';
import Grid from "@mui/material/Grid";
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import InputAdornment from '@mui/material/InputAdornment';
import MaleIcon from '@mui/icons-material/Male';
import FemaleIcon from '@mui/icons-material/Female';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import FormHelperText from '@mui/material/FormHelperText';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import {
    UploadSpeciesDetailInterface,
    getDefaultUploadSpeciesDetail,
    AnnualPopulationInterface,
    TaxonMetadata,
    CommonUploadMetadata,
    UploadSpeciesDetailValidation,
    FIELD_COUNTER,
    OTHER_NUMBER_FIELDS
} from '../../../models/Upload';
import { REQUIRED_FIELD_ERROR_MESSAGE } from '../../../utils/Validation';

interface SpeciesDetailInterface {
    initialData: UploadSpeciesDetailInterface;
    taxonMetadataList: TaxonMetadata[];
    openCloseMetadataList: CommonUploadMetadata[];
    countMethodMetadataList: CommonUploadMetadata[];
    surveyMethodMetadataList: CommonUploadMetadata[];
    samplingUnitMetadataList: CommonUploadMetadata[];
    setIsDirty: (isDirty: boolean) => void;
    handleNext: (data: UploadSpeciesDetailInterface) => void;
    handleSaveDraft: (data: UploadSpeciesDetailInterface) => void;
}

export default function SpeciesDetail(props: SpeciesDetailInterface) {
    const { 
        initialData, taxonMetadataList, openCloseMetadataList,
        countMethodMetadataList, surveyMethodMetadataList, samplingUnitMetadataList,
        setIsDirty, handleNext, handleSaveDraft
    } = props
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(0))
    const [validation, setValidation] = useState<UploadSpeciesDetailValidation>({})

    const updateSpecies = (value: number) => {
        // find taxon
        let _selected = taxonMetadataList.find(x => x.id === value)
        if (_selected) {
            setData({
                ...data,
                taxon_id: value,
                taxon_name: _selected.scientific_name,
                common_name: _selected.common_name_varbatim,
                annual_population: {...data.annual_population},
                intake_populations: [...data.intake_populations],
                offtake_populations: [...data.offtake_populations]            
            })
            setIsDirty(true)
            setValidation({...validation, taxon_id: false})
        }
    }

    const updateYearDetail = (year: number) => {
        setData({
            ...data,
            year: year,
            annual_population: {...data.annual_population},
            intake_populations: [...data.intake_populations],
            offtake_populations: [...data.offtake_populations]            
        })
        setIsDirty(true)
    }

    const updateAnnualPopulation = (field: keyof AnnualPopulationInterface, value: any) => {
        let _total = data.annual_population.total
        if (FIELD_COUNTER.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
            let _currentValue = data.annual_population[field] as number
            _total = _total - (isNaN(_currentValue) ? 0 : _currentValue) + (value as number)
        } else if (OTHER_NUMBER_FIELDS.includes(field)) {
            if (isNaN(value)) {
                value = 0
            }
        }
        setData({
            ...data,
            annual_population: {
                ...data.annual_population,
                [field]: value,
                total: _total,
            },
            intake_populations: [...data.intake_populations],
            offtake_populations: [...data.offtake_populations]            
        })
        setIsDirty(true)
        setValidation({
            ...validation,
            annual_population: {
                ...validation.annual_population,
                [field]: false
            }
        })
    }

    const updateAnnualPopulationSelectValue = (field: keyof AnnualPopulationInterface, value: number, sourceList: CommonUploadMetadata[]) => {
        let _name_field = field.replace('_id', '_name')
        let _selected = sourceList.find(element => element.id === value)
        if (_selected) {
            setData({
                ...data,
                annual_population: {
                    ...data.annual_population,
                    [field]: value,
                    [_name_field]: _selected.name
                },
                intake_populations: [...data.intake_populations],
                offtake_populations: [...data.offtake_populations]            
            })
            setIsDirty(true)
            setValidation({
                ...validation,
                annual_population: {
                    ...validation.annual_population,
                    [field]: false
                }
            })
        }
    }

    const validateSpeciesDetail = () => {
        let _error_validation:UploadSpeciesDetailValidation = {}
        if (data.taxon_id === 0) {
            _error_validation = {..._error_validation, taxon_id: true}
        }
        if (data.year === 0) {
            _error_validation = {..._error_validation, year: true}
        }
        if (data.annual_population.open_close_id === 0) {
            _error_validation = {
                ..._error_validation,
                annual_population: {
                    ..._error_validation.annual_population,
                    open_close_id: true
                }
            }
        }
        if (data.annual_population.count_method_id === 0) {
            _error_validation = {
                ..._error_validation,
                annual_population: {
                    ..._error_validation.annual_population,
                    count_method_id: true
                }
            }
        }
        if (data.annual_population.survey_method_id === 0) {
            _error_validation = {
                ..._error_validation,
                annual_population: {
                    ..._error_validation.annual_population,
                    survey_method_id: true
                }
            }
        }
        if (data.annual_population.sampling_size_unit_id === 0) {
            _error_validation = {
                ..._error_validation,
                annual_population: {
                    ..._error_validation.annual_population,
                    sampling_size_unit_id: true
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
            intake_populations: [...initialData.intake_populations],
            offtake_populations: [...initialData.offtake_populations]
        })
        setValidation({})
    }, [initialData])

    return (
        <Grid container flexDirection={'column'} rowSpacing={2}>
            <Grid item>
                <Grid container flexDirection={'row'} spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item className='InputContainer'>
                                <FormControl variant="standard" required className='DropdownInput' fullWidth
                                        error={validation.taxon_id}>
                                    <InputLabel id="scientific-name-label">Scientific Name</InputLabel>
                                    <Select
                                        labelId="scientific-name-label"
                                        id="scientific-name-select"
                                        value={data.taxon_id ? data.taxon_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateSpecies(parseInt(event.target.value))}
                                        displayEmpty
                                        label="Scientific Name"
                                    >
                                        { taxonMetadataList.map((taxon: TaxonMetadata) => {
                                            return (
                                                <MenuItem key={taxon.id} value={taxon.id}>
                                                    {taxon.scientific_name}
                                                </MenuItem>
                                            )
                                        })                                            
                                        }
                                    </Select>
                                    <FormHelperText>{validation.taxon_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='common-name' label='Common Name' value={data.common_name}
                                    variant='standard' disabled fullWidth helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <LocalizationProvider dateAdapter={AdapterMoment}>
                                            <DatePicker label={'Year of Count'} views={['year']}
                                                slotProps={{ textField: { size: 'small', variant: 'standard', className: 'Calendar', required: true } }}
                                                value={moment({'year': data.year})}
                                                onChange={(newValue: Moment) => updateYearDetail(newValue.year())}
                                            />
                                            <FormHelperText>{' '}</FormHelperText>
                                        </LocalizationProvider>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <FormControl fullWidth>
                                            <FormLabel id="present" className='CustomRadioButtonLabel' required>Species Present on Property</FormLabel>
                                            <RadioGroup
                                                aria-labelledby="present"
                                                name="present-radio-buttons"
                                                row
                                                aria-required
                                                className='RadioGroup'
                                                value={data.annual_population.present}
                                                onChange={(e) => updateAnnualPopulation('present', e.target.value === 'true')}
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
                                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.annual_population?.open_close_id}>
                                    <InputLabel id="open-close-system-label">Open/Closed System</InputLabel>
                                    <Select
                                        labelId="open-close-system-label"
                                        id="open-close-system-select"
                                        value={data.annual_population.open_close_id ? data.annual_population.open_close_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateAnnualPopulationSelectValue('open_close_id', parseInt(event.target.value), openCloseMetadataList)}
                                        displayEmpty
                                        label="Open/Closed System"
                                    >
                                        { openCloseMetadataList.map((common: CommonUploadMetadata) => {
                                            return (
                                                <MenuItem key={common.id} value={common.id}>
                                                    {common.name}
                                                </MenuItem>
                                            )
                                        })                                            
                                        }
                                    </Select>
                                    <FormHelperText>{validation.annual_population?.open_close_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.annual_population?.survey_method_id}>
                                    <InputLabel id="survey-method-label">Survey Method</InputLabel>
                                    <Select
                                        labelId="survey-method-label"
                                        id="survey-method-select"
                                        value={data.annual_population.survey_method_id ? data.annual_population.survey_method_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateAnnualPopulationSelectValue('survey_method_id', parseInt(event.target.value), surveyMethodMetadataList)}
                                        displayEmpty
                                        label="Survey Method"
                                    >
                                        { surveyMethodMetadataList.map((common: CommonUploadMetadata) => {
                                            return (
                                                <MenuItem key={common.id} value={common.id}>
                                                    {common.name}
                                                </MenuItem>
                                            )
                                        })                                            
                                        }
                                    </Select>
                                    <FormHelperText>{validation.annual_population?.survey_method_id ? REQUIRED_FIELD_ERROR_MESSAGE : ' '}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <Grid container flexDirection={'row'} spacing={2}>
                                    <Grid item xs={6}>
                                        <TextField id='area_covered' required label='Sampled Area' value={data.annual_population.area_covered.toString()}
                                            variant='standard' type='number'
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        ha
                                                    </InputAdornment>
                                                ),
                                            }}
                                            onChange={(e) => updateAnnualPopulation('area_covered', parseFloat(e.target.value)) } fullWidth
                                            helperText=" " />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='sampling_note' label='Sampling Notes' value={data.annual_population.note}
                                    variant='standard'
                                    onChange={(e) => updateAnnualPopulation('note', e.target.value) } fullWidth
                                    helperText=" " />
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.adult_male}
                                            onChange={(e) => updateAnnualPopulation('adult_male', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.adult_female}
                                            onChange={(e) => updateAnnualPopulation('adult_female', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.sub_adult_male}
                                            onChange={(e) => updateAnnualPopulation('sub_adult_male', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.sub_adult_female}
                                            onChange={(e) => updateAnnualPopulation('sub_adult_female', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.juvenile_male}
                                            onChange={(e) => updateAnnualPopulation('juvenile_male', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.juvenile_female}
                                            onChange={(e) => updateAnnualPopulation('juvenile_female', parseInt(e.target.value))}
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
                                            inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.total}
                                            helperText=" "
                                        />
                                    </Grid>
                                    <Grid item xs={6}>
                                        <TextField
                                            id='area_available_to_species'
                                            label='Area available to species'
                                            required
                                            InputProps={{
                                                endAdornment: (
                                                    <InputAdornment position="end">
                                                        ha
                                                    </InputAdornment>
                                                ),
                                            }}
                                            type='number'
                                            variant="standard"
                                            fullWidth
                                            value={data.annual_population.area_available_to_species.toString()}
                                            onChange={(e) => updateAnnualPopulation('area_available_to_species', parseFloat(e.target.value))}
                                            helperText=" "
                                        />
                                    </Grid>
                                </Grid>
                            </Grid>
                            <Grid item className='InputContainer'>
                                <TextField id='group' label='Number of groups (prides, herds, etc.)' value={data.annual_population.group ? data.annual_population.group : ''}
                                    inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }}
                                    variant='standard'
                                    onChange={(e) => updateAnnualPopulation('group', parseInt(e.target.value)) } fullWidth
                                    helperText=" " />
                            </Grid>
                            <Grid item className='InputContainer'>
                                <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.annual_population?.count_method_id}>
                                    <InputLabel id="count-method-label">Count Method</InputLabel>
                                    <Select
                                        labelId="count-method-label"
                                        id="count-method-select"
                                        value={data.annual_population.count_method_id ? data.annual_population.count_method_id.toString() : ""}
                                        onChange={(event: SelectChangeEvent) => updateAnnualPopulationSelectValue('count_method_id', parseInt(event.target.value), countMethodMetadataList)}
                                        displayEmpty
                                        label="Count Method"
                                    >
                                        { countMethodMetadataList.map((common: CommonUploadMetadata) => {
                                            return (
                                                <MenuItem key={common.id} value={common.id}>
                                                    {common.name}
                                                </MenuItem>
                                            )
                                        })                                            
                                        }
                                    </Select>
                                    <FormHelperText>{validation.annual_population?.count_method_id ? REQUIRED_FIELD_ERROR_MESSAGE: ' '}</FormHelperText>
                                </FormControl>
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
                                            value={data.annual_population.sampling_effort.toString()}
                                            onChange={(e) => updateAnnualPopulation('sampling_effort', parseFloat(e.target.value)) }
                                            helperText=' '
                                        />
                                    </Grid>
                                    <Grid item xs={8}>
                                        <FormControl variant="standard" required className='DropdownInput' fullWidth error={validation.annual_population?.sampling_size_unit_id}>
                                            <InputLabel id="sampling-unit-label">Sampling Unit</InputLabel>
                                            <Select
                                                labelId="sampling-unit-label"
                                                id="sampling-unit-select"
                                                value={data.annual_population.sampling_size_unit_id ? data.annual_population.sampling_size_unit_id.toString() : ""}
                                                onChange={(event: SelectChangeEvent) => updateAnnualPopulationSelectValue('sampling_size_unit_id', parseInt(event.target.value), countMethodMetadataList)}
                                                displayEmpty
                                                label="Sampling Unit"
                                            >
                                                { samplingUnitMetadataList.map((common: CommonUploadMetadata) => {
                                                    return (
                                                        <MenuItem key={common.id} value={common.id}>
                                                            {common.name}
                                                        </MenuItem>
                                                    )
                                                })                                            
                                                }
                                            </Select>
                                            <FormHelperText>{validation.annual_population?.sampling_size_unit_id ? REQUIRED_FIELD_ERROR_MESSAGE: ' '}</FormHelperText>
                                        </FormControl>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'space-between'}>
                <Grid item>
                    <Button variant='outlined' onClick={() => {
                        handleSaveDraft(data)
                    }}>SAVE DRAFT</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => {
                        if (validateSpeciesDetail()) {
                            handleNext(data)
                        }
                    }}>NEXT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}
