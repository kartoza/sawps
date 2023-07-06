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



interface ActivityDetailInterface {
    initialData: UploadSpeciesDetailInterface;
    setIsDirty: (isDirty: boolean) => void;
    handleBack: (data: UploadSpeciesDetailInterface) => void;
    handleNext: (data: UploadSpeciesDetailInterface) => void;
}

const DUMMY_INTAKE_EVENTS: CommonUploadMetadata[] = [
    {
        'id': 1,
        'name': 'Intake Event 1'
    },
    {
        'id': 2,
        'name': 'Intake Event 2'
    }
]

const DUMMY_OFFTAKE_EVENTS: CommonUploadMetadata[] = [
    {
        'id': 1,
        'name': 'Offtake Event 1'
    },
    {
        'id': 2,
        'name': 'Offtake Event 2'
    }
]

const DUMMY_INTRO_SOURCE: CommonUploadMetadata[] = [
    {
        'id': 1,
        'name': 'Source 1'
    },
    {
        'id': 2,
        'name': 'Source 2'
    }
]

export default function ActivityDetail(props: ActivityDetailInterface) {
    const [data, setData] = useState<UploadSpeciesDetailInterface>(getDefaultUploadSpeciesDetail(0))
    const [validation, setValidation] = useState<UploadSpeciesDetailValidation>({})
    const [intakeEventMetadataList, setIntakeEventMetadataList] = useState<CommonUploadMetadata[]>(DUMMY_INTAKE_EVENTS)
    const [offtakeEventMetadataList, setOfftakeEventMetadataList] = useState<CommonUploadMetadata[]>(DUMMY_OFFTAKE_EVENTS)
    const [introductionSourceMetadataList, setIntroductionSourceMetadataList] = useState<CommonUploadMetadata[]>(DUMMY_INTRO_SOURCE)

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
        props.setIsDirty(true)
        setValidation({
            ...validation,
            annual_population: {
                ...validation.annual_population,
                [field]: false
            }
        })
    }

    useEffect(() => {
        setData({
            ...props.initialData,
            annual_population: {...props.initialData.annual_population},
            intake_population: {...props.initialData.intake_population},
            offtake_population: {...props.initialData.offtake_population}
        })
    }, [props.initialData])

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
                                                onChange={(e) => updateIntakePopulation('founder_population', e.target.value)}
                                            >
                                                <FormControlLabel value={true} control={<Radio size='small' />} label="Yes" />
                                                <FormControlLabel value={false} control={<Radio size='small' />} label="No" />
                                            </RadioGroup>
                                            <FormHelperText>{' '}</FormHelperText>
                                        </FormControl>
                                    </Grid>
                                </Grid>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <Grid container flexDirection={'column'} rowSpacing={1}>
                            <Grid item>
                                <Typography variant='h6'>Off-take</Typography>
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
            <Grid item container flexDirection={'row'} justifyContent={'flex-end'} columnSpacing={2}>
                <Grid item>
                    <Button variant='outlined' onClick={() => props.handleBack(data)}>BACK</Button>
                </Grid>
                <Grid item>
                    <Button variant='contained' onClick={() => props.handleNext(data)}>NEXT</Button>
                </Grid>
            </Grid>
        </Grid>
    )
}